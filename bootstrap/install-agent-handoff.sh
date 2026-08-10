#!/bin/zsh
set -eu

script_dir=${0:A:h}
index_root=${script_dir:h}
block=${script_dir}/MASTERINDEX_MANAGED_BLOCK.md

install_block() {
  local file=$1
  local temp_file
  temp_file=$(mktemp)

  if [[ ! -f $file ]]; then
    cp "$block" "$file"
    return
  fi

  if rg -q '<!-- MASTERINDEX:START -->' "$file"; then
    awk -v block="$block" '
      /<!-- MASTERINDEX:START -->/ {
        while ((getline line < block) > 0) print line
        close(block)
        skipping = 1
        next
      }
      skipping && /<!-- MASTERINDEX:END -->/ { skipping = 0; next }
      !skipping { print }
    ' "$file" > "$temp_file"
  else
    cat "$file" > "$temp_file"
    print >> "$temp_file"
    cat "$block" >> "$temp_file"
  fi

  mv "$temp_file" "$file"
}

claude_is_clean() {
  local repo=$1
  git -C "$repo" diff --quiet -- CLAUDE.md &&
    git -C "$repo" diff --cached --quiet -- CLAUDE.md &&
    [[ -z $(git -C "$repo" ls-files --others --exclude-standard -- CLAUDE.md) ]]
}

while IFS= read -r repo_path; do
  repo=${repo_path/#\~/$HOME}
  if [[ ! -d $repo ]]; then
    print "UNRESOLVED\t${repo_path}"
    continue
  fi

  install_block "$repo/AGENTS.md"
  if claude_is_clean "$repo"; then
    install_block "$repo/CLAUDE.md"
    print "UPDATED\t${repo_path}\tAGENTS.md, CLAUDE.md"
  else
    print "CLAUDE-DIRTY\t${repo_path}\tAGENTS.md only"
  fi
done < <(jq -r '.repos[].repo' "$index_root/current/index.json")
