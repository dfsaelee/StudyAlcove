# StudyAlcove — Asset Inventory & Generation Queue

**Status:** Proposed asset inventory for the first visual production campaign. Counts are targets, not a claim that assets already exist. Priorities: **P0** necessary to validate the art language and first playable Library, **P1** design breadth / V1, **P2** later gameplay polish.

Use this shared inventory to pair each screen with its artwork. Sections A and B belong to pixel-art production. Section C covers UX surfaces and their review mockups. Section D identifies web controls and world icons by where they appear. Sections E and F bring the outputs together for review. [UI specifications](../ui/DESIGN-SYSTEM.md) · [UX inventory](../ux/SCREENS-AND-FLOWS.md) · [Art pipeline](../pixel-art/PIXEL-ART-PIPELINE.md) · [Library handoff](UI-UX-AND-PIXEL-ART.md)

## A. Rooms and environmental art

| Priority | Deliverable | Count | Production output |
|---|---|---:|---|
| P0 | Library concept + layout | 1 room | 16:9 concept, Tiled/JSON grid map, collision/interaction layers |
| P0 | Shared floor/wall/door tiles | 1 kit | 16px tile atlas + source PNGs |
| P0 | Library furniture | ~12 props | Desks (2), chairs (2), lamps (2), shelves (2), plants (2), clock, rug |
| P0 | Library interaction markers | 8–12 seats | Seat IDs, stand/sit coordinates, direction metadata |
| P1 | Café concept | 1 room | Approved concept + layout draft |
| P1 | Night Owl Loft concept | 1 room | Approved concept + layout draft |
| P1 | Greenhouse concept | 1 room | Approved concept + layout draft |
| P1 | Café unique furniture | ~8 props | Counter, round table, stool, pastry case, coffee machine, cup, hanging lamp, window bar |
| P2 | Night Owl unique props | ~8 props | Monitor, PC desk, task lamp, floor pillow, rainy window, couch, shelf, cables |
| P2 | Greenhouse unique props | ~8 props | Planters, vines, garden bench, trellis, glass panels, pots, watering can, hanging leaves |
| P2 | Ambient loops | ~4 | Rain, steam, lamp flicker, plant sway; PNG frames / metadata |

## B. Avatar and animation system

| Priority | Deliverable | Count | Output |
|---|---|---:|---|
| P0 | Canonical avatar base | 1 | 24×32 logical frame, all four directions |
| P0 | Required action set | 4 actions | Idle, walk, sit, focus with fixed pivots and metadata |
| P0 | One working hair/outfit layer proof | 1 each | Transparent layered sprites; overlays align across directions |
| P1 | Hairstyle options | 8 | Short crop, side part, bob, long straight, ponytail, curly, wavy, bun |
| P1 | Outfits | 6 | T-shirt, cardigan, hoodie, sweater, overalls, jacket |
| P1 | Color ramps | curated | Skin / hair / clothing palettes; recolor rather than re-render combinations |
| P1 | Accessories | 4 | Glasses, headphones, cap, hair clip |
| P1 | Emotes | 3 | Wave, happy, sleepy (thinking may be added later) |
| P2 | Optional avatar body silhouettes | 2 more | Same anchors and frame contract |

## C. Web screens and UX

| Priority | Screen mockup | Notes |
|---|---|---|
| P0 | Landing | Product identity, join CTA, art preview |
| P0 | Room browser | Four room cards, unavailable rooms explicitly labeled |
| P0 | In-room HUD | Library canvas, player, timer, room status and controls |
| P0 | Avatar setup | Guest name, basic preset/customization |
| P0 | Desk/focus panel | Sit and timer states |
| P0 | Session completion | Confirm saved focus progress |
| P1 | Profile/history | Session list + total time; streaks where supported |
| P1 | Chat/emotes drawer | Mute and state controls |
| P1 | Settings | Sound, theme, reduced motion, privacy |
| P1 | Private room creation | Invite link and permissions |
| P2 | Achievements | Collection of achievements and badges |
| P2 | Decoration inventory | Unlock and place decor in permitted locations |

**Themes:** initial 3 screen concepts in light mode; once approved, all major mockups use the same design system. Dark mode primarily applies to web chrome and controls; a room's scene can retain its own day/night look. Avoid recoloring every room just to match the UI theme.

## D. UI components and icons

| Priority | Assets | Count / notes |
|---|---|---|
| P0 | StudyAlcove wordmark + symbol | Horizontal logo, compact mark, favicon concept |
| P0 | UI control mini-kit | Primary/secondary/disabled/focus buttons, input, card, toast, timer panel |
| P0 | World icons | timer, desk, chair, join, exit, focus, message, sound, settings (9) |
| P1 | Additional icons | avatar, edit, invite, emote, break, stats, streak, achievements, decorations (9) |
| P1 | HUD state illustrations | connected, reconnecting, empty room, room full, session complete |
| P2 | Decorative seasonal variants | Optional later |

## E. Ordered production batches

1. **Batch 0 — brief and reference direction:** gather 2–4 inspirations with "keep/avoid" notes; lock palette candidates and scale rules.
2. **Batch 1 — three initial UI mockups:** Landing, Room browser, In-room HUD. Separately create Library room concept and canonical character turnaround. **Stop for human review.**
3. **Batch 2 — anchor freeze:** approved wordmark, avatar base, one walk animation, one desk/chair/plant, UI mini-kit. **Stop for pixel QA.**
4. **Batch 3 — Library playable kit:** floor/wall tiles, props, map, collision boxes, desk metadata, PixiJS test scene. **Stop for gameplay check.**
5. **Batch 4 — breadth:** Café, Night Owl Loft and Greenhouse concepts; 8 hairstyles, 6 outfits, 4 accessories; remaining MVP screens.
6. **Batch 5 — variant review:** V1 screens, UI dark-mode variants, selected room playable conversions, animations/emotes.
7. **Batch 6 — polish:** decorations, achievements, ambient loops, additional rooms and accessibility revisions.

## F. File naming and acceptance criteria

Example names:

```
assets/avatars/base/avatar_base_01_walk_south.png
assets/avatars/hair/hair_bob_south.png
assets/props/library/desk_single_01.png
assets/tilesets/shared/interior_16px.png
assets/maps/library_v1.json
assets/icons/world/icon_timer_16.png
assets/atlases/avatar_base_01.json
assets/previews/library_3x.png
```

Every exported game asset must provide: source PNG, expected source dimensions, palette check, alpha check, anchor/pivot, layer or collision data where relevant, and a preview at an integer scale. Every screen mockup must identify the common assets and true UI elements needed to implement it. Check boxes belong in the production tracker, not the images.

## G. Planning boundaries

- Concept art for all four rooms is authorized as a design goal; **full playable map construction is Library-first**.
- Keep AI output and manually cleaned production art separately. A design concept does not count as completed runtime assets.
- No new characters/rooms/features should be silently added by the agent. Ask for a review at each batch gate.
