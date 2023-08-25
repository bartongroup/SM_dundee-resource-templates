#!/bin/bash

# Get the directory of the currently executing script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Confirm with the user
read -p "This will permanently delete all app data. Are you sure? [y/N] " -n 1 -r
echo    # Move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Wipe the directories
    rm -rf "$DIR/../db/"
    rm -rf "$DIR/../logs/"
    rm -rf "$DIR/../sessions/"

    echo "App data wiped successfully!"
else
    echo "Operation aborted."
fi
