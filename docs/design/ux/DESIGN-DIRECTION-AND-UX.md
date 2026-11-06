# StudyAlcove — Design Direction & UI/UX Flows

**Scope:** Product experience and reusable frontend component rules. Start with the [Round 1 design review](../shared/DESIGN-REVIEW-PLAN.md) for the proposed design system, complete screen and component inventories, and mockup sequence. See the [visual brief](../shared/DESIGN-BRIEF.md) and [asset manifest](../shared/ASSET-MANIFEST.md) for the art direction and production queue.

## 1. Experience principles

1. **Start focusing quickly.** A visitor should reach a desk and start a timer without creating an account.
2. **The room is the hero.** Avoid a dashboard that overwhelms the pixel world.
3. **Quiet social presence.** Emotes and chat are optional, unobtrusive, easy to mute.
4. **Be clear about state.** Empty/occupied desk, focusing/on break, joining/reconnecting, and completed session must be distinct.
5. **Gently rewarding.** Focus history and progress support motivation without pressure or compulsory rankings.
6. **Accessible.** Non-pixel typography for important copy, contrast, visible focus, keyboard shortcuts with hints, motion controls and alternative interactions for mouse/keyboard/touch users.

## 2. Information architecture

- **Home:** Hero, Join a room, Room previews, product explanation, guest entry / account entry.
- **Room browser:** Four room visual cards, capacity, room mood, public/private availability, join button. Some rooms may be concept-only or labelled coming soon during the MVP.
- **Avatar setup:** Display name, initial base avatar / hair / outfit / color selection; preview.
- **In room:** Dominant game world, room name and online count, timer, desk prompt, user menu, optional chat/emotes.
- **Session result:** Time credited or reason not credited, return to room, see history.
- **Profile:** Completed sessions, total study minutes, weekly focus history; streaks in V1.
- **Settings:** UI theme, room music/ambience volume, mute chat, motion reduction, keyboard controls, privacy.
- **V1:** Private room creation and invitations, subject to membership and permission support. **Later:** User-published public rooms, decorations inventory and achievement collection.

## 3. Primary user journeys

### Flow A: First-time guest to focusing (MVP)
`Landing → Room browser → Choose Library → Display name/avatar → Connect → Move to an empty desk → Sit → Start Pomodoro → Complete → Completion feedback → Continue or leave`

- Guest identity can be temporary; disclose that durable cross-device history may require an account in V1.
- **Join by code** is an MVP alternative to choosing the Library card. Validate the existing room, reuse guest setup as needed, and wait for its authoritative snapshot before enabling room actions.
- Seat selection communicates occupied vs available without requiring close reading of text.
- Keyboard movement is preferred; click/tap-to-move is a possible enhancement, not an MVP promise.
- A user must also be able to select a desk through an accessible interaction list if movement is difficult.

### Flow B: Returning participant
`Landing → Return to recent room or browse → Join → Reconnect / room sync → Continue a valid ongoing focus session (if supported) or start a new one`

- Don't promise resume-on-crash until server/session rules support it.
- During reconnect, freeze invalid interactions and show a persistent status indicator.

### Flow C: Friend joins the room (V1)
`Create private room → Copy invite link → Friend opens link → Validate invitation → Avatar setup → Join room`

- Handle full, invalid, expired or restricted rooms; never silently redirect into a private room.

### Flow D: Session finishes
`Timer active → server records completion → success banner + focus minutes → history updates → optional break action`

- Server is authoritative; client timer is display only. Distinguish cancelled, interrupted, timed-out and successful states.

## 4. Screen specifications

| Screen | Essential UI | Primary action | Important empty/error state | Phase |
|---|---|---|---|---|
| Landing | Logo, short tagline, hero room art, join CTA, preview cards | Browse rooms | Offline/server status | MVP |
| Room browser | Room cards with mood, occupancy, availability | Join room | No rooms available, full room | MVP (Library live, other previews) |
| Avatar setup | Name field, character preview, hair/outfit swatches | Enter room | Invalid name, inaccessible room | MVP (simple customization) |
| In-room game HUD | Room name, status, movement hints, timer, desk prompt, chat control | Sit/start focus | Reconnecting, full seats, connection lost | MVP |
| Focus/desk panel | Selected seat, timer length, start/pause/cancel behavior | Start focus | Seat taken, session conflict | MVP |
| Completion | Credited minutes, gentle positive feedback | Back to room | Save failed / retry safely | MVP |
| Profile/history | Sessions list, totals, placeholder for streaks | View history | No sessions | MVP basics / V1 streaks |
| Chat/emotes | Expandable minimal panel, mute action | Send/emote | Rate-limited, blocked, disconnected | V1 |
| Settings | Theme, audio, motion, chat/privacy | Save preferences | Unsupported option | V1 |
| Private room | Invite link, membership controls | Create/share | Invalid invite, permission denied | V1 |
| Achievements/decor | Badge gallery and owned decorations | Equip/place item | Locked, missing inventory | V2 |

### Desktop HUD layout
- Top left: room identity and connection indicator.
- Top right: online count and settings/mute options.
- Main central region: PixiJS room canvas, fluid size, integer game zoom where possible.
- Bottom center: compact timer and current focus status, never blocking character movement.
- Bottom right: collapsed chat/emotes and accessible interactive objects menu.
- Context popover on desk/seat interaction, positioned without obscuring character.

### Responsive behavior
- Desktop is the first target; tablet reduces side controls into overlays.
- Mobile is viewable/browsable and should not overflow. Full mobile movement controls may be added as a dedicated follow-up; don't quietly claim mobile playability without testing.
- If game canvas can't maintain integer scale in available width, letterbox rather than distort pixels.

## 5. Components and tokens

Implement UI in React + TypeScript; PixiJS only for game-world rendering and world-specific overlays if needed.

**Component inventory**: `AppShell`, `TopNav`, `RoomCard`, `RoomStatus`, `ConnectionBadge`, `AvatarPreview`, `AvatarCustomizer`, `PrimaryButton`, `SecondaryButton`, `IconButton`, `Modal`, `Popover`, `Toast`, `FocusTimer`, `SeatPrompt`, `SessionSummary`, `ProfileStats`, `EmptyState`, `ChatDrawer`, `SettingsPanel`.

Token names: `color.bg`, `color.surface`, `color.surfaceElevated`, `color.primary`, `color.primaryHover`, `color.accent`, `color.text`, `color.muted`, `color.border`, `color.success`, `color.warning`, `color.error`, `color.focus`; `space.1–12`, `radius.sm/md/lg`, `shadow.panel`, `duration.fast/normal/slow`.

The short names above are the original sketch. Use the proposed semantic [design-token reference](../ui/DESIGN-SYSTEM.md) for exact light/dark pairs and contrast roles, and the [component inventory](../ui/UI-COMPONENTS.md) for shared variants and ownership. Translate the reviewed tokens into CSS variables at the frontend milestone.

### Interaction states
- Buttons: default, hover, pressed, focus-visible, disabled, loading.
- Room cards: available, full, private, coming-soon, selected, keyboard-focused.
- Desk: empty, occupied by you, occupied by someone else, temporarily unavailable.
- Connection: connecting, connected, reconnecting, disconnected, error.
- Timer: idle, active, on-break, completed, interrupted. Avoid claiming a pause feature if backend rules don't allow it.
- Motion: honor reduced-motion setting; no critical information only conveyed through animation.

## 6. UI mockup workflow (follow provided reference method)

1. Collect **2–4 inspiration references** plus notes on what to take and what to avoid. Do not trace or reproduce other projects.
2. Agent drafts `DESIGN-BRIEF.md`, the exact per-screen element lists, copy, and one prompt per screen.
3. Generate **only 3 initial screens**: Landing, Room browser, In-room HUD (the Library room anchor is a separate image).
4. Human reviews with explicit keep/change/remove notes.
5. Create stable reusable anchors: wordmark, avatar sheet, Library reference image, icon mini-kit, common panel/button states.
6. Generate remaining screens and dark theme variants using the same anchors, not independent reimaginations.
7. Review consistency; implement actual components in React, using images as references and vetted assets as files.
8. Compare browser screenshots against approved mockups; log discrepancies and revise.

### Mockup prompt contract
For every screen provide: screen name, purpose, layout viewport, exact UI labels and values, component list in order, common theme tokens, recurring asset IDs, state shown, accessibility expectations, and a list of things **not** to add. Use realistic consistent fictional room/user data across screens. Use approved anchor art as reference.

## 7. User-experience acceptance checks

- Can a new user identify the primary action in 5 seconds?
- Is room capacity/status unambiguous?
- Is it clear when a seat is actually claimed and when a focus session is officially saved?
- Are disconnect, full-room, save failure and reconnection states understandable?
- Does light and dark mode use consistent components and visual hierarchy?
- Can primary operations work with keyboard navigation, legible labels and reduced motion?
- Are game sprites displayed sharply at target integer zoom?

## 8. Handoff to implementation

Provide a React component list, screen state inventory, design tokens (CSS variables), approved screen mockups, exact source icon assets, and world renderer requirements. Keep UI and world interaction logic separated. A screenshot is not executable UI.


## tools :
- to not make the ui look basic and bad we should use as much tools as possible 
- ex: mobbin 
- must use the design doc as reference as asource of truth t
- 