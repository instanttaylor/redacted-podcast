---
name: clickup-process-reconciliation
description: Reconcile an Offline process SOP into a clean, agent-readable ClickUp process page in the house format (Step · Process step · Actor · Notes · LLM Access). Takes a written SOP page (or a meeting transcript + a target page) and reconciles it against live reality — code, n8n, the Offline internal API, Slack — grounding an LLM-Access column in the real credential map so the output doubles as an automation-readiness map. Use when David, Steve, Page, or Taylor says "reconcile this process", "clean up the process doc", "render the process map to ClickUp", "check the SOP against reality", "rerun the [X] process in the new format", or invokes /clickup-process-reconciliation.
---

# ClickUp Process Reconciliation

Turn an Offline process SOP into a clean ClickUp process page in one house format, where every step states what *actually* happens today (verified against code/n8n/API, not the written SOP) and carries a binary **LLM Access** verdict — can an agent do this step via a real credential we hold, or not. Running this across processes produces Offline's **automation-readiness map** (the input to "ai-ify the processes").

Built from the 2026-06 Programming-L10 reconciliation of the 25 One-Off Partner Processes. The original working notes live at `projects/offline/internal/10_org/meetings/2026-06-16_reconciled-table-format.md`; this skill is the living version.

## Preflight: ClickUp connector check

Before anything, verify the ClickUp connector is available — look for a tool named `clickup_*` / `mcp__clickup__*`. If none exists in this session, stop and tell the user:

> "This skill needs the ClickUp connector. Open Cowork → Settings → Connectors and connect ClickUp, then try again."

Do NOT call ClickUp tools that aren't present.

## What this does — explain if asked

Given a process (a written SOP page, or a meeting transcript + a target page), it produces a clean ClickUp process page where:
- each row is the **current** step (not the stale SOP wording),
- **Actor** marks human 🧑 / machine 🤖 / handoff,
- **Notes** carries the real mechanism (endpoints, n8n IDs, files),
- **LLM Access** is a binary ✅/❌ — whether an agent could do that step via a credential we actually hold.

It does NOT invent processes (that's `process-mapping`/`shaner-consulting`) and it does NOT file L10 issues (that's `programming-l10`) — though it surfaces dev bugs and L10 candidates as it goes.

## The house format (the table)

Canonical columns: **`Step | Process step | Actor | Notes | LLM Access`**

- **Step** — `TRIGGER` (one row per intake source — multiple sources = multiple `TRIGGER` rows), then `1`, `1a`, `1b`… Split each human↔machine handoff into its own sub-step. `—` for a real step with no SOP origin (e.g. an automated side effect).
- **Process step** — a clean, current description of what happens. State the truth directly; never carry "the SOP said X but now Y" framing or stale superseded methods. The trigger description lives here on the `TRIGGER` row.
- **Actor** — 🧑 / 🤖 / 🧑→🤖 / 🤖→🧑.
- **Notes** — the real current mechanism: endpoints, fields, files, n8n workflow IDs, owner, caveats, open questions. For a 🤖 row, also make the step's **side effects on real external systems** legible (see rule 4).
- **LLM Access** — **binary ✅ or ❌, never ⚠️/in-between** — plus a short note of what access exists or what's missing (e.g. `❌ fine_print_days write not in the PATCH permit`).

Hard format rules:
1. **Nothing between the page title/subtitle and the table.** No intro prose, no trigger paragraph, no banners — the trigger is a `TRIGGER` row.
2. **Nothing below the table** — unless it's a **HITL / Edge Case table**. A note that matters folds into a `Notes` cell or gets dropped; don't manufacture an edge-case table out of notes.
3. **One process = one table.** Two distinct processes = two pages (split them).
4. **External-system effects must be legible on every 🤖 row — but only where informative.** Mark `✍️ writes:` on any step that writes to a human-facing system (HubSpot, Rails, Gmail, Slack…), naming the object + fields and the gate. Also mark `✍️ writes: none` where a reader would *expect* a write but none happens (the surprising "none" — e.g. a "cleanup" step that's read-only until a flag flips). Do **not** stamp `writes: none` on benign rows — absence of a `✍️` marker means read-only. Use `📖 reads:` the same way, only where the target is informative (which object/fields). This effect axis is **distinct from `LLM Access`**: reads/writes describe what the step *does to real data*; `LLM Access` describes whether an *agent could perform* the step.

### Trigger taxonomy

A `TRIGGER` row is a **real** way the process gets kicked off — one row per source. Three kinds:

- **Composed** — the process runs as a step inside a parent flow (Actor 🤖; name the parent process + step). Label: `TRIGGER · composed`.
- **Manual (MCP)** — a human asks via an MCP client (Claude Desktop / Claude Code) with the seed ID (Actor 🧑→🤖). Label: `TRIGGER · manual (MCP)`.
- **Watcher** — a scheduler / cron / webhook auto-ingests on its own (Actor 🤖; mark built or `❌ not built`). Label: `TRIGGER · watcher`.

Label rows `TRIGGER · <kind>` only when a process has more than one real source; a single-source process is just `TRIGGER`.

**The admin/debug web UI or HTTP server is NOT a trigger.** Internal launchers, debug consoles, and ops-only HTTP endpoints are how an admin pokes the system, not how the process really starts — fold them into a one-line caveat in a trigger's `Notes` ("the … UI is admin debugging only, not a user-facing trigger"), never a `TRIGGER` row. Same for an *intended-but-unbuilt* trigger (e.g. a planned watcher): keep it as a `TRIGGER` row marked `❌ not built` so the target is visible without claiming it exists.

### HITL / Edge Case table (optional, the only thing allowed below the main table)

`Case | Detail | Actor` — **only for genuine human-takeover exception branches** (a real decision/escalation fork), e.g. "complaint is egregious → Steve bypasses the draft and suspends the offer." NOT for descriptive notes or caveats. If there's no real branch, there's no table.

## The reconciliation workflow

1. **Snapshot first.** Before editing any page, fetch + save its current content to disk. ClickUp has no undo you can trust, and edits can duplicate (see gotchas).
2. **Extract the changes** from the source (meeting transcript, ledger, or the SOP itself). For a transcript, capture every stated correction per process.
3. **Reconcile against live reality — don't trust the SOP.** Verify each step in the actual mechanism: grep the code (`offline-event-form`, `premium`, `offline-mcp`), read the n8n workflow JSON (`projects/offline/n8n/daily_sync/workflows/`), check the Offline internal API client (`offline-event-form/lib/offline-api.ts`), or read Slack. Find the *correct current mechanism*, not just "the SOP step is broken."
4. **Fill LLM Access — grounded, never assumed** (see discipline below).
5. **Write content-only** (no `name` AND no `sub_title` in the same call — both are title-class and trigger the dedup gotcha; see gotchas), then **re-fetch and confirm a single table** (dedup check).
6. **Once QA is done, migrate to clean `Process step`.** During reconciliation the 2nd column may be `Original SOP text (verbatim)` (a scaffold to compare against). When the page is reconciled, rewrite it to `Process step` — clean current steps, stale text dropped. **Refactoring an existing SOP is preserve-then-prove:** carry over as much of the original as the house format allows and show how it's *evolving* — don't silently re-author from scratch. House-format compression is allowed, but it is only *safe* because step 7 proves nothing substantive was lost.
7. **Information-loss audit — the final gate, and it must be INDEPENDENT.** Before calling the port/refactor done, compare the NEW ClickUp page against the source of record: the original `.md` for a markdown port, or the **pre-edit snapshot** (step 1) for an existing-page refactor. **Whoever authored the new page does not audit it** — dispatch a fresh subagent (or a clearly separate pass), because silent drops are invisible to the person who made them (you can't audit your own authoring). The auditor enumerates every discrete substantive item in the source — each number, dollar amount, market code, status name, link/Loom, named tool/prompt, edge case, caveat, deliverable / definition-of-done, and open question — marks each PRESENT / ALTERED / ABSENT in the new page, and classifies every ALTERED/ABSENT as **INTENTIONAL** (structural/house-format: section headers, summary tables, reformatting, prose compression, stale-method collapse) or **UNINTENTIONAL** (a substantive detail simply gone that an operator would miss). **Loop every UNINTENTIONAL miss back in**, then re-verify. (Verify the subagent's claims against the source before acting — subagents over-synthesize.)

## LLM Access discipline + the access map

**A ✅ requires a confirmed agent-accessible credential** — not just that *some system* (e.g. n8n) integrates with the service. Verify a token/endpoint exists before marking ✅; otherwise it's ❌ with the gap named. A field can be ✅ on read but ❌ on write — state which.

The live credential/access map is canonical in **`.claude/skills/api-credentials.md`** and **`projects/offline/internal/CLAUDE.md`** — read those, don't trust this summary. As of 2026-06:

- **Offline internal API** (`premium` Rails, `X-API-Key`=`RAILS_API_KEY`, `/api/internal/*`): offers GET + PATCH (no create); `offers/:id/assignments`; `partner_reports/:id/recent_redemptions` (returns `customer_rating`+`customer_feedback`); companies GET/POST/PATCH; accounts GET + `add_managed_offers`/`remove_managed_offers`/`create_partner`; events GET/POST/PATCH; areas; announcements; search. **NOT in the offer PATCH permit:** `fine_print_days`, `takeout_time_restrictions`/`classic_time_restrictions`, `important_notes`, `notes`, `show_in_app`, `cancel_partner_announcement`.
- **offline-mcp worker**: `gmail.modify` for `[REDACTED]` (read+write Steve's box); HubSpot, Slack, GitHub.
- **Creator MCP**: `creators.letsgetoffline.com/api/mcp/*`, `x-api-key`=`CREATOR_API_KEY`.
- **HubSpot**: CRM + Conversations (incl. Sakari SMS channel `[REDACTED]`) but **no `content` scope** → cannot read sales email templates.
- **n8n** holds creds an *agent* cannot reach directly: Intercom, Tremendous, "SL Email" (Steve's Gmail draft cred `[REDACTED]`), "DS's Gmail", "Page's Gmail".
- **No agent credential** for: Intercom, Tremendous, Ramp, Gusto, `partners@`, Sakari's own API.

Common verdicts: a manual partner email = `✅ draftable via Gmail`; a phone call = `❌ human`; a Partners-App UI click-through = `❌ UI workflow`; an existing n8n/skill automation = `✅ runs as n8n / skill` (note it's automation, not agent-portable).

## Gotchas (learned the hard way)

- **ClickUp markdown tables duplicate on a RENAME round-trip.** Triggered by a UI title/emoji edit OR by passing `name` **or `sub_title`** + content in the same `update_document_page` call (`sub_title` is title-class — verified 2026-06-18 it duplicates the table exactly like `name`, and the dup can surface on a *later* fetch even when the immediate re-fetch looked clean). Set a title/subtitle alone, never alongside content. **Collapsing a table that already duplicated:** a direct content-only re-send is NOT reliable — it can collapse on the immediate read then re-duplicate async minutes later (the replace lands on a page that still holds the stale table block). Use a **two-phase collapse** (verified 2026-06-18): (1) write table-free placeholder content (e.g. `_rebuilding…_`) and confirm **0** table headers — this clears the table blocks; (2) write the real single-table content once. This reproduces the clean create-from-empty path, which stays stable. **Always re-fetch to confirm one table — and re-check a few minutes later, since the dup can lag.** Don't hand-edit these pages in the ClickUp editor — have the agent do it via API.
- **The API can't move (reparent) or archive doc pages** — only create/update/read content. Reparenting and archiving are manual sidebar drags; the agent can wipe/create content and recreate-under-a-new-parent, but can't move or archive.
- **Strip means strip.** A stale method folds into one clean step (or is dropped once QA's done), never kept as a parallel "superseded" table.
- **Don't promote unconfirmed old-SOP steps to live steps** — a live step must be confirmed by the transcript or observed reality.
- **Match an automation to a process by its recipient/behavior, not its name** — open the node and check who/what it acts on (a "Partner ... Flow" may be member-facing).
- **Source of truth = the `premium` backend, not HubSpot.** HubSpot is downstream sync (only the designated "Offline Backend Data Sync" deal fields flow back). Never frame HubSpot as a trigger or authority; treat "change a HubSpot field → X happens" SOP framing as suspect.

## Canonical-container model (merge / reconcile target)

A process family gets **one canonical container page** (e.g. `1-Off Partner Processes`) whose body is a short intro; each process is a **sub-page** under it. When merging cleaned pages with legacy ones: migrate everything as sub-pages under the canonical container, and **archive the redundant legacy duplicates** so nothing lives in two places. Pick the canonical page to be the one with existing backlinks (wipe its body, attach the sub-pages) so links survive. Knowledge pages that are *more than* a process (training/FAQ/objection scripts) are kept, not archived — strip only the process parts now captured elsewhere.

## What this skill is NOT

- Not `process-mapping` / `shaner-consulting` (those *discover/design* a process).
- Not `programming-l10` (files L10 issues) or `add-clickup-ticket` (files dev bugs) — but surface candidates for both as you reconcile, for the user to file.
