---
name: guest-pipeline
description: Manage [Redacted] podcast guests end-to-end — from a guest surfacing (inbound pitch to contact@tweenerfund.com, or a host-sourced prospect) through recorded + handed off. Reads the looptwo producer inbox, the "Guests" tab, and the "Slots" tab (recording runway) of the Podcast Tracker sheet, reconciles where each guest stands, and DRAFTS the right next email at each stage (first reply, propose dates, prep, 24-hr reminder, day-of StreamYard link, post-record thank-you) as a Gmail draft for Taylor to review + send. Also updates the tracker row. Use when asked to "manage guests", "who's up next", "guest pipeline", "add a guest", "advance <guest>", "draft the next email to <guest>", "reach out to <guest>", "prep <guest> for recording", or when a guest thread needs a next move. Drafts only — never sends. (For a guest's episode show notes after recording, use prep-recorded-episode.)
---

# Guest pipeline (inviting & managing [Redacted] guests)

Operates the process mapped in [`process/guest-pipeline-process-map.md`](../../../process/guest-pipeline-process-map.md). Two source-of-truth surfaces, no new app:

1. **The looptwo producer inbox** (the dedicated Google account — address in `tracker.local.md`) — the live guest threads (subject usually `Redacted Podcast Guest` or a recording thread). Read via the **Gmail MCP** (`search_threads`, `get_thread`).
2. **The "Guests" tab** of the Podcast Tracker sheet — the mini-DB of one row per guest + stage. Config (spreadsheet ID, tab gids, column maps) lives in the gitignored `.claude/skills/prep-recorded-episode/tracker.local.md`.
3. **The "Slots" tab** — one row per upcoming recording date (`Date · Status · Type · Guest · Ep # · Notes`), Status `Open → Held → Booked → Recorded`, plus `Unavailable` for a cadence date Taylor has blocked (meeting, travel, holiday). Cadence is weekly Wednesdays, ad-hoc allowed; every Wednesday opens as a guest slot, and a host-only recording claims one by flipping its `Type` to `Host-only`. **No calendar integration** — Taylor hand-maintains the Open runway. **Offer a guest the next 5 `Open` slots** (soonest first); never invent one, and never offer or book an `Unavailable` date even when the runway is thin. Keep at least 5 `Open` rows standing ahead of today — if fewer remain, extend the weekly runway before drafting.
4. **The "Guest Log" tab** — the append-only per-guest memory (`Date · Guest · Type · Note`, Type one of `Pitch / Detail / Demo / Contact / Decision`). One row per durable fact worth recalling later: pitch specifics, demo candidates on the table, personal context (meetups, favors owed, company changes spotted in signatures), alternate contact info. Not a copy of the emails — the inbox has those. **Write:** whenever processing a guest thread surfaces a fact like this, append a row (confirm with Taylor like any sheet write). **Read:** before drafting any email to a guest, pull their Guest Log rows and use them to personalize.

**This skill DRAFTS, it does not send.** Every email is a Gmail draft for Taylor to review and send himself. It also **never invents dates** — there's no calendar integration; recording cadence is currently weekly, and the open slots come from the Slots tab (extend the runway only with Taylor's say-so).

**Trigger is manual.** Run when asked, or when a guest thread needs its next move.

## Load config first
Read `.claude/skills/prep-recorded-episode/tracker.local.md` (gitignored) for the Google account, spreadsheet ID, and the **Guests tab** column map + stage enum. If it's missing, ask Taylor for the dedicated Google producer account and the "Redacted Podcast Tracker" spreadsheet ID.

Voice for every draft comes from [`want-to-be-on.md`](../../../want-to-be-on.md) (the pitch) and [`guest-prep.md`](../../../guest-prep.md) (the day-of expectations). Match Taylor's tone: short, warm, low-polish, "you don't need to over-prepare."

**Standard link — always include it in the FIRST Taylor→guest email.** The public "what the show is like" page is `want-to-be-on.md` in the repo, at `https://github.com/instanttaylor/redacted-podcast/blob/main/want-to-be-on.md`. Every guest's first touch from Taylor (whether that's a first-contact or a propose-dates note) links it so they know what they're signing up for. It's a public repo URL — safe to send.

## Modes

Pick the mode from what's asked:

### A) Status / triage — "who's up next", no guest named
1. Read the **Guests tab** and the **Slots tab** (workspace-mcp `read_sheet_values` as the looptwo account).
2. Scan the inbox for active guest threads (`search_threads`, e.g. `subject:"Redacted Podcast Guest" OR subject:"Redacted Recording"`, recent).
3. Reconcile: for each guest, confirm the sheet **Stage** matches the latest email, and surface the **Next action** + who's waiting on whom. Flag any guest the tracker and inbox disagree on.
4. Print a compact pipeline table **plus the runway**: the next few `Open` slots, and the read on it — short on guests (open slots > guests in flight) or short on slots (guests in flight with nowhere to land)? Recommend the single highest-priority next move (usually the guest who's owed a reply).

### B) Advance a guest — a guest is named
1. Pull that guest's full thread (`get_thread`) + their sheet row.
2. Determine their **current stage** from the last email (see stage map below).
3. **Draft the next-stage email** as a Gmail draft (`create_draft`, `replyToMessageId` = the last message in their thread so it threads correctly). Personalize from the thread; fill any host-supplied blanks (dates, StreamYard link) only after asking Taylor.
4. Show Taylor the draft text in chat, note it's saved as a draft (not sent), and tell him what to supply/verify before sending.
5. **Update the tracker row** — advance Stage + set the new Next action + Last touch. Confirm the row change with Taylor before writing.

### C) Add a guest — new prospect
- **Inbound:** Rebecca forwards a pitch from `contact@tweenerfund.com` to Taylor + David. Create a Guests row (Source = `Inbound`, Stage = `Contacted`). Then run mode B to draft the first reply.
- **Host-sourced:** Taylor decides on someone. Create a row (Source = `Host-sourced`, Stage = `Prospect`/`Contacted`) and draft the first cold outreach.
- **Go/no-go is Taylor + David's informal grid-fit call** (genuinely interesting AI work + willing to show real work). Don't auto-commit a guest — confirm they're a yes before drafting outreach.

## Stage → next email (the drafts)

Each stage's draft, grounded in how Taylor actually writes. Keep them short. Bracketed `[...]` = a blank Taylor must fill or confirm.

| Stage (current) | Draft to write | Then set Stage → |
|---|---|---|
| **Contacted** (host-sourced, no reply yet) | **First contact:** link the `want-to-be-on.md` page (public URL above); soften — *"You don't need to 'pitch' us. Just shoot back a few answers to those 3 questions and we'll chat more."* | Contacted |
| **Replied** (guest sent role/team + demo menu) | **Propose dates + narrow topic:** offer the **next 5 `Open` slots from the Slots tab** — *"Right now I'm booking for [the 5 open slot dates]. We record around 10am ET and keep it under an hour. Any of those work?"* + help pick **one** demo. Never invent a date; if there are no Open slots, ask Taylor to add some. Surface the demo-topic candidates in chat first and draft the one Taylor picks — never write your own pick into the email. **If this is the first Taylor→guest email (e.g. a host-sourced yes), include the `want-to-be-on.md` link too.** | Date proposed |
| **Date proposed** (guest picked a date) | **Confirm:** *"Amazing, let's get you on the schedule for [date]. Invite incoming and I'll get you more info soon."* (Taylor sends the actual Google Calendar invite — the skill doesn't.) Then **flip that Slot `Open → Booked`** with the guest attached + Ep #, and stamp the guest's Recording date — confirm both writes with Taylor first. | Booked |
| **Booked** (invite accepted) | **Prep:** send the canonical copy below verbatim. It carries **three** links, the studio link among them — so this email is blocked until Taylor confirms the studio link (see sourcing under **Prepped**). **No pre-calls — all guest comms via email.** | Prepped |
| **Prepped**, ~24h before record | **Reminder:** confirm the date by weekday + number and **include the studio link** — *"All good to record Wednesday the 12th at 10am ET? Here's the [studio link]. It's also in the calendar invite."* Name the date rather than saying "tomorrow": the guest's prep email may predate a reschedule and still show the old date. Put the link in the email rather than only pointing at the invite. **Sourcing the link (applies from the prep email onward):** it's the `Location` on the Google Calendar event and it appears in the guest's `Accepted: …` email in the inbox, so pull it from there and have Taylor confirm it matches the live invite (a rescheduled event keeps its original acceptance email, so the copy on file can predate the move). It is a **standing room URL, not per-recording** — the same link has been reused across guests, so a stale copy can look right and still be wrong. | Reminded |
| **Reminded**, morning of | **Day-of link:** send the canonical copy below verbatim, with the StreamYard studio link from Taylor. | Recorded (after the record) |
| **Recorded** | **Post-record thank-you:** thanks; *"it'll hit the feeds in a few weeks"*; share the `00N/` show-notes folder for review (*"LMK if you see anything you want changed"*); optional meetup. | Follow-up done |

### Prep email — canonical copy

Taylor's wording (2026-08-25). Send it as-is; swap the greeting, the date, and the studio link. **Three** hyperlinks, all anchor text: "What to expect on recording day" → `guest-prep.md`, "recording link to StreamYard" → the studio link, "guest instructions" → StreamYard support. `htmlBody` only, no plain-text `body`. The five list items are a real `<ul>`.

```
Hey [First],

Here's the prep for [Month Dth]. Let me know if you have any questions about it.

What to expect on recording day:
- Bring your show and tell. It does not have to work. We want to understand the story behind why you did it. Maybe a little bit about the broken parts along the way.
- While you walk us through it, we're thinking about where it fits in the business, how it's built at a high level, why you built it, how the AI part evolves, and what you're doing differently next time. We'll probably ask questions about this as you go.
- Here's your recording link to StreamYard you'll use on the day of (also in the invite), which is where you'll record from. Chrome works best.
- Here are some guest instructions. We'll chat for a few minutes and then record for 30 to 45 minutes.
- If anything you don't want on the screen share shows up, tell us in the moment and we'll blur it or cut it.

The recording isn't live.

Taylor
```

The studio link now ships at **prep**, not on the morning of. Don't write "we'll email you the link that morning" — it's already in their hands by then; the reminder and day-of emails repeat it.

### Day-of email — canonical copy

Taylor's wording (2026-07-29). Send it as-is; swap the greeting and drop in the studio link he supplies. Two hyperlinks, both anchor text: "studio link" and "guest instructions". `htmlBody` only, no plain-text `body`.

```
Hey [First],

We're on for 10am ET this morning. Here's the studio link.

Chrome works best. If you haven't used StreamYard before, their guest instructions cover the setup.

We'll chat before we hit record. Bring the one thing you want to show and see you in a bit.

See you at 10,
Taylor
```

Do not add "hop in a few minutes early", the "it doesn't have to work" line, or anything else from `guest-prep.md`. The prep email already covered it.

After **Recorded**, the episode's show notes are `prep-recorded-episode`'s job — that skill also owns collecting any assets the guest offered (e.g. a repo/skill). Hand off; don't duplicate here.

## Hard rules
- **Drafts only — never send.** Use `create_draft`; the human sends. Never call any send path.
- **Never invent dates or links.** Candidate recording dates and the StreamYard studio link come from Taylor. Leave `[bracketed]` blanks and ask; don't guess.
- **Never fabricate guest replies or commitments.** Read the thread; if a stage isn't clearly reached in the emails, ask rather than assume.
- **No assistant opinions in a draft.** A draft carries the host's words and decisions only. Never write "my vote is", "I'd suggest", or any recommendation the host didn't make into an email going out over his name. When a draft needs a judgment call (which demo to narrow to, which angle to push), list the candidate options **in chat** with the supporting detail from the guest's thread, let the host pick, then write the draft from his choice.
- **Confirm before writing to the sheet.** Show the row change first.
- **Public-repo hygiene.** Guest emails + booking details live in the **private sheet** and the **inbox** only — never write a guest's email address, an unlaunched guest's name, or the sheet ID/link into anything under version control. The process map in `process/` stays generic.
- **Thread replies correctly.** Pass `replyToMessageId` so drafts land in the existing guest thread, not a new one.
- **Draft house style — run the `stop-slop` skill on every draft before saving it.** No em dashes. No adverbs (`just`, `really`, `actually`, `genuinely`). No throat-clearing openers ("Here's what we've got…"). Short sentences, active voice, Taylor's warm low-polish tone.
- **Links as anchor text, never raw URLs — and no plain-text fallback when the email has a link.** In `create_draft`, pass `htmlBody` with the link as a hyperlinked phrase (e.g. `<a href="…">what being on the show looks like</a>`) and pass **no `body` at all**. **Gmail rewrites outbound links through its own redirector — `https://www.google.com/url?q=<real-url>&source=gmail&ust=…&sa=E` — and that is normal, expected, and works.** The recipient clicks the anchor and Google forwards them to the real URL. It happens whether the mail is drafted through the API or typed by hand in Gmail, so **do not try to defeat it** (no `#fragment` tricks, no stripping the `<a>` tag). Taylor's own sent mail has always looked like this and guests click through fine. The one genuine failure mode looks different: the params glued onto the URL with **no** `google.com/url?q=` wrapper, e.g. `…/tree/main/011&source=gmail&…`, which 404s (seen once, 2026-08-19). So after creating any draft with a link, read it back via `list_drafts` (`DRAFT_VIEW_FULL`) and check which form you got: wrapper present = fine, ship it; params appended bare = recreate the draft. Note the body comes back empty for a minute or two after creation. Only send a plain-text `body` for emails with zero links. Every `href` ships exactly as Taylor supplied it: no UTMs, no tracking or campaign params, no shorteners, nothing appended.
- **Never edit a draft with `update_draft` once it exists.** It has no `replyToMessageId` parameter, so editing silently moves the draft out of the guest's thread into a new one. To change a draft: confirm Taylor is not mid-edit in Gmail, then `create_draft` fresh with `replyToMessageId` and have him delete the stale one. Check `threadId` in `list_drafts` after every draft write. If the draft's timestamp moved and you did not move it, Taylor is editing it — leave it alone.
