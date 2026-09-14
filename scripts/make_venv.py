##
# MIT License
#
# Copyright (c) 2020 - 2025 Andrew D. King
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
Create a per-OS virtual environment for the IPP exercise components.

The environment is named for the host OS (.venv-win, .venv-linux, or
.venv-macos) so that a single checkout on a drive shared between Windows 11
and WSL can hold a distinct venv for each host without collision. VS Code
selects the matching environment automatically: with exactly one present it
is discovered on open, and the launch configuration pins the right one per OS.

Run it with the interpreter you want the environment built from:

    python scripts/make_venv.py

Add --recreate to delete and rebuild an environment that already exists.
"""

import argparse
import platform
import shutil
import subprocess
import sys
import venv
from pathlib import Path

# Maps platform.system() to the friendly suffix used in the venv folder name.
# Windows 11 native and WSL both live on the shared drive, so each needs its
# own path; WSL reports 'Linux', which correctly shares the linux suffix.
OS_SUFFIX_MAP = {
    "Windows": "win",
    "Linux": "linux",
    "Darwin": "macos",
}


def resolve_venv_dir() -> Path:
    """
    Resolve the per-OS virtual environment directory at the repository root.

    Returns:
        The absolute path to the .venv-<suffix> directory for the host OS.

    Raises:
        SystemExit: If the host OS is not one of the supported platforms.
    """
    system = platform.system()
    suffix = OS_SUFFIX_MAP.get(system)

    if not suffix:
        supported = ", ".join(sorted(OS_SUFFIX_MAP))
        raise SystemExit(
            f"Unsupported platform '{system}'. Expected one of: {supported}."
        )

    # The script lives in <repo>/scripts, so the repository root is its parent.
    repo_root = Path(__file__).resolve().parent.parent

    return repo_root / f".venv-{suffix}"


def venv_python_path(venv_dir: Path) -> Path:
    """
    Return the path to the Python executable inside the given environment.

    Windows places the executable under 'Scripts', while Linux and macOS use
    'bin', so the correct subpath is chosen from the host OS.

    Args:
        venv_dir: The virtual environment directory.

    Returns:
        The path to the environment's Python interpreter.
    """
    if platform.system() == "Windows":
        return venv_dir / "Scripts" / "python.exe"

    return venv_dir / "bin" / "python"


def create_venv(venv_dir: Path, recreate: bool) -> None:
    """
    Create the virtual environment, optionally rebuilding an existing one.

    Args:
        venv_dir: The virtual environment directory to create.
        recreate: When True, delete an existing environment before creating it.
    """
    if venv_dir.exists():
        if not recreate:
            print(f"Environment already exists at {venv_dir}; nothing to do.")
            print("Pass --recreate to delete and rebuild it.")
            return

        print(f"Removing existing environment at {venv_dir}...")
        shutil.rmtree(venv_dir)

    print(f"Creating virtual environment at {venv_dir}...")

    # with_pip=True mirrors the default of `python -m venv`, so the new
    # environment can install the course requirements immediately.
    builder = venv.EnvBuilder(with_pip=True)
    builder.create(str(venv_dir))


def print_next_steps(venv_dir: Path) -> None:
    """
    Print the activation command and dependency-install hint for the host OS.

    Args:
        venv_dir: The virtual environment that was created.
    """
    python_path = venv_python_path(venv_dir)

    print()
    print("Done. The interpreter is at:")
    print(f"    {python_path}")
    print()
    print("Activate it with:")

    if platform.system() == "Windows":
        # Two forms, since students may use either shell on Windows.
        print(f"    {venv_dir}\\Scripts\\Activate.ps1    (PowerShell)")
        print(f"    {venv_dir}\\Scripts\\activate.bat    (Command Prompt)")
    else:
        print(f"    source {venv_dir}/bin/activate")

    print()
    print("Then install the course dependencies with:")
    print(f"    {python_path} -m pip install -r requirements.txt")


def main() -> None:
    """
    Parse arguments, create the per-OS environment, and report next steps.
    """
    arg_parser = argparse.ArgumentParser(
        description=(
            "Create a per-OS virtual environment (.venv-win, .venv-linux, or "
            ".venv-macos) for the IPP exercise components."
        )
    )

    arg_parser.add_argument(
        "--recreate",
        action="store_true",
        help="Delete and rebuild the environment if it already exists.",
    )

    args = arg_parser.parse_args()

    venv_dir = resolve_venv_dir()

    create_venv(venv_dir, args.recreate)
    print_next_steps(venv_dir)


if __name__ == "__main__":
    """
    Entry point when invoked as a script from the command line.
    """
    # Guard against an accidental Python 2 invocation with a clear message
    # rather than a confusing syntax error later in the run.
    if sys.version_info < (3, 8):
        raise SystemExit("This script requires Python 3.8 or newer.")

    main()
