from setuptools import find_packages, setup
import subprocess
import re

def get_version_from_git():
    try:
        # Get the latest tag
        tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'], universal_newlines=True).strip()
        # Remove 'v' prefix if present and return
        return re.sub(r'^v', '', tag)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to a default version if git command fails
        return "0.0.0"

setup(
    name="lipomerge",
    version=get_version_from_git(),
    author="Falko Axmann",
    description="A tool to merge directories containing static libraries or other binaries into universal binaries.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/faaxm/lipomerge",
    license_file="License.txt",
    packages=find_packages(),
    py_modules=["lipomerge"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires=">=3.6",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "lipomerge=lipomerge:main",
        ],
    },
    test_suite="test",
)
