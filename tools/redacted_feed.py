#!/usr/bin/env python3
"""Pull [Redacted] episode metadata from the NC Tweener Talks podcast feeds.

The show rides on the network feed (Transistor), so this filters to the
[Redacted] episodes and surfaces the fields the show-notes READMEs need:
release date, runtime, the audio enclosure, plus per-episode **Apple** and
**YouTube** deep links pulled from two more public sources and joined back on.

Standard library only — no install step.

  python3 tools/redacted_feed.py            # markdown table of all Redacted eps
  python3 tools/redacted_feed.py --json      # same data as JSON
  python3 tools/redacted_feed.py --grep 4    # only episodes whose title matches "4"
  python3 tools/redacted_feed.py --no-enrich # skip Apple/YouTube lookups (RSS only)

Sources, and what each one gives:
  * Transistor RSS  -> date, runtime, audio mp3, share link  (always)
  * Apple lookup    -> per-episode podcasts.apple.com URL     (joined by mp3)
  * YouTube playlist RSS -> per-episode watch URL + video id  (joined by title)

What's still NOT automatable here: the per-episode **Spotify** link (the public
endpoints only expose the show-level URL; per-episode needs the Spotify Web API
with an OAuth client id/secret) and the **Substack** show-notes URL. Both get
filled by hand.
"""

import argparse
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

FEED_URL = "https://feeds.transistor.fm/triangle-tweener-talks"
APPLE_ID = "1774076494"
APPLE_LOOKUP = ("https://itunes.apple.com/lookup?id={id}"
                "&entity=podcastEpisode&limit=200")
YOUTUBE_PLAYLIST_ID = "PLV3BqFp9grX9HGuXrcet1GDzIkU9o2bzy"
YOUTUBE_PLAYLIST_RSS = "https://www.youtube.com/feeds/videos.xml?playlist_id={pid}"
SHOW_SPOTIFY = "https://open.spotify.com/show/1aMrtX8LnIU2w5yoT4uolb"

ITUNES = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
ATOM = "{http://www.w3.org/2005/Atom}"
YT = "{http://www.youtube.com/xml/schemas/2015}"

# RFC-822 month abbreviations -> month number, to turn pubDate into an ISO date
# without pulling in a parser or depending on the host locale.
_MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "redacted-podcast/feed"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def iso_date(pub_date):
    """'Tue, 30 Jun 2026 02:00:00 -0400' -> '2026-06-30' (None on surprise)."""
    if not pub_date:
        return None
    parts = pub_date.split()
    try:
        day, mon, year = parts[1], parts[2], parts[3]
        return f"{int(year):04d}-{_MONTHS[mon]:02d}-{int(day):02d}"
    except (IndexError, KeyError, ValueError):
        return None


def fmt_runtime(seconds):
    """Seconds (string or int) -> 'H:MM:SS' or 'MM:SS'."""
    if seconds is None:
        return None
    try:
        s = int(seconds)
    except (TypeError, ValueError):
        return None
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"


def _norm_title(title):
    """Lowercase, alphanumerics only — for fuzzy title joins across platforms."""
    return re.sub(r"[^a-z0-9]+", "", (title or "").lower())


def apple_links():
    """{mp3_enclosure_url: podcasts.apple.com episode URL} from the iTunes API."""
    data = json.loads(fetch(APPLE_LOOKUP.format(id=APPLE_ID)).decode("utf-8"))
    out = {}
    for r in data.get("results", []):
        if r.get("wrapperType") == "podcastEpisode" and r.get("episodeUrl"):
            # episodeUrl is the same Transistor mp3 the RSS enclosure points to.
            view = (r.get("trackViewUrl") or "").split("&uo=")[0]  # drop tracking param
            out[r["episodeUrl"]] = view or None
    return out


def youtube_links(playlist_id):
    """[(normalized_title, watch_url, video_id)] from the playlist's RSS feed.

    The playlist feed only carries roughly the most recent entries, so older
    episodes simply won't be found — callers must tolerate a None match.
    """
    root = ET.fromstring(fetch(YOUTUBE_PLAYLIST_RSS.format(pid=playlist_id)))
    out = []
    for e in root.findall(f"{ATOM}entry"):
        vid = e.findtext(f"{YT}videoId")
        title = e.findtext(f"{ATOM}title")
        if vid and title:
            out.append((_norm_title(title), f"https://www.youtube.com/watch?v={vid}", vid))
    return out


def _match_youtube(feed_title, yt_entries):
    """Join by normalized-title substring (either direction). Returns (url, id) or (None, None)."""
    key = _norm_title(feed_title)
    for yt_key, url, vid in yt_entries:
        if key and (key in yt_key or yt_key in key):
            return url, vid
    return None, None


def redacted_episodes(xml_bytes, enrich=True):
    root = ET.fromstring(xml_bytes)
    channel = root.find("channel")

    apple = youtube = None
    if enrich:
        try:
            apple = apple_links()
        except Exception as exc:
            print(f"warning: Apple lookup failed ({exc}); apple links omitted", file=sys.stderr)
        try:
            youtube = youtube_links(YOUTUBE_PLAYLIST_ID)
        except Exception as exc:
            print(f"warning: YouTube lookup failed ({exc}); youtube links omitted", file=sys.stderr)

    out = []
    for item in channel.findall("item"):
        title = (item.findtext("title") or "").strip()
        if "redacted" not in title.lower():
            continue
        enc = item.find("enclosure")
        audio = enc.get("url") if enc is not None else None
        yt_url, yt_id = _match_youtube(title, youtube) if youtube else (None, None)
        out.append({
            "network_episode": item.findtext(f"{ITUNES}episode") or item.findtext("episode"),
            "title": title,
            "date": iso_date(item.findtext("pubDate")),
            "runtime": fmt_runtime(item.findtext(f"{ITUNES}duration")),
            "audio": audio,
            "apple": apple.get(audio) if apple else None,
            "spotify": SHOW_SPOTIFY,  # show-level link by convention; per-episode needs the Spotify API
            "youtube": yt_url,
            "youtube_id": yt_id,
            "transistor": item.findtext("link"),
            "guid": item.findtext("guid"),
        })
    # Newest first, by date when we have it.
    out.sort(key=lambda e: e["date"] or "", reverse=True)
    return out


def print_table(eps):
    if not eps:
        print("No [Redacted] episodes found in the feed.", file=sys.stderr)
        return
    print("| Date | Runtime | Title | Apple | YouTube |")
    print("| --- | --- | --- | --- | --- |")
    for e in eps:
        title = e["title"].replace("|", "\\|")
        apple = "[link](%s)" % e["apple"] if e["apple"] else "?"
        yt = e["youtube_id"] or "?"
        print(f"| {e['date'] or '?'} | {e['runtime'] or '?'} | {title} | {apple} | {yt} |")


def main():
    ap = argparse.ArgumentParser(description="Fetch [Redacted] episode metadata from the podcast RSS feed.")
    ap.add_argument("--feed", default=FEED_URL, help="RSS feed URL (default: NC Tweener Talks network feed)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a markdown table")
    ap.add_argument("--grep", metavar="TEXT", help="only episodes whose title contains TEXT (case-insensitive)")
    ap.add_argument("--no-enrich", action="store_true", help="skip Apple/YouTube lookups (RSS feed only)")
    args = ap.parse_args()

    try:
        eps = redacted_episodes(fetch(args.feed), enrich=not args.no_enrich)
    except Exception as exc:  # network, parse, whatever — fail loud, not silent
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.grep:
        needle = args.grep.lower()
        eps = [e for e in eps if needle in e["title"].lower()]

    if args.json:
        print(json.dumps(eps, indent=2))
    else:
        print_table(eps)
    return 0


if __name__ == "__main__":
    sys.exit(main())
