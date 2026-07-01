#!/usr/bin/env python3
"""Render a repo SVG to PNG deterministically, using the vendored JetBrains Mono
font — so brand assets regenerate identically on any machine.

Why this exists: the show's graphics (e.g. assets/guest-grid.svg) are authored
as SVG and embedded in the READMEs as PNG. Regenerating the PNG needs a real
SVG renderer AND the exact font, or the type reflows / substitutes a fallback.
This wraps `resvg` and points it at tools/fonts/JetBrainsMono.ttf (+ skips
system fonts) so the output matches the design regardless of what's installed
system-wide.

  python3 tools/render_svg.py                        # assets/guest-grid.svg -> assets/guest-grid.png @2x
  python3 tools/render_svg.py path/to/foo.svg         # -> path/to/foo.png @2x
  python3 tools/render_svg.py foo.svg -o bar.png --scale 3

Requires `resvg`:  brew install resvg   (or)   cargo install resvg
The font is vendored (OFL) at tools/fonts/ so no font install is needed.
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
FONT = HERE / "fonts" / "JetBrainsMono.ttf"
DEFAULT_SVG = HERE.parent / "assets" / "guest-grid.svg"


def main():
    ap = argparse.ArgumentParser(description="Render a repo SVG to PNG with the vendored JetBrains Mono font.")
    ap.add_argument("svg", nargs="?", default=str(DEFAULT_SVG),
                    help="input SVG (default: assets/guest-grid.svg)")
    ap.add_argument("-o", "--out", help="output PNG (default: input path with .png)")
    ap.add_argument("--scale", type=float, default=2.0,
                    help="scale factor / device-pixel-ratio (default: 2, i.e. a 1280x900 SVG -> 2560x1800)")
    args = ap.parse_args()

    resvg = shutil.which("resvg")
    if not resvg:
        sys.exit("error: `resvg` not found. Install it: `brew install resvg` (or `cargo install resvg`).")
    if not FONT.exists():
        sys.exit(f"error: vendored font missing at {FONT}")

    svg = pathlib.Path(args.svg)
    if not svg.exists():
        sys.exit(f"error: no such SVG: {svg}")
    out = pathlib.Path(args.out) if args.out else svg.with_suffix(".png")

    cmd = [
        resvg,
        "--use-font-file", str(FONT),
        "--skip-system-fonts",   # deterministic: only the vendored font, never a system substitute
        "--zoom", str(args.scale),
        str(svg), str(out),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        sys.exit(f"error: resvg failed ({result.returncode})")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
