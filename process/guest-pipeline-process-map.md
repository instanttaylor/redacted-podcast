# Process Map: Guest Pipeline (inviting & managing [Redacted] guests)

## Metadata
- **Mapped by:** Taylor Cotner
- **Company / Role:** looptwo · co-host + showrunner of [Redacted] (NC Tweener Times network); owns guest scheduling + prep, David co-hosts
- **Date:** 2026-07-13
- **Mapping session:** process-mapping skill → feeds the Process + Context framework (shaner-consulting) at Step 3
- **Reference run:** reconstructed from the Ben Pope (Levitate, Ep 7) email thread on the looptwo producer inbox, pitch → post-record

## Trigger
A prospective guest surfaces, via one of two branches:
- **Inbound** — a pitch lands at `contact@tweenerfund.com` and **Rebecca Ross** forwards it to Taylor + David ("First Response!"). *(Ben Pope path.)*
- **Host-sourced** — Taylor/David decide on someone and Taylor reaches out cold, first contact host→guest.

## End State
Guest is recorded, thanked, any assets they offered are collected, and they've been sent their episode's show-notes folder (`00N/`) to review — at which point the episode hands off to the `prep-recorded-episode` skill.

## Where the pipeline is tracked
Source of truth is **two surfaces**, no new app:
1. **The looptwo producer inbox** (address in the gitignored `tracker.local.md`) — the live threads. Every guest conversation is a "Redacted Podcast Guest" / recording thread here. This is where email drafts get generated along the way.
2. **The Podcast Tracker Google Sheet** — a **Guest Pipeline** tab (mini-DB) holding one row per guest + current stage, so status doesn't live only in Taylor's head. *(The sheet link + gid live in the gitignored `tracker.local.md`, not here — this repo is public.)*

Guest Pipeline tab columns (lean mini-DB — kept simple):

| Column | Purpose |
|--------|---------|
| Guest | Name |
| Company | Org |
| Email | Direct guest email |
| Source | `Inbound` / `Host-sourced` |
| Stage | pipeline stage (enum below) |
| Demo topic | The one thing they'll show |
| Recording date | Locked date/time |
| Episode # | `00N` once assigned |
| Next action | The pending move |
| Notes | Link, redaction flags, last touch, etc. |

**Stage enum** (collapses the 10 steps): `Prospect → Contacted → Replied → Date proposed → Booked → Prepped → Reminded → Recorded → Follow-up done`.

### Recording slots (the "Slots" tab)
A recording date is a **first-class row**, not free text buried in a guest's row. The **Slots** tab holds one row per upcoming recording:

| Column | Purpose |
|--------|---------|
| Date | Recording slot (~10am ET) |
| Status | `Open → Held → Booked → Recorded` |
| Type | `Guest` or `Host-only` (David+Taylor) |
| Guest | Links to the Guests row; blank if open/host-only |
| Ep # | `00N` once assigned (slot ≈ episode, 1:1) |
| Notes | Holds, conflicts (e.g. "David traveling") |

**Cadence:** every-other-Wednesday, ~10am ET, **ad-hoc allowed**. Slots are hand-maintained rows — **no calendar integration**; Taylor keeps the Open runway current and reality (travel, holidays) overrides the cadence. This is what makes Step 4 a lookup instead of guesswork: the dates offered to a guest are simply the **Open** slots, and booking flips that slot to `Booked` + stamps the guest. One slot holds one guest, so double-booking is structurally impossible, and Open-slots-vs-guests-in-pipeline is the runway signal (short on guests, or short on slots?).

## Process Steps

### Step 1: Intake & triage
- **What happens:** Guest surfaces. *Inbound:* pitch hits `contact@`, Rebecca forwards to Taylor + David with the pitch body + LinkedIn. *Host-sourced:* Taylor drafts a cold "Redacted Podcast Guest" email directly (no Rebecca hop).
- **Gate → Step 2:** Hosts have the pitch/context and a guest row exists in the tracker (Stage = Prospect/Contacted).
- **Dependencies:** none (entry point)
- **Edge cases:**
  - Inbound vs host-sourced: the two branches merge at Step 3 — only Step 1 differs.
  - Scot/other Tweener Fund folks may also forward the same pitch; dedupe to one thread/row.

### Step 2: Go/no-go (grid fit)
- **What happens:** Taylor + David decide **informally** whether the guest fits the grid — genuinely interesting AI work + willing to show real work. No formal rubric; Scot/Rebecca defer to the hosts.
- **Gate → Step 3:** Both hosts are a yes and own it (Stage = Contacted).
- **Dependencies:** linear from Step 1
- **Edge cases:**
  - Soft no / not-now: park as `Prospect` rather than killing the row.
  - Only one host reachable: default is proceed (they run the show together but either can commit).

### Step 3: Open direct line + send the 3 questions
- **What happens:** Taylor emails the guest directly, points to `want-to-be-on.md` and softens it — "you don't need to *pitch*, just answer the 3 questions." Establishes the host↔guest thread.
- **Gate → Step 4:** Guest replies with role/team size + a "show & tell" menu (Stage = Replied).
- **Dependencies:** linear from Step 2
- **Edge cases:**
  - Guest offers several possible demos → carried into Step 4 for narrowing.
  - No reply → follow-up nudge; Stage stays Contacted.

### Step 4: Propose dates + narrow the topic
- **What happens:** Taylor offers the **Open slots** from the Slots tab (every-other-Wednesday, ~10am ET, keep the whole thing <1 hr) and helps the guest pick **one** thing to demo. No guessing dates — the offer is whatever's currently `Open`.
- **Gate → Step 5:** Guest picks a date (Stage = Date proposed → Booked on confirm).
- **Dependencies:** linear from Step 3
- **Edge cases:**
  - Guest gives multiple demo ideas → narrow to a single build (e.g. Ben: lead-gen tool OR cold-email program).
  - None of the offered dates work → offer the next wave.

### Step 5: Confirm + calendar invite
- **What happens:** Taylor locks it ("Invite incoming"), sends the Google Calendar invite for the recording. The chosen **Slot flips `Open → Booked`** with the guest attached (and the guest's Recording date stamped) — the two stay in sync.
- **Gate → Step 6:** Guest accepts the calendar invite (Stage = Booked; Slot = Booked; set Recording date + Episode # in tracker).
- **Dependencies:** linear from Step 4
- **Edge cases:**
  - Guest doesn't accept the invite → nudge; don't assume booked until accepted.
  - Booking interleaves with host-only (Taylor+David) recordings on the calendar.

### Step 6: Prep the guest
- **What happens:** Send the `guest-prep.md` rundown **as an email** (the default): pick one thing / it doesn't have to work, the 6 talking-point notes (org context; how it's built high-level, never code; why; problems; how the AI piece evolved; how learnings shape future work), the day-of runbook, how redacting works, and the StreamYard guest-instructions link. Offer a live pre-call only if the guest wants one.
- **Gate → Step 7:** Guest has the prep info (Stage = Prepped).
- **Dependencies:** linear from Step 5 (can be sent any time after booking)
- **Edge cases:**
  - Host traveling → prep goes out fully in writing (what Taylor did with Ben) instead of a live call.
  - Guest asks for a pre-call → schedule the short Zoom.

### Step 7: 24-hr reminder
- **What happens:** Day-before nudge — "All good to record tomorrow at 10am ET?"
- **Gate → Step 8:** Guest re-confirms (Stage = Reminded).
- **Dependencies:** linear from Step 6; time-gated to ~24h pre-record
- **Edge cases:**
  - Guest needs to reschedule → back to Step 4/5.

### Step 8: Day-of — send the StreamYard studio link
- **What happens:** Morning of, Taylor sends the **unique** StreamYard studio link (Chrome ideal) + the guest-instructions article.
- **Gate → Step 9:** Guest has the correct day-of link and joins.
- **Dependencies:** linear from Step 7; time-gated to recording day
- **Edge cases:**
  - Reusing a stale/wrong link → link is per-recording; always send the fresh one.

### Step 9: Record
- **What happens:** Guest joins, brief chat, Taylor hits record, David does the intro, guest demos + conversation. Taylor notes redaction timecodes live (or the guest flags sensitive moments in-flight). Guest stays until their side uploads.
- **Gate → Step 10:** Recording captured and uploaded (Stage = Recorded).
- **Dependencies:** linear from Step 8
- **Edge cases:**
  - Co-host absent (David travel) → one host runs it ("either way we'll be fine").
  - Something sensitive shown → flag timecode for the editor (the [redacted] mechanic).

### Step 10: Post-record follow-up → END STATE
- **What happens:** Thank the guest; send the `00N/` show-notes folder for review ("LMK if you want anything changed"); optional informal meetup. **Collecting + committing any assets the guest offers (e.g. Ben's skill for the repo) is owned by the post-recording show-notes skill (`prep-recorded-episode`), not this process** — this process hands the guest off there.
- **Gate → Done:** Guest has been thanked + sent their `00N/` folder; Stage = Follow-up done. Hand off to `prep-recorded-episode` (which owns asset intake).
- **Dependencies:** linear from Step 9

## Process Summary Table

| # | Step | Gate to Next | Dependencies | Edge Cases |
|---|------|-------------|-------------|------------|
| 1 | Intake & triage | Pitch in hand + tracker row | none | 2 |
| 2 | Go/no-go (grid fit) | Both hosts yes | linear | 2 |
| 3 | Direct line + 3 questions | Guest replies w/ role + demo menu | linear | 2 |
| 4 | Propose dates + narrow topic | Guest picks a date | linear | 2 |
| 5 | Confirm + calendar invite | Invite accepted | linear | 2 |
| 6 | Prep the guest | Guest has prep info | linear (async ok) | 2 |
| 7 | 24-hr reminder | Guest re-confirms | linear, time-gated | 1 |
| 8 | Day-of StreamYard link | Guest joins | linear, time-gated | 1 |
| 9 | Record | Recording uploaded | linear | 2 |
| 10 | Post-record follow-up | Thanked + notes sent | linear | — |

## Edge Case Index

| Step | Edge Case | Impact | Response |
|------|-----------|--------|----------|
| 1 | Inbound vs host-sourced | Changes who initiates + the Rebecca hop | Branch at Step 1; merge at Step 3 |
| 1 | Duplicate forwards (Scot/others) | Two threads/rows for one guest | Dedupe to a single thread + tracker row |
| 2 | Soft no / not-now | Guest shouldn't be lost | Park as Prospect, don't delete |
| 2 | One host reachable | Could stall a decision | Proceed; either host can commit |
| 3 | Guest offers several demos | Ambiguous scope | Carry to Step 4, narrow to one build |
| 3 | No reply | Stalls pipeline | Follow-up nudge; Stage stays Contacted |
| 4 | No offered date works | Can't book | Offer the next wave of dates |
| 5 | Invite not accepted | False "booked" | Nudge; don't mark Booked until accepted |
| 6 | Host traveling | No live pre-call | Send prep fully in writing |
| 6 | Guest wants a call | Needs live prep | Schedule the short Zoom |
| 7 | Guest reschedules | Date moves | Loop back to Step 4/5 |
| 8 | Stale link reused | Guest can't join | Always send the fresh per-recording link |
| 9 | Co-host absent | One host runs it | Proceed solo |
| 9 | Sensitive content shown | Redaction needed | Flag timecode for editor |

## Resolved decisions (from mapping session)
- **Date slots:** modeled as first-class rows in the **Slots** tab (every-other-Wednesday, ad-hoc allowed, no calendar integration). Step 4 offers whatever's `Open`; booking flips a slot to `Booked`. See "Recording slots" above.
- **Go/no-go:** informal grid-fit call by Taylor + David; no rubric.
- **Prep format:** written email is the default; live pre-call only on request.
- **Intake scope:** both inbound (via `contact@`) and host-sourced branches are in scope.
- **Guest assets:** owned by the post-recording skill (`prep-recorded-episode`), not this process.

## Open Questions
- **Guest Pipeline tab:** built in the Podcast Tracker sheet's "Guests" tab and back-filled with current guests. Live pipeline state + the sheet link are kept in the gitignored `tracker.local.md` (not in this public doc).

## Next Step
This process map is ready to feed into the Process + Context framework. Run **`/shaner-consulting`** and bring this document into Step 2/3 (the Process/Context Cycle) to investigate the context each step needs (calendar, sheet, StreamYard, the two intake surfaces) and design the guest-pipeline skill around it.
