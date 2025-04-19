#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PACKAGE_DIR="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

# Run the mdchart executable
if [ -x "$SCRIPT_DIR/bin/mdchart" ]; then
    exec "$SCRIPT_DIR/bin/mdchart" "$@"
elif [ -x "$PACKAGE_DIR/mdchart/bin/mdchart" ]; then
    exec "$PACKAGE_DIR/mdchart/bin/mdchart" "$@"
else
    echo "Error: Could not find mdchart executable"
    exit 1
fi 