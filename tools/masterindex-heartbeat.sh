#!/bin/zsh
set -u

# Daily pull-based heartbeat for every repo listed in current/index.json .repos[].
#
# Writes current/heartbeat.json. Every repo gets a row every run, including
# repos where nothing changed -- that is the point. A stale lastChanged with a
# fresh lastVerified means "quiet and confirmed"; a stale lastVerified means
# nobody looked. Unreachable repos are recorded explicitly, never silently
# skipped.
#
# The check is read-only against every target repo: it does not fetch, pull,
# commit, or edit anything outside current/heartbeat.json.
#
# macOS TCC caveat: when this runs under launchd, repos beneath ~/Documents,
# ~/Desktop, and ~/Downloads are unreadable unless the executing binary
# (/bin/zsh) has Full Disk Access. Without it those repos report as
# unreachable "HEAD unreadable" from the scheduled run while reading fine
# interactively -- a permissions artifact, not repo damage.

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

GIT=/usr/bin/git
DATE=/bin/date
CAT=/bin/cat
JQ=""
for candidate in /opt/homebrew/bin/jq /usr/local/bin/jq /usr/bin/jq; do
  if [[ -x "$candidate" ]]; then
    JQ=$candidate
    break
  fi
done

GH=""
for candidate in /opt/homebrew/bin/gh /usr/local/bin/gh; do
  if [[ -x "$candidate" ]]; then
    GH=$candidate
    break
  fi
done

usage() {
  "$CAT" <<'EOF'
Usage: tools/masterindex-heartbeat.sh [--no-remote] [--stdout] [INDEX_ROOT]

Stamps every repo in current/index.json .repos[] into current/heartbeat.json,
whether or not it changed.

Options:
  --no-remote  Skip gh API lookups for repos with no local clone. Those rows
               are recorded as unreachable(no-local-clone) instead.
  --stdout     Print the JSON to stdout instead of writing heartbeat.json.
  --report     Do not re-check anything. Read the existing heartbeat.json and
               print only the rows that need attention. Exits 1 when any row is
               unreachable, so it can gate a scheduled check.
EOF
}

no_remote=0
to_stdout=0
report_only=0
while [[ ${1:-} == --* ]]; do
  case "$1" in
    --help|-h) usage; exit 0 ;;
    --no-remote) no_remote=1; shift ;;
    --stdout) to_stdout=1; shift ;;
    --report) report_only=1; shift ;;
    *) print -u2 "unknown option: $1"; usage; exit 2 ;;
  esac
done

root=${1:-$(cd -- "$(dirname -- "$0")/.." && pwd)}
index="$root/current/index.json"
out="$root/current/heartbeat.json"

if [[ -z "$JQ" ]]; then
  print -u2 "heartbeat: jq not found"
  exit 2
fi
if [[ ! -f "$index" ]]; then
  print -u2 "heartbeat: no index at $index"
  exit 2
fi

# --report reads the last run rather than performing a new one, so it is safe to
# call often and never rewrites the record.
if (( report_only )); then
  if [[ ! -f "$out" ]]; then
    print -u2 "heartbeat: no heartbeat.json yet; run without --report first"
    exit 2
  fi
  "$JQ" -r '
    "heartbeat from \(.checkedOn)  |  \(.summary.repos) repos  ok \(.summary.ok)  drift \(.summary.drift)  unreachable \(.summary.unreachable)",
    "",
    (([.repos[] | select(.verificationStatus == "unreachable")]) as $u |
      if ($u | length) > 0 then
        "UNREACHABLE", ($u[] | "  \(.repo)  --  \(.note // "no detail")"), ""
      else empty end),
    (([.repos[] | select(.verificationStatus == "drift")]) as $d |
      if ($d | length) > 0 then
        "DRIFT",
        ($d[] | "  \(.repo)  --  \(.dirtyFiles) dirty, \(.unpushedCommits) unpushed  (\(.branch // "?"))"),
        ""
      else empty end)
  ' "$out"
  if [[ $("$JQ" -r '.summary.unreachable' "$out") != "0" ]]; then
    exit 1
  fi
  exit 0
fi

today=$("$DATE" +%Y-%m-%d)
stamp=$("$DATE" -u +%Y-%m-%dT%H:%M:%SZ)
quiet_cutoff=$("$DATE" -v-30d +%Y-%m-%d)

# Resolve a repo token from .repos[].repo into a local path, if one exists.
#   ~/foo               -> $HOME/foo
#   github:owner/name   -> $HOME/name when that clone exists, else remote-only
resolve_path() {
  local token=$1
  case "$token" in
    "~/"*) print -- "$HOME/${token#\~/}" ;;
    github:*)
      local name=${token##*/}
      if [[ -d "$HOME/$name/.git" ]]; then
        print -- "$HOME/$name"
      else
        print -- ""
      fi
      ;;
    /*) print -- "$token" ;;
    *) print -- "" ;;
  esac
}

rows=()

for token in ${(f)"$("$JQ" -r '.repos[].repo' "$index")"}; do
  path=$(resolve_path "$token")

  source="local"
  vstatus="ok"
  note=""
  branch=""
  head_sha=""
  last_changed=""
  dirty=0
  unpushed=0

  if [[ -n "$path" && -d "$path/.git" ]]; then
    branch=$("$GIT" -C "$path" --no-optional-locks rev-parse --abbrev-ref HEAD 2>/dev/null)
    head_sha=$("$GIT" -C "$path" --no-optional-locks rev-parse --short HEAD 2>/dev/null)
    last_changed=$("$GIT" -C "$path" --no-optional-locks log -1 --format=%cs 2>/dev/null)
    porcelain=$("$GIT" -C "$path" --no-optional-locks status --porcelain 2>/dev/null)
    if [[ -z "$porcelain" ]]; then
      dirty=0
    else
      dirty=${#${(f)porcelain}}
    fi

    # Compare against the tracked upstream only. No fetch: this reports what is
    # already known locally, so a stale ref is a reporting limit, not an error.
    if "$GIT" -C "$path" --no-optional-locks rev-parse '@{u}' >/dev/null 2>&1; then
      unpushed=$("$GIT" -C "$path" --no-optional-locks rev-list --count '@{u}..HEAD' 2>/dev/null || print 0)
    else
      unpushed=0
      note="no upstream tracking branch"
    fi

    if [[ -z "$head_sha" ]]; then
      vstatus="unreachable"
      note="git repo present but HEAD unreadable (empty repo?)"
    elif (( dirty > 0 || unpushed > 0 )); then
      vstatus="drift"
    fi

  elif [[ "$token" == github:* && $no_remote -eq 0 && -n "$GH" ]]; then
    source="remote"
    slug=${token#github:}
    api=$("$GH" api "repos/$slug/commits?per_page=1" \
          --jq '.[0] | "\(.sha[0:7])\t\(.commit.committer.date[0:10])"' 2>/dev/null)
    if [[ -n "$api" ]]; then
      head_sha=${api%%$'\t'*}
      last_changed=${api##*$'\t'}
      branch=$("$GH" api "repos/$slug" --jq '.default_branch' 2>/dev/null)
      note="no local clone; reported from GitHub API"
    else
      vstatus="unreachable"
      note="no local clone and GitHub API lookup failed"
    fi

  else
    vstatus="unreachable"
    source="none"
    if [[ "$token" == github:* ]]; then
      note="no local clone; remote lookup skipped"
    else
      note="path does not exist or is not a git repo"
    fi
  fi

  rows+=("$("$JQ" -n \
    --arg repo "$token" \
    --arg path "$path" \
    --arg source "$source" \
    --arg status "$vstatus" \
    --arg verified "$today" \
    --arg changed "$last_changed" \
    --arg branch "$branch" \
    --arg sha "$head_sha" \
    --arg note "$note" \
    --argjson dirty "${dirty:-0}" \
    --argjson unpushed "${unpushed:-0}" \
    '{
      repo: $repo,
      localPath: (if $path == "" then null else $path end),
      source: $source,
      verificationStatus: $status,
      lastVerified: $verified,
      lastChanged: (if $changed == "" then null else $changed end),
      branch: (if $branch == "" then null else $branch end),
      headSha: (if $sha == "" then null else $sha end),
      dirtyFiles: $dirty,
      unpushedCommits: $unpushed,
      note: (if $note == "" then null else $note end)
    }')")
done

payload=$(printf '%s\n' "${rows[@]}" | "$JQ" -s \
  --arg generated "$stamp" \
  --arg today "$today" \
  --arg cutoff "$quiet_cutoff" \
  '{
    schemaVersion: 1,
    description: "Daily pull-based repo heartbeat. Every repo is stamped every run, including repos with no activity. lastVerified means the checker looked; lastChanged means the repo actually moved.",
    generatedAt: $generated,
    checkedOn: $today,
    summary: {
      repos: length,
      ok: ([.[] | select(.verificationStatus == "ok")] | length),
      drift: ([.[] | select(.verificationStatus == "drift")] | length),
      unreachable: ([.[] | select(.verificationStatus == "unreachable")] | length),
      quiet30d: ([.[] | select(.lastChanged != null and .lastChanged < $cutoff)] | length)
    },
    repos: sort_by(.repo)
  }')

if (( to_stdout )); then
  print -- "$payload"
else
  print -- "$payload" > "$out"
  print "heartbeat: wrote $out"
  print -- "$payload" | "$JQ" -r '.summary | "  \(.repos) repos | ok \(.ok) | drift \(.drift) | unreachable \(.unreachable)"'
fi
