#!/usr/bin/env python3
import os
import sys
import subprocess
import pkg_resources

def find_executable():
    """Find the mdchart executable in the package."""
    try:
        # Get the package's location
        package_dir = os.path.dirname(os.path.abspath(__file__))
        executable = os.path.join(package_dir, 'bin', 'mdchart')
        
        if os.path.exists(executable):
            return executable
        
        # If not found in the package, try the system path
        result = subprocess.run(['which', 'mdchart'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        
        raise FileNotFoundError("Could not find mdchart executable")
    except Exception as e:
        print(f"Error finding mdchart executable: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    try:
        executable = find_executable()
        os.execv(executable, [executable] + sys.argv[1:])
    except Exception as e:
        print(f"Error running mdchart: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 