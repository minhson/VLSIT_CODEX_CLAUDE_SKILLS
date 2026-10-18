#!/usr/bin/env python3
"""Waveform helper for the bundled offline WaveDrom: VCD reading, WaveJSON check, HTML viewer.

Actions:
  check            report whether the bundled WaveDrom files are present and unchanged
  vcd-info         list the signals, scopes and time range of a VCD file
  vcd-to-wavejson  convert chosen signals and a time window of a VCD file to WaveJSON
  lint             check the structure of a WaveJSON file (strict JSON)
  html             build one self-contained HTML viewer from a WaveJSON file

Exit codes: 0 success, 1 error or lint errors (the message is the last line),
3 a bundled asset is missing or has a wrong checksum.

Standard library only. Text files are always read and written as UTF-8. The WaveDrom
library is read from ../assets/wavedrom and is inlined into the HTML, so the viewer
needs no network.

Examples:
  wavedrom_waveform.py check
  wavedrom_waveform.py vcd-info sim.vcd
  wavedrom_waveform.py vcd-to-wavejson sim.vcd --signals "clk,top.dut.data*" --start 100ns --end 500ns --out w.json
  wavedrom_waveform.py lint w.json
  wavedrom_waveform.py html w.json --out w.html --title "Write cycle"
"""
import argparse
import fnmatch
import hashlib
import html as htmllib
import json
import re
import sys
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "wavedrom"
CHECKSUMS = ROOT / "assets" / "CHECKSUMS.txt"
LIB_FILES = ["wavedrom.unpkg.min.js", "skins/default.js"]
WAVE_CHARS = set("pnPNlhLH01xzud=2345.|")
DATA_CHARS = set("=2345")
UNITS = {"s": 1, "ms": 10 ** -3, "us": 10 ** -6, "ns": 10 ** -9, "ps": 10 ** -12, "fs": 10 ** -15}
MAX_CYCLES = 400


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_checksums():
    table = {}
    for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) == 2 and re.fullmatch(r"[0-9a-f]{64}", parts[0]):
            table[parts[1].lstrip("*")] = parts[0]
    return table


def asset_problems():
    problems = []
    if not CHECKSUMS.is_file():
        return ["missing: assets/CHECKSUMS.txt"]
    table = expected_checksums()
    for name in LIB_FILES + ["LICENSE"]:
        path = ASSETS / name
        if not path.is_file():
            problems.append("missing: assets/wavedrom/%s" % name)
        elif table.get(name) != sha256(path):
            problems.append("checksum mismatch: assets/wavedrom/%s" % name)
    return problems


def action_check(_args):
    problems = asset_problems()
    if problems:
        print("NOT READY")
        print("; ".join(problems))
        return 3
    print("READY: WaveDrom assets present, SHA-256 match")
    return 0


# ----------------------------------------------------------------------------- VCD

class Vcd:
    def __init__(self):
        self.timescale = (1, "ns")
        self.vars = []          # dicts: id, name, scope, width, kind
        self.changes = {}       # id -> [(time, value)]
        self.end = 0


def parse_vcd(path):
    vcd = Vcd()
    scope = []
    tokens = Path(path).read_text(encoding="utf-8", errors="replace").split()
    i, n, now = 0, len(tokens), 0
    in_defs = True
    while i < n:
        tok = tokens[i]
        if in_defs:
            if tok == "$timescale":
                j = tokens.index("$end", i)
                text = "".join(tokens[i + 1:j])
                m = re.fullmatch(r"(\d+)([a-z]+)", text)
                if m and m.group(2) in UNITS:
                    vcd.timescale = (int(m.group(1)), m.group(2))
                i = j
            elif tok == "$scope":
                scope.append(tokens[i + 2])
                i = tokens.index("$end", i)
            elif tok == "$upscope":
                if scope:
                    scope.pop()
                i = tokens.index("$end", i)
            elif tok == "$var":
                j = tokens.index("$end", i)
                body = tokens[i + 1:j]
                if len(body) >= 4:
                    vcd.vars.append({"kind": body[0], "width": int(body[1]) if body[1].isdigit() else 1,
                                     "id": body[2], "name": body[3], "scope": ".".join(scope)})
                i = j
            elif tok == "$enddefinitions":
                in_defs = False
                i = tokens.index("$end", i)
        else:
            if tok.startswith("#") and tok[1:].isdigit():
                now = int(tok[1:])
                vcd.end = max(vcd.end, now)
            elif tok in ("$dumpvars", "$dumpall", "$dumpon", "$dumpoff", "$end", "$comment"):
                if tok == "$comment":
                    i = tokens.index("$end", i)
            elif tok[0] in "bB" and i + 1 < n:
                vcd.changes.setdefault(tokens[i + 1], []).append((now, tok[1:].lower()))
                i += 1
            elif tok[0] in "rR" and i + 1 < n:
                vcd.changes.setdefault(tokens[i + 1], []).append((now, "real"))
                i += 1
            elif tok[0] in "01xXzZ" and len(tok) > 1:
                vcd.changes.setdefault(tok[1:], []).append((now, tok[0].lower()))
        i += 1
    return vcd


def full_name(v):
    return (v["scope"] + "." if v["scope"] else "") + v["name"]


def to_ticks(text, vcd):
    """Convert '100', '100ns' or '1.5us' to VCD time units."""
    m = re.fullmatch(r"\s*([0-9.]+)\s*([a-z]*)\s*", text)
    if not m:
        raise ValueError("bad time value: %s" % text)
    value, unit = float(m.group(1)), m.group(2)
    if not unit:
        return int(round(value))
    if unit not in UNITS:
        raise ValueError("unknown time unit: %s" % unit)
    scale = vcd.timescale[0] * UNITS[vcd.timescale[1]]
    return int(round(value * UNITS[unit] / scale))


def action_vcd_info(args):
    path = Path(args.vcd)
    if not path.is_file():
        print("ERROR: VCD file not found: %s" % path)
        return 1
    vcd = parse_vcd(path)
    print("timescale: %d%s; last time: %d; signals: %d" % (vcd.timescale + (vcd.end, len(vcd.vars))))
    shown = 0
    for v in vcd.vars:
        count = len(vcd.changes.get(v["id"], []))
        if args.active and count <= 1:
            continue
        if shown >= args.max:
            print("... %d more; narrow with --pattern or --active" % (len(vcd.vars) - shown))
            break
        if args.pattern and not fnmatch.fnmatch(full_name(v), args.pattern):
            continue
        print("%-50s width=%-3d changes=%d" % (full_name(v), v["width"], count))
        shown += 1
    return 0


def sample(changes, t):
    value = "x"
    for time, val in changes:
        if time > t:
            break
        value = val
    return value


def wave_for(var, changes, ticks):
    wave, data, last = [], [], None
    for t in ticks:
        value = sample(changes, t)
        if var["width"] == 1 and value in ("0", "1", "x", "z"):
            ch, label = value, None
        elif value == "real":
            raise ValueError("%s is a real-valued signal; analog signals are not supported" % full_name(var))
        else:
            bits = value.rjust(var["width"], value[0] if value[0] in "xz" else "0")
            if set(bits) == {"x"}:
                ch, label = "x", None
            elif set(bits) == {"z"}:
                ch, label = "z", None
            else:
                ch = "="
                label = bits if ("x" in bits or "z" in bits) else "%X" % int(bits, 2)
        key = (ch, label)
        if key == last:
            wave.append(".")
        else:
            wave.append(ch)
            if label is not None:
                data.append(label)
        last = key
    return "".join(wave), data


def build_groups(entries, force_group):
    scopes = {e["scope"] for e in entries}
    if len(scopes) <= 1 and not force_group:
        return [e["item"] for e in entries]
    root = {"items": [], "kids": {}}
    for e in entries:
        node = root
        for part in (e["scope"].split(".") if e["scope"] else ["top"]):
            node = node["kids"].setdefault(part, {"items": [], "kids": {}})
        node["items"].append(e["item"])

    def render(name, node):
        return [name] + node["items"] + [render(k, v) for k, v in node["kids"].items()]

    return [render(k, v) for k, v in root["kids"].items()]


def action_vcd_to_wavejson(args):
    path = Path(args.vcd)
    if not path.is_file():
        print("ERROR: VCD file not found: %s" % path)
        return 1
    out = Path(args.out) if args.out else None
    if out and out.exists() and not args.force:
        print("ERROR: %s already exists; pass --force to overwrite it" % out)
        return 1
    vcd = parse_vcd(path)
    patterns = [p.strip() for p in args.signals.split(",") if p.strip()] if args.signals else ["*"]
    chosen = []
    for v in vcd.vars:
        name = full_name(v)
        if any(fnmatch.fnmatch(name, p) or fnmatch.fnmatch(v["name"], p) for p in patterns):
            if v["id"] not in {c["id"] for c in chosen}:
                chosen.append(v)
    if not chosen:
        print("ERROR: no signal matches %s; run vcd-info to list the names" % patterns)
        return 1
    try:
        start = to_ticks(args.start, vcd) if args.start else 0
        end = to_ticks(args.end, vcd) if args.end else vcd.end
        step = to_ticks(args.period, vcd) if args.period else 0
    except ValueError as exc:
        print("ERROR: %s" % exc)
        return 1
    if args.period and step <= 0:
        print("ERROR: --period %s is shorter than one VCD time unit (%d%s)" % ((args.period,) + vcd.timescale))
        return 1
    if end <= start:
        print("ERROR: the window is empty (start %d, end %d)" % (start, end))
        return 1
    if not step:                       # finest step that keeps every change inside the window on a tick
        step = 0
        for v in chosen:
            for time, _ in vcd.changes.get(v["id"], []):
                if start < time <= end:
                    step = gcd(step, time - start)
        step = step or (end - start)
    cycles = (end - start) // step + 1
    if cycles > MAX_CYCLES:
        print("ERROR: %d cycles exceed the limit of %d; narrow the window or pass a larger --period" % (cycles, MAX_CYCLES))
        return 1
    ticks = [start + k * step for k in range(cycles)]
    entries = []
    try:
        for v in chosen:
            wave, data = wave_for(v, vcd.changes.get(v["id"], []), ticks)
            item = {"name": v["name"], "wave": wave}
            if data:
                item["data"] = data
            entries.append({"scope": v["scope"], "item": item})
    except ValueError as exc:
        print("ERROR: %s" % exc)
        return 1
    unit = "%d%s" % vcd.timescale
    doc = {"signal": build_groups(entries, args.group),
           "head": {"text": "%s: t=%d..%d (%s units), %d per cycle" % (path.name, start, end, unit, step)}}
    text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    if out:
        out.write_text(text, encoding="utf-8")
        print("OK: wrote %s (%d signals, %d cycles, step %d x %s)" % (out, len(chosen), cycles, step, unit))
    else:
        sys.stdout.write(text)
    return 0


# ----------------------------------------------------------------------------- WaveJSON lint

def lint_signals(items, problems, nodes, path="signal"):
    for idx, item in enumerate(items):
        where = "%s[%d]" % (path, idx)
        if isinstance(item, list):
            start = 1 if item and isinstance(item[0], str) else 0
            lint_signals(item[start:], problems, nodes, where)
        elif isinstance(item, dict):
            if not item:
                continue
            if "wave" in item:
                wave = item["wave"]
                if not isinstance(wave, str):
                    problems.append(("error", "%s: wave must be a string" % where))
                    continue
                bad = sorted({c for c in wave if c not in WAVE_CHARS})
                if bad:
                    problems.append(("error", "%s (%s): invalid wave characters %s" % (where, item.get("name", "?"), "".join(bad))))
                if wave[:1] == ".":
                    problems.append(("error", "%s (%s): wave cannot start with '.'" % (where, item.get("name", "?"))))
                need = sum(1 for c in wave if c in DATA_CHARS)
                data = item.get("data", [])
                have = len(data.split()) if isinstance(data, str) else len(data) if isinstance(data, list) else -1
                if have < 0:
                    problems.append(("error", "%s: data must be a list or a string" % where))
                elif have < need:
                    problems.append(("warning", "%s (%s): %d data labels for %d '='-type cells" % (where, item.get("name", "?"), have, need)))
                if not isinstance(item.get("name", ""), str):
                    problems.append(("error", "%s: name must be a string" % where))
            elif "name" not in item and "node" not in item:
                problems.append(("warning", "%s: entry without name or wave" % where))
            for key in ("period", "phase"):
                if key in item and not isinstance(item[key], (int, float)):
                    problems.append(("error", "%s: %s must be a number" % (where, key)))
            if isinstance(item.get("period"), (int, float)) and item["period"] <= 0:
                problems.append(("error", "%s: period must be positive" % where))
            if isinstance(item.get("node"), str):
                nodes.update(c for c in item["node"] if c not in ".")
        else:
            problems.append(("error", "%s: must be an object or a group array" % where))


def lint_doc(doc):
    problems, nodes = [], set()
    if not isinstance(doc, dict) or not isinstance(doc.get("signal"), list):
        return [("error", "top level must be an object with a 'signal' array")]
    lint_signals(doc["signal"], problems, nodes)
    for edge in doc.get("edge", []) if isinstance(doc.get("edge"), list) else []:
        m = re.match(r"\s*(\S)\S*?\s*(\S)\s*", edge) if isinstance(edge, str) else None
        ends = re.findall(r"[A-Za-z]", edge.split(" ")[0]) if isinstance(edge, str) else []
        missing = [c for c in (ends[:1] + ends[-1:]) if c not in nodes]
        if not m or missing:
            problems.append(("error", "edge '%s' refers to node(s) %s that no 'node' string defines" % (edge, "".join(missing) or "?")))
    cfg = doc.get("config", {})
    if isinstance(cfg, dict) and "hscale" in cfg and not isinstance(cfg["hscale"], int):
        problems.append(("error", "config.hscale must be an integer"))
    return problems


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def action_lint(args):
    try:
        doc = load_json(args.wavejson)
    except (OSError, ValueError) as exc:
        print("ERROR: cannot read %s as strict JSON: %s" % (args.wavejson, exc))
        return 1
    problems = lint_doc(doc)
    errors = [p for p in problems if p[0] == "error"]
    for level, text in problems:
        print("%s: %s" % (level.upper(), text))
    count = sum(1 for _ in iter_signals(doc.get("signal", []))) if not errors else 0
    print("%s: %d errors, %d warnings%s" % ("FAIL" if errors else "PASS", len(errors), len(problems) - len(errors),
                                           "" if errors else ", %d signals" % count))
    return 1 if errors else 0


def iter_signals(items):
    for item in items:
        if isinstance(item, list):
            for sub in iter_signals(item[1 if item and isinstance(item[0], str) else 0:]):
                yield sub
        elif isinstance(item, dict) and item.get("wave") is not None:
            yield item


# ----------------------------------------------------------------------------- HTML viewer

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#fff;--fg:#1a1a1a;--line:#c9c9c9;--panel:#f5f5f5;--err:#b00020}
@media (prefers-color-scheme:dark){:root{--bg:#1d1d1d;--fg:#eee;--line:#444;--panel:#2a2a2a;--err:#ff8a80}}
body{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,sans-serif}
h1{font-size:18px;margin:0 0 4px}.meta{color:#777;margin:0 0 12px}
.bar{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px}
button{background:var(--panel);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:6px 12px;cursor:pointer}
#stage{overflow:auto;border:1px solid var(--line);border-radius:6px;padding:12px;background:#fff}
#err{color:var(--err);white-space:pre-wrap;margin-top:12px}
details{margin-top:12px}pre{background:var(--panel);padding:12px;border-radius:6px;overflow:auto}
</style></head><body>
<h1>__TITLE__</h1><p class="meta">Offline WaveDrom __VERSION__ viewer. Source: __SOURCE__</p>
<div class="bar"><button id="svg">Save SVG</button><button id="png">Save PNG</button><button id="copy">Copy WaveJSON</button></div>
<div id="stage"><div id="WaveDrom_Display_0"></div></div><div id="err"></div>
<details><summary>WaveJSON source</summary><pre id="src"></pre></details>
<script type="application/json" id="wavejson">__JSON__</script>
<script>__SKIN__</script>
<script>__LIB__</script>
<script>
(function(){
var text=document.getElementById('wavejson').textContent,doc=JSON.parse(text);
document.getElementById('src').textContent=JSON.stringify(doc,null,2);
function svgNode(){return document.querySelector('#WaveDrom_Display_0 svg');}
function save(name,blob){var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;a.click();}
try{wavedrom.renderWaveForm(0,doc,'WaveDrom_Display_');}catch(e){document.getElementById('err').textContent='WaveDrom could not draw this WaveJSON: '+e.message;}
function svgText(){var s=svgNode();if(!s)return null;var c=s.cloneNode(true);c.setAttribute('xmlns','http://www.w3.org/2000/svg');return new XMLSerializer().serializeToString(c);}
document.getElementById('svg').onclick=function(){var t=svgText();if(t)save('waveform.svg',new Blob([t],{type:'image/svg+xml'}));};
document.getElementById('png').onclick=function(){var t=svgText(),s=svgNode();if(!t)return;var w=s.width.baseVal.value,h=s.height.baseVal.value,img=new Image();
img.onload=function(){var c=document.createElement('canvas');c.width=w*2;c.height=h*2;var x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);x.scale(2,2);x.drawImage(img,0,0);c.toBlob(function(b){save('waveform.png',b);});};
img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(t);};
document.getElementById('copy').onclick=function(){navigator.clipboard&&navigator.clipboard.writeText(text);};
})();
</script></body></html>
"""


def action_html(args):
    problems = asset_problems()
    if problems:
        print("ERROR: " + "; ".join(problems))
        return 3
    src = Path(args.wavejson)
    try:
        doc = load_json(src)
    except (OSError, ValueError) as exc:
        print("ERROR: cannot read %s as strict JSON: %s" % (src, exc))
        return 1
    errors = [t for lvl, t in lint_doc(doc) if lvl == "error"]
    if errors and not args.allow_errors:
        print("ERROR: lint found %d error(s); first: %s" % (len(errors), errors[0]))
        return 1
    out = Path(args.out) if args.out else src.with_suffix(".html")
    if out.exists() and not args.force:
        print("ERROR: %s already exists; pass --force to overwrite it" % out)
        return 1
    version = re.search(r"wavedrom (\d+\.\d+\.\d+)", (ASSETS / LIB_FILES[0]).read_text(encoding="utf-8")[:200])
    page = PAGE
    body = json.dumps(doc, ensure_ascii=False).replace("</", "<\\/")
    for key, value in (("__TITLE__", htmllib.escape(args.title or src.stem)),
                       ("__VERSION__", version.group(1) if version else "?"),
                       ("__SOURCE__", htmllib.escape(src.name)),
                       ("__JSON__", body),
                       ("__SKIN__", (ASSETS / LIB_FILES[1]).read_text(encoding="utf-8")),
                       ("__LIB__", (ASSETS / LIB_FILES[0]).read_text(encoding="utf-8"))):
        page = page.replace(key, value)
    out.write_text(page, encoding="utf-8")
    print("OK: wrote %s (%d KB, opens offline)" % (out, len(page) // 1024))
    return 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("check", help="verify the bundled WaveDrom files")
    info = sub.add_parser("vcd-info", help="list signals and time range of a VCD file")
    info.add_argument("vcd")
    info.add_argument("--pattern", help="show only names matching this glob, e.g. 'top.dut.*'")
    info.add_argument("--active", action="store_true", help="hide signals that never change")
    info.add_argument("--max", type=int, default=80, help="maximum lines (default 80)")
    conv = sub.add_parser("vcd-to-wavejson", help="convert signals and a time window to WaveJSON")
    conv.add_argument("vcd")
    conv.add_argument("--signals", help="comma-separated names or globs (default: all)")
    conv.add_argument("--start", help="window start, e.g. 100 or 100ns (default: 0)")
    conv.add_argument("--end", help="window end (default: last time)")
    conv.add_argument("--period", help="time per drawn cycle (default: the finest step that fits every change)")
    conv.add_argument("--group", action="store_true", help="always group by scope")
    conv.add_argument("--out")
    conv.add_argument("--force", action="store_true")
    lint = sub.add_parser("lint", help="check a WaveJSON file")
    lint.add_argument("wavejson")
    page = sub.add_parser("html", help="build the offline HTML viewer")
    page.add_argument("wavejson")
    page.add_argument("--out")
    page.add_argument("--title")
    page.add_argument("--allow-errors", action="store_true", help="build even when lint reports errors")
    page.add_argument("--force", action="store_true")
    args = parser.parse_args()
    return {"check": action_check, "vcd-info": action_vcd_info, "vcd-to-wavejson": action_vcd_to_wavejson,
            "lint": action_lint, "html": action_html}[args.action](args)


if __name__ == "__main__":
    sys.exit(main())
