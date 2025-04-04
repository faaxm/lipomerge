# lipomerge

This package merges two directories containing static libraries for two different architectures into one directory with universal binaries. Files that don't end in ".a" or are mach-O binaries (Typically `.dylib` or executable) will just be copied over from the first directory.

## Installation

To install the package, use:

```
pip install lipomerge
```

## Usage

Run it like this:

```
python3 -m lipomerge <arm64-dir-tree> <x64-dir-tree> <universal-output-dir>
```

## Requirements

- macOS
- `lipo` must be installed on your system.

## License

This project is licensed under the GPL v3 license.

## Resources
* [A blog post on using lipo to build universal binaries](https://www.f-ax.de/dev/2021/01/15/build-fat-macos-library.html)
* [A blog post on building universal binaries with vcpkg](https://www.f-ax.de/dev/2022/11/09/how-to-use-vcpkg-with-universal-binaries-on-macos/)

## Contribute

Style is enforced by pre-commit:

```
pip install pre-commit
pre-commit install
```
