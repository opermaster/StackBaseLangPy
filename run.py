"""
Build and test runner for the custom language compiler.
Replaces the Makefile: examples/<name>.txt -> build/<name>.c (via src/main.py)
                        -> build/<name>(.exe) (via gcc + lib/stack.c)

Subcommands:
  ctest              - create reference (expected) test results (results/<name>.txt)
  test               - build all files and compare their output to the reference results
  compile <index>    - build a single file by its index in FILES
  last               - build the last file in FILES

Programs using scanf/fgets:
  If a test <name> needs stdin input, put the data it expects in
  inputs/<name>.txt - it will be piped into the program automatically.
  If no such file exists but the program still waits for input, a
  timeout (see TIMEOUT) kicks in and the test is marked as SKIPPED
  instead of hanging the whole script.
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

# ---------- Path constants ----------
ROOT_DIR = Path(__file__).resolve().parent

SRC_DIR = ROOT_DIR / "src"
MAIN_PY = SRC_DIR / "main.py"

EXAMPLES_DIR = ROOT_DIR / "examples"
BUILD_DIR = ROOT_DIR / "build"
LIB_DIR = ROOT_DIR / "lib"
LIB_SOURCE = LIB_DIR / "stack.c"

RESULTS_DIR = ROOT_DIR / "results"   # reference (expected) outputs
INPUTS_DIR = ROOT_DIR / "inputs"     # stdin data for tests using scanf/fgets

EXE_SUFFIX = ".exe" if os.name == "nt" else ""

# ---------- List of test files (without extension) ----------
FILES = [
    "first",
    "second",
    "third",
    "forth",
    "fifth",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven"
]

TIMEOUT = 5  # seconds. Prevents programs waiting for input (with no inputs file) from hanging tests


def ensure_dirs():
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    INPUTS_DIR.mkdir(parents=True, exist_ok=True)


def compile_file(name: str) -> Path:
    """Build examples/<name>.txt -> build/<name>.c -> build/<name>(.exe)"""
    src_txt = EXAMPLES_DIR / f"{name}.txt"
    out_c = BUILD_DIR / f"{name}.c"
    out_exe = BUILD_DIR / f"{name}{EXE_SUFFIX}"

    if not src_txt.exists():
        raise FileNotFoundError(f"Example file not found: {src_txt}")

    print(f"[{name}] Compiling to C...")
    subprocess.run(
        [sys.executable, str(MAIN_PY), str(src_txt), str(out_c)],
        check=True,
    )

    print(f"[{name}] Compiling to exe (gcc)...")
    subprocess.run(
        [
            "gcc",
            str(LIB_SOURCE),
            "-o", str(out_exe),
            str(out_c),
            "-I", str(LIB_DIR),
        ],
        check=True,
    )

    return out_exe


def get_input_data(name: str):
    """Return the content of inputs/<name>.txt to use as stdin, or None if it doesn't exist."""
    input_file = INPUTS_DIR / f"{name}.txt"
    if input_file.exists():
        return input_file.read_text(encoding="utf-8")
    return None


def run_exe(exe_path: Path, name: str):
    """
    Run the compiled exe.
    If an input file exists, feed it to stdin.
    If no input file exists but the program still waits for input (scanf/fgets),
    TIMEOUT kicks in and the function returns None (test will be SKIPPED).
    """
    input_data = get_input_data(name)
    try:
        result = subprocess.run(
            [str(exe_path)],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return None


def cmd_ctest():
    """Build all files and save their output as the reference result."""
    ensure_dirs()
    for name in FILES:
        try:
            exe_path = compile_file(name)
        except subprocess.CalledProcessError:
            print(f"[{name}] BUILD ERROR, skipping.")
            continue

        output = run_exe(exe_path, name)
        if output is None:
            print(
                f"[{name}] Program is waiting for input and inputs/{name}.txt "
                f"doesn't exist - reference NOT saved. Add inputs/{name}.txt if needed."
            )
            continue

        result_file = RESULTS_DIR / f"{name}.txt"
        result_file.write_text(output, encoding="utf-8")
        print(f"[{name}] Reference result saved: {result_file}")


def cmd_test():
    """Build all files and compare their output to the reference results."""
    ensure_dirs()
    passed, failed, skipped = 0, 0, 0

    for name in FILES:
        result_file = RESULTS_DIR / f"{name}.txt"

        try:
            exe_path = compile_file(name)
        except subprocess.CalledProcessError:
            print(f"[{name}] BUILD ERROR")
            failed += 1
            continue

        output = run_exe(exe_path, name)

        if output is None:
            print(f"[{name}] SKIPPED (needs stdin input, inputs/{name}.txt doesn't exist)")
            skipped += 1
            continue

        if not result_file.exists():
            print(f"[{name}] No reference in results/{name}.txt - run 'ctest' first")
            skipped += 1
            continue

        expected = result_file.read_text(encoding="utf-8")
        if output == expected:
            print(f"[{name}] OK")
            passed += 1
        else:
            print(f"[{name}] FAIL: output doesn't match the reference")
            print(f"  Expected: {expected!r}")
            print(f"  Got:      {output!r}")
            failed += 1

    print(f"\nTotal: {passed} OK, {failed} FAIL, {skipped} SKIPPED")


def cmd_compile(index: int):
    """Build a single file by its index in FILES."""
    ensure_dirs()
    if index < 0 or index >= len(FILES):
        print(f"Invalid index {index}. Valid range: 0..{len(FILES) - 1}")
        return
    name = FILES[index]
    exe_path = compile_file(name)
    print(f"[{name}] Done: {exe_path}")


def cmd_last():
    """Build the last file in FILES."""
    ensure_dirs()
    name = FILES[-1]
    exe_path = compile_file(name)
    print(f"[{name}] Done: {exe_path}")


def main():
    parser = argparse.ArgumentParser(description="Build and test runner for the custom language compiler")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("ctest", help="Create reference test results")
    subparsers.add_parser("test", help="Build all files and compare with reference results")

    compile_parser = subparsers.add_parser("compile", help="Build a single file by index")
    compile_parser.add_argument("index", type=int, help="Index of the file in FILES")

    subparsers.add_parser("last", help="Build the last file in FILES")

    args = parser.parse_args()

    if args.command == "ctest":
        cmd_ctest()
    elif args.command == "test":
        cmd_test()
    elif args.command == "compile":
        cmd_compile(args.index)
    elif args.command == "last":
        cmd_last()


if __name__ == "__main__":
    main()
