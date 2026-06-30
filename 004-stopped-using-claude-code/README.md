# Episode 4 — We Stopped Using Claude Code Mid-Build. Here's What We Built Instead

**Released:** June 17, 2026 · **Runtime:** 41:36

📝 **Full show notes:** [Read on tweenertimes.com](https://www.tweenertimes.com/p/redacted-episode-4-we-stopped-using)
🎧 **Listen:** [Apple](https://podcasts.apple.com/us/podcast/redacted-episode-4-we-stopped-using-claude-code-mid/id1774076494?i=1000773076948) · [Spotify](https://open.spotify.com/show/1aMrtX8LnIU2w5yoT4uolb) · [YouTube](https://www.youtube.com/watch?v=flnJJIhY_gk)

A double build session. Taylor Cotner walks through the multi-agent HubSpot cleanup pipeline he's been iterating on for weeks — now running on the **Anthropic SDK** with Claude Code out of the orchestration loop — and David Shaner demos rebuilding Offline's partner landing page from scratch with **Claude Design** and **Claude Code**. Most of the episode is screen sharing, so it's best viewed on YouTube.

## What we cover

- **No Claude Code in the loop** — Taylor stopped using Claude Code as the *orchestrator* in his HubSpot pipeline (he still builds the app with it). Removing it as a mid-workflow decision-maker gave him full control over inputs and outputs at every step.
- **Custom eval system built from scratch** — an Excel-grid eval page: models as columns, test cases as rows, each cell showing pass/fail and cost. Used to measure Haiku, Sonnet, GPT-5, and GPT-5 Mini against real messy HubSpot data.
- **GPT-5 Mini at 10–20× less cost** — lead qualifier evals: $1.00/run on Sonnet vs. $0.05 on GPT-5 Mini. Core cleanup evals: $1.50 vs. $0.14.
- **$20 for 133M tokens overnight** — using the **Vercel AI Gateway** (swap any model without changing code), Taylor ran 200 HubSpot restaurant cleanups in one night for $20 total.
- **Self-grading pipeline** — the pipeline grades its own output after each run; anything below an A auto-spawns a Sonnet rerun with no human catch. A B on 101 Craft Kitchen auto-escalated and came back an A.
- **Real mess-ups make the best evals** — nearly every eval case came from a real HubSpot error (e.g. the system once invented a "Kim company" to link unrelated restaurants — linked by an owner contact ≠ linked by company structure).
- **The conveyor belt metaphor** — David's landing-page pipeline starts with live sales transcripts from Steve and aims to end with a generated, voice-of-customer partner page. "In an ideal world, I've got a black box in the middle."
- **Claude Design → Claude Code handoff** — Claude Design's share feature generates a markdown handoff doc (file map, token contract, panel build notes) that Claude Code reads first, bridging design intent to implementation.
- **One person, 7–8 hats replaced** — David processed reviews, tightened positioning, built wireframes, designed the mobile experience, wrote code, and shipped a PR — no designer, copywriter, or front-end dev.
- **GPT-5 "overthinks"** — working theory: full GPT-5 goes too abstract on structured cleanup tasks, which may be why Mini outperforms it.
- **The iceberg** — once cleanup and the landing page are done, the plan surfaces above the water: automated emails, Instagram DMs, and a fully AI-run lead-gen function on top of the clean data.

> **Didn't see what was shown on-air?** We don't always post everything — some of it stays redacted. **[Request a file →](mailto:contact@tweenerfund.com?subject=%5BREDACTED%5D%20Ep%204%20file%20request)**
