# Offline BD Walkthrough Playbook

Manual BD process for the ~14 target companies that came out of David's original work with [REDACTED]. The goal is to keep David warm with specific execs at each company through a repeatable pattern: track the relationship state, monitor the company's public signals, and engage thoughtfully on LinkedIn when something material happens.

The first end-to-end run was on **Vox Media / Eater** (May 2026). That run defined the playbook below. Replicate the same shape per company.

## Per-company directory layout

```
biz_dev/
├── README.md                  (this file)
├── plan.md                    (original March 2026 automation design — kept for context, superseded by this playbook)
└── <company-slug>/
    ├── contacts.jsonl         (one contact per line, full state of play per person)
    ├── <company>-narrative-arc.md  (chronological relationship history, with quoted moments)
    ├── state-of-play.md       (Phase 5.5 readable briefing — David approves this before Phase 6)
    ├── intel-config.yaml      (queries, jobs board URL, LinkedIn URLs, canonical sources)
    ├── intel-ledger.jsonl     (append-only, one news/job/post per line — dedupe source of truth)
    ├── timeline.md            (human-readable view of the ledger, newest-first by month)
    └── linkedin-snapshots/    (raw HTML + extracted posts JSON per profile, dated by run)
```

The vox-eater/ directory is the working reference implementation.

## Process — five phases

### Phase 1. Contacts (~30 min)
Start every company by getting the contact list right.

1. **Gmail search** for the company's email domain across all directions:
   `from:(company.com) OR to:(company.com)`. Use the canonical `_gmail.py` block at `.claude/skills/code-blocks/blocks/gmail-thread-read.md` — it strips quoted-reply chains. Iterate page by page until exhausted.
2. **Distinct threads + participants**: extract every unique sender/recipient at the company's domain (and subdomains like `contractors.*`).
3. **Body Man DB** (`projects/personal/gtm-brand/body-man/db/contacts.db`) — check if any of them already exist with personal notes.
4. **LinkedIn title lookup** via WebSearch per name — produces title, tenure, slug.
5. **Build `contacts.jsonl`** — one JSON object per line per contact. Fields:
   - `name`, `emails`, `title`, `company`, `linkedin`
   - `track` (editorial / corp_dev / sponsor / EA / etc.)
   - `introduction` (how the relationship started, with date)
   - `current_status` (WARM / DORMANT / PARKED / NEW / NOT A TARGET)
   - `ball_in_court` (david / them / parked / n/a)
   - `last_meaningful_exchange` (date + 1-line)
   - `arc_summary` (relationship history in 2-3 sentences)
   - `behavioral_notes` (response cadence, who they loop in, surprises)
   - `key_quotes` (1-2 actual sentences from emails where phrasing matters)

### Phase 2. Narrative arc (~60 min)
Read the email bodies — not just headers. Subagent OK for volume but **verify factual claims against saved source data before reporting** (subagents over-synthesize on thin data, fabricating internally-consistent details).

Produce `<company>-narrative-arc.md` covering:
- Origin (who introduced David to whom, when)
- Each substantive touchpoint with date + quoted language at turning points
- Stalls, kills, reboots — what was actually said, not what was inferred
- Where it sits today and whose ball it's in

The narrative arc is the document David reads before any call with the company. It supersedes any inference made from email-thread headers.

### Phase 3. Intel config (~20 min)
Build `intel-config.yaml` per company. Fields:
- `search_rules`: `no_year_padding: true` (year qualifiers like "2026" suppress canonical-title matches — bias recent through topical specificity instead)
- `canonical_sources`: company press room / newsroom URL, blog, jobs API. **WebFetch is blocked on many media-co domains (eater.com, voxmedia.com) — use curl with a Mozilla User-Agent as fallback.**
- `news_queries`: company-level + brand-level + industry-context + per-person (all 7+ contacts, cheap to include). NO year tokens.
- `jobs`: ATS detection (Greenhouse / Lever / Ashby — most have public JSON APIs) + brand bucketing
- `linkedin`: per-person profile + activity URLs + 2 company page URLs (main + brand)
- `output`: ledger + timeline paths, dedupe by canonical URL

### Phase 4. Intel sweep (~30 min)
**Initial run** = 6-month window. **Subsequent runs** = no time filter, dedupe by ledger.

1. **News pull** — fire all news queries in parallel via WebSearch. Dedupe by canonical URL (strip `utm_*`, `fbclid`, `gclid`, `ref=`). Treat the same story covered by different publishers as SEPARATE items — different framings matter.
2. **Jobs pull** — one GET to the ATS API. Bucket by brand. Filter to last 6 months on first run, dedupe after. **Always capture each surfaced role's direct URL** (Greenhouse `absolute_url` / `careers.toasttab.com/jobs?gh_jid=<id>`, Workable `jobs/view/<id>`) into the ledger + timeline so David can click straight through — don't list a job title without its link.
3. **Canonical sources** — direct fetch each one (curl when WebFetch is blocked). The company's own press room is the most reliable source of in-window announcements that WebSearch misses.
4. **Three-layer summary** per ledger entry:
   - `summary_piece` — what THIS item actually says
   - `summary_landscape` — how it fits in the company's broader landscape
   - `summary_impact` — how it may impact Offline's relationship with the company
   - **CRITICAL**: `summary_impact` is descriptive, not prescriptive. Do not include "we should X" / "outreach opportunity" / "conversion target" framing. David decides what to do with findings.
5. **Append to `intel-ledger.jsonl`** and **insert into `timeline.md`** (newest-first by month).

### Phase 5. LinkedIn pass (~20 min, requires logged-in Chrome)
Use chrome-devtools MCP against a logged-in Chrome instance. The MCP uses its own profile at `~/.cache/chrome-devtools-mcp/chrome-profile/` — log in to LinkedIn there once, cookies persist.

For each LinkedIn URL in the config:
1. `navigate_page`, then `wait_for` content text
2. `evaluate_script` to extract posts as JSON → save to `linkedin-snapshots/<slug>.posts.json`
3. `evaluate_script` to grab `main` outerHTML → save to `linkedin-snapshots/<slug>.html`
4. Sequential, not parallel — parallel calls overwrite the same file

Output: surface engageable post permalinks (`https://www.linkedin.com/feed/update/urn:li:activity:XXXXX/`) so David can interact directly. Append the highest-signal posts to the ledger + timeline.

**Team inventory (optional sub-process):** to inventory a target's full *current* team (function breakdown + verified roster, noise stripped), follow `linkedin-team-inventory.md`. Run it interactively via the `claude-in-chrome` MCP — never a headless LinkedIn bot (account-ban risk). Done for [REDACTED] + [REDACTED]; output lands in `<company>/headcount-roster.md`.

### Phase 5.5. State-of-play briefing + REVIEW GATE (mandatory — do not skip to Phase 6)
**Hard stop. Before any wedge or draft work, produce a single readable synthesis David approves.**

After the intel is gathered (Phases 1–5, or a re-run), write/refresh `<company>/state-of-play.md` — a prose briefing (not raw ledger dumps) that David reads and signs off on *before* engagement. It synthesizes the narrative arc + timeline + contacts + any re-run delta into:
1. **Who the company is** (one paragraph) + why they matter to Offline
2. **The relationship** — current state, whose ball, the most actionable signal
3. **Current intel picture** — what the (re-)run found, net-new items called out, date-checked
4. **Contact map** — who, and *why the entry point is who it is*
5. **Where it sits / open paths** — descriptive, **no wedge or recommendation yet**

Then **present it and STOP.** Do not proceed to the wedge brainstorm or drafts in the same turn. David reviews, corrects, and explicitly approves. The wedge is downstream of his sign-off — surfacing intel and proposing outreach in one breath is the failure mode this gate exists to prevent (added 2026-06-08 per David: "I'd like to be able to review that before we move on to the wedge").

The Phase 6 wedge brainstorm (`<company>/phase6-wedge-brainstorm.md`) may be *prepared* but is not *presented* until the gate clears.

### Phase 6. Engage (in-session, after David approves the Phase 5.5 briefing)
This is where a run actually ends: David drafts outreach emails to specific contacts, in the session.

1. **David dictates the rough content** per contact; the agent polishes lightly — preserve his words and register, don't reinterpret. Short, conversational, no corporate polish.
2. **Create Gmail drafts only — never send.** Use the Gmail API directly (MCP is blocked), composing per `.claude/skills/code-blocks/blocks/gmail-email-body.md` (multipart/alternative; plain MIMEText hard-wraps at ~70 chars). Reply on the existing thread when one is live (thread ID from the narrative arc's source-threads table + `In-Reply-To`/`References` headers); fresh email otherwise.
3. **Log the engagement**: note the draft (date, recipient, thread) in the contact's `behavioral_notes`/`arc_summary` trail and the narrative arc's "Where it sits" section. `ball_in_court` stays `david` until the draft is actually sent.
4. David edits/sends from Gmail on his own schedule.
5. **A/B drafts:** when comparing copy approaches, stack both versions in ONE draft per recipient (divider blocks + "delete the version you don't use"), never parallel drafts to the same person — avoids accidental double-sends.
6. **Register every outreach in `biz_dev/followups.yaml`** — the follow-up cadence ledger.

### Phase 7. Follow-up cadence (automated via /bootup)
Cold outreach needs ~5 touches. The ledger is `biz_dev/followups.yaml` (5-touch ladder:
+4/+8/+15/+25/+40 days from initial send, tunable per the `cadence_days` key).

`_followups_check.py` runs as /bootup Offline background process #9 and is zero-maintenance:
- **Send detection** uses `in:sent` + DRAFT-label exclusion (drafts appear in plain Gmail
  search — never count them as sends). First real send sets `sent_date` and starts the clock.
- **Touch counting**: each later David-sent message to the contact counts as the next touch.
- **Reply detection** auto-stops the cadence (status → `replied`) and surfaces a 🎉 in bootup.
- Manual states: set `status: closed` + `closed_reason` to abandon a thread.

Bootup Phase 4 prints the 🔔 due list (who, touch #, overdue days, wedge). David sends the
follow-up from Gmail; next bootup counts it automatically.

## Re-run model

Every subsequent run for a company:
1. Re-fetch all news queries + canonical sources + jobs API + LinkedIn pages
2. Build a candidate set of items
3. Dedupe against the existing `intel-ledger.jsonl` by canonical URL (fallback: hash of publisher+title)
4. Only NEW items go into the timeline + ledger
5. Time window is NOT enforced on re-runs — dedupe replaces it

## Rules learned (read before each new-company run)

These came out of the Vox/Eater walkthrough; they apply to every future company.

1. **No year-padding on queries.** "Eater app news 2026" suppresses the literal canonical announcement "The Eater App Just Got a Lot Better." Use bare topical queries and filter by published date in post-processing.
2. **Press rooms are canonical, not searchable.** WebSearch misses what's on the company's own press page. Always fetch the press room directly each run.
3. **Verify subagent factual claims.** Spot-check biographical, employer/title, and "X named Y in their post" claims against saved source data before relaying — subagents fabricate internally-consistent details when source material is thin.
4. **Read message bodies, not headers.** For state-of-play synthesis, use the canonical `_gmail.py` block which strips quoted-reply chains. Headers alone produce lazy reads.
5. **No unbidden recommendations.** Summaries describe implications, not actions. Don't translate findings into outreach plans inside the ledger.
6. **Different publishers covering the same story are separate ledger items.** Adweek + Puck + Status framings differ — keep all three.
7. **WebFetch is blocked on many media-co domains.** Fall back to curl with `-A "Mozilla/5.0"`.
8. **Never inflate an exploratory artifact into a capability claim.** A repo, a PoC, a test integration, a deck — the existence of an artifact is NOT evidence Offline "has built" or "has shipped" the thing. State capabilities at the altitude the *operator* states them, not the altitude a subagent synthesizes from a GitHub commit. Concrete failure (2026-06-03/08): the single-commit `fidel-poc` sandbox got written up as "the architecture question is resolved / Offline built its own member-rules layer," with invented version numbers (Next.js 16 vs actual 14). That propagated from the Fidel arc → wedge brainstorm → [REDACTED] briefing. David caught it at the email layer (his sent copy: "ran a working PoC against your API to test it out… nothing card-linked yet") but the docs stayed wrong for weeks. **Before any capability sentence enters a briefing or a draft, verify it against source (the repo, the operator, the sent record) — and when in doubt, under-claim.** Card-linked specifically: Offline is POS-discount-button based; card-linking is exploratory, not built.

## When you onboard a new company

1. Create `biz_dev/<company-slug>/` with the same six file shape.
2. Phase 1 → Phase 5 in order. Don't skip Phase 2 (narrative arc) — it's what makes the intel timeline interpretable later.
3. Use vox-eater/ as the working example. The `intel-config.yaml` there is the closest thing to a template.
4. Each company gets its own ledger. No cross-company sharing.

## Status (as of 2026-06-03)

**All 18 companies have completed initial walkthroughs** (runs executed 2026-05-18/19 via the parallel prompts in `parallel-run-prompts.md`, plus the four pilot runs). Notable run results:

- ✅ Vox / Eater — first complete run; **re-run 2026-06-03** (first use of the re-run model: 12 new ledger entries → 58 total). Re-run surfaced the May 20 [REDACTED]/Lupa deal (Eater excluded → spins into unnamed "RemainCo" under [REDACTED]), Penske all-or-nothing talks for the unsold brands, and [REDACTED]'s departure to Crown/Ten Speed Press. (Note: Adweek's late-May Capital One mention is recycled 2025 Puck tire-kicking, not new interest — Capital One exited the Eater app partnership Mar 2026.)
- ✅ Toast — 24 ledger entries, 18 contacts. SMS-layer enrichment via iMessage proved critical (75 messages with Craig Daniel changed the M&A timeline framing entirely).
- ✅ [REDACTED] — 14 entries, 11 contacts. Cross-channel triangulation validated; LinkedIn surfaced Mark Tisdale's March 2026 departure.
- ✅ ClassPass / Playlist — 12 entries, 7 contacts. ClassPass F&B = timed-pickup commerce, not full-service integration; Playlist+EGYM merger close explains the 10-month silence.
- ✅ SevenRooms, DoorDash, Rewards Network, Axios/Cox, The Infatuation, [REDACTED], Bilt, Amex (+Resy/Tock/Rooam), Capital One, Chase, Visa, Atlas (intel-only, no Gmail history), Yonder, Fidel — all complete per the parallel-run protocol.

**Phase 5 (LinkedIn pass) backlog:** only 5 of 18 companies have LinkedIn snapshots (vox-eater, toast, inkind, bilt, seated). The other 13 deferred Phase 5 (concurrent-session Chrome profile locks during the parallel runs) — several have explicit `DEFERRED.md` markers in their `linkedin-snapshots/` dirs listing open verification items (e.g. capital-one: Barry Frish departure date, Monica [REDACTED] title).

**Re-run cadence:** no companies besides vox-eater have been re-swept since 2026-05-18/19.

- ✅ Owner.com — onboarded 2026-06-03 (19th company). Cold prospect, intel-only (Atlas pattern — zero Gmail history, no Body Man contacts). $1B-valuation restaurant SaaS (websites/commission-free ordering/AI marketing for independents; "Shopify for local business"). 7 ledger entries, 4 contacts (all NEW: Guild, Bloembergen, Lehman, Norton). Key intel: Givefront acquisition (May 2026), Popmenu lawsuit over Grader (Jan 2026), ex-Shopify VP Design hired as CDO. Offline overlap: Raleigh Raw (Offline partner) is an Owner customer.
- ✅ Dorsia — onboarded 2026-06-26 (20th company). **Intel-only / strategic REFERENCE, not an outreach target** (Atlas pattern — no `dorsia.com` Gmail history, no Body Man contacts). Members-only prepay-minimum reservation + events platform (named after the *American Psycho* restaurant); founder/CEO Marc Lotenberg (also runs Surface Media). ~30K paying members, $100K–$200K/day (CNN Mar 2026); $50.4M seed+A, Feb 2025, Index Ventures, $146M valuation. 14 ledger entries, 9 contacts (3 LinkedIn-confirmed + Lonsdale; the supply-side VPs are UNVERIFIED theorg.com names). **Why it's here:** David actively cites Dorsia as the "bougie top-of-funnel membership tier" comparable in his live Eater conversation (Krupnick, 2026-06-26). Only-ever Offline touchpoint: then-VP Ramy Kerdany was on The Supper Club's list when Dorsia acquired it (Mar 2025) — now unstaffed (Ramy departed). Phase 5 (LinkedIn) deferred. Held as a monitored comparable pending David's Phase 5.5 review.

Pairing notes:
- **Chase ↔ The Infatuation**: same parent (JPMorgan Chase has owned The Infatuation since 2021). Run as separate walkthroughs but cross-reference moves.
- **Amex bundle**: Amex / Resy / Tock all share an exec surface — bundled in the Amex walkthrough.
- **SevenRooms ↔ DoorDash**: same parent (DoorDash acquired SevenRooms) — separate walkthroughs, cross-reference moves.
- **Axios + Cox**: combined dir (`biz_dev/axios-cox/`) since both flow through the same parent.
