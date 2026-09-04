#!/usr/bin/env bash
# Builds the Power Automate import package (.zip) for LU1 Activity 1.
#
# Reads GEMINI_API_KEY from the repo-root .env and injects it into the flow
# definition at build time, so the key is never stored in a tracked source file.
#
# Usage:  ./build-package.sh            -> package WITH the key baked in
#         ./build-package.sh --no-key   -> package with a placeholder instead
#
# The resulting zip is git-ignored. Do not commit it: with the key baked in it
# is a credential.

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$HERE/../.." && pwd)"
ENV_FILE="$REPO_ROOT/.env"
BUILD="$HERE/.build"
OUT="$HERE/LU1-Activity1-MarinaTrust-PowerAutomate.zip"

PLACEHOLDER="PASTE_YOUR_GEMINI_API_KEY_HERE"
KEY="$PLACEHOLDER"

if [[ "${1:-}" != "--no-key" ]]; then
  if [[ -f "$ENV_FILE" ]]; then
    # shellcheck disable=SC1090
    KEY="$(grep -E '^GEMINI_API_KEY=' "$ENV_FILE" | head -1 | cut -d= -f2- | tr -d '"'"'"' \r\n')"
    if [[ -z "$KEY" ]]; then
      echo "warning: GEMINI_API_KEY empty in .env — using placeholder" >&2
      KEY="$PLACEHOLDER"
    fi
  else
    echo "warning: no .env at $ENV_FILE — using placeholder" >&2
  fi
fi

rm -rf "$BUILD" "$OUT"
mkdir -p "$BUILD/Microsoft.Flow/flows/LU1MarinaTrustOnboarding"

python3 "$HERE/make-package.py" "$BUILD" "$KEY"

( cd "$BUILD" && zip -qr "$OUT" . )
rm -rf "$BUILD"

if [[ "$KEY" == "$PLACEHOLDER" ]]; then
  echo "Built (placeholder key): $OUT"
  echo "After import, open the 'Gemini decision' HTTP action and paste your key into the URI."
else
  echo "Built (key baked in): $OUT"
  echo "This zip contains a live API key — do not commit or share it."
fi
