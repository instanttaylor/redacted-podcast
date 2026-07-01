# Process Map: [Redacted] Post-Recording Workflow

## Metadata
- **Mapped by:** Taylor Cotner
- **Company / Role:** NC Tweener · podcast producer (for [Redacted])
- **Date:** 2026-06-30
- **Mapping session:** process-mapping skill → feeds the Process + Context framework (shaner-consulting) at Step 3

## Summary

What started as "the post-recording process" split into **two processes with different triggers**, because the show runs on an every-other-week cadence (record one week, publish the opposite week):

- **Process 1 — Record-week producer handoff.** Triggered by a recording ending.
- **Process 2 — Publish-week show-notes staging.** Triggered by the Substack "ready for review" ping. ⭐ This is the meaty one and the candidate for automation (it's the work this skill/agent already does).

A third process — **Go-live finalize** (filling platform links once the episode is actually live) — is deliberately scoped OUT and noted at the end.

---

# Process 1 — Record-week producer handoff

## Trigger
A recording session ends — the episode is in the can (raw recording done).

## End State
Producer notified; the tracking sheet's columns A–G are complete for the just-recorded episode.

## Process Steps

### Step 1: Update the episode tracking sheet (columns A–G only)
- **What happens:** During recording, Taylor keeps a running cut-list / production-notes doc (things to cut, flags). After the recording wraps, he opens the master episode tracking sheet and updates **only A–G** on the just-recorded episode's row:
  - **A** = episode number
  - **B** = featuring
  - **C** = recorded date
  - **F** = podcast recording status → **Done**
  - **G** = paste production notes
  - He deliberately does **not** touch **D** (featured email) or **E** (drop date), and never edits anything past column G — that territory is owned by the producer / later stages.
- **Gate → Step 2:** Row A/B/C set, F = Done, G pasted.
- **Dependencies:** Linear from trigger; depends on the live cut-notes taken *during* recording.
- **Edge cases:**
  - Episode rows are pre-created — this is a *verify/update*, not a *create*. (Ripple: mirrors the repo's pre-created `00N/` stub folders.)
  - Leaving D/E blank is intentional — they're owned downstream. **Column E (drop date) is the value that later drives Process 2's timing**, so it's a cross-process dependency, not a missing field.

### Step 2: Notify the producer (Slack) → END STATE
- **What happens:** Once A–G are set, Taylor sends a Slack ping to the producer that the episode is ready to edit.
- **Gate → Done:** Producer has been pinged.
- **Dependencies:** Linear from Step 1.
- **Context note (why there's no "deliver files" step):** The raw recording **auto-lands in the cloud** (StreamYard) in a location the producer already has access to — so there is no manual file-handoff step.

---

# Process 2 — Publish-week show-notes staging ⭐

## Trigger
The Substack **"ready for review"** Slack ping — Taylor is an editor on the post; the message says the post is scheduled and editable until Wednesday morning, with a link to the scheduled post.
**Backstop triggers:** the every-other-week cadence, or a manual one-off run. (Taylor: "let's go with the ping for now; I can always run it one-off if needed.")

## End State
The episode's show notes are **committed to `main`** — the `00N-slug/` folder, its README, and the root-README episode-table row — with every not-yet-available value left as a **`_TBD_` marker**. Those markers ARE the pending list (greppable with `grep -r _TBD_`).

## Process Steps

### Step 1: Receive the go-live signal
- **What happens:** Taylor gets the Slack ping with the scheduled-post link, and confirms *which* episode is imminent and its **scheduled drop date**. He can cross-check the tracking sheet or rely on the cadence. Underlying driver: **keep the show notes from falling behind.**
- **Gate → Step 2:** He knows the episode, the drop date, and that a Substack draft exists.
- **Dependencies:** The trigger itself.
- **Edge cases:** He may self-initiate from the cadence rather than waiting for the ping.

### Step 2: Retrieve the gated Substack draft *(human)*
- **What happens:** Taylor opens the post (an editor `/publish/post/...` link, since he's an editor) and copies the **title, description, and "what we cover"** content — the source material for the repo notes.
- **Gate → Step 3:** Draft content is in hand.
- **Dependencies:** Linear from Step 1.
- **Edge cases:** The post is **gated/scheduled** — there is **no public URL yet**, so the repo's "Full show notes" link is necessarily `_TBD_` until it publishes Wednesday. *(Open question: a Substack API could fetch the gated draft and remove this manual copy.)*

### Step 3: Assemble show-notes links + "files shared on-air" *(human → increasingly agent)*
- **What happens:** Taylor gathers the links and files that belong in the episode's show notes. This is not one bucket — it's a **link checklist** with four categories, one of which is now a deterministic standing rule:
  1. **Guest LinkedIn — ALWAYS.** Every episode's notes include the guest's LinkedIn, whether or not it came up on-air. This is a standing rule, so it's the one category an agent can satisfy from just the guest name (no capture needed). *(Ep 7 guest: Ben Pope.)*
  2. **Guest company / how-to-get-in-touch link.** The guest's business or contact URL. *(Ep 7: `levitatesolutions.ai` — get in touch with Ben.)*
  3. **Demos shown on-air.** Product/demo URLs surfaced during the episode. *(Ep 7: `https://www.levitate.ai/getmyscore` — the demo.)*
  4. **External resources referenced on-air.** Blogs, tools, or docs someone pointed to. *(Ep 7: Simon's agentic-engineering blog.)*
- **Gate → Step 4:** The four categories have been walked; category 1 is always filled, 2–4 are filled or explicitly empty.
- **Dependencies:** **Parallel** with Step 2 (independent of the draft content).
- **Edge cases / REMAINING GAP:** Category 1 (LinkedIn) is solved — deterministic from the guest name. Categories 2–4 still have **no canonical capture source**: they default to **production notes (sheet column G)**, otherwise memory, with a **separate assets drop** sometimes happening later. When 2–4 are all empty the folder falls back to the **"request a file" footer** (as in Eps 3–5). *The narrowed gap — capturing 2–4 live — is the seed of a future "during-show capture" process.*

### Step 4: Build the repo notes *(skill / agent)*
- **What happens:** Create/rename the `00N-slug/` folder and write the episode README:
  - title; **Released = scheduled drop date**; intro from the description; "what we cover" from the draft; a **Links** section built from the Step 3 checklist (guest LinkedIn always; guest company, demos, and referenced resources when present); files-shared section (or the request-a-file footer).
  - Runtime, the listen links (Apple/Spotify/YouTube), and the public show-notes URL are left as `_TBD_` (Spotify uses the show-level link by convention).
- **Gate → Step 5:** Folder + README exist; known values filled, unknowns marked `_TBD_`.
- **Dependencies:** Linear from Step 2 (and Step 3).
- **Edge cases:** Because the episode isn't live yet, **all** platform links + runtime + public Substack URL + YouTube thumbnail are necessarily `_TBD_`.

### Step 5: Update the root README episode table *(skill / agent)*
- **What happens:** Add the EP row (date, title, links as `_TBD_`, thumbnail `_TBD_` until the YouTube video is live) and keep the stub-folder note (`00N`–`015`) correct.
- **Gate → Step 6:** Table row is present.
- **Dependencies:** Linear from Step 4.

### Step 6: Commit to `main` + leave the pending list *(skill / agent)* → END STATE
- **What happens:** Commit straight to `main`. The `_TBD_` markers serve as the pending list — no PR, no separate tracker.
- **Gate → Done:** Committed; `grep -r _TBD_` surfaces exactly what the go-live process must fill.
- **Dependencies:** Linear from Step 5.

---

# Downstream process (scoped OUT, noted): Go-live finalize
When the episode actually publishes (Wednesday), run `tools/redacted_feed.py` to pull the now-available **Apple / Spotify / YouTube / runtime**, plus the **public Substack URL** and the **YouTube thumbnail**, replace the `_TBD_` markers, and commit. Separate trigger (episode goes live), separate process — not mapped here.

---

## Process Summary Table

| # | Process | Step | Gate to Next | Owner | Dependencies | Edge Cases |
|---|---------|------|-------------|-------|-------------|-----------|
| 1.1 | Record handoff | Update tracking sheet A–G | A/B/C set, F=Done, G pasted | Taylor | Linear; needs live cut-notes | 2 |
| 1.2 | Record handoff | Notify producer (Slack) | Producer pinged (END) | Taylor | Linear from 1.1 | 0 (raw auto-lands) |
| 2.1 | Notes staging | Receive go-live signal | Knows episode + drop date + draft exists | Taylor | Trigger (ping) | 1 |
| 2.2 | Notes staging | Retrieve gated Substack draft | Draft content in hand | Taylor | Linear from 2.1 | 1 |
| 2.3 | Notes staging | Assemble files shared on-air | Shared-files list known | Taylor | Parallel with 2.2 | 1 (GAP) |
| 2.4 | Notes staging | Build repo notes | Folder+README, knowns filled / `_TBD_` | Agent | Linear from 2.2 (+2.3) | 1 |
| 2.5 | Notes staging | Update root README table | Table row present | Agent | Linear from 2.4 | 0 |
| 2.6 | Notes staging | Commit to main + pending list | Committed; `grep _TBD_` = pending (END) | Agent | Linear from 2.5 | 0 |

## Edge Case Index

| Step | Edge Case | Impact | Response |
|------|-----------|--------|----------|
| 1.1 | Episode row pre-created | Verify vs. create | Update the existing row; don't add one |
| 1.1 | D/E left blank intentionally | E (drop date) feeds Process 2 timing | Treat as a cross-process dependency, not a gap |
| 2.1 | Self-initiate from cadence | Process can run without the ping | Allow a manual/cadence trigger |
| 2.2 | Gated/scheduled post, no public URL | Show-notes link can't be filled yet | Leave `_TBD_`; fill at go-live |
| 2.3 | Guest LinkedIn is a standing rule | Always required, even if not shown on-air | Agent fills from guest name — no capture needed |
| 2.3 | No canonical source for links 2–4 (company / demo / referenced resource) | Links section may be incomplete | Use production notes → memory → assets drop; else request-a-file footer |
| 2.4 | Episode not live | All platform links/runtime/thumbnail unknown | Mark every one `_TBD_` |

## Open Questions
*(Inputs for the Process + Context framework's context investigation.)*
1. **Capture source for show-notes links 2–4 (company / demo / referenced resource).** Narrowed from the old "no source for shared files" gap: category 1 (guest LinkedIn) is now a deterministic standing rule the agent can fill. Categories 2–4 still need a source. Candidate: a future *during-show capture* process so shareable links are logged live instead of reconstructed from production notes / memory / ad-hoc assets drops.
2. **Substack API** to fetch the gated draft would eliminate the manual copy in Step 2.2 (and could auto-fire the Process 2 trigger).
3. **Per-episode Spotify links** aren't exposed by any public endpoint — would need the Spotify Web API (OAuth). Show-level link used by convention for now.
4. **Sheet access.** The agent can't read column G (production notes); the handoff requires Taylor to paste them, or to grant the agent access to the tracking sheet.

## Next Step
This process map is ready to feed into the Process + Context framework. Run **`/shaner-consulting`** and bring this document into Step 2/3 (the Process/Context Cycle) to investigate the context each step needs — especially the data sources behind the Open Questions — and design the automation around Process 2.
