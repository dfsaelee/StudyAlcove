# Character proof · StudyAlcove

Open **START-HERE.html** in a browser. It runs offline. Turnaround, Walk, and Study control the left portrait. The room always shows the selected person studying at the writing desk. Pause motion to inspect a frame. Both views read the same composed strip.

## Review images

- **previews/base-reference-native.png** and **base-reference-4x.png** compare the bare redraw with the supplied chibi, modular body, and gait references.
- **previews/four-looks.png** shows the four interchangeable hair and clothing combinations on all ten poses.
- **previews/library-crop.png** and **library-bob.png** show the two main looks in the 320×192 Library. Each has a 3× companion.
- The **walk** and **study** PNGs in previews are transparent animated PNGs. Each of the four combinations has both loops.

## Layer contract

All sheets have ten adjacent 24×32 cells and a (12,29) pivot. Draw rear hair, base body, outfit, then front hair. The body includes hands and footwear. Color replacements apply within their respective layer only. Front hair can cover part of a wrist in the north-facing study pose.

| Columns (zero-based) | Poses | Playback |
|---|---|---|
| 0–3 | Stand south, west, east, north | Static directions |
| 4–7 | East walk | 8 fps |
| 8–9 | North seated study | 3 fps |

Use the blank strip and native guide in **authoring** to make a new overlay. The landmark coordinates are local to each frame. The chair in this review is tucked four logical pixels closer to the desk than in the v2 preview. The frame origin is (27,61) in room pixels. The front chair rail draws over the seated body at (31,86).

## Review checkpoint

The next art assignments are Café, Night Owl Loft, and Greenhouse thumbnails and the StudyAlcove mark and wordmark. Those feed the Landing, Room Browser, and Main Study Room designs after character feedback. The full 36-frame redraw and wider cosmetic catalog follow the proof review.

