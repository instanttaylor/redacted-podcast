#!/usr/bin/env python3
"""
Combine several per-prospect dossiers into one scrollable "Day Ahead" page.

Why this exists: Ben prefers a single page he scrolls through as the day runs,
not one file per meeting. Research each prospect normally (each writes its own
dossier with assets/template.html, saved to its client folder), then run this to
stitch them under one masthead + day overview + cross-room watch-outs, with a
sticky time-nav. The per-prospect dossiers stay on disk too.

Usage:
    python3 combine_day.py <config.json>

config.json:
{
  "out_path": "/abs/path/to/YYYY-MM-DD-day-ahead.html",
  "template_path": "/abs/path/to/skills/prospect-research/assets/template.html",
  "page_title": "The Day Ahead - Tue, June 30 2026",
  "page_description": "one-line meta description",
  "topbar_label": "The Day Ahead &middot; 30 Jun",
  "day_header_html": "<header class=\"mast\">...</header>\n<p class=\"seclabel\">The shape of the day</p>...<div class=\"watch\">...</div>",
  "meetings": [
    {"anchor": "m1", "time_label": "9:00 AM ET", "name_label": "Example Group",
     "dossier_path": "/abs/.../example-group-prospect-research.html"},
    ...
  ]
}

The day_header_html is written by the skill (it is the cross-meeting synthesis:
masthead + stat strip + drop-cap "shape of the day" + day-level watch-outs). Reuse
the same CSS classes the template uses (mast, stats, note/lead/drop, priority-list,
readcols/askfirst, watch). No em dashes, including &mdash;/&ndash;/literal entities.
"""
import json, re, sys, pathlib


def style_block(path: str) -> str:
    t = pathlib.Path(path).read_text()
    m = re.search(r"<style>.*?</style>", t, re.S)
    if not m:
        raise SystemExit(f"no <style> block found in {path}")
    return m.group(0)


def inner_wrap(path: str) -> str:
    """Return the inner HTML of a dossier's <div class="wrap">...</div>."""
    t = pathlib.Path(path).read_text()
    if '<div class="wrap"' not in t:
        raise SystemExit(f"no .wrap container in {path}")
    seg = t.split('<div class="wrap"', 1)[1]
    seg = seg.split(">", 1)[1]            # past the opening tag (may carry id="...")
    inner = seg.rsplit("</div>", 1)[0]    # drop the wrap-closing </div>
    # strip per-dossier section-label ids so anchors don't collide across meetings
    inner = re.sub(r'\sid="(read|snapshot|stack|today|ai|ask|top)"', "", inner)
    return inner


EXTRA_CSS = """
<style>
  html{scroll-behavior:smooth}
  .dayslot{scroll-margin-top:64px}
  .slotrule{display:flex;align-items:center;gap:14px;margin:70px 0 0;font-family:var(--mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase}
  .slotrule::after{content:"";flex:1;height:2px;background:var(--line-strong)}
  .slotrule .t{color:var(--rust);font-weight:700}
  .slotrule .n{color:var(--ink-faint)}
  .dayslot header.mast{padding:24px 0 22px;border-bottom:1px solid var(--line)}
  .dayslot header.mast .kicker{display:none}
</style>
"""


def build_nav(label: str, meetings: list) -> str:
    links = ['<a href="#top">Overview</a>']
    for m in meetings:
        links.append(f'<a href="#{m["anchor"]}">{m["time_label"].split(" ")[0]} {m["name_label"].split(" ")[0]}</a>')
    return (
        '<div class="topbar">\n  <div class="inner">\n'
        f'    <span><b>{label.split("&middot;")[0].strip()}</b> &middot;{label.split("&middot;",1)[1] if "&middot;" in label else ""}</span>\n'
        f'    <nav class="nav">{"".join(links)}</nav>\n'
        "  </div>\n</div>\n"
    )


def main(cfg_path: str):
    cfg = json.loads(pathlib.Path(cfg_path).read_text())
    css = style_block(cfg["template_path"])
    nav = build_nav(cfg.get("topbar_label", "The Day Ahead"), cfg["meetings"])

    slots = []
    for m in cfg["meetings"]:
        body = inner_wrap(m["dossier_path"])
        slots.append(
            f'<section class="dayslot" id="{m["anchor"]}">\n'
            f'  <div class="slotrule"><span class="t">{m["time_label"]}</span>'
            f'<span class="n">{m["name_label"]}</span></div>\n{body}\n</section>'
        )

    html = (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{cfg["page_title"]}</title>\n'
        f'<meta name="description" content="{cfg.get("page_description","")}">\n'
        + css + "\n" + EXTRA_CSS +
        '\n</head>\n<body>\n'
        + nav +
        '\n<div class="wrap" id="top">\n'
        + cfg["day_header_html"] + "\n\n"
        + "\n\n".join(slots)
        + "\n</div>\n</body>\n</html>\n"
    )

    # guard: no em/en dashes
    bad = html.count("—") + html.count("&mdash;") + html.count("–") + html.count("&ndash;")
    leftover = len(re.findall(r"{{[^}]*}}", html))
    out = pathlib.Path(cfg["out_path"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"wrote {out} ({len(html)} bytes); dashes={bad} leftover_placeholders={leftover}")
    if bad or leftover:
        print("WARNING: clean these before delivering (no em/en dashes; no {{placeholders}}).")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 combine_day.py <config.json>")
    main(sys.argv[1])
