# Research Lanes

Four independent lanes. If subagents are available, run one per lane in parallel and reconcile after; each lane should reach its own conclusions before seeing the others, that independence is what makes the later contradiction-check meaningful. If you are already inside a subagent and cannot fan out further, work the lanes yourself in order but keep them separate in your notes.

For every claim a lane produces, record a **source** and a **confidence** (Verified / Inferred / Unknown). A lane that finds nothing should say "nothing found" for its area, not pad.

---

## Lane A - Company

**Goal:** what the business actually does, how it makes money, how big it is, where it operates, and anything topical that signals their state of mind.

**Tools:**
- `WebSearch` for: the company name, `"<company>" reviews`, `"<company>" owner OR founder`, `<company> services`, recent news, `<company> careers OR jobs` (job posts reveal tools, pain, and growth).
- `WebFetch` on their **own website** (About, Services, Team, Contact), Google Business / reviews, and any press. The site's own words are the most reliable source for services and self-description; quote them.
- The `web-browser` skill when a page is JS-heavy, gated, or you need to see it rendered (maps, review sites, directories).

**Look for:** business model (transactional vs recurring vs retainer; who pays and for what), service lines, team size (cross-check directory claims against the website and LinkedIn, directories routinely overstate), locations/territory, years in business, recent changes (new office, hiring, acquisition, award), and visible weaknesses (one-page site, `noindex`, no online booking, stale blog). Those weaknesses are often opportunity hooks.

**Gotcha:** marketing copy and lead-gen directories exaggerate size and scope. Treat any headcount/revenue number as Inferred until a second source agrees. If the company is small/private, expect sparse data, that is normal, not a failure.

---

## Lane B - Person

**Goal:** who Ben is actually talking to, their role and authority, background, tenure, and a couple of *genuine* rapport-building details.

**LinkedIn (primary source for a person):** LinkedIn blocks anonymous scraping, so the path is **interactive, through a browser Ben is already signed into**:
- Use the `web-browser` skill to open the person's LinkedIn profile (and the company page). Because the session runs in Ben's signed-in browser, you can read the rendered profile: headline, current + past roles, tenure, education, location, posts/activity, and "about."
- **If an interactive logged-in browser is not available** (e.g. you are running autonomously / Ben is away), do **not** fake it. Fall back to public web search for the person (`"<name>" "<company>"`, `"<name>" linkedin`, news, bios, podcast/webinar appearances, association listings) and clearly mark LinkedIn-derived facts as Unknown/Inferred. Note in the dossier that a live LinkedIn pass is still open.

**Also pull:** company "meet the team" bios, conference/webinar/podcast appearances, professional association or licensing listings, local news, published articles. These are public and reliable.

**Fun facts:** only include ones that are (a) true and sourced and (b) usable to build rapport without being creepy, a niche specialty, a notable career arc, a community/board role, an award, a shared interest, the origin of the business. No private-life details, no guessing. A great fun fact gives Ben a warm, specific opener. If you don't have one, leave it out.

**Read on state of mind:** infer (and label as Inferred) what's likely on their plate, owner-operator stretched thin, recently grew and drowning in ops, compliance-spooked, burned by a prior tool. This shapes how Ben runs the call.

---

## Lane C - Internal / prior touches (CRM + history)

**Goal:** where they sit in Levitate's world already, so Ben doesn't walk in cold or repeat himself.

**HubSpot** (`Marketing 3P Insights` / HubSpot MCP):
- `hubspot_search` / `search_crm_objects` / `get_crm_objects` / `hubspot_get_object` to find the **contact, company, and deal**. Search by **company name or contact email**, not by owner.
- Pull: lifecycle/deal stage, deal owner, amount (note: AI Solutions deal amounts are nominal placeholders, not real value), source, associated contacts, recent activity, form submissions.
- **Gotchas (from project memory):** there is **no AI Solutions pipeline or tag**, and **deal owner is not a reliable filter**. Don't conclude "not a customer" from a missing record, search a couple of ways before giving up.

**Levitate CRM** (`Levitate` MCP): `contacts_search` -> `contacts_get_profile` -> `contacts_get_timeline`, and `companies_search`. Returns internally-captured profile, tags, and interaction timeline. Only contains what's been logged in Levitate.

**Prior meeting notes:** if Ben has met them, notes are in `02_areas/meetings/granola/` and `02_areas/meetings/google-recorder/`, and the client folder may link them. Read for pains already voiced, objections, pricing discussed, and next steps, those are gold and must not be contradicted.

**Gmail** (`gmail` skill / `gmail-cli`): search `from:<name>@<domain>` or the domain for prior threads. Empty for a true cold prospect, that's fine.

**Output the CRM-context block:** deal stage, deal owner, source/how-they-came-in, prior touches, any voiced pains or objections, and buying signals. If a folder/README already exists, treat it as the baseline of truth.

---

## Lane D - Vertical and pain patterns

**Goal:** load the proven, repeatable pains and Levitate-buildable opportunities for this prospect's vertical so the recommendations stand on evidence, not improvisation.

**Primary source:** read the living **Pain-Point Atlas** at `01_projects/ai-solutions-consulting/pain-points-atlas.md`. It is organized by pain point, each tagged with the industries and companies that flagged it and the concrete AI opportunity that solves it. Find this prospect's vertical in **Appendix A (Industry index)** to get its top pains, then read those pain sections for the opportunity language and the peer companies (useful social proof: "we built exactly this for another agency").

**Secondary source:** `references/vertical-playbooks.md` distills the atlas into per-vertical incumbent tech stacks, typical manual workflows, and the opportunities that recur. Use it to seed Lane A/B's "what tools do they probably run" and Step 3's opportunity ideation.

**Incumbent tech stack:** name the systems this vertical typically runs (e.g. insurance: EZLynx / AMS360 / Applied Epic / HawkSoft / QQCatalyst; legal: Clio / MyCase / Gavel.io; CPA: CCH Axcess / TaxDome / QuickBooks Online; advisory: Redtail / Wealthbox / Albridge / Income Lab; nonprofit: DonorPerfect / Bloomerang / Raiser's Edge / CampMinder). Mark each as Verified (they said it / it's on their site) or Inferred (typical for the vertical). For each, note the integration angle (native, Zapier, CSV, API/MCP, or "validate on the call").

---

## Reconciliation note

After the lanes report, before drafting: list every place two sources disagree and resolve each into a stated correction. The most common conflicts: company size (directory vs reality), vertical/business-model (outreach-template boilerplate vs what they actually do), and which person Ben is meeting. Getting these wrong on a live call is expensive, so they earn an explicit "correction" callout in the dossier.
