#!/bin/zsh
set -eu

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

CAT=/bin/cat
CHMOD=/bin/chmod
CP=/bin/cp
LAUNCHCTL=/bin/launchctl
MKDIR=/bin/mkdir
MKTEMP=/usr/bin/mktemp
MV=/bin/mv
PLUTIL=/usr/bin/plutil
RM=/bin/rm

usage() {
  "$CAT" <<'EOF'
Usage: bootstrap/install-masterindex-drift-launchagent.sh [--check-now] [--unload] [--source-root PATH] [INDEX_ROOT]

Installs a safe six-hour LaunchAgent for MasterIndex drift detection.
The installer copies tools/masterindex-drift-check.sh into
~/Library/Application Support/MasterIndex and writes logs under
~/Library/Logs/MasterIndex. The scheduled check is read-only.

Options:
  --check-now  Install, load, and run the LaunchAgent immediately.
  --source-root PATH
               Copy the checker from this checkout instead of INDEX_ROOT.
  --unload     Unload and remove the LaunchAgent.
EOF
}

label=com.billdonner.masterindex.drift
check_now=0
unload=0
source_root=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --help|-h)
      usage
      exit 0
      ;;
    --check-now)
      check_now=1
      shift
      ;;
    --unload)
      unload=1
      shift
      ;;
    --source-root)
      source_root=${2:-}
      if [[ -z "$source_root" ]]; then
        print "ERROR: --source-root requires a path" >&2
        exit 2
      fi
      shift 2
      ;;
    *)
      break
      ;;
  esac
done

script_dir=${0:A:h}
default_root=${script_dir:h}
index_root=${1:-$default_root}
index_root=${index_root/#\~/$HOME}
source_root=${source_root:-$default_root}
source_root=${source_root/#\~/$HOME}
checker="$source_root/tools/masterindex-drift-check.sh"

launch_agents="$HOME/Library/LaunchAgents"
support_dir="$HOME/Library/Application Support/MasterIndex"
log_dir="$HOME/Library/Logs/MasterIndex"
plist="$launch_agents/$label.plist"
installed_checker="$support_dir/masterindex-drift-check.sh"

if (( unload )); then
  "$LAUNCHCTL" bootout "gui/$UID" "$plist" 2>/dev/null || true
  "$RM" -f "$plist"
  print "Removed $plist"
  exit 0
fi

if [[ ! -x "$checker" ]]; then
  print "ERROR: drift checker is not executable: $checker" >&2
  exit 2
fi

"$MKDIR" -p "$launch_agents" "$support_dir" "$log_dir"
"$CP" "$checker" "$installed_checker"
"$CHMOD" 755 "$installed_checker"

temp_plist=$("$MKTEMP")
"$CAT" > "$temp_plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$label</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>$installed_checker</string>
    <string>$index_root</string>
  </array>
  <key>StartInterval</key>
  <integer>21600</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$log_dir/drift.out.log</string>
  <key>StandardErrorPath</key>
  <string>$log_dir/drift.err.log</string>
  <key>WorkingDirectory</key>
  <string>$index_root</string>
</dict>
</plist>
EOF

"$PLUTIL" -lint "$temp_plist" >/dev/null
"$MV" "$temp_plist" "$plist"

"$LAUNCHCTL" bootout "gui/$UID" "$plist" 2>/dev/null || true
"$LAUNCHCTL" bootstrap "gui/$UID" "$plist"
"$LAUNCHCTL" enable "gui/$UID/$label"

if (( check_now )); then
  "$LAUNCHCTL" kickstart -k "gui/$UID/$label"
fi

print "Installed $label"
print "Plist: $plist"
print "Checker: $installed_checker"
print "Logs: $log_dir/drift.out.log and $log_dir/drift.err.log"
