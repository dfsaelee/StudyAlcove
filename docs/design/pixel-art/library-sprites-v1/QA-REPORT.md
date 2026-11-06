# Library sprite QA

**Ready for art review · November 6, 2026.** An independent QA agent inspected the final exports against the project's [pixel-art pipeline](../PIXEL-ART-PIPELINE.md) and [Library asset manifest](../../shared/ASSET-MANIFEST.md). Open the [review walkthrough](REVIEW.md) for the starting image, source sheets and motion previews.

| Check | Result |
|---|---|
| Pixel grid, palette and alpha | All 24 cleaned PNGs use the declared palette. Across the pack, 28 of the 32 swatches appear. Every pixel is fully opaque or fully transparent. The cream and charcoal inventory sheets show crisp edges and consistent pixel scale. |
| Avatar sheets and layers | All four sheets measure 216×128 px. Their 36 cells have transparent margins, use the same 24×32 frame and share the (12, 29) foot pivot. Compositing body, outfit and hair reproduces the final sheet pixel for pixel. |
| Motion | Each south, west, east and north row contains two idle frames, four distinct walk poses, one sit pose and two focus frames. All 32 animated views in the three GIFs match the corresponding source frames at exactly 4×. GIF frame times are 500 ms for idle, 120 ms for walk and 330 ms for focus. Adjacent-frame overlays show a stable head position horizontally, a one-pixel breathing motion and alternating steps. |
| Library kit | All 12 props have matching source dimensions and metadata. All seven 16×16 atlas cells match their individual source tiles. Floor courses align in the preview, and the center doorway has a continuous opening. |
| Seats and prop scale | Eight unique seats have in-bounds sit and stand coordinates, north-facing metadata and valid desk and chair IDs. All eight standing points land on visible floor in the native room. The 6× seating detail shows the avatar seated at both desk types with the chair in front of the lower body and the hands reaching the work surface. |

## Finding fixed and rechecked

The back hair originally covered the hands in all three north-facing sit and focus frames. The revised poses place the hands beside the head. The final composites retain 12–13 visible hand-colored pixels per pose, and the right hand changes position between focus frames. The fix is visible in [both desk closeups](../../../../art/library/library-sprites-v1/previews/seated-detail.png) and the [rebuilt focus GIF](../../../../art/library/library-sprites-v1/previews/focus-4x.gif).

## For the art review

The native sprites preserve the concept's green cardigan, amber wood and autumn foliage. The native furniture uses broad color blocks and a sparser surface treatment than the painted concept. The [charcoal inventory](../../../../art/library/library-sprites-v1/previews/inventory-dark.png) also shows how the darkest hair and shoe outlines blend into a dark surround. The [room preview](../../../../art/library/library-sprites-v1/previews/library-native.png) shows their intended contrast against the honey floor.

This review covers the sprite pack and its static room arrangement. Collision, pathfinding and live seat interaction require a playable room and remain unverified.
