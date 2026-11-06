# StudyAlcove · Reusable UI components

**Proposed default · Round 1.** These are responsibilities and proposed React inputs for design review. Introduce each component at its first screen. The MVP needs one shared Button, one Dialog and a small room view. Chat, account and inventory controls enter with their respective features.

The general UI layer contains DOM controls and product views. The game-world integration layer connects those views to a room snapshot and renders its world through PixiJS. In both layers, interactions with text, focus, forms and assistive technology belong in the DOM. [Visual states and tokens](DESIGN-SYSTEM.md) · [Screen placements and release scope](../ux/SCREENS-AND-FLOWS.md)

## General UI · shared controls

| Component | Purpose and main props | Variants | Interaction and state |
|---|---|---|---|
| `Button` | Submit a form or invoke one command. `children, type, variant, disabled, busy, onClick`. | Primary, secondary, tertiary, destructive. An ordinary link handles navigation. | Hover, pressed, focus-visible, disabled, pending. During a request show the action in progress (e.g. “Joining…”), preserve its width and suppress repeat activation. Place actionable errors beside the control. |
| `IconButton` | Compact named action in a toolbar. `label, icon, pressed?, expanded?, controls?, onClick`. | Action, toggle, disclosure. | Reuse button states. Expose the action name on all input devices, current toggle state when applicable, and expanded state for a disclosure. |
| `Card` | Group related content. `heading?, children, footer?`. | Flat or framed. | A static card takes no focus. Put the actual link or button inside. A selected option uses its native radio control. |
| `Dialog` | A labelled modal task. `open, title, description?, onClose, initialFocus?, children`. | Centered, wide customizer, compact sheet. | Opening moves focus into the dialog, Tab stays within it, Escape cancels the current step, close returns focus. Rejection stays inline and preserves entered values. |
| `Popover` | A small contextual panel. `trigger, open, onOpenChange, label, children`. | Desk information, compact picker. | Anchor to trigger and flip at edges. Escape and outside activation close. Keyboard dismissal restores trigger focus. A touch sheet can reuse the same contents in Dialog. |
| `Tooltip` | Supplemental description for an already named control. `target, description`. | Above or below as space permits. | Appears on hover or keyboard focus, remains while hovered and dismisses on Escape. Required instructions are visible in the parent panel. |
| `Toast` | Brief result after a local action. `message, tone, onDismiss`. | Information, success. | Announce once, keep it out of the tab order unless it contains a dismissal button. Persistent errors, reconnect instructions and credit decisions belong in the relevant panel. |
| `Field` | Associate label, hint and error with a native control. `id, label, hint?, error?, children`. | Text input, select, checkbox, switch, range. | Native keyboard behavior, focus ring, invalid message and retained value after rejection. Connect hint/error IDs to the control. |

Use ordinary links, fieldsets, lists, progress elements and buttons directly for navigation, progress, option groups and simple tabs/menus. Add shared wrappers only if repeated behavior justifies them. If a composite primitive is adopted, apply the documented focus, dismissal and selection rules. Selecting a UI library requires review.

## General UI · product views

| Component | Purpose and main props | Variants | Interaction and state |
|---|---|---|---|
| `AppShell` | Landmarks and focus order. `navigation, currentDestination, children, footer?`. | Page or room. | Page navigation moves focus to the destination heading. The room shell gives keyboard users direct access to room actions. TopNav can remain local to AppShell. |
| `RoomCard` | Compare a room and enter its join flow. `room, availability, occupancy?, preview, onJoin`. | Playable public, restricted with valid access, concept preview. | A join action appears when available. Handle full, offline and unknown counts explicitly. Keep a preview’s status visible. Private rooms shown here require listing permission. |
| `AvatarPreview` | Present the chosen avatar from approved frame layers. `appearance, facing, description`. | Setup preview, small portrait. | Static DOM image/stack at integer scale. Preserve frame and pivot when an option changes. Missing layers fall back to an available base and identify the unavailable option. |
| `AvatarCustomizer` | Edit a draft appearance. `options, value, onChange, onSave, saving, error?`. | Guest presets or full editor. | Group radio options by category, label colors in words, retain the draft on failure. Cancel discards the draft. Offer validated combinations only. |
| `SessionSummary` | Explain a session result. `outcome, creditedMinutes?, retry?, onReturn, onHistory?`. | Checking, credited, interrupted, cancelled, timed out, save failed. | Credited minutes appear after durable confirmation. Pending and failure keep a safe route back to the same result. Repeated responses update one summary. |
| `ProfileStats` | Show totals and recent completed sessions. `totals, sessions, period?, loadState, onRetry`. | MVP recent activity, V1 history/streaks. | Loading, empty, ready and failed. Distinguish zero minutes from unavailable history. Pair charts with equivalent text or rows. |
| `SettingsPanel` | Edit supported preferences. `section, preferences, capabilities, onChange, saveState`. | Appearance, audio, controls, privacy, account. | Use a single panel with sections. Changes announce their result and errors identify the affected setting. Account controls depend on an identity model. |

An empty state can begin as a heading, explanation and optional existing Button in its owning view. MVP can inline a room status label in RoomCard. Keep a single implementation for the former names PrimaryButton/SecondaryButton (Button variants), Modal (Dialog), and ConnectionBadge (ConnectionIndicator).

## Game-world integration · room components

| Component | Purpose and main props | Variants | Interaction and state |
|---|---|---|---|
| `RoomCanvas` | Own the PixiJS scene, camera and input surface. `map, snapshot, selfId, viewport, inputEnabled, onMoveIntent, onInteract`. | Loading shell, live scene, last confirmed view during reconnection. | Apply membership/poses after snapshot. Forward movement only while its controls own focus. Render/asset failure exposes DOM recovery and the interaction list where supported. Dispose renderer, listeners and textures owned by this instance on exit. |
| `GameHUD` | Arrange DOM controls around the visible world. `room, connection, self, seats, session, capabilities, actions`. | Desktop perimeter, compact control bands. | Keep controls operable while canvas input is suspended. Gate commands by connection and capability. The same seat list supports keyboard, pointer and touch. |
| `ConnectionIndicator` | Explain whether room actions are available. `phase, reason?, onRetry?, onLeave`. | Small HUD label, persistent recovery panel. | Connecting, synced, reconnecting, offline, rejected. Announce a phase change once. Keep retry progress visible. An open socket still awaits a fresh room snapshot. |
| `PlayerStatus` | Present the local player's activity. `displayName, activity, seatLabel?`. | Standing, seated, focusing, on break. | Read-only text and icon, refreshed from confirmed state. Announce meaningful local transitions separately from frequent peer movement. |
| `SeatPrompt` | Inspect or claim a seat by stable ID. `seat, selfId, canInteract, pending, onClaim, onRelease`. | Anchored panel or row in the accessible desk list. | Free, occupied by self/other, unavailable, claim pending, rejected. Both entry points use the same validation and show who holds the seat when known. |
| `FocusTimer` | Show time and valid actions. `sessionState, endsAt, serverClockOffset, allowedActions, pending, onAction`. | Desk setup, compact HUD, post-session break. | Idle, starting, active, verifying, ended, interrupted. Render remaining time from server timing. Display 00:00 while awaiting the result. Announce phase changes and expose remaining time on request. |
| `ChatDrawer` | View and send nearby messages when available. `messages, canSend, muted, connection, onSend, onMute`. | Collapsed launcher, nonmodal dock, modal sheet. | Empty, ready, sending, failed, rate-limited. Preserve unsent text, restore focus on close, and keep movement keys inactive during composition. A connection recovery never automatically resends a message. |

## One seat, two ways to reach it

1. Robin reaches Desk 03 in the Library or chooses **Desk 03 · Window** from **Desks**. Each path opens the same SeatPrompt for the same server seat ID. Outside interaction range, the list gives Robin the direction and distance to the desk plus labelled directional step buttons. Each step uses the room's normal validated move. On arrival, both entry points enable **Sit here**.
2. **Sit here** sends one intent. While pending, both entry points display **Taking seat…**. Until the authoritative reply, the renderer keeps the last confirmed pose. If another participant claimed it first, the panel offers another available desk.
3. A successful claim enables **Start focus**. The confirmed start supplies the session ID and end time to FocusTimer. The client can draw a countdown between messages. At zero the display changes to **Checking your session…**.
4. A durable completion for that session updates SessionSummary and history once. After a timeout or reconnect, re-read session status and use the same logical request for a permitted retry. If the server reports cancellation or interruption, show that reason.

One room owner in React coordinates the connection, snapshot, pending commands and accessible views. PixiJS consumes that state and emits user intent. Menus mounting or a UI theme change should never initiate another join, change a world palette or restart a timer. Wire formats and final command names belong to the backend milestone.
