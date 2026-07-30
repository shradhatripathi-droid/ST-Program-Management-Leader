#!/bin/bash
set -euo pipefail

REPO_URL="https://github.com/shradhatripathi-droid/ST-Program-Management-Leader.git"
ROOT="$(cd "$(dirname "$0")" && pwd)"

cd "$ROOT"

if ! command -v git >/dev/null 2>&1; then
  echo "Git is not installed. Install Xcode Command Line Tools:"
  echo "  xcode-select --install"
  exit 1
fi

if [ ! -d .git ]; then
  git init
  git branch -M main
  git remote add origin "$REPO_URL"
else
  git remote set-url origin "$REPO_URL"
fi

git add index.html experience-detail_5.html index-v2.html README.md GITHUB_SETUP.md .nojekyll assets/ open-portfolio.sh push-to-github.sh .gitignore
git commit -m "Publish program management leader portfolio" || true
git push -u origin main

echo ""
echo "Done. GitHub Pages:"
echo "  https://github.com/shradhatripathi-droid/ST-Program-Management-Leader/settings/pages"
echo ""
echo "Live site:"
echo "  https://shradhatripathi-droid.github.io/ST-Program-Management-Leader/"
