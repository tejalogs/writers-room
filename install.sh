#!/usr/bin/env bash
# Writers' Room installer: no Node.js required (needs bash plus git or curl + tar).
#
#   curl -fsSL https://raw.githubusercontent.com/tejalogs/writers-room/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/tejalogs/writers-room/main/install.sh | bash -s -- --claude
#
# Targets:
#   (default) --project   ./.agents/skills/writers-room   (Antigravity, Codex, Gemini CLI: this project)
#             --claude    ~/.claude/skills/writers-room    (Claude Code: all projects)
#             --path DIR  DIR/writers-room
# Options:
#             --ref REF   branch or tag to install (default: main)
set -euo pipefail

REPO="tejalogs/writers-room"
SKILL="writers-room"
REF="main"
DEST_PARENT=".agents/skills"

usage() {
  cat <<'EOF'
Writers' Room installer (no Node.js required)
  --project   install to ./.agents/skills/writers-room (default; Antigravity, Codex, Gemini CLI)
  --claude    install to ~/.claude/skills/writers-room (Claude Code)
  --path DIR  install to DIR/writers-room
  --ref REF   branch or tag to install (default: main)
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --project) DEST_PARENT=".agents/skills" ;;
    --claude)  DEST_PARENT="$HOME/.claude/skills" ;;
    --path)    shift; DEST_PARENT="${1:?--path needs a directory}" ;;
    --ref)     shift; REF="${1:?--ref needs a branch or tag}" ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1 (try --help)" >&2; exit 2 ;;
  esac
  shift
done

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "→ Downloading $REPO@$REF"
if command -v git >/dev/null 2>&1; then
  git clone --quiet --depth 1 --branch "$REF" "https://github.com/$REPO.git" "$TMP/repo"
elif command -v curl >/dev/null 2>&1 && command -v tar >/dev/null 2>&1; then
  mkdir -p "$TMP/repo"
  curl -fsSL "https://codeload.github.com/$REPO/tar.gz/$REF" | tar -xz -C "$TMP/repo" --strip-components=1
else
  echo "✗ Need git, or curl and tar, to download the skill." >&2
  exit 1
fi

SRC="$TMP/repo/skills/$SKILL"
if [ ! -f "$SRC/SKILL.md" ]; then
  echo "✗ Download looks wrong: $SRC/SKILL.md not found." >&2
  exit 1
fi

DEST="$DEST_PARENT/$SKILL"
mkdir -p "$DEST_PARENT"
if [ -e "$DEST" ]; then
  BACKUP="$DEST.bak-$(date +%Y%m%d-%H%M%S)"
  mv "$DEST" "$BACKUP"
  echo "→ Existing install moved to $BACKUP"
fi
cp -R "$SRC" "$DEST"

echo "✓ Installed Writers' Room to $DEST"
echo
echo "Next: ask your agent to \"write a blog / podcast script / ad / landing page / video script about ...\""
echo "Optional brand pack: mkdir -p .writers-room && cp -R \"$DEST/brand-template/\"* .writers-room/"
