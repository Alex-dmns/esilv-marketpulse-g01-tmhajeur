#!/usr/bin/env bash
# Print the next semantic version tag from the commit messages since the last tag.
#   feat!: or BREAKING CHANGE -> MAJOR
#   feat:                     -> MINOR
#   anything else (fix:, ...) -> PATCH
# First release: v1.0.0
set -euo pipefail

last_tag=$(git describe --tags --abbrev=0 --match 'v[0-9]*.[0-9]*.[0-9]*' 2>/dev/null || true)

if [ -z "$last_tag" ]; then
  echo "v1.0.0"
  exit 0
fi

subjects=$(git log --format=%s "${last_tag}..HEAD")
bodies=$(git log --format=%b "${last_tag}..HEAD")

IFS=. read -r major minor patch <<< "${last_tag#v}"

if grep -qE '^[a-z]+(\([^)]*\))?!:' <<< "$subjects" || grep -q 'BREAKING CHANGE' <<< "$bodies"; then
  major=$((major + 1)); minor=0; patch=0
elif grep -qE '^feat(\([^)]*\))?:' <<< "$subjects"; then
  minor=$((minor + 1)); patch=0
else
  patch=$((patch + 1))
fi

echo "v${major}.${minor}.${patch}"
