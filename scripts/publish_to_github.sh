#!/usr/bin/env bash
# Create the public portfolio repository (if needed) and push the current branch.
# Run from the repository root after `gh auth login`.

set -euo pipefail

repository="Shashankpabitwar123/prepinterview-ai-product-analytics"
branch="$(git branch --show-current)"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree is not clean. Commit or stash changes before publishing."
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI is not authenticated. Run: gh auth login"
  exit 1
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  if gh repo view "$repository" >/dev/null 2>&1; then
    git remote add origin "https://github.com/$repository.git"
  else
    gh repo create "$repository" --public --source=. --remote=origin
  fi
fi

git push -u origin "$branch"
echo "Published: https://github.com/$repository"
