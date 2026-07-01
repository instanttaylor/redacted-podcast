# Vertical Playbooks

Distilled from the AI Solutions Pain-Point Atlas (`01_projects/ai-solutions-consulting/pain-points-atlas.md`). Use this to seed two things: (1) the **incumbent tech stack** a prospect probably runs, and (2) the **proven, repeatable opportunities** for their vertical, so recommendations stand on real evidence and you can cite peer firms as social proof. Always defer to the live atlas when it's richer or newer than this summary.

How to use a playbook: load it before/while researching a prospect in that vertical. Use the stack list to know what to look for and to populate the "incumbent stack" block. Use the proven opportunities as your starting candidate set in Step 3, then tailor to what *this* prospect actually voiced. The peer companies named are real AI Solutions prospects/clients, use them as "we've built this for other [vertical] firms" social proof, but never overstate the relationship.

Cross-vertical truths worth leading with:
- **Owner / key-person bottleneck** (8 firms, every vertical): the owner or a tiny team is the single point all non-revenue admin passes through. Frame AI as a cheaper-than-headcount backfill that returns hours to billable/relationship work.
- **Daily "who do I contact today" briefing** (9 firms): a morning brief pulling the CRM list + pre-loaded context + light web research. Near-universal; almost always a fast win.
- **Manual data re-entry across disconnected systems** (9 firms): pull source record once, auto-populate destination forms/portals, draft for human review.
- **Missed follow-ups / no keep-in-touch cadence** (8 firms): Levitate Keep In Touch with per-contact scoring and overdue flags. The native Levitate fast win.

---

## Insurance (independent agencies)

**Incumbent stack:** EZLynx, Applied Epic, AMS360, HawkSoft, QQCatalyst, AgencyBloc (AMS); carrier portals + ACORD forms; multi-rater/comparative raters; Sunfire (Medicare); Outlook/Teams. Often a "no real CRM" gap for the book of business.

**How they run today (typical):** re-keying the same client data into 10+ carrier portals + ACORD forms (~2 hrs/day at some shops); remarketing/re-quoting cancellations and renewals by shopping each client to 4-5 carriers (35-40% of team time); manual commission reconciliation across agency + agent portals for many carriers; combing 20-50 page medical/loss records by hand; no shared work calendar.

**Proven opportunities:**
- **Re-quote / remarketing engine** (Perryton, Stassen, Tri-State, MBW): pull the cancellation/renewal list from the AMS, run it through the rater/per-carrier submission, output a per-client comparison sorted by renewal date + a "who to call today" list with a drafted re-engagement email. Carrier-portal re-verification stays human where APIs are gated. *This is usually the hero build for insurance.*
- **Form-fill / ACORD automation** (Tri-State, MBW, Stassen): pull the source record once, auto-populate carrier applications/ACORD, human reviews before submit.
- **Commission reconciliation** (Lordes, Perryton): ingest agency-side + agent-side carrier commission statements, reconcile line by line, flag discrepancies, with strict anti-hallucination on dollar amounts.
- **Daily policy-context briefing** (Lordes, Perryton, Stassen): morning email/desktop brief pulling each customer's policy context so staff aren't clicking around EZLynx.
- **Compliance gating** (Lordes, MBW): the highest-value task (medical records) is often the one they *can't* touch in consumer AI, stand up a compliant environment (BAA/HIPAA) to unlock it.

---

## Legal (small firms / litigation)

**Incumbent stack:** Clio, MyCase, Gavel.io / Clio Draft (court-form assembly); Word; intake forms (often Zapier from ads); e-filing portals.

**How they run today (typical):** staff hand-pull case data from the practice-management system and hand-type it into court-form tools; each pleading needs a bespoke multi-page declaration authored from scratch; incoming email is the de-facto task list; deep procedural know-how (e.g. computing response-due dates) lives in one or two long-tenured staff.

**Proven opportunities:**
- **Court-form / data re-entry automation** (Gentry Law): pull every case data point from MyCase once, auto-populate Clio Draft/Gavel court forms, human review.
- **Document drafting from source material** (Gentry Law): wire Claude to case records + templates to draft the bespoke declaration/pleading in the firm's format, turning from-scratch authoring into review-and-approve. *Often the hero build.*
- **Email -> tracked tasks with deadlines** (Gentry Law): triage the inbox, turn mail into assigned tasks with surfaced deadlines so nothing is missed.
- **Intake capture + conflict check** (Gentry Law): parse each lead/intake form, dedupe, create a structured record, run a conflict/vetting pre-check, draft the engagement letter + request-for-info, file an attorney-review task.
- **Onboarding / knowledge capture**: record procedural know-how into a queryable internal wiki to de-risk key-person dependence.

---

## Accounting / CPA / bookkeeping

**Incumbent stack:** CCH Axcess, TaxDome, MyTaxPrep Office, Sigma Tax Pro, Drake; QuickBooks Online; client questionnaires (Excel/Word); document portals.

**How they run today (typical):** keying questionnaire answers field-by-field into tax software, re-entering firm e-filing IDs 100+ times/season; reconciling bank statements vs QBO by hand; chasing clients for missing docs across a 4-tier escalation (chat -> email -> text -> phone), 40-100 hrs/season; opening/renaming files clients upload "willy nilly"; tracking time in Excel and building each QBO invoice one by one.

**Proven opportunities:**
- **Bank-vs-QBO reconciliation / discrepancy detection** (Jackson): ingest bank-statement PDFs vs the QBO ledger, reconcile line by line, flag duplicate checks / wrong vendor / mis-posted payments, strict anti-hallucination on amounts. *The single clearest quick win in the whole dataset; usually the hero for CPAs.*
- **Document-chasing "nag" agent** (Freedom Financial, M&N, Cameron Rose): tag a client once, AI runs a calibrated escalating cadence until the item arrives, with a status dashboard.
- **Document parsing + auto-file/rename** (Freedom Financial, Jackson): read uploads, extract the data points, auto-rename and file, push structured fields into the system of record.
- **Data re-entry into tax software** (M&N): auto-populate from the questionnaire/source doc, human review.
- **Time-logging -> QBO invoice drafting** (M&N, Lipkin): conversational time logger that appends to a timesheet, then drafts QBO invoices for review. (Logging alone has no value without pushing to QBO, build the whole loop.)

---

## Financial advisory / wealth management

**Incumbent stack:** Redtail, Wealthbox (CRM); Albridge, Income Lab (planning/performance); Schwab/custodian portals; DocuSign; Catchlight, LinkedIn Sales Navigator, county property records (prospecting); FMG (marketing). Often a fragmented stack with no single sign-on.

**How they run today (typical):** retyping demographic data into 3+ systems and ~100-page DocuSign account forms; tracking annuity anniversaries by logging into 14 carrier portals; manual quarterly performance-report runs per client; monthly review-letter mailers from Word templates; binary done/not-done task tracking with no progress visibility; inbox torched with wholesaler spam (1,500+ unread).

**Proven opportunities:**
- **Action-item / open-loop tracking with "paranoid mode"** (Context Financial, Cameron Rose, FP-NM, Old Raleigh): connect email + calendar + CRM, track each open request beginning-to-end, flag commitments going stale. (A buried, missed action item cost one firm a client ~$30K, the stakes story sells this.)
- **Keep-in-touch / auto-drip** (Old Raleigh, Cameron Rose, Long Road): Levitate KIT with per-contact scoring and overdue flags; the native fast win.
- **Anniversary / date-trigger consolidation** (Cameron Rose, Long Road): read policy/registration history, consolidate date triggers into the calendar/CRM, auto-fire the right touch.
- **Form / data re-entry automation** (Cameron Rose, Context, Long Road): one-source-of-truth auto-fill into account paperwork.
- **Recurring report generation** (Cameron Rose, Old Raleigh): pull from Albridge/CRM and auto-generate the quarterly/performance report for review. *Often the hero.*
- **Compliance gating** (Old Raleigh): SEC/broker-dealer rules flag "AI"/"Claude" and bar account numbers/PII from general LLMs, a compliant environment unlocks the real work.

---

## Nonprofit (development / fundraising)

**Incumbent stack:** DonorPerfect, Bloomerang, Raiser's Edge (donor CRM); CampMinder (camps); Constant Contact (email); spreadsheets, or no CRM at all.

**How they run today (typical):** tiered donor touchpoints (postcards, emails, calls, handwritten notes) executed "when I think of it"; manual wealth-screening on Zillow/Redfin for the top ~50 prospects while thousands go unmined; qualitative donor notes never recorded for lack of bandwidth; disconnected systems (child-keyed registrations vs parent-keyed fundraising) hand-synced.

**Proven opportunities:**
- **Daily capacity-ranked "donors to call today"** (Camp Tawonga, BBBS, Guaptry): morning brief with donor context + LinkedIn/property signals pre-loaded, contact higher-capacity donors first.
- **Keep-in-touch cadence / stewardship at scale** (BBBS, Guaptry, Walter Anderson): 5-7 structured touches per donor per year on a reliable cadence, in the ED's authentic voice.
- **Bulk wealth / capacity enrichment** (Camp Tawonga, Walter Anderson): ingest names+addresses, return home-value bands + LinkedIn + trust signals, tag and rank the whole database so overlooked high-capacity prospects surface.
- **CRM that maintains itself** (BBBS, Guaptry, Walter Anderson): inbox/document-scanning agent that auto-creates and updates donor records and tags, or stand Levitate up as the system of record where none exists.
- **Cross-system record matching** (Camp Tawonga): fuzzy relationship logic mapping child records to parent constituents, ambiguous matches flagged for review.

---

## Executive search / recruiting

**Incumbent stack:** often spreadsheets + a thin/absent CRM (Levitate as first CRM); calendars; Word/Google Docs for client-facing docs; meeting recorders.

**How they run today (typical):** hand-building client-facing calibration docs from each recorded meeting (1.5-2 hrs per set) plus 15-40+ scored candidate write-ups/week; booking candidate meetings onto senior calendars 10-20x/day; weekly client update consolidated by hand; a tiny BD team that can't maintain relationships at scale; AI output that breaks native Word formatting and forces reformatting.

**Proven opportunities:**
- **Calibration-doc + candidate write-up autopilot** (Nautical): wire Claude to the recorded-meeting transcript + scoring, auto-draft the client-facing doc in native format. *The hero, and the source of the "AI output must preserve native formatting" lesson, use pre-built templates that Claude fills content-only.*
- **Proactive scheduling agent** (Nautical): take a candidate's availability, read the senior calendar, book the slot automatically; pair with a shared team calendar feeding the daily brief.
- **Keep-in-touch to amplify a 2-person BD team** (Nautical): automated relationship maintenance at scale.
- **Weekly client report generation** (Nautical): auto-consolidate outreach metrics into the recurring client update.
- **Daily meeting-prep briefs** (Nautical): 7am attendee-research briefs, optionally DISC-aware.

---

## Other / outside the core six (e.g. home services, trades)

No atlas playbook, so research harder from the company's own site and lean on the cross-vertical truths. The Dan Eastham dossier (termite/WDO inspection) is the worked example: even with no vertical playbook, the wins were (1) Levitate keep-in-touch to the referral sources that feed the business, (2) automated review requests, (3) instant lead-intake confirmation, and (4) a marquee custom build (AI-drafted compliant inspection reports from field notes). The pattern holds: a couple of fast Levitate-native relationship wins + one genuine custom AI build on their biggest manual time-sink.
