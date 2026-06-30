# Episode 6 artifact — AI-ification Context Map (Process 2: show-notes staging)

> This is a **work artifact generated on the episode** (recorded 2026-06-30). The episode is about AI-ifying the [Redacted] post-recording workflow, so the process documents we produced *are* the show material. This file is the **context-mapping / agent-readiness** output (ai-ification **stage 3**) for the automation target.
>
> Source process map: [`../process/post-recording-process-map.md`](../process/post-recording-process-map.md)
> Framework: Shaner Consulting Process+Context, Step 3 (Process/Context Cycle). **Fork: Path A — recurring.**

## What we're assessing
*"Could an agent execute **Process 2 — publish-week show-notes staging** today, and if not, is it missing process or context?"*

The **process** is clear (mapped). Every gap is **context/access**. The headline result: the input I expected to be hardest — the production notes — is **already reachable**, and the agent can even see today's Episode 6 row.

## Process + Context table

| # | Process | Trigger | Steps | Context required (✅ have / ⚠️ path / ❌ don't) |
|---|---------|---------|-------|-----------------------------------------------|
| 2 | Publish-week show-notes staging | Tweener Fund Slack "ready for review" ping (backstop: cadence / manual) | Receive signal → retrieve draft → assemble shared files → build folder+README → update root table → commit to `main` w/ `_TBD_`s | **Repo conventions** (folder pattern, README + root-table format) ✅<br>**`tools/redacted_feed.py`** ✅<br>**Show-level Spotify URL** ✅<br>**Git commit access (main)** ✅<br>**Production notes / "shared on-air"** — sheet col G ✅<br>**Scheduled drop date** — sheet col E ✅ (blank until producer sets it)<br>**Substack** — title/desc/public-URL via public page (WebFetch, no login) ✅; full "what we cover" body via WebFetch at go-live ✅ (paste if needed pre-publish)<br>**"Ready for review" ping** — Tweener Fund Slack (channel `[redacted]`) ❌ not connected (manual trigger) |
| 1 | Record-week handoff *(context, not the target)* | Recording ends | Update sheet A–G → Slack producer | Live cut-notes ✅ (human)<br>Tracking-sheet **write** access ✅ (same sheet)<br>Notify producer via Slack ❌ (no admin access to install a Slack app/connector) |

## Confirmed access (facts, not assumptions)

- **Episode tracking sheet** — `workspace-mcp`, a **dedicated Google account** `[redacted]`, spreadsheet ID `[redacted]`.
  - Header row 2 → **A** Episode · **B** Featuring · **C** Recorded · **D** Featured Email · **E** Drop Date · **F** Podcast Recording · **G** Production Notes.
  - Verified live: **Ep 6 = recorded 6/30, status Done, production notes present, drop date blank.** (Ep 5 drop date = 7/1, confirming "out tomorrow.")
  - ⚠️ Account nuance: the sheet lives under a **dedicated Google account** — the agent must query as that account (the other connected Google account doesn't have this sheet).

- **Substack** — tested via Chrome 2026-06-30. The editor link `/publish/post/<id>` redirects to the public post URL; for a scheduled-but-unpublished post the public page renders **title + subtitle + cover + the canonical slug** with no login, and gates the body behind a "Publishes on …" countdown.
  - Discovered byproduct: **Ep 5 public show-notes URL = `https://www.tweenertimes.com/p/redacted-episode-5-the-rage-log-ai`** (was a TBD).

## Connection scorecard

| Source | Status | Mechanism / next action |
|---|---|---|
| Tracking sheet (col G + col E) | ✅ Connected | `workspace-mcp` @ a dedicated Google account `[redacted]` |
| Repo (conventions, tool, git) | ✅ In-repo | — |
| Substack | ✅ via WebFetch (no credential) | **Tested 2026-06-30:** the public gated page exposes title + subtitle + cover + canonical slug pre-publish; full body appears at publish. WebFetch pre-stage for title/desc/URL, WebFetch again at go-live for "what we cover." Editor login (Chrome) would be needed *only* to read the body before publish — not worth it; paste covers that gap. |
| Tweener Fund Slack ("ready for review" ping) | ❌ No Slack admin access → **manual trigger** | Channel `[redacted]` in the Tweener Fund Slack. We have **no admin access to any Slack workspace**, so no app/connector (token *or* OAuth) can be installed. The trigger stays human-in-the-loop. |
| Google Drive / Gemini meeting notes | 🚫 Out of scope | Reachable, but Taylor said **do not use** |

## Agent-readiness verdict (stage 3)
**Ready to build, with a known input contract.** Every input is ✅ or has a clean no-credential path: repo conventions, the RSS tool, git, production notes + drop date (sheet via workspace-mcp), and Substack (WebFetch). **One item is human-in-the-loop:**
- **Trigger** — the "ready for review" ping lives in the Tweener Fund Slack (channel `[redacted]`). Steady state: **manual trigger** (invoke the process when the ping arrives). Automating it would require Slack-workspace admin access we don't have, so it stays manual — not a blocker for building the rest.

This does not block an arch spike; it scopes it.

## Open questions (carried forward)
1. **Trigger automation** — blocked: no Slack admin access to install an app/connector for the Tweener Fund Slack (channel `[redacted]`). Trigger stays manual unless Slack admin access becomes available.
2. **"Shared on-air" source** — col G production notes are cut/redaction notes, *not* a list of files shared on screen. The canonical "what files to post" source is still unsolved (the future "during-show capture" process from the process map).

## Next step (deferred by decision)
**Architecture spike (ai-ification stage 6 / Shaner Step 4).** Decide the agent shape (likely a Claude Code skill / hybrid that reads the sheet via workspace-mcp, WebFetches the Substack post, builds the repo notes, and calls `redacted_feed.py`). Not done in this session — context first, architecture when context is answered.
