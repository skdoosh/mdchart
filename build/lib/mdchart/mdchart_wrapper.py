#!/usr/bin/env python3
import os
import sys
import subprocess
import pkg_resources

def find_executable():
    """Find the mdchart executable."""
    try:
        # Get the package's location
        package_dir = os.path.dirname(os.path.abspath(__file__))
        executable = os.path.join(package_dir, 'bin', 'mdchart')
        
        if os.path.exists(executable):
            return executable
        
        raise FileNotFoundError("Could not find mdchart executable")
    except Exception as e:
        print(f"Error finding mdchart executable: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    try:
        executable = find_executable()
        os.chmod(executable, 0o755)  # Make executable
        result = subprocess.run([executable] + sys.argv[1:])
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running mdchart: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 