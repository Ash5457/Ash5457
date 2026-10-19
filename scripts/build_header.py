#!/usr/bin/env python3
"""
Render assets/header.svg: a fastfetch-style terminal window for the GitHub profile README.

- ASCII banner + system-info panel, drawn as real SVG text with an embedded font,
  so it looks the same on every OS and browser.
- CSS-only animation (GitHub strips scripts from SVGs): the command types itself,
  output prints line by line, then the cursor blinks. Respects prefers-reduced-motion.
- The "Latest" row is live: the most recently pushed public repo, pulled from the
  GitHub API. The workflow in .github/workflows/profile.yml reruns this daily.

Standard library only. Usage:
    python3 scripts/build_header.py                                   # fetch from the API
    python3 scripts/build_header.py --latest secure-remote-access:2026-10-12   # offline
"""

import argparse
import base64
import html
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("America/Toronto")
except Exception:  # tz database missing: fall back to UTC dates
    TZ = None

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "header.svg"
FONTS = ROOT / "assets" / "fonts"

# ---------------------------------------------------------------- edit me ---
USER = os.environ.get("PROFILE_USER", "Ash5457")  # GitHub login
SHELL_USER, HOST = "ash", "fedora"                # prompt: ash@fedora:~$
COMMAND = "fastfetch"

BANNER = """\
 █████╗ ███████╗██╗  ██╗
██╔══██╗██╔════╝██║  ██║
███████║███████╗███████║
██╔══██║╚════██║██╔══██║
██║  ██║███████║██║  ██║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝""".splitlines()

# (key, value). Inline colour markup: {green:text} {amber:text} {blue:text} {dim:text}
# A value of None is filled in from the GitHub API at build time.
INFO = [
    ("OS", "Fedora Linux · Hyprland"),
    ("Role", "IT support → security"),
    ("Certs", "CompTIA A+ {green:✓} · Security+ {amber:(studying)}"),
    ("Labs", "AD build & migration · Fedora hardening"),
    ("Base", "Keswick, ON · York Region / GTA"),
    ("Latest", None),
    ("Status", "{green:●} open to helpdesk & junior SOC roles"),
]
# ----------------------------------------------------------------------------

# GitHub dark palette, so the window matches the restyled metrics render
C = {
    "body": "#0d1117", "bar": "#161b22", "border": "#30363d",
    "fg": "#c9d1d9", "dim": "#8b949e", "green": "#3fb950", "blue": "#58a6ff",
    "amber": "#d29922", "red": "#f85149",
}
SWATCHES = ["#484f58", "#f85149", "#3fb950", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#b1bac4"]

FS = 14                    # font size (px)
ADV = FS * 1233 / 2048     # DejaVu Sans Mono advance width per character
LH = 20                    # line height
# The banner uses a slightly larger size so block glyphs (2433 units tall) fill a
# whole row and stack without gaps, the way they do in a real terminal.
BANNER_FS = LH * 2048 / 2433
BANNER_ADV = BANNER_FS * 1233 / 2048
BANNER_ASCENT = BANNER_FS * 1921 / 2048
PAD, BAR, TOP = 22, 30, 16
GAP = 4                    # spaces between banner and info panel
KEY_W = 8                  # info keys are padded to this width

TYPE_START, TYPE_STEP = 0.5, 0.075   # seconds
ROW_START_GAP, ROW_STEP = 0.3, 0.07

MARKUP = re.compile(r"\{(\w+):([^}]*)\}")


def plain(text):
    return MARKUP.sub(lambda m: m.group(2), text)


def tspans(text, default="fg"):
    parts, pos = [], 0
    for m in MARKUP.finditer(text):
        if m.start() > pos:
            parts.append((text[pos:m.start()], default))
        parts.append((m.group(2), m.group(1)))
        pos = m.end()
    if pos < len(text):
        parts.append((text[pos:], default))
    return "".join(f'<tspan class="{c}">{html.escape(t, quote=False)}</tspan>' for t, c in parts)


def latest_push(user, token=None):
    """Most recently pushed public repo (skipping forks, archives and the profile repo)."""
    url = f"https://api.github.com/users/{user}/repos?type=owner&sort=pushed&per_page=30"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json", "User-Agent": f"{user}-profile-header"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=15) as resp:
        repos = json.load(resp)
    for repo in repos:
        if repo.get("fork") or repo.get("archived") or repo["name"].lower() == user.lower():
            continue
        pushed = datetime.fromisoformat(repo["pushed_at"].replace("Z", "+00:00"))
        if TZ:
            pushed = pushed.astimezone(TZ)
        return repo["name"], pushed.strftime("%Y-%m-%d")
    return None


def font_face(weight, filename):
    data = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f'@font-face{{font-family:"DVM";font-weight:{weight};'
            f'src:url(data:font/woff2;base64,{data}) format("woff2")}}')


def build(latest):
    info = []
    for key, value in INFO:
        if value is None:
            if not latest:
                continue
            value = f"{latest[0]} {{dim:({latest[1]})}}"
        info.append("{key:" + key.ljust(KEY_W) + "}" + value)

    title = f"{SHELL_USER}@{USER}"
    rows = ["{green:" + SHELL_USER + "}{fg:@}{green:" + USER + "}",
            "{dim:" + "-" * len(title) + "}"] + info
    n_out = len(rows) + 1                      # +1 for the colour swatches

    banner_w = max(len(line) for line in BANNER)
    info_x = PAD + banner_w * BANNER_ADV + GAP * ADV   # info panel left edge (px)
    prompt_len = len(f"{SHELL_USER}@{HOST}:~$ ")
    info_chars = max(len(plain(r)) for r in rows)

    W = round(max(PAD * 2 + (prompt_len + len(COMMAND) + 1) * ADV,
                  info_x + (info_chars + 1) * ADV + PAD))
    H = BAR + TOP + (n_out + 3) * LH + 10      # command + output + blank + prompt

    def top(i):                                # top edge of content row i
        return BAR + TOP + i * LH

    def base(i):                               # text baseline of content row i
        return top(i) + 15

    def x(c):
        return PAD + c * ADV

    def prompt_tspans():
        return (f'<tspan class="green b">{SHELL_USER}@{HOST}</tspan><tspan class="fg">:</tspan>'
                f'<tspan class="blue b">~</tspan><tspan class="fg">$ </tspan>')

    out_start = TYPE_START + len(COMMAND) * TYPE_STEP + ROW_START_GAP
    end = out_start + n_out * ROW_STEP + 0.2

    svg = []
    add = svg.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'xml:space="preserve" role="img" aria-labelledby="title desc">')
    summary = "; ".join(re.sub(r"\s{2,}", ": ", plain(r).strip(), count=1) for r in rows[2:])
    add(f'<title id="title">{html.escape(SHELL_USER)}@{html.escape(HOST)}: {html.escape(COMMAND)}</title>')
    add(f'<desc id="desc">{html.escape(summary)}</desc>')

    css = [
        font_face(400, "DejaVuSansMono-subset.woff2"),
        font_face(700, "DejaVuSansMono-Bold-subset.woff2"),
        f'text{{font-family:"DVM","DejaVu Sans Mono",Menlo,Consolas,monospace;font-size:{FS}px;fill:{C["fg"]};white-space:pre}}',
        ".b{font-weight:700}",
        f'.key{{fill:{C["green"]};font-weight:700}}',
        *[f".{n}{{fill:{C[n]}}}" for n in ("fg", "dim", "green", "blue", "amber", "red")],
        ".ttl{font-size:12px}.btn{font-size:8px}",
        ".a{opacity:0;animation:show .01s linear forwards}",
        "@keyframes show{to{opacity:1}}@keyframes hide{to{opacity:0}}",
        f".tc{{animation:tcmove {len(COMMAND) * TYPE_STEP:.3f}s steps({len(COMMAND)}) {TYPE_START}s forwards,"
        f"hide .01s linear {out_start - ROW_START_GAP / 2:.3f}s forwards}}",
        f"@keyframes tcmove{{to{{transform:translateX({len(COMMAND) * ADV:.2f}px)}}}}",
        ".blink{animation:blink 1.1s step-end infinite}",
        "@keyframes blink{50%{opacity:0}}",
        "@media (prefers-reduced-motion:reduce){.a{opacity:1;animation:none}.tc{display:none}.blink{animation:none}}",
    ]
    add("<defs>")
    add(f"<style>{''.join(css)}</style>")
    add(f'<clipPath id="win"><rect width="{W}" height="{H}" rx="8"/></clipPath>')
    b_top = top(1 + max(0, (n_out - len(BANNER)) // 2))
    add(f'<linearGradient id="bn" gradientUnits="userSpaceOnUse" x1="0" y1="{b_top}" x2="0" y2="{b_top + len(BANNER) * LH}">'
        '<stop offset="0" stop-color="#56d364"/><stop offset="1" stop-color="#39c5cf"/></linearGradient>')
    add('<filter id="glow" x="-5%" y="-30%" width="110%" height="160%"><feGaussianBlur stdDeviation="2.2" result="b"/>'
        '<feComponentTransfer in="b" result="g"><feFuncA type="linear" slope="0.55"/></feComponentTransfer>'
        '<feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    add("</defs>")

    # window chrome
    add('<g clip-path="url(#win)">')
    add(f'<rect width="{W}" height="{H}" fill="{C["body"]}"/>')
    add(f'<rect width="{W}" height="{BAR}" fill="{C["bar"]}"/>')
    add(f'<rect y="{BAR - 1}" width="{W}" height="1" fill="{C["border"]}"/>')
    add("</g>")
    add(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="8" fill="none" stroke="{C["border"]}"/>')
    add(f'<text class="ttl dim" x="{W / 2:.1f}" y="19.5" text-anchor="middle">{SHELL_USER}@{HOST}: ~</text>')
    for i, (glyph, fill, ink) in enumerate([("─", C["border"], C["dim"]), ("□", C["border"], C["dim"]),
                                            ("✕", C["red"], C["body"])]):
        cx = W - PAD - (2 - i) * 20 + 2
        add(f'<circle cx="{cx}" cy="15" r="6.5" fill="{fill}"/>')
        add(f'<text class="btn" x="{cx}" y="17.8" text-anchor="middle" style="fill:{ink}">{glyph}</text>')

    # row 0: prompt, then the command types itself one character at a time
    add(f'<text x="{x(0):.2f}" y="{base(0)}">{prompt_tspans()}</text>')
    for i, ch in enumerate(COMMAND):
        add(f'<text class="a" x="{x(prompt_len + i):.2f}" y="{base(0)}" '
            f'style="animation-delay:{TYPE_START + i * TYPE_STEP:.3f}s">{html.escape(ch)}</text>')
    add(f'<rect class="tc" x="{x(prompt_len):.2f}" y="{top(0) + 2}" width="{ADV:.2f}" height="16" fill="{C["fg"]}"/>')

    # output rows: banner line + info line print together, like a real terminal.
    # The banner is vertically centred against the info panel.
    offset = max(0, (n_out - len(BANNER)) // 2)
    for r in range(n_out):
        row = r + 1
        add(f'<g class="a" style="animation-delay:{out_start + r * ROW_STEP:.3f}s">')
        if 0 <= r - offset < len(BANNER):
            add(f'<text class="b" x="{x(0):.2f}" y="{top(row) + BANNER_ASCENT:.2f}" '
                f'style="fill:url(#bn);font-size:{BANNER_FS:.2f}px" '
                f'filter="url(#glow)">{html.escape(BANNER[r - offset])}</text>')
        if r < len(rows):
            cls = ' class="b"' if r == 0 else ""
            add(f'<text{cls} x="{info_x:.2f}" y="{base(row)}">{tspans(rows[r])}</text>')
        else:
            for k, color in enumerate(SWATCHES):
                add(f'<rect x="{info_x + k * 3 * ADV:.2f}" y="{top(row) + 3}" width="{ADV * 3:.2f}" height="14" fill="{color}"/>')
        add("</g>")

    # final prompt with a blinking cursor
    last = n_out + 2
    add(f'<g class="a" style="animation-delay:{end:.3f}s">')
    add(f'<text x="{x(0):.2f}" y="{base(last)}">{prompt_tspans()}</text>')
    add(f'<rect class="blink" x="{x(prompt_len):.2f}" y="{top(last) + 2}" width="{ADV:.2f}" height="16" fill="{C["fg"]}"/>')
    add("</g>")
    add("</svg>")
    return "\n".join(svg) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--latest", help="skip the API, e.g. secure-remote-access:2026-10-12")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    if args.latest:
        name, _, date = args.latest.partition(":")
        latest = (name, date)
    else:
        try:
            latest = latest_push(USER, os.environ.get("GITHUB_TOKEN"))
        except Exception as exc:
            if args.out.exists():
                print(f"GitHub API unavailable ({exc}); keeping the existing header.")
                return 0
            print(f"GitHub API unavailable ({exc}); building without the Latest row.")
            latest = None

    svg = build(latest)
    if args.out.exists() and args.out.read_text(encoding="utf-8") == svg:
        print("header.svg unchanged")
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(svg, encoding="utf-8")
    print(f"wrote {args.out.relative_to(ROOT) if args.out.is_relative_to(ROOT) else args.out}"
          f" ({len(svg) // 1024} KB, latest={latest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
