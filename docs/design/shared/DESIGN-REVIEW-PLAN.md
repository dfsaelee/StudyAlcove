# StudyAlcove · Round 1 design review

**Please approve or revise** the foundations and screen architecture before commissioning three light-theme mockups. The first review should answer whether a guest can find the Library, claim a desk, and tell when their focus time has been saved.

## What to read

| Document | Where to look during review |
|---|---|
| [UI, UX and pixel-art handoff](UI-UX-AND-PIXEL-ART.md) | Trace a real seat from its art metadata through a proposed claim, focus feedback and live verification. |
| [Design system](../ui/DESIGN-SYSTEM.md) | Compare semantic light/dark tokens, contrast pairs, type and dimensions. Inspect the HUD safe zones, keyboard states and reduced-motion behavior. |
| [Screens and flows](../ux/SCREENS-AND-FLOWS.md) | Start with the screen inventory. Follow a guest from room selection to credited time, then try the same journey with a full room, occupied desk or dropped connection. |
| [UI components](../ui/UI-COMPONENTS.md) | Check which controls are shared, what information each receives and how a seat claim reaches both the world and the keyboard-accessible desk list. |
| [Design direction and UX](../ux/DESIGN-DIRECTION-AND-UX.md) | Existing product priorities and first-review workflow. The detailed proposals above extend this overview. |

## Decision record

**Already approved** means the brief explicitly approves a concept or the product/engineering instructions establish a constraint. **Proposed default** covers the details of these drafts unless individually marked. **Requires review** reserves a decision for the product owner or for evidence from the backend or art review. Design approval and working software are separate milestones.

| Decision | Status | Consequence for the first mockups |
|---|---|---|
| StudyAlcove and its four room concepts, with Library playable first | Already approved | Use Library, Café, Night Owl Loft and Greenhouse. Library is the joinable example. The other three have previews. |
| Desktop-first React/TypeScript interface, PixiJS world, orthographic 3/4 top-down art | Already approved · brief and project constraints | Draw walkable aisles, desks and avatars on the world grid. Place text, navigation, timer and accessible interactions in surrounding HTML. |
| Guest room-code entry, authoritative seats and timing, durable completion | Already approved · master plan | Offer room code and public-card entry to the same join flow. Enable room actions after a snapshot. Credit time after the server confirms a saved session. |
| Cream and forest web chrome, Nunito Sans, rounded outline controls and indexed world art with its own lighting | Proposed default | Start in light mode. Review the same Library scene with dark chrome in the later theme pass. |
| Accessible desk list plus keyboard movement, timer at the lower edge, settings and social tools collapsed | Proposed default | Preserve visibility of Robin, the selected desk and its approach. Compact layouts can move controls outside the image. |
| Private invites and chat/emotes in V1, public listing creation later | Proposed default · scope | MVP room code joins an existing room. Invite validation, public-list permissions and moderation need a supported policy before those screens are enabled. |
| History access after a guest credential expires, cross-device account linking, pause/resume, break timing and safety of restoring an active session | Requires review | A valid guest can see recent saved activity. Gate account linking and active pause. Show a post-session break separately from credited focus. |
| Final logo/wordmark, actual font assets, pixel palette, sprite proportions, mobile movement | Requires review | Use labelled provisional references. Review avatar legibility in a chair and at integer zoom. Mobile scope starts with browsing, forms and equivalent room actions as supported. |

## Sources and reconciliations

The [design brief](DESIGN-BRIEF.md), [UX direction](../ux/DESIGN-DIRECTION-AND-UX.md), [pixel pipeline](../pixel-art/PIXEL-ART-PIPELINE.md) and [asset manifest](ASSET-MANIFEST.md) provide the discipline-specific guidance for these reviews. The engineering roadmap and agent instructions are kept in this repository. [Coding agent master plan](../../roadmap.md) · [Agent instructions](../../../AGENTS.md)

| Difference in the references | Proposed resolution |
|---|---|
| The UX sketch starts with room cards. The MVP contract requires joining by code. | Put **Room code** and **Join by code** beside the cards. Both entrances use the same room validation, guest setup and snapshot. A curated Library entry can supply a known room code until a directory exists. |
| The UX phase summary calls private rooms “later” while the detailed screen table assigns them to V1. | Use V1 for invite-only creation/joining and later for user-published public listings. Listing and invitation permissions require their own rules. |
| The art manifest puts the profile mockup at P1 while the demo requires recent completed focus time. | Show basic totals/history in MVP. Stage the dedicated profile artwork and streaks separately. P0/P1/P2 are design production priorities. MVP/V1/later describe product availability. |
| The brief sketches pause, resume and sit animation options. The backend leaves disconnect semantics open, and the art pipeline specifies a static baseline seat pose. | In round 2 show confirmed focus running. Reserve pause/resume for explicit server support. For the anchor use one seated frame per direction and two focus frames per direction, pending sprite review. |
| The UX overview lists short token names and two button components. | The design system defines semantic roles for both themes. Map those roles once to CSS at implementation. Use one Button with visual variants. |
| The UI review wants early room scenes while the backend roadmap schedules the playable frontend at milestone 5. | Use concept art and fictional data for mockup decisions. Schedule runtime assets, integration and two-browser testing with their respective milestones. |

## Local references for the first review

| Existing reference | What to carry forward | Where the StudyAlcove brief takes precedence |
|---|---|---|
| [Café room](../../../art/references/backgroundcafecozy.jpg) | Warm wood, greenery and distinct seating areas. | Leave the Library's aisles, chair approaches and seat markers clear. |
| [Furniture sheet](../../../art/references/chairsprites.jpg) | Differentiate shelves, lamps and chairs by silhouette at a glance. | Use StudyAlcove's orthographic grid and consistent pixel scale. Angled pieces require a new orthographic drawing. |
| [Layered character reference](../../../art/references/char%20free/global.png) | Align body, hair and clothing through a walk cycle. | Validate the proposed 24×32 frame, foot pivot (12, 29) and four directions on the canonical avatar. |

Use these as visual references. A chosen concept goes through the pipeline’s native-size, palette, alpha, anchor and collision checks before it enters a playable room.

## Five rounds and their review gates

| Round | Work and evidence | Gate before the next round |
|---|---|---|
| **1 · Foundations** | This document set, explicit states, data ownership, responsive behavior and artwork dependencies. | Owner reviews the decisions above and records changes. This is the current gate. |
| **2 · Representative mockups** | Generate the three light-theme compositions below. Prepare a separate Library composition and a base character study for scale review, keeping their assets separately identifiable. | Review keep/change/remove notes per image. Approve a direction across the Library, avatar and HUD together. Resolve revisions before expanding the set. |
| **3 · Reusable anchors** | Collect approved wordmark/mark, four-direction character and sample walk, Library scene, desk/chair/plant samples, pixel icon style and a light/dark control mini-kit. | Record the selected file and revision for each anchor. Check at native scale and at 3×/4×. Approve focus visibility, seated silhouette, camera perspective and icon legibility. |
| **4 · Remaining screens** | Use approved anchors for guest setup/join, seats/timer, completion and recovery first. Add history and settings, then V1/later as scheduled. Show narrow layouts, representative failures and both themes for major screens. | Compare the same strings, controls and room art across screens. Record the selected frame for each surface, theme and priority. |
| **5 · React implementation** | At an approved frontend milestone, map tokens to CSS variables, build the MVP DOM controls, connect room intents/snapshots, then add PixiJS rendering. Placeholders can exercise the integration. | Compare browser captures to approved frames. Demonstrate a keyboard-only session, responsive layouts, two clients racing for one seat, reconnect and retry-safe saved credit. |

## Three round-2 mockup briefs

**Shared direction (proposed).** Use a 1440×900 CSS-pixel reference viewport, light theme, desktop geometry and exact role names from the design system. Use one working wordmark wherever the brand appears and the same Library scene in all three. Where an anchor is pending, identify the provisional reference in the review notes. Use Nunito Sans for actionable text, one rounded vector family for web controls and crisp integer-scaled world pixels. Limit the composition to the listed controls and labels. Leaderboards, marketing badges, extra navigation, decorative copy and baked-in world text are out of scope.

Use these proposed reference IDs in the prompt log. **brand-wordmark** appears on Landing and Room Browser. **library-room** supplies the hero view, browser thumbnail and HUD environment. **avatar-base-01** supplies Robin's seated figure in the HUD. **ui-controls** supplies the web control treatments across all three screens. Attach the current file revision to each ID when it exists and record the approved revision at the anchor review.

| Mockup | Composition and exact sample content | What the reviewer should try |
|---|---|---|
| **Landing** | Header with **StudyAlcove**. Hero with **A little place to focus, together.**, **Browse rooms** and a Library view that clearly shows a desk and lamp. Below it, a compact **Rooms** preview with named room images. Keep the CTA readable if the image fails. Use the current brand mark candidate and Library composition. | Ask someone to point to the first action within five seconds and explain whether an account is required. |
| **Room browser** | Header, **Rooms** heading, **Room code** field and **Join by code**, then four RoomCards. **Library** · **3 of 10 online** · **Join Library**. **Café**, **Night Owl Loft**, **Greenhouse** each carry **Coming soon**. Use Library thumbnail and labelled concept placeholders for absent previews. No join action on preview-only cards. | Find both ways to enter. Identify which room is playable and distinguish connected people from available desks. Check a visible focus ring on the Library action. |
| **In-game HUD** | Center the Library around **Robin**, seated at **Desk 03 · Window**. Keep a clear aisle visible. Upper left **Library** · **Connected**. Upper right **4 online** and supported controls/help. Lower center **Focusing** · **24:38**, counting down from 25 minutes. Lower right **Desks**. Reserve space for collapsed chat/emotes in a later social-enabled variant. Use the same Library and character studies as the anchor candidates. | Find Robin and the desk before reading any panel. Identify the active timer and connection state. Show how a keyboard user would open Desks while movement keys are suspended. |

Use 3 online before Robin joins and 4 afterwards. Reserve **25 minutes added · Library** for a confirmed completion. A proposed 5-minute break earns no study credit.

For each future image, log screen and state, viewport/theme, exact prompt and copy, input reference IDs and revisions, output filename, reviewer, date and keep/change/remove notes. A blank approval entry means review is pending. Preserve originals and identify the selected revision before reusing it.

## Round 1 coverage audit

| Brief requirement | Evidence in this packet | Verification still needed at the stated gate |
|---|---|---|
| Colors, both themes and contrast | Design system pairs semantic inks, fills, borders, rings and state colors and reports measured ratios. | Compare rendering over opaque panels, forced colors, browser focus and actual fonts in round 5. |
| Type, spacing, icon family, shape | Tokens and examples cover text roles, grid/gutters, control sizes, icon sizes, elevations and selection. | Inspect the same three compositions together in round 2, including the HUD's available world area. |
| Component states, keyboard, motion | Control-state specifications plus component contracts cover pending, failure, input ownership, focus recovery and reduced motion. | Run a keyboard-only and reduced-motion walkthrough with real widgets in round 5. |
| Screen and journey coverage | Screen inventory, per-surface specs and nine journeys include guest/code entry, reconnect, breaks, profile and later unlocks. | Review the phase labels against supported backend capabilities before commissioning each batch. |
| Responsive layout, overflow and world integration | Design system gives layout measurements. The screen specs place desktop/mobile controls. The component trace follows a desk ID into confirmed seat and timer state. | Check at 320, 768 and 1440 CSS px, zoomed text and long names. Test two clients after integration. |
| Artwork and failure/empty states | Screen specs identify world/preview assets, reusable components and recovery paths. The manifest/pipeline identify production outputs and pixel QA. | Review the three initial mockups and the separate world/character samples before freezing reusable anchors. |

**Review exercise (about 15 minutes).** Trace Robin from **Join by code** to **25 minutes added · Library**. At the seat claim, let a second guest win. During completion, drop the connection. Mark which action becomes available at each server reply, which message Robin sees and which draft needs adjusting. Then record keep/change/remove feedback and a decision on round 2.


