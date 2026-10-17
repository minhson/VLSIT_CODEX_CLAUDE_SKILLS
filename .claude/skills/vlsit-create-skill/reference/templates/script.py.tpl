#!/usr/bin/env python3
"""TODO(fill): one line - what this script does for the skill.

Actions:
  check   report whether this machine is ready (read-only)
  run     TODO(fill): the main task

Exit codes: 0 success, 1 error (the message is the last line), 3 a prerequisite
is missing.

Standard library only. Text files are always read and written as UTF-8, because
the default encoding on Windows is the local code page.

Examples:
  {{SCRIPT}} check
  {{SCRIPT}} run input.txt --out result.txt
"""
import argparse
import sys
from pathlib import Path


def action_check(_args):
    # TODO(fill): test every prerequisite; print READY, or NOT READY plus a "missing:" line
    print("READY")
    return 0


def action_run(args):
    source = Path(args.path)
    if not source.is_file():
        print("ERROR: input file not found: %s" % source)
        return 1
    text = source.read_text(encoding="utf-8")
    # TODO(fill): do the work; print one result line, not the full data
    if args.out:
        out = Path(args.out)
        if out.exists() and not args.force:
            print("ERROR: %s already exists; pass --force to overwrite it" % out)
            return 1
        out.write_text(text, encoding="utf-8")
        print("OK: wrote %s" % out)
    else:
        print("OK: read %d characters from %s" % (len(text), source))
    return 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("check", help="report whether this machine is ready")
    run = sub.add_parser("run", help="do the main task")
    run.add_argument("path", help="input file")
    run.add_argument("--out", help="output file")
    run.add_argument("--force", action="store_true", help="overwrite an existing output file")
    args = parser.parse_args()
    return {"check": action_check, "run": action_run}[args.action](args)


if __name__ == "__main__":
    sys.exit(main())
