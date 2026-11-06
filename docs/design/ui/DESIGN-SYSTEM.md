# StudyAlcove design system

**Round 1 · Proposed for review**

The visitor should be able to find an available Library desk, sit, and tell when their focus time has been credited. Give those actions the clearest labels and strongest contrast. Keep the middle of the room free for the player, the desk and the route between them.

| Decision status | Scope |
|---|---|
| Already approved | StudyAlcove, the four room concepts and Library-first production. The project calls for React/TypeScript interface elements, a PixiJS world, guest entry and server-authoritative room and session state. |
| Proposed default | Every token, dimension, component treatment, animation and layout rule below. Existing palette and type choices in the visual brief are candidates for this review. |
| Requires review | Wordmark and optional pixel face, final vector and pixel icon samples, readability of the HUD over the actual Library, avatar scale and mobile playability. Product decisions about active-session pause, reconnect and retention belong with the session contract. |

Read the [visual brief](../shared/DESIGN-BRIEF.md) for the room concepts, the [screen and journey specifications](../ux/SCREENS-AND-FLOWS.md) for where to use these rules, and the [pixel art pipeline](../pixel-art/PIXEL-ART-PIPELINE.md) for source art dimensions, pivots and frame timing.

## Color and theme

Use the same semantic key in both themes. All values below are sRGB hex. At implementation, `color.surface.primary` would map to `--color-surface-primary`. Store one value per theme and let component recipes reference it. The default is **System**. An explicit Light or Dark choice takes precedence on this device. While System is selected, respond to operating-system changes.

Page, surface, text and border roles form the neutral palette. Use their warm neutrals for most of the screen so the stronger brand and status colors draw attention to an action or change.

| Token | Light | Dark | Use |
|---|---|---|---|
| `color.background.page` | `#F7F2E8` | `#192522` | Page and gutters |
| `color.surface.primary` | `#FFF9EF` | `#24332D` | Cards, inputs, resting controls, solid HUD plates |
| `color.surface.elevated` | `#FFFFFF` | `#2D3D35` | Open popover, menu, drawer, dialog |
| `color.surface.subtle` | `#ECEFDF` | `#33443B` | Grouped section with ordinary text |
| `color.text.primary` | `#26352C` | `#F2F2E7` | Titles, body, control labels |
| `color.text.secondary` | `#405347` | `#D4DFD4` | Supporting instructions |
| `color.text.muted` | `#58695D` | `#C2D0C3` | Metadata and placeholders on page/primary/elevated surfaces |
| `color.text.inverse` | `#FFFFFF` | `#192522` | Labels and glyphs on primary/destructive filled controls |
| `color.brand.primary` | `#54765D` | `#A6C6A5` | Leaf green, primary action and progress fill |
| `color.brand.secondary` | `#79573D` | `#D7B799` | Wood-toned secondary brand detail or short label |
| `color.brand.accent` | `#C28B5C` | `#E3B47E` | Warm decorative badge detail with a separate text label |
| `color.control.primary.hover` | `#405C48` | `#C0D8BC` | Hovered primary action |
| `color.control.primary.pressed` | `#314A39` | `#8DB28E` | Depressed primary action |
| `color.control.secondary.hover` | `#E2E7D9` | `#394A40` | Hover fill on secondary and tertiary controls |
| `color.control.secondary.pressed` | `#D6DECF` | `#405347` | Pressed fill, with primary text |
| `color.control.destructive.default` | `#A23E3C` | `#F3A29F` | Confirmed destructive action |
| `color.control.destructive.hover` | `#8B3532` | `#F6B9B5` | Destructive hover |
| `color.control.destructive.pressed` | `#722D2A` | `#E18F8C` | Destructive press |
| `color.border.subtle` | `#D7D8C7` | `#54665A` | Decorative card edges and dividers |
| `color.border.control` | `#6A796D` | `#97AD9A` | Essential field, checkbox and secondary control outlines |
| `color.focus.ring` | `#245DB0` | `#9AC1FF` | Keyboard focus outline against opaque chrome |
| `color.selection.fill` | `#DBE9DA` | `#344F3E` | Selected choice, tab or text selection |
| `color.selection.ink` | `#284B34` | `#DEEEDD` | Selected label, checkmark or active underline |
| `color.status.success` | `#357A55` | `#91D4A8` | Saved or connected, check icon + text |
| `color.status.warning` | `#A56620` | `#F0C184` | Attention icon on page/primary/elevated surfaces |
| `color.status.warningText` | `#83501B` | `#F0C184` | Warning text such as “Reconnecting” |
| `color.status.error` | `#B24743` | `#F3A29F` | Invalid field, failed request, error icon and copy |
| `color.status.info` | `#315F86` | `#A1C9ED` | Informational hint, inline link or icon |
| `color.disabled.fill` | `#E4E6DA` | `#35453C` | Unavailable control |
| `color.disabled.ink` | `#576457` | `#B4C2B4` | Disabled label or glyph |
| `color.loading.track` | `#E0E5D9` | `#35453C` | Progress track or static skeleton fill |
| `color.tooltip.fill` | `#26352C` | `#F2F2E7` | Tooltip plate |
| `color.tooltip.ink` | `#FFFFFF` | `#192522` | Tooltip label |
| `color.overlay.scrim` | `#18231D66` | `#00000080` | Modal backdrop, 40% / approximately 50% opaque |

**Recipes.** Primary control default and loading progress fill both reference `color.brand.primary`. Secondary defaults to primary surface, primary text and control border. Tertiary rests on the containing surface with primary text. A disabled control uses the disabled pair at full opacity. A pending filled button keeps its enabled fill and inverse label while its label describes the operation. Reserve the loading track for progress bars and reserved content space. Keep status copy on page, primary or elevated surfaces. For example, “Desk 03 is occupied” uses text and a seat icon, and offers “Find another desk.”

Theme changes affect the DOM chrome, including plates behind text, dialog backdrops, tooltips and native form controls. World lighting, indexed sprites, preview illustrations and room thumbnails use the authored scene palette in both themes. Tie a Night Owl lamp or Library daylight change to scene metadata. Give a world marker a fixed pixel keyline and mirror its meaning in the accessible desk list.

**Mapping the earlier shorthand.** Earlier names take the same `color.` prefix. Map `bg / surface / surfaceElevated` to `background.page / surface.primary / surface.elevated`. Map `primary / primaryHover / accent` to `brand.primary / control.primary.hover / brand.accent`, and `text / muted / border` to `text.primary / text.muted / border.subtle`. Success, warning and error map to their `status.*` roles, and `focus` to `focus.ring`. Use `border.control` for essential input edges and `status.warningText` for warning captions.

### Contrast check

Ratios below were calculated from the hex pairs using linearized sRGB relative luminance, `(lighter + 0.05) / (darker + 0.05)`. Values are displayed to two decimals. For rows listing more than one pair, the table gives the lowest ratio in each theme. Target at least 4.5:1 for ordinary text and 3:1 for essential graphics, input boundaries and the ring against its adjacent surface. [Text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) · [Non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

| Foreground / background | Light | Dark |
|---|---:|---:|
| Primary text / page, primary surface, elevated surface | 11.56 | 10.18 |
| Secondary text / same three surfaces | 7.39 | 8.36 |
| Muted or placeholder text / same three surfaces | 5.24 | 7.16 |
| Inverse label / primary default, hover, pressed | 5.09 | 6.69 |
| Inverse label / destructive default, hover, pressed | 6.38 | 6.40 |
| Primary text / secondary hover and pressed fills | 9.34 | 7.32 |
| Selected ink / selection fill | 7.77 | 7.45 |
| Success, warning **text**, error and info / page, primary, elevated | 4.63 | 5.73 |
| Control boundary / page, primary, elevated, secondary hover and pressed | 3.33 | 3.44 |
| Focus ring / page, primary, elevated | 5.76 | 6.25 |
| Disabled label / disabled fill | 4.94 | 5.47 |
| Progress fill / loading track | 3.97 | 5.44 |
| Tooltip label / tooltip plate | 12.90 | 14.02 |

Two specific corrections to the brief matter. Light warning amber on a card gives **4.43:1** for text, so use the darker warning ink (**6.41:1**). The subtle border on the primary card surface gives **1.38:1 light / 2.16:1 dark**. The stronger control border gives **4.39:1 / 5.52:1** in the same place. Use accent ochre solely as decoration. Measure final rendered labels and focus rings again over real HUD plates, in both themes, with forced colors and zoom.

## Typography

| Family token | Stack | Use |
|---|---|---|
| `font.ui` | `"Nunito Sans", system-ui, "Segoe UI", sans-serif` | Wordmark fallback, all reading and interaction |
| `font.numeric` | Same as UI, with tabular lining figures | Timer, capacity and study time. Keep a stable five-character timer slot. |
| `font.pixel` | `"Press Start 2P", "Courier New", monospace` | Optional wordmark or one very short decorative room label beside readable text |

| Role | Family, weight | Desktop size / line | Phone size / line | Letter spacing |
|---|---|---|---|---|
| Wordmark | UI 700 by default | 24 / 30 | 20 / 25 | −0.02em |
| Page heading | UI 700 | 32 / 40 | 24 / 30 | −0.02em |
| Section heading | UI 700 | 24 / 30 | 20 / 25 | −0.01em |
| Card heading | UI 700 | 20 / 25 | 20 / 25 | 0 |
| Body or form value | UI 400 | 16 / 24 | 16 / 24 | 0 |
| Button, nav or field label | UI 600 | 16 / 24 | 16 / 24 | 0 |
| Supporting text | UI 400 | 14 / 21 | 14 / 21 | 0 |
| Metadata | UI 600 | 12 / 18 | 12 / 18 | +0.01em |
| Timer or leading stat | Numeric 700 | 32 / 40 | 24 / 30 | 0 |
| Optional pixel lettering | Pixel 400 | 16 / 24 | 16 / 24 | 0 |

Sizes are design pixels at the default 16px root. Specify text in rem and line heights proportionally so user text scaling works. Tablet uses desktop type unless the content column is narrow. Allow 45–65ch for prose, up to 70ch, and 48ch for instructions in a form. Give the wordmark an accessible name. Keep timer labels, important actions, chat and status messages in the UI face even if the pixel sample is approved.

## Spacing, layout and the room viewport

`space.n` is `4 × n` CSS px, for integer n from 0 through 16. Common steps are 4 for icon alignment, 8 for label/field spacing, 12 for small clusters, 16 for grid gaps, 24 for cards and sections, 32 for page gutters, and 48 for distinct page sections. Use 44px minimum interactive width and height, including the hit area around a 16–24px glyph. Keep adjacent touch targets 8px apart where possible.

| Layout rule | Desktop ≥1024px | Tablet 640–1023px | Phone <640px |
|---|---|---|---|
| Page | Centered content up to 1200px, 32px outer gutters | 24px gutters | One column with 16px gutters |
| Shell | 64px top nav, identity left, destinations/actions right | 64px nav, collapse secondary links | 56px nav, expandable labelled menu |
| Room browser | Fill usable width with columns ≥280px and 16px gaps, fitting up to four columns at 1200px | Same fit rule, generally two | One fluid card |
| Room card | 16:9 preview then name, mood, occupancy/availability and join. 24px body padding. | Same | 16px body padding |
| Side panel | 320px end drawer when camera has space | End drawer over reserved edge, otherwise sheet | Bottom sheet, max 70dvh, scroll inside |
| Dialog | Centered, 480px standard, 640px for avatar editor | Same sizes, limited to width minus 32px | 16px exterior gap. Stack actions when labels wrap |
| Page footer | After public-page content in normal flow | Same | Same. Room uses the HUD action rail |

Dialog padding is 24px (phone 16px). Keep 16px between fields and 24px between content and actions. Cap dialog height at viewport height minus 32px and safe-area insets, with a scrolling body. Buttons have 16px horizontal and 8px vertical padding with 44px minimum height. Inputs/selects are at least 44px high with 12px horizontal padding. Heights are minima. Let labels wrap and fields grow. Wrap long names, URLs and errors anywhere if necessary. If room names need a two-line preview, expose the full name on its destination and accessible name. Keep occupancy and primary actions readable. Test a 320px viewport plus enlarged text.

### The world and its controls

- Use the desktop 16:9 Library illustration to review composition. Size the live room to its container. The camera computes a logical view in art pixels, uses nearest-neighbor sampling and snaps camera positions to the source grid. Prefer 3× or 4× integer zoom. Step down to 2× or 1× when space is limited. Center and letterbox any remainder or adjust the logical camera window around the controlled avatar. Preserve square pixels and reachable desks at each size.
- Give HUD rails a 16px inset (8px on phones) plus device safe-area insets. Top left holds room/status and top right holds presence/preferences. Bottom center holds the timer and bottom right holds object list/chat where available. Use solid plates. Start with 56px reserved top and 72px bottom, then measure the actual rail bounds after wrapping. Protect the central 60% of viewport width and 50% of height from persistent panels.
- Anchor a desk prompt to the projected seat rectangle, flip/clamp it at edges, and keep it clear of the controlled avatar, desk and focused element. If either rail wraps onto the player or the drawer clips a desk, move controls into a DOM rail outside the canvas, or show the desk detail below the viewport. On a phone, prioritize room identity, compact timer and “Desks.” Move the rest into the labelled menu. Open one contextual sheet at a time.
- React owns HUD, dialogs, accessible object list, status announcements and input focus. PixiJS owns tiles, collision-aligned markers, avatars and visual state. Both read the same room snapshot. Choosing “Desk 03 · Window” in the keyboard list sends the same validated interaction intent as using its world target. Selecting it can show a route or request a supported interaction, subject to the same movement, range and seat-availability rules.
- Offer a direct path to the object list before the canvas. Capture movement keys only while game controls have focus. Tab can leave the world. Opening any text field, menu or dialog suspends movement input. Support browsing, the object list and normal scrolling on phones. On-screen movement and tap-to-walk need a separate playtest and product decision.

## Icons, panels and elevation

Use one rounded outline family (Lucide is the proposed choice) in React. Use a 24-unit viewBox, 2-unit rounded strokes, centered on a square box. Sizes are 16px with metadata, 20px beside a button label and 24px for standalone navigation. Use the foreground text token or the matching status ink. Hover and press change the containing control's fill. A functional icon-only control gets an accessible verb and object such as “Mute room audio” plus a matching tooltip. Paired icons are decorative to assistive technology.

| Context | Proposed icon vocabulary |
|---|---|
| Nav, room, avatar | House, DoorOpen, UserRound |
| Focus, break, stats | Timer, Coffee, ChartColumn |
| Chat, settings, audio | MessageCircle, Settings, Volume2 / VolumeX |
| Achievement, connection | Award, Wifi / WifiOff. Pair with “Connected”, “Reconnecting” or “Offline” |
| Edit, close, back, confirm, cancel | Pencil, X, ArrowLeft, Check, X with a visible “Cancel” label in dialogs |

Use the custom 16×16 or 24×24 indexed symbols on the world layer for seat markers, focus, emotes and other diegetic cues. Use the same world glyph in an item preview at integer scale if the UI is describing that game object. Keep the editor, HUD and menus on the vector control set. See the [art queue](../shared/ASSET-MANIFEST.md) for the planned world icons.

| Token | Value and application |
|---|---|
| `radius.none / sm / md / lg / pill` | 0px pixel frame, 8px control/tooltip, 12px card/menu, 16px dialog/drawer, 999px switch track |
| `stroke.divider / control / frame` | 1px subtle separator, 1px essential control border, 2px optional stepped decorative frame around a world preview |
| `focus.width / offset` | 3px solid focus ring, 2px gap matching the opaque containing surface. Apply to every keyboard target. Keep clear of scroll clipping. Use system Highlight in forced colors. |
| `shadow.panel` | Light `0 2px 6px #26352C14`, dark `0 2px 6px #00000040`. Cards may stay flat. |
| `shadow.overlay` | Light `0 8px 24px #26352C29`, dark `0 8px 24px #00000066`. Menu, popover, modal above opaque plate. |
| `layer.world / hud / popover / scrim / dialog / notice` | 0 / 10 / 20 / 30 / 40 / 50 in the room stacking context. Put notices about a modal inside that modal's accessible scope. |

Reserve the scrim for a modal. Background content becomes inert while it is open. A non-modal popover uses an 8px anchor gap and 8px viewport clearance. A tooltip uses the inverse plate, 8px × 12px padding, 240px max width and supporting type. Use flat opaque panel fills and keep outlines clear at both themes.

## Interaction states

Use native form semantics where practical. If Base UI primitives are chosen later, apply these exact recipes to their open, highlighted, checked, invalid and disabled states. One pending request suppresses duplicate activation. Keep focus on its trigger while possible. Carry feedback in text and shape alongside color.

| Control | Rest, hover and press | Other visible states and behavior |
|---|---|---|
| Primary button | Brand fill + inverse ink, with primary hover/pressed fills | Pending keeps the width stable and shows the action in progress (“Joining…”). Completion moves to the destination or gives inline confirmation. |
| Secondary button | Primary surface + control border and secondary hover/pressed fills | For alternatives such as “Choose another room.” All buttons share focus/disabled rules. |
| Tertiary / icon button | Bare label or named glyph on plate, with secondary hover/pressed fill | Toggle uses selected fill + check or glyph change and explicit state. Inline links remain underlined. |
| Destructive button | Destructive fill + inverse ink with its two state fills | State the consequence (“End focus session”). Pending until confirmed. Recovery and retry remain visible on failure. |
| Text input | Primary surface, persistent label, control border. Hover darkens/lightens border to text.secondary | Focus ring. Invalid adds error outline, icon, field-specific message and `aria-invalid`. Validated success uses check plus “Saved” when meaningful. Associate help/error via `aria-describedby`. Preserve typed text after errors. |
| Select | Same field recipe. Trigger shows text and chevron | Open popup with current value checked, active option visibly highlighted. Prefer native select. Custom listbox supports arrows, Home/End, typeahead, Enter and Escape. |
| Checkbox / switch | Whole label is a ≥44px target. Off uses control outline with empty checkbox or thumb at start. Hover/press uses secondary fill on label area. | Checked uses brand fill with inverse check, or thumb at end. Space toggles. Use checkbox for multi-select and a named switch for an immediate binary preference. Announce checked state. |
| Tab list | Text on surface, hover/press secondary fill | Active gets selected ink, 2px underline and `aria-selected`. Focus remains distinguishable. Arrows/Home/End move focus. Enter/Space activates when content loads. Tab enters panel. |
| Card / room card | Informational card stays flat. Put a single named join control on an actionable card, with the button treatment above. | Show “3 of 10 online”, “Full”, “Private” or “Coming soon” in text. Reserve image space while loading. Give disabled joining a reason. Use the browser’s “Join by code” control for code entry. |
| Dialog / modal drawer | Elevated plate, title, visible close action and scrim | Move focus to heading or first safe action. Contain Tab and Shift+Tab, Escape requests close. Guard meaningful unsaved edits. Restore focus to opener or next logical target after navigation. |
| Non-modal popover | Opaque elevated plate next to trigger, distinct open trigger | Set expanded state. Escape closes and returns focus. Outside press closes. Only trap focus when the surface is explicitly modal. |
| Tooltip | Open on pointer dwell (400ms) or keyboard focus (immediately) | Remain open while hovered/focused. Escape dismisses. Touch users get a persistent name/help path. Put interactive content in a popover. |
| Menu | Elevated plate, named trigger and expanded state | Arrow keys/Home/End move between items. Enter/Space activates, Escape returns. Visible row highlight. Check selected option. Retain reason text for unavailable actions. |
| Toast / inline notice | Status icon, text, optional action on solid plate | Announce once in a polite status region. Benign confirmation may dismiss after 6s, paused on focus/hover. Keep actionable failures and reconnect notices visible until addressed. Avoid stealing focus. |
| Progress | Brand fill on loading track plus labelled value or indeterminate status | Use determinate values only for known totals. Expose accessible name, value and max when applicable. Failed load replaces busy state with reason and retry. Static skeletons are decorative. |
| Navigation | Named links, hover/pressed fill, focus ring | Current destination has underline and `aria-current="page"`. Mobile disclosure reports expanded state. Back restores previous destination and focus where possible. |
| Desk / timer controls | Offer “Sit here” for an available desk, show “Taking seat…” while pending, then offer “Start focus” after confirmation. | Active, awaiting confirmation, completed, interrupted and on-break each have text. At zero show “Checking your session…” until server acknowledgement, then show credited time such as “25 minutes added · Library”. Retry against the same session. Offer active pause only if supported. |
| Avatar option | Named single-select swatches/tiles on primary surface, with secondary fill on hover or press | Selection uses filled check, selected outline, name and radio semantics. Arrow keys move in a group. Locked options name their requirement. Save confirmation uses the acknowledged outfit. Failure preserves the draft. |

Press Enter on links and Enter/Space on buttons. Use a visible `:focus-visible` outline independent of selection, invalidity and hover. Disabled controls use the disabled pair and an adjacent reason when consequential. Escape never sends a destructive action. After invalid submission, focus the first invalid field. Use polite announcements for meaningful transitions, a persistent inline error for failed actions and an immediately announced alert only when interruption is warranted. Keep per-second timer ticks out of live regions.

## Motion

`ease.standard` = `cubic-bezier(.2,0,.2,1)`, `ease.enter` = `cubic-bezier(.2,.8,.2,1)`, `ease.exit` = `cubic-bezier(.4,0,1,1)`. Use non-bouncing timing curves. Durations are UI milliseconds. The renderer owns sprite frames and interpolation.

| Interaction | Duration, curve and visible response |
|---|---|
| Hover, pressed, release | `duration.fast` 120ms standard fill change. Press may move contents down 1px. Release returns them. |
| Page change | `duration.normal` 180ms enter opacity on incoming chrome after navigation. Focus destination heading. |
| Dialog or sheet | `duration.slow` 220ms enter, opacity and ≤8px travel. Close in 160ms exit. Move/restore focus as part of the open/close action. |
| Menu or popover | 120ms enter with opacity and ≤4px travel, 120ms exit. Keyboard input responds immediately. |
| Notification | 160ms enter, 120ms exit. Completion shows a single check plus credited minutes after acknowledgement. Optional sound follows audio preference. |
| Loading | Optional 900ms linear spinner cycle beside “Joining…”. Keep space reserved. Determinate bars ease between actual updates in 120ms. |
| Join / leave room | 180ms enter/exit on UI plate. Hold the join status through snapshot and artwork preparation. Move focus into the ready room. Leaving returns focus to the browser. |
| Reconnection | Show persistent status immediately. Fade status glyph in 120ms. Announce “Reconnected” once after sync. Keep retries and elapsed time textual. |

With system reduced motion **or** an app request to reduce motion, use 0ms for travel, fades, presses and progress interpolation. Replace spinners with a static icon plus status text. Disable nonessential camera smoothing and ambient looping where appropriate while preserving meaningful position and action changes. Reserve QA of avatar movement, action frame rate and camera behavior for the pixel pipeline and renderer playtest.

## What to check at each review

1. **Round 2, three static desktop light mockups.** On Landing and Room Browser, locate the room entry action and read Library occupancy. On the Library HUD, find Robin, window Desk 03 and the current focus status. Check margins and focus-ring clearance. Record keep/change/remove against a particular token, component or screen state.
2. **Rounds 3–4, anchor approval and screen variants.** Review the wordmark, world markers, character scale and control samples. Inspect phone-width compositions and dark variants after the desktop review. Confirm important text stays on opaque plates and the HUD can expose a desk without covering Robin.
3. **Round 5, interactive checks.** At 320px and with enlarged text, open the desk panel and object list, then reconnect. Check wraps, focus, announcements, both themes, forced colors and reduced motion. Verify “Joining…”, credited minutes and reconnection remain distinguishable. The ratios above validate token pairs. Playability, rendered contrast and responsive behavior require this later test.

# tooling :
- shadcn/ui — Core UI foundation

Buttons, dialogs, forms, tabs, tooltips, cards, and other reusable React components. You own the component source, so we can customize it to match StudyAlcove rather than being stuck with a stock appearance.

Use for: Application interface and reusable components.
8bitcn/ui — Pixel-style component inspiration

Retro buttons, dialogue boxes, cards, menus, and even game-style interface blocks. The library includes customizable React components and an optional MCP integration for coding assistants. 
8bitcn/ui+1


Use for: In-game panels, HUD, dialogue boxes, and themed menus.
Pixelarticons — Consistent icon family

Over 1,000 free icons on a consistent 24×24 pixel grid, available as React components and SVG files. There's also an MCP integration. 
Pixelarticons+1


Use for: Timer, settings, sound, chat, rooms, achievements, and navigation.
Realtime Colors — Colors and typography

Preview color combinations on a realistic website, including light/dark modes, before assigning semantic tokens. It also provides a Figma plugin. 
Realtime Colors+1


Use for: Brand palette and theme exploration.

Storybook — Component testing and documentation

Lets us build and preview each component independently, including hover, disabled, loading, and error states, without needing the whole game running. 
Storybook docs

Use for: Visual review, component states, and regression testing.

Motion for React — Interface animation

Useful for modal transitions, subtle button feedback, room-card entrances, and switching panels. It also provides an official /motion coding-agent skill. 
Motion for React
| Tool | When to use it | What to bring back |
|---|---|---|
| **Mobbin** | When a flow has an unresolved question, such as where a returning guest should enter a room code. | One or two reference links and a sentence explaining which interaction would help a StudyAlcove guest. |
| **21st.dev MCP** | When exploring a specific component, such as a room card or avatar picker. | One candidate treatment adapted to StudyAlcove’s tokens. Show its keyboard focus, narrow layout and unavailable state. |
| **Taste Skill** | After drafting Landing, Room Browser and the Library HUD. | A short critique naming the screen, the visible problem and one proposed change. Record the exact skill name and source here once selected. |