# StudyAlcove — Visual Design Brief

**Status:** Proposed visual baseline, ready for concept review (not final art approval)  
**Product:** A cozy multiplayer pixel-art study space — *A little place to focus, together.*  
**Primary delivery:** Desktop-first responsive React + TypeScript UI; PixiJS 2D room renderer.  
**Art direction:** Classic 16-bit cozy RPG, strictly top-down / 3/4 top-down game perspective (no isometric projection).

This brief records the shared visual direction and its original palette candidates. Maintain exact interface tokens in the [UI design system](../ui/DESIGN-SYSTEM.md), player behavior in [screens and flows](../ux/SCREENS-AND-FLOWS.md), and source-art specifications in the [pixel-art pipeline](../pixel-art/PIXEL-ART-PIPELINE.md). The [handoff guide](UI-UX-AND-PIXEL-ART.md) explains where these decisions meet.

## 1. Experience goals

- Feel warm, quiet, welcoming, lightly nostalgic, and social without being distracting.
- Let a first-time visitor join a room, sit down, and start focusing quickly.
- Make presence and progress visible at a glance without noisy gamification.
- Character, furniture, tiles and UI icons must look like they belong to **one** coherent game.
- Accessibility and usability outrank decorative fidelity. Text should be readable; focus controls should be obvious.

## 2. Approved world concepts

| Room | Mood | Signature objects | Gameplay layout | First production priority |
|---|---|---|---|---|
| **Library** | Warm amber light, wood, quiet | Bookshelves, reading lamps, study carrels, plants, clock | Solo desk rows, clear walkable aisle, 8–12 seats | **P0 — playable first** |
| **Café** | Soft bustle, amber/terracotta | Counter, cups, pastries, hanging lights, round tables | Small-group tables plus window bar, 8–12 seats | **P1 — playable second** |
| **Night Owl Loft** | Indigo, rain, lamp glow | Rainy windows, monitors, floor cushions, task lights | Computer desks, quiet seating, 6–10 seats | **P1 concept / P2 playable** |
| **Greenhouse** | Gentle daylight, leafy greens | Vines, glass panels, planters, timber benches | Open sightlines, garden tables, 6–10 seats | **P1 concept / P2 playable** |

**Initial art deliverable:** one approved concept illustration for *each* room; an actual buildable tilemap, tileset, props and interaction metadata for the Library first. Concept art is **not** the runtime room map.

## 3. Visual system (proposal; finalize after first visual review)

### Game art rules
- 16-bit-inspired handcrafted pixel aesthetic: pixel clusters, deliberate 1-pixel outlines where appropriate, restrained shading, no airbrush gradients.
- Logical tile size **16×16 art pixels**, with display magnification typically **3× or 4×** (integer scaling); default runtime room logical canvas is sized to fit camera needs, not hardcoded image pixels.
- Character base **16×24 logical pixels** within a **24×32 transparent frame** (provisional; validate visual readability before production). Foot anchor consistent at `(12, 29)` on that frame. All hairstyles/outfits follow the same frame and pivot.
- Orthographic 3/4 top-down view: tops of desks visible, character directions north/south/east/west. No perspective/scale changes from room to room.
- Only integer coordinates in source pixel art. No smooth resampling, rotated sprites, blurred glow painted into functional sprites, or mixed pixel-grid sizes.
- Use lighting overlays in the renderer for ambient effects **outside** indexed pixel sprites when needed.

### UI design tokens — light mode

| Role | Hex | Usage |
|---|---|---|
| Background | `#F7F2E8` | Page base |
| Surface | `#FFF9EF` | Cards and panels |
| Elevated surface | `#FFFFFF` | Modal and popover backgrounds |
| Primary | `#54765D` | Main action buttons |
| Primary hover | `#405C48` | Hovered action |
| Accent | `#C28B5C` | Warm highlights, achievements |
| Text primary | `#26352C` | Headings, body |
| Text muted | `#58695D` | Descriptions |
| Border | `#D7D8C7` | Card divisions and fields |
| Success | `#357A55` | Completed session |
| Warning | `#A56620` | Reconnecting / attention |
| Error | `#B24743` | Failed action / disconnect |
| Focus ring | `#245DB0` | Keyboard-focus visibility |

### UI design tokens — dark mode

| Role | Hex | Usage |
|---|---|---|
| Background | `#192522` | Page base |
| Surface | `#24332D` | Cards |
| Elevated surface | `#2D3D35` | Modals |
| Primary | `#A6C6A5` | Main actions |
| Primary hover | `#C0D8BC` | Hovered action |
| Accent | `#E3B47E` | Highlights |
| Text primary | `#F2F2E7` | Headings and body |
| Text muted | `#C2D0C3` | Descriptions |
| Border | `#54665A` | Outlines |
| Success | `#91D4A8` | Completed session |
| Warning | `#F0C184` | Attention |
| Error | `#F3A29F` | Error |
| Focus ring | `#9AC1FF` | Keyboard focus |

These colors are the original web-interface candidates. Use the measured light and dark pairings in the [UI design system](../ui/DESIGN-SYSTEM.md) for controls and text. The [pixel-art pipeline](../pixel-art/PIXEL-ART-PIPELINE.md) defines the separate indexed palette for sprites.

### Typography
- **UI sans:** `Nunito Sans` (or system sans fallback): warm yet legible. Avoid pixel body text.
- **Pixel title face:** optional `Press Start 2P` in very limited short headings/logo only; use a readable alternative if it is too dense.
- Suggested type scale: 12/14/16/20/24/32 px; body 16 px, secondary 14 px, small metadata 12 px.
- Weights: 400 body, 600 labels, 700 headings. Line height: 1.45–1.6 body; 1.15–1.25 headings.

### Spacing, shapes, depth
- 4px base grid: 4 / 8 / 12 / 16 / 24 / 32 / 48 spacing tokens.
- UI corners: 8px small controls, 12px cards, 16px larger panels; game sprite silhouettes remain pixel-accurate.
- Borders: 1px regular UI; optional 2px pixel-border variant for decorative in-room overlays.
- Shadows: subtle, low-opacity, single-direction shadows. Do not use diffuse effects on sprites.
- Typical desktop content width 1200px; responsive layouts; the room viewport is dominant.

### Iconography, motion and states
- UI: one consistent clean rounded outline icon family (e.g. Lucide) outside the game world.
- In-game: custom 16×16 or 24×24 indexed pixel icons (timer, desk, chair, message, focus, achievements, edit, volume, settings).
- UI button motion: 120–180ms transitions; panels 180–240ms; honor `prefers-reduced-motion`.
- Avatar walk: provisional 4 frames per direction, 8 fps; idle 2 frames, 2 fps; sit and focus 2–4 frames. All values subject to animation review.
- Component states required: default, hover, pressed, keyboard focus, disabled, loading, success/error; never convey state by color alone.

## 4. First-review visual anchors

Produce these **before** the entire asset library:
1. **Library composition:** one 16:9 desktop overview with obvious paths, desks and readable seat locations.
2. **Character turnaround:** base character in four directions plus hair/outfit layering proof, on transparent uniform grid.
3. **In-room UI:** library game view with overlay for timer, player status, chat button and room name.
4. **Logo / wordmark:** StudyAlcove text, one small recognizable pixel mark; transparent output.
5. **UI mini-kit:** light and dark panel, primary/secondary buttons, icon sample, timer, focus state.

Review all five as a set: perspective, pixel scale, character size relative to furniture, palette, legibility and personality. Freeze approved anchors; use them as image references for all follow-up generations.

## 5. Consistency contract

- Reuse approved anchor art, colors, outlines, tile size, character proportions, and UI typography in every downstream prompt.
- Screens are **mockups**, never shipped as flattened interactive interfaces. Build UI as actual React components.
- Each reusable asset must exist as a stable, independently addressable source file; do not re-extract the same button/icon from separate screenshots.
- Avoid unintended faces on props, new mascots, random extra navigation, exaggerated gradients, illegible pixel text or different camera angles.
- Always record prompt, seed/settings if available, source anchor references, reviewer notes and output filename.

## 6. Review gates

- **Gate A — Direction:** Library composition, avatar, in-room screen approved as a coherent trio.
- **Gate B — Anchor assets:** logo, reference base avatar, furniture samples and UI mini-kit approved.
- **Gate C — Production quality:** alpha cleanliness, fixed grid, palette bounds, frames/anchors, collision alignment and animation previews pass checks.
- **Gate D — Screens:** UI flows coherent in both themes, keyboard and mobile behaviors considered.
- **Gate E — Handoff:** individual sprite PNGs / packed atlases + metadata, tilemap JSON, token definitions and component specs are ready for implementation.

## 7. Explicit exclusions from this design round

No fully finished multiplayer implementation, backend rewrite, animated GIF as the sole source of animation frames, or four complete tilemaps before the Library kit is validated. Skip unapproved cosmetic features and generated stock-photo elements.

See the [UX direction](../ux/DESIGN-DIRECTION-AND-UX.md) for user journeys and the [asset manifest](ASSET-MANIFEST.md) for planned deliverables.
