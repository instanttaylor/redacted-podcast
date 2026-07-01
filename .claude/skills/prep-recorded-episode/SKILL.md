---
name: prep-recorded-episode
description: Prep a just-recorded [Redacted] episode's show notes ahead of launch (BEFORE it goes live) — build the 00N folder, README, and root-table row from the guest name, the tracker sheet, and the Substack draft, leaving _TBD_ markers for what isn't available yet (runtime, live platform links). Use after recording an episode, when a launch is scheduled or the Substack "ready for review" ping arrives, or when asked to "prep episode N" / "stage episode N". (After it launches, use finalize-launched-episode instead.)
---

# Prep a recorded episode (pre-launch show-notes staging)

This is **Process 2** in [`process/post-recording-process-map.md`](../../../process/post-recording-process-map.md). It stages a recorded episode's notes with `_TBD_` markers **before the episode launches**; the go-live values get filled later, once it's live, by the `finalize-launched-episode` skill. The `_TBD_` markers ARE the pending list — `grep -rn _TBD_` surfaces exactly what still needs filling.

**Trigger is manual** (the Substack "ready for review" ping lives in a Slack we can't connect to). Run this when asked, or when you know an episode is imminent.

## Inputs
- **Required:** episode number `N`, guest name. Ask if not given.
- **Auto-fetched** (don't ask for these first — go get them): drop date + production notes from the tracker sheet; title / subtitle / public URL from the Substack page.

## Steps

1. **Load tracker config.** Read `.claude/skills/prep-recorded-episode/tracker.local.md` (gitignored) for the Google account + spreadsheet ID + column map. If it's missing, ask Taylor for the dedicated Google account email and the "Redacted Podcast Tracker" spreadsheet ID.

2. **Read the sheet row** via `workspace-mcp` `read_sheet_values` as that Google account. Get **column E (drop date)** and **column G (production notes)** for episode `N`. Column E is often blank pre-schedule — that's fine, it stays `_TBD_`.

3. **Pull the Substack draft.** WebFetch the scheduled post's public page for **title, subtitle, and canonical public URL**. Pre-publish, the body is **gated** — the title/subtitle/URL still render, but the "what we cover" body does not. If you need the body now, **ask Taylor to paste it**; otherwise leave "what we cover" as `_TBD_`.

4. **Build the Links checklist — propose, confirm, NEVER guess.** Four categories (see the process map). For each, present a candidate for yes/no/edit before writing; **anything unconfirmed goes in as `_TBD_`, never a guessed URL.**
   - **Guest LinkedIn — always.** WebSearch for it, propose the match, confirm. (Watch for name/company mismatches — verify the person, not just the name.)
   - **Guest company / how-to-get-in-touch**, **demo(s) shown on-air**, **external resources referenced** — pull candidates from column G notes + ask Taylor; confirm each.

5. **Write the folder README.** Create `00N/` (or rename to `00N-slug/` only once there's a title). Use the template below. Fill knowns; mark unknowns `_TBD_`.

6. **Do NOT add a row to the root README "Episodes" list.** That list is **launched episodes only** — an unlaunched episode never appears there. The Episodes-list row gets added later, at launch, by `finalize-launched-episode`. Prep only creates the `00N/` folder + its README. If the stub-folder note below the table names this folder, keep it accurate.

7. **Confirm before commit.** Show `git diff` and `grep -rn _TBD_ 00N*`. On approval, commit straight to `main` (this repo works directly on main). Otherwise leave it staged.

## Folder README template

```markdown
# Episode N — <title or _TBD_>

**Guest:** <name> · **Recorded:** <Month D, YYYY> · **Released:** <drop date or _TBD_> · **Runtime:** _TBD_

📝 **Full show notes:** [Read on tweenertimes.com](<substack URL or _TBD_>)
🎧 **Listen:** [Apple](_TBD_) · [Spotify](https://open.spotify.com/show/1aMrtX8LnIU2w5yoT4uolb) · [YouTube](_TBD_)

<intro from the Substack subtitle/description, or a _TBD_ placeholder>

## What we cover

- <bullets from the draft, or "_TBD — pulled from the Substack draft during publish-week staging._">

## Links

- **<Guest> on LinkedIn** — <url or _TBD_>
- **<Company>** — get in touch with <guest first name> — <url or _TBD_>
- **<Demo name>** — the demo shown on-air — <url or _TBD_>
- **<Resource>** — <url or _TBD_>

> **Didn't see what was shown on-air?** We don't always post everything — some of it stays redacted. **[Request a file →](mailto:contact@tweenerfund.com?subject=%5BREDACTED%5D%20Ep%20N%20file%20request)**
```
(Spotify uses the show-level link by convention. Drop any Links bullet that has no entry and isn't required — but the LinkedIn bullet is always present, `_TBD_` if unconfirmed.)

## Boundaries
- Don't touch tracking-sheet columns D/E (owned downstream). This skill only *reads* the sheet.
- Don't fabricate links or "what we cover" content. `_TBD_` is always the safe answer.
- Go-live values (runtime, Watch/Apple/YouTube, public thumbnail) are `finalize-launched-episode`'s job — leave them `_TBD_`.
