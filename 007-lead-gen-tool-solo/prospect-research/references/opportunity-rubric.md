# Opportunity Rubric

The opportunities are the payload of the dossier, they're what lets Ben advise live instead of just listening. The goal is **3-5 grounded, Levitate-buildable opportunities plus 1-2 bold flagged ideas**, each genuinely useful and none invented. Quality here comes from ideating widely and then verifying hard.

## Step 1 - Ideate widely (diverge)

Generate 6-10 candidate opportunities from three angles, so you're not just pattern-matching one:
1. **Their voiced pains** (from prior meeting notes / CRM / what they say on their own site, e.g. a one-page `noindex` site, no online booking). Strongest evidence.
2. **The vertical's proven pains** (atlas + `vertical-playbooks.md`). What firms exactly like them repeatedly flag.
3. **The owner-bottleneck lens**: what non-revenue admin is this specific person clearly doing themselves that a backfill could absorb? What would they hand a cloned version of themselves first?

If you have subagents, it's worth having one ideate from the "bold / outside-the-box" angle independently, divergent thinking benefits from not being anchored on the safe list.

## Step 2 - Verify hard (converge)

Run every candidate through this rubric. A separate verification perspective (subagent if available) should try to *kill* each one. To survive as a **core** opportunity it must pass all four:

1. **Real pain.** Is there evidence they actually feel this, voiced it, it's strongly typical for their vertical, or a signal on their site/footprint shows it? If you're assuming the pain with no evidence, it's not core (it might be bold).
2. **ROI-positive.** Plausibly saves more (time/money/risk) than the build + subscription costs. You must be able to state a rough number (see ROI below). If you can't size it at all, you don't understand it well enough to pitch it.
3. **Levitate-buildable.** There is a real mechanism: a Levitate native feature (Keep In Touch, automations, campaigns), Claude + a confirmed MCP/API, Zapier, CSV import/export, or a Cowork/script build. **Name the mechanism.** If no real path exists, it's bold/speculative, not core, and must be flagged.
4. **Not generic.** It's specific to *their* workflow, not "use AI to save time." Test: would this exact bullet appear on a competitor's pitch to any firm? If yes, sharpen it until it's unmistakably about them.

Anything that fails #1 or #2 gets cut. Anything that fails #3 or #4 either gets sharpened or moves to "bold."

## Step 3 - Split core vs bold

- **Core (3-5):** pass all four. These are what Ben confidently pitches.
- **Bold (1-2):** genuinely interesting, clearly labeled as speculative. A bold idea may fail #1 (pain unvalidated, "if this is true for you, here's a wild one") or #3 (no confirmed integration path yet, "this would need us to validate X"). Bold ideas show range and provoke good discovery, but Ben must know they're not yet de-risked, so the dossier flags them explicitly. Never let a bold idea masquerade as a sure thing.

## Step 4 - Pick the hero and the fast wins

- **Hero / marquee build (mark exactly one):** the highest combination of pain intensity x buildability x stickiness. Usually a genuine custom AI build on their single biggest manual time-sink (re-quote engine, bank-vs-QBO reconciliation, court-form/declaration drafting, calibration-doc autopilot), not just outreach. This is what makes the engagement feel custom and hard to rip out.
- **Fast wins:** pair the hero with 1-2 lighter **Levitate-native** wins (Keep In Touch, automated review requests, daily briefing) that prove value quickly and are easy to say yes to. The classic shape is "a couple of fast relationship wins + one marquee custom build."

Rank the opportunities so Ben can see the order to raise them in.

## ROI estimation

Ben asked for a rough ROI/time-saved per opportunity so each lands as a business case, not a feature. Keep it honest and clearly an estimate:
- **Anchor on atlas signals** where they fit: meeting prep ~15-20 min/person; insurance data entry ~2 hrs/day (~200 hrs/month at some shops); CPA document-chasing ~40-100 hrs/season; quarterly report runs "a busy week every quarter"; remarketing 35-40% of team time.
- **Convert to a unit Ben can say out loud:** hours/week reclaimed, or $/year at a rough loaded labor rate (state the rate you assumed, e.g. "~$30-50/hr loaded"). Or frame against the alternative they're weighing ("cheaper than the ~$20/hr admin you're considering").
- **Always label the assumption and the confidence.** "Est. ~6-8 hrs/week if remarketing volume matches the vertical norm, confirm volume on the call" is perfect. A false-precise "saves $43,200/yr" is not.
- When you can't size it, say "size unknown, the discovery question below is how we'd size it." That's a feature, it gives Ben a reason to ask.

## Anti-hallucination guardrails (opportunities)

- Never claim an integration **exists** if it's unconfirmed. "Native EZLynx integration" only if verified; otherwise "would connect via [path], to validate."
- Never cite a peer firm we "helped" unless it's actually in the atlas, and don't overstate the relationship.
- Never promise a specific outcome percentage as fact. Improvements are estimates.
- If the prospect operates in a regulated space (PHI, tax/financial PII, SEC/broker-dealer), surface the **compliance gate** as part of the relevant opportunity, the highest-value task is often the one they currently can't touch, and a compliant environment is the unlock.

## What each opportunity needs in the dossier

For every opportunity (core and bold): a crisp **name**, the **manual pain** it removes (one line, in their terms), **why Levitate can build it** (the mechanism, only if real), a **rough ROI / time-saved** (estimate + assumption), and a **discovery question** that validates and sizes it on the call. Bold ones additionally carry a visible "bold" flag.
