#!/bin/zsh
set -u

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

GIT=/usr/bin/git
PYTHON=/usr/bin/python3
AWK=/usr/bin/awk
CAT=/bin/cat
DATE=/bin/date
JQ=""
for candidate in /opt/homebrew/bin/jq /usr/local/bin/jq /usr/bin/jq; do
  if [[ -x "$candidate" ]]; then
    JQ=$candidate
    break
  fi
done

usage() {
  "$CAT" <<'EOF'
Usage: tools/masterindex-drift-check.sh [--strict] [INDEX_ROOT]

Validates the MasterIndex contract and reports local drift from origin/main.
The check is read-only: it does not pull, rebase, commit, or edit files.

Options:
  --strict  Exit non-zero when schema errors, dirty files, or remote drift exist.
EOF
}

strict=0
if [[ ${1:-} == "--help" || ${1:-} == "-h" ]]; then
  usage
  exit 0
fi
if [[ ${1:-} == "--strict" ]]; then
  strict=1
  shift
fi

script_dir=${0:A:h}
default_root=${script_dir:h}
index_root=${1:-$default_root}
index_root=${index_root/#\~/$HOME}

timestamp=$("$DATE" "+%Y-%m-%dT%H:%M:%S%z")
check_status=0

report() {
  print "[$timestamp] $*"
}

fail() {
  report "ERROR $*"
  check_status=2
}

warn() {
  report "WARN $*"
  if (( check_status == 0 )); then
    check_status=1
  fi
}

require_file() {
  local path=$1
  if [[ ! -f "$index_root/$path" ]]; then
    fail "missing $path"
  fi
}

report "MasterIndex drift check starting root=$index_root"

if [[ ! -e "$index_root/.git" ]]; then
  fail "not a git checkout: $index_root"
else
  branch=$("$GIT" -C "$index_root" branch --show-current 2>/dev/null || true)
  head_sha=$("$GIT" -C "$index_root" rev-parse --short HEAD 2>/dev/null || true)
  report "git branch=${branch:-detached} head=${head_sha:-unknown}"
fi

for path in current/index.json tasks/index.json current/handoffs/index.json current/inventory.md; do
  require_file "$path"
done

if [[ -n "$JQ" ]]; then
  for path in current/index.json tasks/index.json current/handoffs/index.json; do
    if ! "$JQ" -e . "$index_root/$path" >/dev/null; then
      fail "invalid JSON in $path"
    fi
  done

  required_keys=(generatedAt scope summary ascApps clusters entities services repos gaps)
  for key in $required_keys; do
    if ! "$JQ" -e --arg key "$key" 'has($key)' "$index_root/current/index.json" >/dev/null; then
      fail "current/index.json missing top-level key: $key"
    fi
  done

  if ! "$JQ" -e 'has("globalTasks") and has("entryTasks")' "$index_root/tasks/index.json" >/dev/null; then
    fail "tasks/index.json missing globalTasks or entryTasks"
  fi
elif [[ -x "$PYTHON" ]]; then
  "$PYTHON" - "$index_root" <<'PY'
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
errors = []
for rel in ("current/index.json", "tasks/index.json", "current/handoffs/index.json"):
    try:
        json.loads((root / rel).read_text())
    except Exception as exc:
        errors.append(f"invalid JSON in {rel}: {exc}")

try:
    index = json.loads((root / "current/index.json").read_text())
    for key in ("generatedAt", "scope", "summary", "ascApps", "clusters", "entities", "services", "repos", "gaps"):
        if key not in index:
            errors.append(f"current/index.json missing top-level key: {key}")
except Exception:
    pass

try:
    tasks = json.loads((root / "tasks/index.json").read_text())
    for key in ("globalTasks", "entryTasks"):
        if key not in tasks:
            errors.append(f"tasks/index.json missing {key}")
except Exception:
    pass

if errors:
    for error in errors:
        print(error)
    sys.exit(1)
PY
  if [[ $? -ne 0 ]]; then
    fail "JSON validation failed"
  fi
else
  warn "jq and python3 not found; skipped JSON validation"
fi

if [[ -e "$index_root/.git" ]]; then
  dirty=$("$GIT" -C "$index_root" status --short --untracked-files=all 2>/dev/null || true)
  if [[ -n "$dirty" ]]; then
    warn "working tree has uncommitted changes"
    print "$dirty"
  fi

  remote_sha=$("$GIT" -C "$index_root" ls-remote origin refs/heads/main 2>/dev/null | "$AWK" '{print $1}' || true)
  local_sha=$("$GIT" -C "$index_root" rev-parse HEAD 2>/dev/null || true)
  if [[ -z "$remote_sha" ]]; then
    warn "could not read origin/main with git ls-remote"
  elif [[ -z "$local_sha" ]]; then
    fail "could not read local HEAD"
  elif [[ "$remote_sha" != "$local_sha" ]]; then
    warn "local HEAD differs from origin/main local=${local_sha:0:12} remote=${remote_sha:0:12}"
  else
    report "local HEAD matches origin/main"
  fi
fi

case $check_status in
  0) report "MasterIndex drift check passed" ;;
  1) report "MasterIndex drift check completed with warnings" ;;
  *) report "MasterIndex drift check failed" ;;
esac

if (( strict )); then
  exit $check_status
fi
exit 0
