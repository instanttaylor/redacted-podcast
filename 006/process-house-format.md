# [Redacted] Podcast — Process Pages (house format)

_Rendered into the `clickup-process-reconciliation` house format (`Step | Process step | Actor | Notes | LLM Access`). Source: [`../process/post-recording-process-map.md`](../process/post-recording-process-map.md) + verified access in [`./ai-ification-context-map.md`](./ai-ification-context-map.md). Local markdown artifact — **not** pushed to ClickUp. `LLM Access` ✅ means a confirmed agent-accessible credential exists today; the Actor column reflects current reality._

---

## Process 1 — Record-week producer handoff

| Step | Process step | Actor | Notes | LLM Access |
|---|---|---|---|---|
| TRIGGER | A recording session ends — the episode is in the can | 🧑 | Every-other-week record cadence. Raw audio/video auto-lands in the cloud (StreamYard) for the producer — no manual file handoff | ❌ human event |
| 1 | Take live cut / redaction notes during the recording | 🧑 | Running cut-list + redaction flags (e.g. blur a moment if a partner's name/email is on screen). Becomes col G | ❌ human judgment, live |
| 2 | Update the episode tracking sheet, columns A–G only | 🧑 | Episode tracking sheet (ID `[redacted]`), a dedicated Google account. Set **A** episode# · **B** featuring · **C** recorded · **F** status→Done · **G** paste production notes. ✍️ writes: those cells on the episode row; never **D** featured-email / **E** drop-date, never past G | ✅ read+write via `workspace-mcp` (`read_sheet_values` / `modify_sheet_values`) — write not yet exercised |
| 3 | Slack-ping the producer that the episode is ready to edit | 🧑 | ✍️ writes: Slack message to the producer | ❌ no admin access to install a Slack app/connector |

---

## Process 2 — Publish-week show-notes staging

| Step | Process step | Actor | Notes | LLM Access |
|---|---|---|---|---|
| TRIGGER · manual (MCP) | Taylor invokes the staging process for the imminent episode | 🧑→🤖 | Steady state. Kicked off when he sees the ping or by cadence | ✅ human-invoked |
| TRIGGER · watcher | "Ready for review" ping auto-detected | 🤖→🧑 | Tweener Fund Slack, channel `[redacted]` ("scheduled, editable until Wed AM"). **❌ not built** — no Slack admin access to install an app/connector | ❌ no Slack admin access |
| 1 | Identify the imminent episode + its scheduled drop date | 🧑→🤖 | 📖 reads: tracking sheet **A** (episode#) + **E** (drop date); cross-check cadence | ✅ sheet read via `workspace-mcp` (dedicated account) |
| 2 | Retrieve the Substack post: title, description, public URL | 🤖 | 📖 reads: public post page (WebFetch). Pre-publish exposes title + subtitle + canonical slug; full "what we cover" body appears only at publish | ✅ WebFetch, no credential — *body* pre-publish ❌ (gated) → paste |
| 3 | Assemble the "files shared on-air" list | 🧑 | No canonical source: col G is cut/redaction notes, not a shared-files list; reconstructed from memory / ad-hoc assets drop; often none → use the "request a file" footer | ❌ no source to read (the future "during-show capture" gap) |
| 4 | Create/rename the `00N-slug/` folder + write the episode README | 🤖 | From title + drop date (Released) + description + "what we cover". ✍️ writes: new folder + `README.md`. Runtime / listen-links / show-notes-URL left `_TBD_` | ✅ local file ops |
| 5 | Add the episode row to the root README table | 🤖 | ✍️ writes: root `README.md`. Thumbnail `_TBD_` until the YouTube video is live; keep the stub-folder note correct | ✅ local file ops |
| 6 | Run `tools/redacted_feed.py` for any already-live links | 🤖 | 📖 reads: Transistor RSS + Apple lookup API + YouTube playlist RSS. For a not-yet-published episode it returns nothing → leave `_TBD_` | ✅ stdlib tool, public feeds |
| 7 | Commit to `main` (no PR) | 🤖 | ✍️ writes: git commit to `main`. The `_TBD_` markers ARE the pending list (`grep -r _TBD_`) | ✅ local git |

#### HITL / Edge cases

| Case | Detail | Actor |
|---|---|---|
| Files requested/forgotten after the fact | Something shown on-air wasn't posted → a separate **assets drop** is added to the folder later | 🧑 |
| Body needed before publish | The gated draft body isn't public yet → Taylor **pastes** the "what we cover" text | 🧑 |

---

## Process 3 — Go-live finalize (fill the `_TBD_`s once published)

| Step | Process step | Actor | Notes | LLM Access |
|---|---|---|---|---|
| TRIGGER · watcher | The episode publishes (Wed 10:30am ET) | 🤖→🧑 | **❌ not built** — no publish watcher; run manually at/after go-live | ❌ no watcher |
| TRIGGER · manual (MCP) | Taylor/agent runs the finalize pass after the episode is live | 🧑→🤖 | Steady state | ✅ human-invoked |
| 1 | Pull runtime + Apple + YouTube for the now-live episode | 🤖 | `tools/redacted_feed.py --grep "episode N"`. 📖 reads: Transistor RSS + Apple lookup + YouTube playlist RSS | ✅ stdlib tool, public feeds |
| 2 | WebFetch the published post for full "what we cover" + confirm public URL | 🤖 | 📖 reads: public Substack post | ✅ WebFetch, no credential |
| 3 | Replace the `_TBD_` markers in the episode README + root table | 🤖 | Runtime, Apple, Spotify (show-level by convention), YouTube + thumbnail, public Substack URL. ✍️ writes: `README.md` files | ✅ local file ops |
| 4 | Commit to `main` | 🤖 | ✍️ writes: git commit | ✅ local git |

---

### Readiness summary (from the LLM Access column)
- **Fully agent-accessible today:** sheet read/write (`workspace-mcp`, dedicated account), Substack public fields/body (WebFetch), repo file + git ops, the RSS tool.
- **Human-in-the-loop by necessity:** the watcher triggers (no Slack admin access; no publish watcher), live cut-notes, the "files shared on-air" list, and the pre-publish body (paste).
- **Verdict:** Process 2 and Process 3 are ready to build behind a manual trigger; Process 1's only ❌ is the Slack producer ping (no admin access to install a Slack app/connector).
