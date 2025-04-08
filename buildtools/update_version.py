#!/usr/bin/env python3
import os
import re
import subprocess
import sys


def get_latest_version():
    try:
        # Get the latest tag
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=True,
        )
        tag = result.stdout.strip()

        # Extract version number from tag (remove 'v' prefix)
        version = tag.lstrip("v")
        return version
    except subprocess.CalledProcessError:
        print("Error: No git tags found", file=sys.stderr)
        sys.exit(1)


def update_setup_py(version):
    setup_py_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "setup.py")
    with open(setup_py_path, "r") as f:
        content = f.read()

    # Replace version string
    new_content = re.sub(r'version="[^"]*"', f'version="{version}"', content)

    with open(setup_py_path, "w") as f:
        f.write(new_content)


def main():
    version = get_latest_version()
    update_setup_py(version)
    print(f"Updated setup.py with version {version}")


if __name__ == "__main__":
    main()
