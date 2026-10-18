#!/usr/bin/env python3
"""Create, check and edit an ASIC IP design specification written in the VLSIT template.

Actions :
  env                              report Python, openpyxl, PyMuPDF and LaTeX availability (read-only)
  init NAME --out FILE [--id ID]   copy the bundled template and fill the title, ip_name and document_id
  check FILE [--json]              verify structure and content (see below); exit 1 when errors exist
  mark-not-required FILE SECTION --reason TEXT [--date YYYY-MM-DD]
                                   replace the body of section "7" or "7.4" with the Not required line
  sections FILE                    list sections with their status: filled, not-required, N/A, TBD, placeholder
Checks  : all 22 sections present in order with the template titles; leftover template placeholders
          (<...>); "N/A" without a reason; "Not required" lines without date and reason; unique REQ-IDs
          in section 3 with a verification method; every REQ of section 3 appears in section 19;
          every REQ used elsewhere is defined; each TBD is listed in section 20.
Exit    : 0 success, 1 findings or error, 3 prerequisite missing.
Standard library only; text is read and written as UTF-8.
Examples:
  vlsit_spec_tool.py init "APB to TL-UL Bridge" --out apb2tlul_Design_Specification.md
  vlsit_spec_tool.py mark-not-required spec.md 7.4 --reason "no power domains in this IP"
  vlsit_spec_tool.py check spec.md
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "reference" / "templates" / "VLSIT_ASIC_IP_Design_Specification_Template.md"
PLACEHOLDER = r"<(?!/?(?:br|td|tr|th|table|p|strong|em|sup|sub|a|img|code|ul|li|details|summary)\b)[^<>\n]{1,80}>"
NR = "**Not required (confirmed by user, %s):** %s"
NR_RE = re.compile(r"\*\*Not required \(confirmed by user, (\d{4}-\d{2}-\d{2})\):\*\* \S")
REQ_RE = re.compile(r"\bREQ-[A-Z]+-\d{3}\b")


def read(path):
    return Path(path).read_text(encoding="utf-8")


def split_sections(text):
    """Return a list of (number, title, start_line, end_line) for '## N. Title' headings (outside code)."""
    lines, out, in_code = text.splitlines(), [], False
    for i, line in enumerate(lines):
        if line.startswith("```") or line.startswith("~~~"):
            in_code = not in_code
        m = None if in_code else re.match(r"## (\d+)\. (.*)", line)
        if m:
            out.append([int(m.group(1)), m.group(2).strip(), i, len(lines)])
    for a, b in zip(out, out[1:]):
        a[3] = b[2]
    return [tuple(s) for s in out]


def template_titles():
    return [(n, t) for n, t, _, _ in split_sections(read(TEMPLATE))]


def strip_code(text):
    return re.sub(r"(```|~~~).*?\1", "", text, flags=re.S)


def action_env(_a):
    ok = True
    print("python: %s" % sys.version.split()[0])
    for mod, label in (("openpyxl", "openpyxl (CSR workbook)"), ("pymupdf", "PyMuPDF (PDF conversion)")):
        found = importlib.util.find_spec(mod) is not None or (mod == "pymupdf" and importlib.util.find_spec("fitz") is not None)
        print("%s: %s" % (label, "found" if found else "MISSING (ask the user before installing)"))
    local = Path(os.environ.get("LOCALAPPDATA", "")) / "tectonic" / "tectonic.exe"
    tex = [c for c in ("tectonic", "pdflatex", "xelatex", "lualatex") if shutil.which(c) or (c == "tectonic" and local.is_file())]
    print("latex: %s" % (", ".join(tex) if tex else "MISSING (ask the user: install tectonic or MiKTeX, or use draw.io)"))
    return 0 if ok else 3


def action_init(a):
    out = Path(a.out)
    if out.exists() and not a.force:
        print("ERROR: %s already exists; pass --force to overwrite it" % out)
        return 1
    text = read(TEMPLATE)
    ident = a.id or re.sub(r"[^A-Z0-9]+", "-", a.name.upper()).strip("-") + "-SPEC"
    text = text.replace('"<PROJECT>-<IP>-SPEC"', '"%s"' % ident).replace('"<IP full name> Design Specification"', '"%s Design Specification"' % a.name)
    text = text.replace('ip_name: "<IP name>"', 'ip_name: "%s"' % a.name).replace("# <IP Name> Design Specification", "# %s Design Specification" % a.name)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print("OK: wrote %s from the template (%d sections)" % (out, len(template_titles())))
    return 0


def section_status(body):
    plain = strip_code(body)
    if NR_RE.search(plain):
        return "not-required"
    if re.search(r"\bN/A\b", plain) and len(plain.strip().splitlines()) <= 6:
        return "N/A"
    if re.search(r"<[A-Za-z][^<>\n]{0,80}>", plain.replace("<br>", "")):
        return "placeholder"
    if re.search(r"\bTBD\b", plain):
        return "TBD"
    return "filled"


def findings_for(text):
    errors, lines = [], text.splitlines()
    secs = split_sections(text)
    want = template_titles()
    got = [(n, t) for n, t, _, _ in secs]
    if got != want:
        missing = [w for w in want if w not in got]
        errors.append("sections differ from the template: missing %s; found %d of %d" % (missing[:4], len(got), len(want)))
    for n, title, s, e in secs:
        body = "\n".join(lines[s + 1:e])
        plain = strip_code(body)
        status = section_status(body)
        if status == "placeholder":
            hit = re.search(r"<[A-Za-z][^<>\n]{0,80}>", plain.replace("<br>", ""))
            errors.append("section %d: template placeholder left: %s" % (n, hit.group(0)))
        for m in re.finditer(r"\bN/A\b(?!\s*[-:(]\s*\S)", plain):
            line = plain[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")
            if "Mark inapplicable" not in line and "N/A with a reason" not in line:
                errors.append("section %d: 'N/A' without a reason near: ...%s..." % (n, line.strip()))
                break
        if "Not required" in plain and not NR_RE.search(plain):
            errors.append("section %d: 'Not required' line must read: %s" % (n, NR % ("YYYY-MM-DD", "reason")))
    sec = {n: "\n".join(lines[s:e]) for n, _, s, e in secs}
    s3, s19, s20 = sec.get(3, ""), sec.get(19, ""), sec.get(20, "")
    defined = {}
    for line in s3.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and cells and REQ_RE.fullmatch(cells[0]):
            if cells[0] in defined:
                errors.append("section 3: duplicate %s" % cells[0])
            defined[cells[0]] = cells
            if len(cells) < 5 or not cells[-1] or cells[-1].startswith("<"):
                errors.append("section 3: %s has no verification method" % cells[0])
            if not re.search(r"\b(shall|should|may)\b", cells[1] if len(cells) > 1 else "", re.I):
                errors.append("section 3: %s does not use shall/should/may" % cells[0])
    if 3 in sec and not defined and not NR_RE.search(s3):
        errors.append("section 3 defines no REQ-ID")
    in19 = set(REQ_RE.findall(s19))
    for req in defined:
        if req not in in19 and not NR_RE.search(s19):
            errors.append("%s is not traced in section 19" % req)
    used = set(REQ_RE.findall(strip_code(text)))
    for req in sorted(used - set(defined)):
        errors.append("%s is used but not defined in section 3" % req)
    tbd_secs = [n for n, _, s, e in secs if n != 20 and re.search(r"\bTBD\b", strip_code("\n".join(lines[s + 1:e])))]
    if tbd_secs and "TBD" not in s20:
        errors.append("TBD used in section(s) %s but section 20 records none" % tbd_secs)
    return errors


def action_check(a):
    text = read(a.file)
    errors = findings_for(text)
    if a.json:
        print(json.dumps({"errors": errors}, indent=2))
    else:
        for e in errors:
            print("ERROR: " + e)
        print("%s: %d error(s), %d section(s)" % ("PASS" if not errors else "FAIL", len(errors), len(split_sections(text))))
    return 1 if errors else 0


def action_sections(a):
    text = read(a.file)
    lines = text.splitlines()
    for n, title, s, e in split_sections(text):
        print("%2d %-48s %s" % (n, title[:48], section_status("\n".join(lines[s + 1:e]))))
    return 0


def action_mark(a):
    text = read(a.file)
    lines = text.splitlines()
    target = a.section.strip()
    pat = re.compile((r"## %s\. " if "." not in target else r"### %s ") % re.escape(target))
    idx = next((i for i, l in enumerate(lines) if pat.match(l)), None)
    if idx is None:
        print("ERROR: section %s not found" % target)
        return 1
    level = 2 if "." not in target else 3
    end = len(lines)
    for j in range(idx + 1, len(lines)):
        m = re.match(r"(#{1,6}) ", lines[j])
        if m and len(m.group(1)) <= level:
            end = j
            break
    new = lines[:idx + 1] + ["", NR % (a.date or date.today().isoformat(), a.reason), ""] + lines[end:]
    Path(a.file).write_text("\n".join(new).rstrip("\n") + "\n", encoding="utf-8")
    print("OK: section %s marked Not required (%d lines replaced)" % (target, end - idx - 1))
    return 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("env")
    i = sub.add_parser("init")
    i.add_argument("name")
    i.add_argument("--out", required=True)
    i.add_argument("--id")
    i.add_argument("--force", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("file")
    c.add_argument("--json", action="store_true")
    s = sub.add_parser("sections")
    s.add_argument("file")
    m = sub.add_parser("mark-not-required")
    m.add_argument("file")
    m.add_argument("section")
    m.add_argument("--reason", required=True)
    m.add_argument("--date")
    a = parser.parse_args()
    return {"env": action_env, "init": action_init, "check": action_check, "sections": action_sections,
            "mark-not-required": action_mark}[a.action](a)


if __name__ == "__main__":
    sys.exit(main())
