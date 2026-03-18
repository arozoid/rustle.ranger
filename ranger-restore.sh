#!/usr/bin/env bash
# ranger-restore.sh
# Usage: ranger-restore.sh DEST N
DEST="$1"
N="$2"

# move the N most recent files from ranger-trash to DEST
ls -1t ~/.ranger/ranger-trash | head -n "$N" | while read f; do
    mv "$HOME/.ranger/ranger-trash/$f" "$DEST"
done
