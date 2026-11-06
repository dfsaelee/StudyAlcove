# StudyAlcove — Pixel Art Production & QA Pipeline

**Goal:** Turn generated visual concepts into reliable sprites, tilemaps and animations for a PixiJS multiplayer game. This document is a practical asset-engineering contract, not only a prompt-writing guide.

## 1. Biggest failure modes and required safeguards

| Failure mode | Detect | Prevent / fix |
|---|---|---|
| Mixed pixel scales ("mixels") | Inspect at 800% on visible pixel grid; identify inconsistent 1-pixel stroke widths | Generate to declared logical dimensions; reconstruct on grid; nearest-neighbor resize; reject internally blurred/multi-scale work |
| Anti-aliased / dirty alpha edges | Find partially transparent edge pixels; inspect on both cream and charcoal | Clear alpha or use a small defined alpha set; manually correct important edges; don't blindly threshold shadows intended to be soft overlays |
| Unbounded palette | Count unique RGBA colors on source at native size | Map source art to approved indexed palette; reserve a controlled set of shades; manually review quantization |
| Animation drift / shifting character | Overlay frames and show center/foot-guide; compute bounding boxes | Identical frame cells and foot anchor; fixed base template and hair/outfit overlay pivots; edit frames, not redraw independently |
| Variable proportions / crop | Compare bounding boxes and landmarks; check padding inside cells | Frame template locked; no clipping; same character scale for all directions and outfits |
| Impossible scenery | Inspect top-down perspective, door widths, reachable seats and furniture footprints | Build rooms from collision-aware tiles/props; verify walkability; redraw incorrect props |
| Repeated incompatible assets | Compare icons/hair/outfits across mockups | One canonical asset per ID, referenced everywhere |

A general image model can help with art direction; **it cannot guarantee production-ready pixel art**. Programmatic cleanup must be followed by visual review. Clean pixels do not prove good animation.

## 2. Source coordinate and sizing contract (provisional)

- Tile grid: **16×16 logical source pixels**.
- Character per animation frame: **24×32 px transparent canvas**, with a consistent foot pivot **(12, 29)**, same for every direction and outfit. Target visual body roughly 16×24 px.
- Direction order: `south, west, east, north` (document explicitly in metadata).
- Essential movements: idle 2 frames/direction, walk 4 frames/direction, sit 1 frame/direction, focus 2 frames/direction, emote 2–4 frames for relevant directions.
- Start with **one** canonical avatar template. Validate all directions and animations before variations.
- Prop footprints expressed in tile cells; prop source images may be larger than their collision footprint.
- In PixiJS use `scaleMode: 'nearest'`, integer zoom when possible, consistent anchor/pivot and no fractional camera/sprite coordinates at native pixel scale.
- A design-preview image may be high resolution; accepted runtime sprites must be exported at the logical source resolution.

**Do not upscale a fuzzy AI image and mistake it for genuine low-resolution pixel art.** Pixel-perfect cleanup or manual redraw may be required.

## 3. Palette policy

- Start with one curated global **24–32 color shared palette** for world and avatar source art; allow a small, explicitly named room-specific palette subset for Night Owl Loft / Greenhouse if needed.
- Aim for ~8–16 colors per small sprite, not hundreds of near-identical shades. Palette size is a design target, not a guarantee for every art type.
- Explicit ramps: outline, skin/hair, wood, foliage, metal/stone, light and shadow.
- World lighting/color washes can be runtime overlays separate from indexed sprite pixels. Avoid baking dozens of fractional-opacity glow pixels into props.
- Review color accessibility and meaningful differentiation; colors should not be the only cue for interactable state.

## 4. Generate anchors before bulk art

1. Produce Library perspective / room composition concept.
2. Produce canonical front-facing base character at required logical proportions.
3. Produce a four-direction character turnaround, keeping landmarks and outfit consistent.
4. Produce one idle, one walk and one sit animation sample; fix alignment until stable.
5. Produce one chair, one desk, one bookshelf, one plant, one floor/wall sample and one icon mini-set.
6. Freeze approved assets in `assets/anchors/`. Later generations must reference these exact files and IDs.

A large mixed spritesheet is useful for visual brainstorming, but for cleanup export **one asset per transparent PNG** (or one consistently gridded frame sheet) with stable naming.

## 5. Avatar layers and animation

Layer order per frame (base approach): **body/skin → clothing → hair → accessories**; adjust occlusion per direction where required (e.g., hair behind head for front/back views). Each layer uses the same 24×32 frame canvas and identical foot pivot.

| Animation | Directions | Frames | Rate | State |
|---|---|---|---|---|
| idle | 4 | 2 | ~2 fps | Required baseline |
| walk | 4 | 4 | ~8 fps | Required baseline |
| sit | 4 | 1 | static | Required baseline |
| focus/typing | 4 | 2 | ~3 fps | Required baseline |
| wave | south first | 3 | ~5 fps | V1 |
| happy / sleepy / thinking | south first | 2–4 | ~3–5 fps | V1 |

### Avatar variant plan
- **8 hairstyles**: short crop, side part, bob, long straight, ponytail, curly, wavy, bun; every style must match the same head frame and directions.
- **6 outfits**: casual tee, cardigan, hoodie, sweater, overalls, jacket; support palette variants instead of generating every combination independently.
- **Skin tones**: establish inclusive, distinct indexed color ramps and test outline/lighting against every room.
- Accessories: glasses, headphones, cap, hair clip. Only promise combinations actually validated for clipping.
- Keep base body templates small and reusable. Do not generate all 8×6×4 combinations as separate images.

## 6. Room production process

**Concept → tiled layout → art tiles/props → collision metadata → anchors & interaction points → QA → PixiJS preview**.

Each playable room needs:
- Editable layout source (JSON / Tiled map) with predictable tile layer ordering.
- Tile atlas; floor, walls, boundaries and doors.
- Object props with footprints and render layering: below player / at-player / above player (e.g., bookshelf foreground).
- Walkable grid and explicit collision zones.
- Desk and seat IDs with interaction positions and facing directions; visual position and server-side seat ID must agree.
- Spawn points, walkable routes, accessible desk entry/exit, max seats and server room ID.
- A consistency screenshot from the actual engine, not only the generated mockup.

**Library** first. After Library architecture is proven, reuse its map/prop formats for Café, Night Owl Loft, Greenhouse.

## 7. Sprite cleanup & validation procedure

Run these checks on **source PNGs**, not only the exported atlas:

1. Confirm expected native width and height; frames never silently resize.
2. Inspect transparent margin and trim only if the animation metadata preserves original anchor / source canvas.
3. Count unique opaque colors; compare against palette budget and whitelist.
4. Flag nonzero non-255 alpha values for manual review. Genuine semitransparent overlays may be exceptions with explicit tags.
5. Confirm exact frame grid and no cropped limbs, hair or props.
6. Show a contact sheet of every animation on both light and dark backgrounds.
7. Overlay two consecutive frames at 50% opacity to detect anchor/body shifts.
8. Play each action on a nearest-neighbor preview at 3× / 4×, test walk loop and transitions.
9. Verify world-scale proportions: avatar versus chair, desk, door and tile.
10. Compare in-game renders with approved anchors and log any deviations.

### Example minimal metadata

```json
{
  "id": "avatar_base_01",
  "source": "avatars/base_01.png",
  "frameWidth": 24,
  "frameHeight": 32,
  "pivot": { "x": 12, "y": 29 },
  "directions": ["south", "west", "east", "north"],
  "animations": {
    "walk_south": { "frames": [0, 1, 2, 3], "fps": 8 },
    "idle_south": { "frames": [4, 5], "fps": 2 }
  }
}
```

This metadata is illustrative; the final atlas indices / JSON schema must be generated to match the actual exported frames.

## 8. Prompting contract for AI asset generation

Each prompt must specify:
- Exact asset ID / file path and intended usage (concept, runtime sprite, tile, UI mockup).
- Approved art anchors attached or referenced.
- Orthographic 3/4 top-down view, **16×16 tile grid**, palette constraints and outline rules.
- Logical resolution, frame/cell count and exact character pivot where relevant.
- Background requirement (transparent sprite vs full-background concept).
- Explicit prohibitions: smooth gradients, anti-aliasing, mismatched grid, extra limbs, shadows outside bounds, text on world sprites, changed costume between frames.
- Deliverable and QA expectation. Ask for *one controlled asset/action at a time* when precision matters.

**Template**:

> Create `[ASSET_ID]` for StudyAlcove, classic cozy 16-bit RPG pixel art. Match attached approved Library/avatar/furniture anchors exactly. Orthographic 3/4 top-down viewpoint; 16px tile grid; indexed-palette-style flat pixel clusters with hard edges. Deliver `[N]` frames on identical `[W]×[H]` transparent logical canvases with foot pivot `[X,Y]`. Preserve character body, hair, clothing, outline thickness, and scale in every frame. No antialiasing, blurred pixels, gradient texture, floating props, cropped limbs, perspective changes, added icons or UI text. Output for manual grid/palette/alpha QA.

## 9. Documentation and suggested asset folders

The [workspace index](../../../README.md) locates the design documents. The [asset manifest](../shared/ASSET-MANIFEST.md) tracks production priorities, the [handoff guide](../shared/UI-UX-AND-PIXEL-ART.md) connects the art to room interactions, and the [Library review](library-sprites-v1/REVIEW.md) points to the current sprite pack.

For a production asset repository, the suggested layout is:

```
assets/
  anchors/
  concepts/
  raw/
  cleaned/
  avatars/
  tilesets/
  props/
  icons/
  atlases/
  maps/
  previews/
```

Keep raw outputs unmodified for provenance. Production code imports from curated `assets/cleaned`, built atlases, and map data only.

## 10. Human review checkpoints

- **Review 1:** Three concept screens + Library room and base avatar. Approve perspective, scale, and feel.
- **Review 2:** Canonical anchors / first animation sample. Approve sprite correctness.
- **Review 3:** Complete Library tileset and furniture; interactable seat map in renderer.
- **Review 4:** Other room concepts, variant hairstyles/outfits, remaining UI screens.
- **Review 5:** Cross-room playable scene consistency, accessibility, and asset metadata handoff.

Log every revision as `asset ID / issue / action / approved by / date` rather than regenerating everything.
