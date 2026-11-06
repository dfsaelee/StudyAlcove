# StudyAlcove screens and flows

**Round 1 · Proposed for review.** Read the inventory first. Its rows define the purpose, primary action, presentation and release target of each surface. The matching specification gives the visual order, components, sample data, behavior, recovery paths, destinations, responsive treatment, accessibility and artwork. The nine journeys at the end trace how these surfaces work together.

## Decisions and reading guide

- **Already approved.** The design brief identifies four approved world concepts and the Library as the first playable room. The browser can show artwork for all four while enabling entry only for rooms the server offers. See [Design brief](../shared/DESIGN-BRIEF.md).
- **Existing project requirements.** A guest can join an existing room by code. The server issues identity, controls membership, movement and timing, and records completion once. React owns the accessible interface and PixiJS renders the room. These constraints come from the [coding master plan](../../roadmap.md) and [design direction](DESIGN-DIRECTION-AND-UX.md).
- **Proposed default.** This label covers all layouts, actions, copy examples and release assignments below unless another status appears. The examples describe intended behavior. Data names describe what a view needs and leave protocol and schema changes for their own milestone.
- **Requires review.** Confirm the server rules for interruption, active-session resume, pause and leaving, the private-room permission model, account linking, streak calculation and decoration placement before exposing those controls. Chat and private-room UI target V1. Public creation and collections target Later pending a product decision. The master plan's room-creation API can support development fixtures earlier.

**Review fixture.** Robin is a guest. The Library has ten places. Use three people before Robin joins and four including Robin after entry when showing consecutive steps. Seat availability comes from the seat list independently of the people count. Use “Desk 03 · Window”, a 25-minute focus session and, when supported, a five-minute break. LIB7K is a fictional public room code. A private invitation carries its own server-validated access information.

## Screen inventory

| ID | Surface and purpose | Primary action | Presentation | Priority |
|---|---|---|---|---|
| E1 | Landing · choose how to enter | Browse rooms | Page | MVP |
| E2 | Room browser · find an available room or enter its code | Join room | Page with inline code entry | MVP |
| E3 | Guest entry · identify the joining player | Enter room | Dialog in browser or invite entry | MVP |
| E4 | Join room · wait for an authoritative room snapshot | Enter when ready | Transition view in room shell | MVP |
| G1 | Multiplayer room · move and find a seat | Approach a desk | Page with canvas and DOM controls | MVP |
| G2 | HUD · read current room and player state | Open the relevant room control | Persistent DOM regions in room | MVP |
| G3 | Desks · find a reachable seat through a list | Choose desk | Drawer from HUD | MVP |
| G4 | Desk interaction · inspect and claim a seat | Sit here | Context panel | MVP |
| G5 | Pomodoro · start and track focused time | Start focus | Seated desk panel, then compact HUD timer | MVP |
| G6 | Focus completion · show whether time was credited | Back to room | In-room result panel | MVP |
| G7 | Pause or break · rest between sessions | End break | Timer panel state | V1, capability gated |
| G8 | Connection lost · recover the room state | Retry connection | Persistent banner, expanded recovery panel | MVP |
| G9 | End session or leave room · explain the effect | Confirm the chosen action | Confirmation dialog when credit is at risk | MVP |
| S1 | Nearby chat · communicate within the room's allowed range | Send message | Drawer | V1 |
| S2 | Emotes · send a quiet gesture | Choose emote | Popover | V1 |
| S3 | Create room · set a room's access before creation | Create room | Dialog in browser | V1 private / Later public |
| S4 | Invitation · share or validate access to a private room | Copy invite / Join room | Host popover / guest entry view | V1 |
| P1 | Avatar customization · change appearance | Save appearance | Dialog using guest-entry editor | MVP presets / V1 in-room edits |
| P2 | Profile and statistics · see verified progress | View history | Page, or returnable from room | MVP recent totals / V1 weekly detail |
| P3 | Study history and streaks · inspect past study time | Review sessions | Section within profile | MVP recent history / V1 streaks |
| P4 | Achievements · understand an earned badge | Inspect badge | Collection section in profile | Later |
| P5 | Decoration inventory · select and place an owned item | Place item | Room drawer, then placement mode | Later |
| T1 | Appearance · choose theme and motion preference | Apply appearance | Settings panel section | V1 |
| T2 | Audio · adjust music and ambience | Adjust sound | Settings section and quick mute control | V1 |
| T3 | Controls and help · find an available way to play | Open desks or return to room | HUD help panel shared with settings | MVP hints / V1 full section |
| T4 | Privacy · manage supported social preferences | Save preferences | Settings panel section | V1 |
| T5 | Account · understand guest identity and available account actions | Inspect or manage identity | Settings panel section | V1, capability gated |

## Shared layout and interaction

Use the breakpoints, gutters, target sizes, safe zones and focus rules in the [design system](../ui/DESIGN-SYSTEM.md). A normal page contains skip link, header/navigation, main heading and content, then the footer. Keep Home, Rooms and Profile in the page navigation as their features become available. The room uses its own compact HUD and “Leave room” exit. A footer belongs below page content and stays outside the room viewport.

In the room reserve space above and below the world for controls. Keep identity and connection at the top left, count and settings at the top right, the timer at bottom center and Desks, Chat and Emotes at bottom right. Place the desk panel on the open side of the selected seat. Dock it below the world when it would cover the player or seat. Use a side drawer on wide layouts, a sheet on small ones, and one expanded panel at a time. Measure the remaining world area after accounting for overlays and safe-area insets. Preserve aspect ratio, render at integer zoom and letterbox or adjust the camera view. The 16:9 Library concept is a composition reference. Keep UI text and controls at CSS pixel sizes when the camera zoom changes.

Below 640 CSS px, stack page content and dock HUD controls in a wrapping bar. From 640–1023 px collapse supplementary navigation and use sheets when the canvas loses room. At 1024 px and above use the desktop arrangement with a 1200 px page maximum. The proposed drawer is 320 px on wide screens. Labels wrap, actions grow vertically, and long names can break across lines. Only secondary summaries may truncate, with their full text available on focus or activation. Permit scrolling within a tall sheet and keep its action reachable at 200% text size. Test at 320 CSS px, with the software keyboard open, and with long localized labels.

Closing a dialog returns focus to its opener or the next logical target if that opener disappeared. Support Escape, an explicit Close/Back button, visible focus and 44 px targets. A modal makes its background inert and traps focus. A nonmodal drawer stays in the page's focus order and returns focus on close. Release movement bindings while a form, panel or dialog owns a key. Accessible lists and controls issue the same validated commands as world interactions. Announce status transitions once, and keep consequential results visible long enough to reread. Brief toasts supplement a persistent saved or failed state.

**Reading each specification.** “States” follows the order **loading / empty / error / success** with an explicit fallback for static content. “Adaptation and art” describes responsive behavior, accessibility and required artwork. Component names refer to planned responsibilities in the [component inventory](../ui/UI-COMPONENTS.md). Where a composition has few controls, use native form fields and existing primitives. Art IDs and formats are specified by the [asset manifest](../shared/ASSET-MANIFEST.md) and [pixel pipeline](../pixel-art/PIXEL-ART-PIPELINE.md).

## Entry and navigation

### E1 · Landing

- **Order and components.** Header and wordmark → heading “A little place to focus, together” → Browse rooms → Library illustration → room previews → short guest-entry explanation and footer. Use the page shell, Button and RoomCard. A returning guest sees “Return to Library” beside Browse rooms when a recent room is known.
- **Data, interaction and destinations.** The Library preview describes amber reading lamps and quiet desk rows. Browse opens E2. Return attempts E4 after identity validation. A missing credential opens E3.
- **States.** Keep the heading and Browse available while preview art loads / a first visit omits Return / offline status offers retry and keeps previews readable / an available recent room has a named Return action.
- **Adaptation and art.** Two-column hero collapses to heading, action, then image. Focus reaches Browse before previews. Give the meaningful room illustration a short description and hide duplicate thumbnail descriptions. Use the wordmark and Library concept.

### E2 · Room browser and code entry

- **Order and components.** Rooms heading → labeled “Room code” field and Join by code → room cards in Library, Café, Night Owl Loft, Greenhouse order → conditional Create room. Each RoomCard contains preview, name, mood, public/private disclosure where permitted, capacity and one available action.
- **Data, interaction and destinations.** “Library · Public · 3 of 10 online · Join Library”. Resolve LIB7K on submission, then E3 for a new guest or E4 for an existing one. Enable a card only when its room is open. Keep concept cards labeled “Coming soon”. Private rooms require an authorized invitation or permitted code.
- **States.** Reserve card space while loading / “No rooms are open” retains code entry and Refresh / unavailable, full or invalid codes keep the field editable and offer Browse / validated room opens guest entry or join. A list fetch failure keeps code entry usable if metadata lookup is available.
- **Adaptation and art.** Responsive grid becomes a single column. Make the Join button's accessible name specific to its room. Read capacity and availability as text. Reuse four concept crops or a named placeholder as art becomes available.

### E3 · Guest display name and avatar

- **Order and components.** Room name → labeled display-name field → AvatarPreview and available presets → brief explanation of guest history → Enter room and Back. Use Dialog, AvatarCustomizer and Button.
- **Data, interaction and destinations.** Draft “Robin” and a validated avatar preset. Submit once, keep the selected destination, resolve guest identity, then enter E4. Existing valid guests skip this form. Cancel returns to E2 or S4.
- **States.** Wait for guest creation with an in-place pending label / offer a default body when optional layers are missing / preserve the name and preset on validation or network failure, focus the first invalid field / a valid guest proceeds to the requested room.
- **Adaptation and art.** Preview beside controls on desktop, above them on mobile. Use labeled radio choices and text names for color options. Announce the selected look. Use the canonical layered character and only validated presets.

### E4 · Join room and loading

- **Order and components.** Requested room name → ConnectionIndicator → current stage → Cancel or Retry. Reuse the room shell and an indeterminate progress indicator. Show “Joining Library” then “Loading room” while waiting for its snapshot and playable view.
- **Data, interaction and destinations.** Target room ID, valid guest, connection state, initial snapshot and essential asset readiness. Enter G1 only when ready. Cancel abandons this join attempt, releases any acquired membership and returns to E2 or S4. Ignore a late reply from an abandoned attempt.
- **States.** Named stages and no invented percentage / missing destination returns to E2 with code entry / full, restricted or removed room offers a specific recovery action, transient failures allow Retry / one current snapshot establishes player, desks and room count.
- **Adaptation and art.** Center a compact status region on all widths. Announce changes politely. Cancel stays reachable without a pointer. A reusable Library thumbnail is optional. Essential rendering failure offers Retry and Browse.

## Core gameplay

### G1 · Main multiplayer study room

- **Order and components.** Skip to room controls → room heading and connection → RoomCanvas → Desks and controls → session status. Use GameHUD for G2 and an accessible DOM summary alongside the PixiJS canvas.
- **Data, interaction and destinations.** Room snapshot with bounds, players, positions, seat IDs and interaction points. Move with a supported input, approach Desk 03 and open G4, or use G3. The server validates movement and seat availability. Leave uses G9 when relevant.
- **States.** E4 during first synchronization / “You’re the first here” when alone, and “No desks available” when all are taken / G8 freezes actions during loss, drawing failure keeps DOM recovery actions available / display authoritative presence and reachable desks after sync.
- **Adaptation and art.** Keep player and nearest interactable visible at allowed integer zoom. A narrow device can browse, read status and use the desk list. Full touch locomotion requires review/testing. Put world-only arrow keys behind deliberate canvas focus and provide a keyboard path back to DOM controls. Use the Library tilemap, collision and seat metadata, layered furniture and player animations.

### G2 · In-game HUD

- **Order and components.** Room name and ConnectionIndicator → online count and settings → PlayerStatus and compact FocusTimer → Desks → optional Chat/Emotes → Leave room. Use buttons with text equivalents, especially for icon-only actions.
- **Data, interaction and destinations.** “Library · Connected · 4 online”, “Robin · Seated”. Current seat/session and enabled capabilities determine the actions. Open G3/G5, S1/S2 or T1–T5 from the appropriate control, preserving room context.
- **States.** Show “Syncing” and reserve the timer slot / idle state offers Find a desk / disconnected state links to G8 and disables world actions / indicate Connected, seated, focusing or on break as confirmed.
- **Adaptation and art.** On mobile move lower controls into a bar outside the world and keep the focused control above the keyboard. Use named landmarks, readable counts and stable focus order. Reuse the chosen UI icons. World indicators can reuse the manifest's pixel markers.

### G3 · Accessible desk list

- **Order and components.** Desks heading → live availability summary → list of named seats with availability → selected seat details. Use a drawer, native list and Buttons.
- **Data, interaction and destinations.** “Desk 03 · Window · Available”, “Desk 04 · Occupied”. Activate a row to open G4. The alternative path must allow an accessible player to reach and claim a seat under the same movement, range and occupancy rules. As a baseline, expose labeled directional step buttons, current tile, and the direction/distance to the selected seat. Each step requests the same bounded move as a keyboard arrow and reports a blocked path. Once in range, enable Sit here. A one-action approach can replace the steps only when the controller supports a validated route. Review this path on the Library map at the movement milestone.
- **States.** “Loading desks” while seat data arrives / all occupied keeps the list visible and offers Return to room / a lost race refreshes the affected row and suggests another available desk / server confirmation identifies “Your seat”.
- **Adaptation and art.** Dock beside the canvas or open as a sheet. Preserve focus on a row across occupancy updates. Label each seat and expose its availability without color. Seat icons are optional. Reuse map metadata as the common source of visible and listed desk IDs.

### G4 · Desk interaction panel

- **Order and components.** Seat name and location → availability → Sit here or Stand up → Close. Use a context panel with Button and PlayerStatus. Only a confirmed seat shows the start controls in G5.
- **Data, interaction and destinations.** Desk 03, current owner and the player's position. Confirm “Sit here” once, wait for the server, then show “You’re seated”. An occupied seat offers Open desks (G3). Stand up during focus opens G9 when the action risks losing credit.
- **States.** “Taking seat…” / no nearby desk directs to G3 / out of reach or claimed by another player refreshes the state and offers G3 / seated state opens the focus setup and updates the avatar pose.
- **Adaptation and art.** Anchor away from the avatar on desktop, dock below the viewport on narrow layouts. Focus enters the panel after explicit interaction. Use the desk/chair, seat marker and sitting frame from the same Library kit.

### G5 · Pomodoro timer

- **Order and components.** Seated status → supported duration or fixed label “25 minutes” → Start focus. Once started show FocusTimer, “Focusing”, time remaining and End session. Use tabular numerals and a single dispatch per action.
- **Data, interaction and destinations.** Server session ID, start/end timestamps and state. Render the countdown against the confirmed end time. Restore the displayed time after tab suspension from the server state. Zero switches to G6 pending confirmation. End session opens G9.
- **States.** “Starting…” until acknowledged / without a seat, Find a desk opens G3 / conflicting active session triggers a state refresh, a rejected start leaves Retry available / accepted start shows e.g. “24:59 remaining”.
- **Adaptation and art.** Compact panel in the lower HUD keeps a stable width around digits. Give the timer an accessible name, announce start and completion once and let the user read the current value on demand. Reuse the focus pose and an optional timer icon.

### G6 · Focus completion

- **Order and components.** SessionSummary title → credited duration and room → Back to room → View history, and Take a break when supported. Keep the result accessible after any transient toast.
- **Data, interaction and destinations.** Use the server result for this session. Show “25 minutes added · Library” only after durable confirmation. Resolve an uncertain result by reading its status or retrying with the same completion identity. Repeated acknowledgments update the same summary.
- **States.** “Checking your session…” at zero / cancelled, interrupted or timed-out results state the server's reason and actual credited amount / “Couldn’t confirm study time” offers Check again without adding minutes locally / confirmed time updates P2/P3 once and enables return to G1 or G7.
- **Adaptation and art.** Use a compact panel or bottom sheet. Announce the result once, keep its heading focusable and allow silent, motion-free completion. Optional success marker from the UI kit. No separate scene art required.

### G7 · Break and conditional pause

- **Order and components.** Session state → optional five-minute break duration → End break or Back to desk. Reuse FocusTimer and Button. A genuine active-focus Pause/Resume control requires a server capability and explicit credit rules.
- **Data, interaction and destinations.** After a confirmed G6 result, a supported break can run independently of recorded focus time. Its end returns to G4/G5. If active pause is later supported, show stored remaining time after acknowledgment and resume the same session.
- **States.** Pending transition shows “Starting break…” / unsupported breaks leave Back to room available in G6 / a rejected pause or resume restores the last confirmed state and offers Check again / break end offers Start another session explicitly.
- **Adaptation and art.** Use the same HUD slot on every viewport. Convey “On break” in text and keep alert sounds optional. Use a break icon or the existing seated pose.

### G8 · Connection lost and reconnecting

- **Order and components.** ConnectionIndicator → persistent “Reconnecting to Library” status → last confirmed session state → Retry or Browse rooms. After unsuccessful attempts expand the banner to a recovery panel.
- **Data, interaction and destinations.** Current identity, target room, last known session ID and fresh server snapshot. Suspend movement, seat, timer and social mutations. Reconcile identity, position, seat and session before enabling controls. A former position or seat requires current server confirmation.
- **States.** Describe the current connection attempt / no restorable session offers G3/G4 / expired credentials open E3, removed room offers E2, continued network failure keeps Retry / state “Reconnected” and restore G1, G5 or G6 according to the new snapshot and durable session result.
- **Adaptation and art.** A wrapping banner above the world becomes an inline panel on mobile. Announce transitions once per distinct state, allow manual retry via keyboard and suppress repeated auditory announcements. Reuse connection icons. No new sprite required.

### G9 · End session or leave room

- **Order and components.** Action-specific title → known effect on the current session → Keep focusing → End session or Leave room. Use Dialog only for a consequential choice. Idle Leave returns directly to E2.
- **Data, interaction and destinations.** Check session status and the supported leave rule. For confirmed cancel-without-credit, the dialog can say “End this session without adding study time?” If the rule is unresolved, offer a separate explicit End session according to supported policy and leave any unsettled result available for status lookup.
- **States.** Show pending action while awaiting acknowledgment / with no active session skip the credit dialog / a lost acknowledgment goes to G8 or Check status / accepted end updates the session state, accepted leave exits to E2. Cancel returns focus to the original control.
- **Adaptation and art.** Center dialog on wide screens, keep both actions visible in a sheet on mobile. Start focus on Keep focusing. Differentiate the destructive action with explicit text. No artwork required.

## Social

### S1 · Nearby chat

- **Order and components.** “Nearby chat” heading and mute → room/range description → chronological messages → labeled composer and Send. Open the drawer from G2 and close it to return to the same room. Deliver only messages the server authorizes for the player's current scope.
- **Data, interaction and destinations.** Example message “Robin · 10:15 · Good luck studying!” Render user text as text. Enter sends from the single-line composer. A send in progress keeps its draft attached to the pending message. Acknowledgment clears it. Chat settings open T4.
- **States.** Show “Loading chat” / “No nearby messages yet” or “Chat is muted” / offline, blocked or rate-limited send keeps the draft and explains the available next action / append confirmed messages, preserve reading position when the user scrolls back.
- **Adaptation and art.** Side drawer becomes a sheet above the software keyboard. Name authors and times, let the user control announcements, and disable world bindings while typing. Use the common chat icon. No character portraits required.

### S2 · Emote picker

- **Order and components.** Emotes trigger → short labeled list “Wave”, “Happy”, “Sleepy” → close. Use a popover with one button per approved emote.
- **Data, interaction and destinations.** Each enabled emote has a display name, authorized action ID and compatible sprite. Choose Wave once, return focus to its G2 trigger and show the acknowledged gesture near the player's avatar.
- **States.** Wait for the available emote set / an empty set hides the trigger / rate limit or disconnect gives a reason and keeps the selection available after recovery / an accepted emote shows “Robin waved” in the optional activity description.
- **Adaptation and art.** Anchor above the trigger or show a wrapping sheet. Tab reaches each button. Escape returns to the trigger. Give motion-reduced users a static glyph and text. Use the character's vetted emote frames or corresponding static glyphs.

### S3 · Create a public or private room

- **Order and components.** Create room heading → room name → approved room template → access setting and explanation → Create room, Cancel. Use Dialog, labeled native fields and Buttons. When only private creation is supported, show “Private · invitation required” as fixed text.
- **Data, interaction and destinations.** “Robin’s reading room” using the Library template. Private creation lets an authorized host invite others through S4. A later Public choice would let an approved host publish a discoverable study room in E2. Eligibility, moderation and publishing rules **require review**. Publication requires a separate policy and a server permission check. Enable actions only for the user's confirmed capabilities.
- **States.** Disable duplicate submits while creating / no available templates gives Back to rooms / invalid name or missing permission keeps edits visible and explains the field or restriction. On an ambiguous response, resolve the original request before allowing another creation / on success show the new room and the permitted Share or Enter action.
- **Adaptation and art.** Single-column form in dialog or mobile sheet. Group visibility options under an explicit legend, name who may join and focus errors on submission. Reuse a Library concept crop for the template if needed.

### S4 · Room invitation

- **Order and components.** Host sees room name, access summary, invitation field and Copy invite in a popover. A recipient opens a dedicated entry view with validity status, allowed room details and Join room. Use a read-only field, Button and ConnectionIndicator.
- **Data, interaction and destinations.** Invite token, server validation result and permitted room summary. Show “Join Robin’s reading room” only when metadata access is authorized. Join goes to E3 or E4, retaining the invitation through the guest step. A failed private invite never joins another room automatically.
- **States.** “Checking invitation…” / no link yet offers an authorized Create invitation action or explains why sharing is unavailable / expired, invalid, forbidden or full invites offer Request a new invite from the host or Browse rooms. When clipboard access fails, allow manual selection and copy / host sees Copied, recipient explicitly joins the validated room.
- **Adaptation and art.** Keep a long link within the read-only field, label it and announce copy feedback once. The recipient page stacks status and actions on narrow screens. Use an optional template thumbnail only after metadata is authorized.

## Personalization and progress

### P1 · Avatar customization

- **Order and components.** AvatarPreview → supported categories (e.g. hair, outfit, color) → named choices → Save appearance and Cancel. Reuse AvatarCustomizer inside E3 for starter presets and inside a room dialog for later edits.
- **Data, interaction and destinations.** Draft layer IDs and palette variants, e.g. bob and cardigan when validated. Preview a draft locally. Cancel discards it. Save returns to E3 or G1 after acceptance. Peers see the committed appearance once synchronization is supported.
- **States.** Keep the previous look visible while options load / default to the base look when optional sets are empty / invalid or retired combination leaves the prior selection intact and identifies the conflicting option / saved preview and authoritative room avatar match.
- **Adaptation and art.** Two columns become one scrolling sheet. Use labeled radio groups with selected checks. Expose a text description of the assembled look and offer a static preview with reduced motion. All layers share the approved frame and pivot. Include only combinations checked for clipping.

### P2 · Profile and focus statistics

- **Order and components.** Profile heading and guest scope → total credited time → completed-session count → recent history link. V1 can add a labeled weekly chart with equivalent values as text. Use AvatarPreview, stat cards and a list.
- **Data, interaction and destinations.** After a first saved Library session, “25 minutes studied · 1 completed session”. Read completed data for the current identity. View history opens P3. From the room, preserve the active session and an explicit Back to room path. If routing would leave membership, show a returnable panel until that lifecycle is supported.
- **States.** Show labels with pending totals / verified empty history gives “0 minutes” and Browse rooms / failed reads show Retry and identify previously loaded totals as stale / confirmed results show the refreshed total once.
- **Adaptation and art.** Place totals side by side on desktop, stack or wrap on mobile. Use clear units, headings and text equivalents for charts. Reuse the avatar preview if available. Statistics need no illustrations.

### P3 · Study history and streaks

- **Order and components.** History heading → guest-history scope → recent sessions newest first → conditional streak summary and weekly detail. Use a semantic list or table and text summaries.
- **Data, interaction and destinations.** A completed row reads “Library · 25 minutes · Nov 6”. Render server instants in a labeled local time zone. Credit totals derive from completed server records. Streak counts require an agreed day boundary, qualifying-session rule and service calculation. Navigate from P2/G6 and back to P2 or the originating room.
- **States.** “Loading sessions” / “Finish a session to see it here” / preserve already-read rows on refresh failure and offer Retry / show an updated row keyed by the same session ID after duplicate acknowledgments.
- **Adaptation and art.** Table columns can become stacked labeled rows. Do not force sideways scrolling. Use spoken dates and units and supply a textual streak count when enabled. Optional shared streak icon. No generated chart art.

### P4 · Achievements and badges

- **Order and components.** Collection heading → earned and locked items → selected item's title, description and unlock rule. Use cards with a detail panel in P2. Add a link to P5 only for awards linked to a decoration.
- **Data, interaction and destinations.** Illustrative badge “First session” for one confirmed focus session. Award IDs, conditions, earned status and date come from the service. Inspect an item and return to the same collection position.
- **States.** Load with stable card placeholders / “Your earned badges will appear here” / on a failed collection read, keep the last confirmed items marked stale and offer Retry / an unlock updates one badge and gives a quiet description.
- **Adaptation and art.** Grid becomes a list on narrow screens. Name the badge, condition and earned/locked state in text. Use approved pixel badge assets on neutral UI surfaces. Specific awards and art **require review**.

### P5 · Decoration inventory and placement

- **Order and components.** Room and placement permission → inventory → item details → choose allowed location → preview → Place item or Cancel. Use a drawer, list and buttons, with a PixiJS preview overlay for the world.
- **Data, interaction and destinations.** Illustrative owned “Desk fern”, permitted location and current room revision. Selecting the fern shows a preview until server confirmation. Offer a DOM list of permitted locations alongside pointer selection. Exit returns to G1. A badge may lead here from P4.
- **States.** Wait for authoritative ownership and room permissions / “No decorations yet” or “No open places” leaves an exit / insufficient rights, conflicting placement or busy slot refreshes choices and removes the uncommitted preview / confirmed placement updates the room and item state together.
- **Adaptation and art.** Wide drawer docks beside the world. Narrow sheet collapses to location, confirm and cancel during preview. Announce selection, orientation if supported, and location in text. Use an inventory thumbnail and scale-matched world sprite with footprint and valid placement metadata.

## Settings and help

Use one settings panel with a section list on wide layouts. Narrow layouts open one section at a time and provide Back to settings. Inside a live room keep the room mounted behind the panel. Theme, motion and simple audio changes can preview immediately. A failed preference write must say whether the current setting is temporary. Server-governed privacy or account actions show a pending state until acknowledged.

### T1 · Appearance and theme

- **Order and components.** Appearance heading → System, Light, Dark → reduced-motion option → Close. Use radio group, Switch and a small panel sample with real UI tokens.
- **Data, interaction and destinations.** Selected preference and resolved system theme. System follows the device when available. Theme changes apply to React surfaces, text, icons and focus. The Library retains its own lighting and sprite palette. Return to G2 or the originating page.
- **States.** Use the system preference while loading / an unset choice defaults to System / on storage failure keep the current view usable and label the change “For this visit” / a saved choice shows the selected option on reopen.
- **Adaptation and art.** Stack choices at small widths. Label the setting group and selected state, preserve visible focus through theme changes and honor system reduced motion from first paint. Reuse one sample control in each theme. No new world art.

### T2 · Audio controls

- **Order and components.** Master mute → supported music and ambience sliders → current percentages → Close. G2 can expose a quick mute button with the same underlying setting.
- **Data, interaction and destinations.** Example “Ambience · 30%”. Start audio only after permitted user interaction. Muting preserves volume values for later unmute. Return to G2 or another settings section.
- **States.** Disable sliders while capabilities load / omit a missing track and state when a room has no audio / unavailable playback or persistence reports the affected control and allows Retry / all representations reflect confirmed mute and enabled volume values.
- **Adaptation and art.** Full-width sliders on mobile, keyboard arrows and programmatic values for each labeled range. Provide visual feedback for all cues. Use a consistent volume icon. Sound assets and their rights require separate review.

### T3 · Controls and help

- **Order and components.** Controls heading → movement and room-interaction instructions → Desks alternative → panel navigation and Close. G2 shows a brief “Find a desk” hint linking directly to G3.
- **Data, interaction and destinations.** Display supported bindings from the actual input configuration, e.g. “Arrow keys to move” when available. Explain how to focus the world, release focus and activate a nearby desk. Open Desks (G3) or return to the caller.
- **States.** Show the basic desk-list path while bindings resolve / missing device bindings leave DOM controls available / failed binding lookup retains the desk action and a readable fallback / opening Desks focuses the first usable choice.
- **Adaptation and art.** Use text plus optional keycap glyphs. Touch guidance matches tested capability. Show a browse/desk-list path when mobile movement is unavailable. Help works with keyboard and screen reader alone. No sprite required.

### T4 · Privacy preferences

- **Order and components.** Guest identity and visibility explanation → supported chat/mute preferences → Save preferences and Close. Use labeled Switches and short descriptions of effects.
- **Data, interaction and destinations.** Example “Mute nearby chat”. Speak plainly about what other room participants can see, such as the display name and avatar. Distinguish local notification/mute behavior from server-enforced membership or blocking. Expose only supported settings. Return to S1, G2 or the originating page.
- **States.** Disable server-governed choices while fetching / with no configurable privacy settings show the current visibility explanation / on save failure restore last confirmed settings and retain a retryable draft / confirm which preferences are saved and apply local mute immediately where supported.
- **Adaptation and art.** Stack label, description and control on mobile. Associate descriptions with their inputs and announce save outcome. Use a common UI icon only if it helps identification. No new art required.

### T5 · Account settings

- **Order and components.** Current identity → guest history/device scope → supported account actions → return. Use a settings section, labeled values and Buttons. An in-room link to P1 can edit the current look when that feature exists.
- **Data, interaction and destinations.** “Robin · Guest on this browser”. Explain the project's actual retention and recovery rules. Account linking, sign-in, cross-device history, deletion and credential recovery **require review** before any corresponding action is offered. An existing guest can continue to G2 or P2.
- **States.** Read the current identity / no credential offers guest entry E3 when joining / expired identity asks the user to re-enter and explains the possible loss of access to earlier history / a valid identity shows its supported scope and confirmed actions.
- **Adaptation and art.** Use one column and keep long account identifiers off the main room HUD. Give identity fields readable labels and never display raw credentials. Reuse AvatarPreview. No account illustration required.

## Nine user journeys

1. **First-time visitor joins a public room.** E1 Browse rooms → E2 choose Library or enter LIB7K → E3 enter Robin and select a preset → E4 validate membership, connect and receive snapshot → G1 with G2 showing the room count. An invalid code returns focus to the field. A full room found during the handshake returns the guest to E2 with their identity intact. Cancel during loading releases this join. A concept room offers its description only.
2. **Returning visitor resumes a session.** E1 Return to Library → validate the existing guest → E4 → read fresh membership, seat and session state → G5 only for a server-confirmed active session. A completed session opens G6 or is visible in P3. Expired identity goes to E3. A removed room returns to E2. If the server has no resumable session, report that outcome and offer G3. Keep unconfirmed elapsed time out of totals.
3. **Walk to a desk and start focusing.** G1 move within validated bounds → G4 inspect Desk 03, Sit here → wait for confirmed ownership → G5 Start focus → server acknowledges start/end → compact timer. G2 → G3 provides the complete accessible path via valid movement/seat interactions. A competing claim refreshes G3. If a session already exists, read it before showing any further Start action.
4. **Complete a Pomodoro.** G5 reaches zero → G6 “Checking your session…” → durable completion → “25 minutes added” → Back to room, P3 or optional G7. A write timeout retains the session identity and retries/reconciles the same completion. A repeated success yields one history row. Cancelled, interrupted or timed-out sessions show the authoritative outcome. Ending early uses G9 before any supported cancellation.
5. **Disconnect and reconnect.** In G1 or G5, loss of connection opens G8 → freeze invalid actions → reconnect with current guest → receive fresh snapshot and study-session status → restore G1, active G5 or resolved G6. A reassigned seat sends the user back to G3. An expired credential sends the user through E3. A closed room offers E2. A pending completion is checked before any retry. Keep Retry and Browse available after repeated failures.
6. **Customize an avatar.** In MVP, E3 → P1 starter preset preview → confirm guest entry → E4/G1. With V1 in-room editing, G2 → P1 → choose supported layers → preview → Save → G1 shows the accepted appearance. Cancel restores the committed look. A rejected or missing combination leaves a descriptive error and lets the user change only the affected option. During reconnection, keep a draft local until the server can accept it.
7. **Create or join a private room.** Authorized host E2 → S3 choose Private → Create room → S4 Copy invite → recipient opens S4 → validate access and confirm Join → E3 if needed → E4/G1. If copying fails, offer manual copy. If creation acknowledgment is lost, reconcile the original request. Full, expired, invalid and restricted invitations offer safe exit to E2. Unauthorized users get only the information they are permitted to see. A separately authorized public creation uses S3 and shows in E2 only after publication is confirmed.
8. **Review study statistics.** G6 View history or page navigation → P2 read credited totals → P3 read a dated Library session → return to origin. A supported weekly view and configured streak use the same verified records. A new guest gets an inviting empty state, failed loads offer Retry, and an expired guest credential leads to the account explanation. Opening statistics during a live session preserves its status and return path.
9. **Unlock and equip a decoration.** After the service confirms an eligible award, P4 describes the badge and owned item → open P5 in a permitted room → choose Desk fern → select an allowed slot in the world or DOM list → preview → Place item → authoritative room update → G1. A locked item shows its condition. Read-only access permits inspection. An occupied slot refreshes locations. Cancel drops the preview. After a disconnect, reconcile ownership and the target location before repeating the command.

## Review walkthrough

Use E1, E2 and G2 for the first mockup round. Trace the first four journeys using Robin's fixture. For each journey try the specified failure with a keyboard, at a narrow viewport, and with reduced motion. For the desk-list path, demonstrate how a player reaches a legal interaction point and claims the same desk as a canvas user. For completion and reconnect, inspect screens before and after acknowledgment. Reviewers should be able to identify who owns the seat, whether study time has been credited, and what action remains available.

Before scheduling the V1 and Later screens, resolve pause/resume and break rules, guest-history scope, invite permissions, public publication, accessible movement, chat range, streak day boundaries and permitted decoration slots with the relevant product and backend owners. Record decisions in the [review plan](../shared/DESIGN-REVIEW-PLAN.md). These follow-up decisions do not block a review of the three representative views.
