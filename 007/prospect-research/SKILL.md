---
name: prospect-research
description: >-
  Research a prospect BEFORE a Levitate AI Solutions demo or discovery call and produce a single
  self-contained HTML dossier Ben can study to prep AND glance at live during the call. Use this
  WHENEVER Ben is about to meet, demo, or discover with a prospect/company and wants background,
  e.g. "research [person] at [company] before my demo", "I'm meeting [company] tomorrow, prep me",
  "build a prospect one-pager / dossier / brief for [X]", "who am I talking to at [company] and
  where could AI help them", "dig into [prospect] before our call", "what should I know before I
  talk to [name]". Trigger even when Ben names only a person, a company, a LinkedIn URL, or a
  HubSpot deal and not the word "research" but clearly wants pre-call intel on an external prospect
  (e.g. "got a call with the owner of [agency] at 2, give me something to work from"). It mines
  LinkedIn (via a browser Ben is signed into), the company's web presence, HubSpot + Levitate CRM,
  prior meeting notes, and the AI Solutions Pain-Point Atlas, runs an agent team that researches
  independently and adversarially fact-checks itself, and proposes 3-5 Levitate-buildable AI
  automation opportunities (plus 1-2 bold flagged ideas) with ROI estimates and discovery questions. It preps a single prospect, or your whole day of calls combined into one scrollable "Day Ahead" page.
  Do NOT use for: processing a meeting AFTER it happened (use post-meeting), looking up an internal
  Levitate employee (use who-is-lookup), a deal-credit dispute (use deal-credit), or a generic
  topic research report with no specific prospect/demo (use deep-research).
---

# Prospect Research — pre-demo AI Solutions dossier

Ben sells **Levitate AI Solutions**: custom AI builds that automate the manual, tedious back-office work of small professional-services firms (insurance agencies, law firms, CPAs/bookkeepers, financial advisors, nonprofits, exec-search shops). Before a demo or discovery call he wants to walk in already understanding the prospect's business, their likely state of mind, where their hours actually go, and where AI could earn its keep, so he can advise them live instead of asking blind.

This skill produces **one self-contained HTML dossier per prospect** that does two jobs at once:

1. **Live cheat-sheet** he glances at mid-call: logistics, flags, the top opportunities, and the best questions, all above the fold.
2. **Deeper brief** he reads beforehand: who they are, fun facts, business model and services, the tools they run today, how their work runs by hand, the full opportunity set with ROI, CRM context, and the question bank.

The single most important rule: **be accurate, never invent.** Ben reads this aloud-adjacent on a live call with a real prospect. A confidently wrong "fun fact" or a fabricated tool name is far worse than an honest "we don't know yet, ask them." When data is thin, say so and turn the gap into a question.

## Inputs (be flexible)

Minimum viable input is **a person's name + their company**. Also accept, in any combination:
- A **LinkedIn profile URL**
- A **company domain / website**
- A **HubSpot contact or deal URL** (or a name to search HubSpot for)
- **Only a company** (then identify the most likely person Ben is meeting from the CRM/meeting invite, and say who you assumed)

If the input is ambiguous (common name, multiple companies), state the assumption you are proceeding on and flag it as a thing to confirm. Do not stall asking for clarification you can resolve by looking.

## Output modes

Pick the shape by the ask:

- **Single dossier** (default for one prospect): one self-contained HTML file saved to that prospect's client folder, `01_projects/ai-solutions-consulting/clients/<slug>/<YYYY-MM-DD>-<slug>-prospect-research.html`.
- **Daily briefing** (default when Ben asks to prep a *day* or *several meetings*: "prep my day", "research today's calls", "who am I meeting today", "build my day-ahead"): ONE scrollable "Day Ahead" page combining every external prospect meeting that day. Ben wants to scroll through the day, not jump between files, so do not hand back separate files for a multi-meeting day.

### Building the daily briefing
1. Pull the day's calendar (Google Calendar `list_events`) and keep only the **external prospect** meetings. Skip internal Levitate meetings (1-1s, tiger teams, reviews, PPE, etc.). Note each meeting's time, attendees, and description.
2. Research each prospect with the full process below (Steps 0-4). Each prospect still gets its own dossier written to its client folder via `assets/template.html`, so the per-prospect file exists too. If you can spawn subagents, run one prospect per subagent in parallel.
3. Synthesize a **day header**: a masthead (title "The Day Ahead", the date, a 4-stat strip), a drop-cap "shape of the day" overview with a priority-ordered list of the rooms, and a **cross-room watch-outs** panel (timezone traps, schedule clashes, no-shows, "don't blur these two similar firms", existing-customer vs net-new). Reuse the template's classes. Skeleton below.
4. Run `scripts/combine_day.py <config.json>` to stitch the day header + each per-prospect dossier into one page with a sticky time-nav. Save to `01_projects/ai-solutions-consulting/daily-briefings/<YYYY-MM-DD>-day-ahead.html`. The config takes `out_path`, `template_path` (the assets/template.html), `page_title`, `page_description`, `topbar_label`, `day_header_html` (the filled skeleton), and `meetings: [{anchor:"m1", time_label, name_label, dossier_path}]` in time order.

Day-header skeleton (fill it, no em dashes):
```html
<header class="mast">
  <p class="kicker">Field briefing &middot; prepared {{DATE}}</p>
  <h1 class="title">The Day <em>Ahead</em></h1>
  <p class="subtitle">{{N}} external rooms today. Who's in each, where the hours go, and where AI fits.</p>
  <p class="dateline"><b>{{WEEKDAY, DATE}}</b> &middot; all times {{TZ}}</p>
  <div class="stats"><!-- 4 stats: rooms / net-new / returning / window --></div>
</header>
<p class="seclabel">The shape of the day</p>
<div class="note">
  <p class="lead"><span class="drop">{{X}}</span>{{cross-day overview: which room has momentum, which are listen-mode, the recurring opportunity shape}}</p>
  <div class="readcols">
    <div><p class="minilabel">Where your energy goes</p><ol class="priority-list"><!-- rooms in priority order --></ol></div>
    <div><p class="minilabel">True across the day</p><ul class="askfirst"><!-- 3 staple questions --></ul></div>
  </div>
</div>
<p class="seclabel">Read before you dial (the whole day)</p>
<div class="watch"><h3>Cross-room traps</h3><ul><!-- one li per cross-meeting trap --></ul></div>
```

## How the work is structured (the agent team)

The user specifically wants an **agent team that thinks independently, compares notes, and fact-checks itself** rather than one agent free-associating. Structure the work in three movements:

1. **Fan-out research** across four independent lanes. **If you can spawn subagents (you are the main agent), dispatch one subagent per lane in parallel** so each forms its view without anchoring on the others, then reconcile. If you cannot spawn subagents (you are already running inside one), work the lanes yourself, in order, but keep them mentally separate. Lane details, exact tools, and gotchas live in `references/research-lanes.md`.
2. **Synthesize + reconcile.** Merge the lanes into one picture. Where sources disagree (directory says "20 employees," the call says "two people"), surface it as an explicit **correction**, do not silently average. This is where the "size correction" / "vertical correction" style of flag comes from.
3. **Adversarial verification.** A distinct verification perspective (a separate subagent if available, otherwise a deliberate fresh pass) tries to *break* the draft: is this the right person and right company? Is each "fact" actually sourced? Is each opportunity a real pain, ROI-positive, and something Levitate AI Solutions can actually build, or is it generic AI hand-waving? Downgrade or cut anything that fails. This pattern is borrowed from the `deep-research` skill, see `references/opportunity-rubric.md` for the exact rubric.

Independent research, then reconciliation, then an adversarial pass is what keeps this honest. Skipping the verification movement is the main way these dossiers go wrong.

## Process

### Step 0 - Resolve identity and load what we already know
Before any web research, check what is already on hand, so you neither duplicate it nor contradict it:
- **Existing client/prospect folder**: look under `01_projects/ai-solutions-consulting/clients/<slug>/`. If a `README.md` exists, read it, it has the company, contacts, stage, deal owner, prior pain points, and meeting links.
- **HubSpot** (contact, company, deal) and **Levitate CRM** (contact profile + timeline). Exact tools and the "owner is not a reliable filter / no AI Solutions pipeline" gotchas are in `references/research-lanes.md`.
- **Prior meeting notes** (Granola / Google Recorder / Zoom) if Ben has talked to them before.
- **Gmail** threads if Ben has emailed them.

Decide the **slug** (kebab-case, e.g. `example-law-firm`, matching any existing folder) and the prospect's **vertical** early, the vertical drives the playbook in Step 3.

### Step 1 - Fan-out research (four lanes)
Run the four lanes from `references/research-lanes.md`:
- **Lane A - Company**: web presence, services, business model, size, locations, news, reviews, job posts.
- **Lane B - Person**: LinkedIn (via the browser Ben is signed into, see the interactive-login note), background, tenure, role, public footprint, genuine rapport-building fun facts.
- **Lane C - Internal / prior touches**: HubSpot + Levitate CRM + meeting notes + email, where they are in the funnel and what's been said.
- **Lane D - Vertical and pain patterns**: read the live **Pain-Point Atlas** at `01_projects/ai-solutions-consulting/pain-points-atlas.md` and `references/vertical-playbooks.md` to load the proven pains, incumbent tech stack, and AI opportunities that recur in this vertical.

### Step 2 - Synthesize
Build the picture: who they are, fun facts (only genuine, sourced ones), business model + services, the **incumbent tech stack** they likely run (with your integration angle for each), and **how it runs today** (the manual workflows, your read on where the hours go). Tag claims with confidence. Reconcile conflicts into explicit corrections.

### Step 3 - Generate AI opportunities (3-5, plus 1-2 bold)
This is the payload. Ideate widely, then verify hard, using `references/opportunity-rubric.md`. Each surviving opportunity needs: a crisp name, the manual pain it removes, **why Levitate can build it** (the integration/mechanism, only if a real path exists), a **rough ROI / time-saved estimate**, and a **discovery question** that validates whether it's real for them. Ground the core 3-5 in the atlas's proven patterns for their vertical; **flag 1-2 genuinely outside-the-box ideas as "bold"** so Ben knows which are speculative. Rank them, mark one as the **hero / marquee custom build**.

### Step 4 - Build the question set
Assemble discovery questions from `references/discovery-questions.md`: Ben's staples (walk me through your day; what CRM/back-office systems; have you used AI before), the tailored ones this prospect's situation calls for, and the one validating question per opportunity from Step 3. Put the 3 strongest at the top for live use.

### Step 5 - Render the HTML
Fill `assets/template.html` (do **not** rebuild markup from scratch, that is what the template is for). Keep the live cheat-sheet above the fold, the brief below. Map every section. Drop sections you genuinely have nothing for rather than padding them. Then, if polish is wanted, hand the file to the `frontend-design` skill (`/frontend-design:frontend-design`) for a visual pass, per Ben's global rule that HTML deliverables go through it.

### Step 6 - Save and report
Save to the prospect's folder: `01_projects/ai-solutions-consulting/clients/<slug>/<YYYY-MM-DD>-<slug>-prospect-research.html` (create the folder if it doesn't exist). Then give Ben, in chat: the file path, a 3-line spoken-style summary (who, where the hours go, the marquee build), and a short list of **open questions / low-confidence items** he should confirm on the call. Do not commit to git or send anything externally unless asked, this is his prep doc.

## Hard rules (Ben's conventions)
- **Never invent.** Unknown is a valid, useful answer that becomes a question. Mark confidence on every nontrivial claim: **Verified** (primary source or 2+ independent), **Inferred** (reasoned from indirect evidence, say so), **Unknown**.
- **Only name a tool or integration if a real path exists**: native Levitate integration, Zapier, CSV import/export, or a confirmed API/MCP. If unconfirmed, frame it as something to validate, don't promise it.
- **No em dashes**, including the `&mdash;` / `&ndash;` / literal `—` HTML entities. Use commas, hyphens, or `&middot;`. Direct, second-person, confident. Lead with the live state, not history.
- **Opportunities must be Levitate-buildable or clearly flagged as bold/speculative.** No generic "use AI for everything" filler.
- **The prospect is external.** For internal Levitate people, this is the wrong skill (use who-is-lookup).

## Reference files
- `references/research-lanes.md` - the four lanes, exact tools/MCPs/queries, the LinkedIn interactive-login path, and source gotchas.
- `references/vertical-playbooks.md` - per-vertical incumbent tech stack, typical manual workflows, and proven AI opportunities (distilled from the Pain-Point Atlas).
- `references/opportunity-rubric.md` - how to ideate, the adversarial verification rubric, the buildable-vs-bold split, and how to estimate ROI.
- `references/discovery-questions.md` - the question bank by category, plus how to generate a validating question per opportunity.
- `assets/template.html` - the single-prospect dossier scaffold (editorial field-briefing style). Fill it; don't rebuild it.
- `scripts/combine_day.py` - stitches multiple per-prospect dossiers into one scrollable "Day Ahead" page for daily-briefing mode (see Output modes).

Always prefer the live atlas at `01_projects/ai-solutions-consulting/pain-points-atlas.md` over the distilled playbook when they differ, the atlas is regenerated as new calls land.
