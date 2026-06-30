# Episode 5 — The Rage Log: AI-Powered Lead Gen, a Living Landing Page, and the Trick That Stops Claude From Making the Same Mistake Twice

**Released:** July 1, 2026 · **Runtime:** _TBD_

📝 **Full show notes:** [Read on tweenertimes.com](_TBD_)
🎧 **Listen:** [Apple](_TBD_) · [Spotify](https://open.spotify.com/show/1aMrtX8LnIU2w5yoT4uolb) · [YouTube](_TBD_)

Episode 5 goes deep inside Offline. Same format as always: each host shows what they've actually been building this week, then Taylor closes with the story of turning a 36-hour AI rage spiral into something genuinely useful. Candid, specific, and honest about what's still not working.

## What we cover

- **The outreach brief** — before any LLM writes an email, Taylor's system assembles a per-account context doc: connected contacts, communication history, open support tickets, similar partners, and the reason for reaching out. That brief becomes the input to the writing step, making outreach context-aware instead of generic.
- **B2B Hinge** — the lead graph is tiered: green (existing Offline partners), yellow (warm, one or two degrees away), blue (cold, in-market). "A B2B version of Hinge," because nearly every target account is only one or two introductions away.
- **2,000 locations geocoded in ~1 hour** — Claude wrote a script hitting the Google Places API to add lat/long to every restaurant location in HubSpot. ~10 errors fixed by hand; weeks of work compressed into about an hour.
- **Replacing LLMs with code** — Taylor is intentionally swapping prompt-based workflows for deterministic code. For market geography he replaced LLM prompts with lat/long/radius fields: more reliable, easier to audit, simpler to update without touching prompts.
- **The human–AI conveyor belt** — Steve trailblazes the sales process, Taylor automates it, Steve surfaces edge cases one lead at a time. Concrete examples beat broad observations for improving the system.
- **The rage log and gotcha registry** — Taylor had Claude review every conversation where he got frustrated, identify recurring mistakes, and compile a "rage log," then refined it into a "gotcha registry" of known failure patterns to consult before new work begins.
- **Hooks as memory engineering** — rather than relying on claude.md or built-in memory, Taylor uses Claude Code hooks to auto-inject the gotcha registry into every planning step, so each implementation plan is checked against past failures before any code is written.
- **The Slack bot PM experiment** — David built a Claude agent that ran the final landing-page asset collection by pinging teammates in Slack and checking for updates every 15 minutes via the loop command. Autonomous agents work better with a clear manifest of exactly what to check and what to do.
- **AI photo tagging at scale** — David used a cheap AI model to tag 2,000–3,000 Google Drive images with marketing metadata (individuals, couples, groups, food, events, hospitality staff, bartenders), so Claude can retrieve images by category instead of manual browsing.
- **The trust argument for context-aware outreach** — as AI-generated outreach gets more common, emails that demonstrate genuine knowledge of an account become more valuable. AI lowers the cost of gathering context, making personalized, context-rich outreach a stronger competitive advantage.

> **Didn't see what was shown on-air?** We don't always post everything — some of it stays redacted. **[Request a file →](mailto:contact@tweenerfund.com?subject=%5BREDACTED%5D%20Ep%205%20file%20request)**
