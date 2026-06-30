# tools

Small, dependency-free helpers for maintaining the show-notes repo.

## `redacted_feed.py`

Pulls [Redacted] episode metadata from three public sources and joins them into
one record per episode, so you don't have to read links off each platform by
hand when writing show notes.

```sh
python3 tools/redacted_feed.py            # markdown table of all Redacted episodes
python3 tools/redacted_feed.py --json      # same data as JSON
python3 tools/redacted_feed.py --grep 4    # only episodes whose title matches "4"
python3 tools/redacted_feed.py --no-enrich # RSS feed only, skip Apple/YouTube
```

### Sources

| Source | Gives | Joined on |
| --- | --- | --- |
| Transistor RSS (`feeds.transistor.fm/triangle-tweener-talks`) | `date`, `runtime`, `audio` mp3, `transistor` share link | — |
| Apple lookup API (`itunes.apple.com/lookup?id=1774076494&entity=podcastEpisode`) | `apple` per-episode URL | mp3 enclosure |
| YouTube playlist RSS (`youtube.com/feeds/videos.xml?playlist_id=…`) | `youtube` URL + `youtube_id` | normalized title |

### Boundaries (these still get filled by hand)

- **Spotify** per-episode link — public endpoints only expose the *show* URL
  (`open.spotify.com/show/1aMrtX8LnIU2w5yoT4uolb`). Per-episode requires the
  Spotify Web API with an OAuth client id/secret.
- **Substack** show-notes URL — not in any feed.
- A **brand-new episode** won't appear until the Transistor feed publishes it,
  and **older episodes** drop out of YouTube's recent-items playlist RSS (so
  `youtube` comes back empty for them).
