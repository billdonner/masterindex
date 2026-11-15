#!/bin/zsh
# Nancy's IONOS uploader — password is requested for each upload and is never saved.
# Double-click this file in Finder, or drag files onto it.

set -u

SFTP_HOST='home350968887.1and1-data.host'
SFTP_PORT='22'
DEFAULT_SFTP_USER='acc1957362779'
CONFIG_FILE="$HOME/.nancy-ionos-sftp-user"
GUI_MODE="${NANCY_GUI:-0}"

show_dialog() {
  /usr/bin/osascript - "$1" <<'APPLESCRIPT'
on run argv
  display alert "Nancy Upload" message (item 1 of argv)
end run
APPLESCRIPT
}

fail() {
  if [[ "$GUI_MODE" == '1' ]]; then
    show_dialog "Upload stopped: $1"
    exit 1
  fi
  print -u2 -- "\nUpload stopped: $1"
  print -- 'Press Return to close this window.'
  read -r
  exit 1
}

choose_files() {
  # A Finder picker avoids asking Nancy to find or type full file paths.
  /usr/bin/osascript <<'APPLESCRIPT'
try
  set chosenItems to choose file with prompt "Choose the files to send" with multiple selections allowed
  set outputText to ""
  repeat with oneItem in chosenItems
    set outputText to outputText & POSIX path of oneItem & linefeed
  end repeat
  return outputText
on error number -128
  return ""
end try
APPLESCRIPT
}

if [[ -r "$CONFIG_FILE" ]]; then
  SFTP_USER="$(<"$CONFIG_FILE")"
else
  SFTP_USER="$DEFAULT_SFTP_USER"
  [[ "$SFTP_USER" =~ '^[A-Za-z0-9_-]+$' ]] || fail 'That username contains an unexpected character.'
  umask 077
  print -r -- "$SFTP_USER" > "$CONFIG_FILE" || fail 'Could not save the username.'
fi

typeset -a FILES
if (( $# )); then
  FILES=("$@")
else
  while IFS= read -r picked; do
    [[ -n "$picked" ]] && FILES+=("$picked")
  done < <(choose_files)
fi
(( ${#FILES} )) || fail 'No files were selected.'

for file in "${FILES[@]}"; do
  [[ -f "$file" ]] || fail "Not a file: $file"
done

print -- "Sending ${#FILES} file(s) to Nancy's private IONOS folder."

if [[ "$GUI_MODE" == '1' ]]; then
  SFTP_PASSWORD="$(/usr/bin/osascript <<'APPLESCRIPT'
try
  set answer to display dialog "Enter the SFTP password Nancy was given. It will not be saved." with title "Nancy Upload" default answer "" with hidden answer buttons {"Cancel", "Upload"} default button "Upload" cancel button "Cancel"
  return text returned of answer
on error number -128
  return ""
end try
APPLESCRIPT
)"
else
  print -n -- 'SFTP password (not saved): '
  read -r -s SFTP_PASSWORD
  print
fi
[[ -n "$SFTP_PASSWORD" ]] || fail 'No password was entered.'

# macOS includes SFTP and Expect. The password is passed only to this short-
# lived helper process, never to a command argument or a saved file.
export NANCY_SFTP_PASSWORD="$SFTP_PASSWORD"
unset SFTP_PASSWORD
/usr/bin/expect -f - -- "$SFTP_USER" "$SFTP_HOST" "$SFTP_PORT" "${FILES[@]}" <<'EXPECT'
set timeout -1
set user [lindex $argv 0]
set host [lindex $argv 1]
set port [lindex $argv 2]
set files [lrange $argv 3 end]
set failures 0

proc sftp_quote {text} {
  set escaped [string map [list "\\" "\\\\" "\"" "\\\"" "\n" ""] $text]
  return "\"$escaped\""
}

set password $env(NANCY_SFTP_PASSWORD)

spawn /usr/bin/sftp -o StrictHostKeyChecking=accept-new -P $port -- "$user@$host"
set password_attempts 0
expect {
  -re "(?i)password:" {
    incr password_attempts
    if {$password_attempts > 1} {
      send_user "The SFTP password was rejected; stopping.\n"
      exit 1
    }
    send -- "$password\r"
    exp_continue
  }
  "sftp> " {}
  -re "Host key verification failed" {
    send_user "The server fingerprint was not accepted; stopping.\n"
    exit 1
  }
  eof { exit 1 }
}
set password ""

foreach file $files {
  set filename [file tail $file]
  set remote_exists 1
  send -- "ls -l [sftp_quote $filename]\r"
  expect {
    -re "(?i)(no such file|not found)" {
      set remote_exists 0
      exp_continue
    }
    "sftp> " {}
    eof {
      send_user "Connection closed before $filename could be checked.\n"
      exit 1
    }
  }

  if {$remote_exists} {
    set put_command "put -a"
  } else {
    set put_command "put"
  }
  send_user "\nUploading: $filename\n"
  set upload_succeeded 1
  send -- "$put_command [sftp_quote $file] [sftp_quote $filename]\r"
  expect {
    -re "(?i)(couldn't|failure|no such file|permission denied)" {
      set upload_succeeded 0
      exp_continue
    }
    "sftp> " {
      if {$upload_succeeded} {
        send_user "Finished: $filename\n"
      } else {
        send_user "Could not finish: $filename (run this uploader again to resume).\n"
        incr failures
      }
    }
    eof {
      send_user "Connection closed before $filename finished. Run again to resume.\n"
      exit 1
    }
  }
}
send -- "bye\r"
expect eof
exit [expr {$failures > 0}]
EXPECT
UPLOAD_STATUS=$?
unset NANCY_SFTP_PASSWORD

if (( UPLOAD_STATUS )); then
  fail 'One or more files were not completed. Run the uploader again to resume.'
fi

if [[ "$GUI_MODE" == '1' ]]; then
  show_dialog 'All selected files were uploaded successfully.'
else
  print -- '\nAll selected files were uploaded successfully.'
  print -- 'Press Return to close this window.'
  read -r
fi
