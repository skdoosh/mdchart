#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

def find_executable():
    """Find the mdchart executable in the system PATH."""
    # First try to find the executable in PATH
    executable = shutil.which('mdchart')
    if executable:
        return executable
    
    # If not found in PATH, check common installation locations
    common_paths = [
        '/usr/local/bin/mdchart',
        '/usr/bin/mdchart',
        os.path.expanduser('~/.local/bin/mdchart')
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    raise FileNotFoundError(
        "Could not find mdchart executable. Please make sure it is installed "
        "and available in your PATH. You can install it by running 'make' "
        "in the project directory."
    )

def main():
    try:
        executable = find_executable()
        result = subprocess.run([executable] + sys.argv[1:])
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running mdchart: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 