---
name: finalize-launched-episode
description: Finalize a [Redacted] episode's show notes AFTER it launches (this runs post-publish, NOT right after recording) — pull live metadata (date, runtime, Apple, YouTube, thumbnail) via tools/redacted_feed.py, confirm the Substack show-notes URL is live, and replace the _TBD_ markers left during prep in the folder README and the root-table row. Use when an episode goes live / publishes, or when asked to "finalize episode N". (Before launch, use prep-recorded-episode instead.)
---

# Finalize a launched episode (go-live)

This is the **Go-live finalize** process noted at the end of [`process/post-recording-process-map.md`](../../../process/post-recording-process-map.md). It runs after `prep-recorded-episode`, **once the episode has actually launched/published** — not right after recording. It replaces the `_TBD_` markers left during prep with the now-available links and runtime.

**Trigger is manual:** run when the episode publishes (the same day it drops on the feeds).

## Inputs
- **Required:** episode number `N`.

## Steps

1. **Pull live metadata:**
   ```sh
   python3 tools/redacted_feed.py --grep N --json
   ```
   Match the record for episode `N`. If the result is **empty**, the Transistor feed hasn't published the episode yet — **stop and say so** (nothing to finalize).

   The JSON gives: `date`, `runtime`, `apple`, `youtube`, `youtube_id`. `spotify` is the show-level link (by convention). The **thumbnail** is `https://img.youtube.com/vi/<youtube_id>/hqdefault.jpg`.

2. **Confirm the Substack show-notes URL is live.** If the folder README still has `_TBD_` for "Full show notes", determine the public URL (from staging notes / the Substack page) and **WebFetch it to confirm it's published, not gated/scheduled.** Only write a URL you've confirmed resolves to the live post.

3. **Fill the folder README** (`00N…/README.md`): replace its `_TBD_`s — Runtime, Full show notes URL, Apple link, YouTube link.

4. **Add the row to the root README "Episodes" list.** The Episodes list is **launched-only**, so `prep-recorded-episode` deliberately did NOT create this row — you add it now, at launch, **newest-first at the top of the `<table>`**, fully populated (no `_TBD_`). Then fix the stub-folder note beneath the table if it still lists this folder as a stub. Template:

   ```html
   <tr>
   <td width="300"><a href="<youtube watch URL>"><img src="https://img.youtube.com/vi/<youtube_id>/hqdefault.jpg" width="300" alt="Episode N"></a></td>
   <td valign="top">

   ### EP 0N · <title>
   `<drop date>` · <runtime>

   ▶ [Watch](<youtube>) · 🎧 [Apple](<apple>) · [Spotify](https://open.spotify.com/show/1aMrtX8LnIU2w5yoT4uolb) · 📝 [Show notes](<substack URL>) · 📁 [Files](00N…/)

   </td>
   </tr>
   ```

5. **Confirm before commit.** Show `git diff` and verify `grep -c _TBD_ 00N…/README.md` is `0` (or that any remaining `_TBD_` is genuinely still unavailable). On approval, commit straight to `main`.

## Boundaries
- **Spotify stays the show-level link.** Per-episode Spotify URLs need the Spotify Web API with OAuth (not wired up). Don't invent a per-episode Spotify link.
- **Older episodes** drop out of the YouTube playlist RSS, so `youtube` can come back empty — leave `_TBD_` (or ask) rather than guessing a video id.
- Don't fabricate any URL. A confirmed `_TBD_` beats a wrong link.
