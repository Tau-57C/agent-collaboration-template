#!/bin/bash
set -eu

source_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd -P)

if [ "$#" -eq 2 ] && [ "$1" = "--project" ]; then
    project=$2
elif [ "$#" -eq 0 ]; then
    project=$(/usr/bin/osascript <<'APPLESCRIPT'
try
    set projectFolder to choose folder with prompt "Choose the project root for Agent Collaboration."
    return POSIX path of projectFolder
on error number -128
    return ""
end try
APPLESCRIPT
    )
    if [ -z "$project" ]; then
        exit 0
    fi
else
    printf '%s\n' 'Usage: Install on macOS.command [--project PATH]' >&2
    exit 2
fi

if ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 11))'; then
    printf '%s\n' 'Setup needs Python 3.11 or later available as python3.' >&2
    exit 1
fi

python3 "$source_dir/tools/install.py" "$project" --apply
printf '\n%s\n' 'Open the project in your assistant.' \
    'New project: Initialize collaboration.' \
    'Existing project: Import the existing project.'
