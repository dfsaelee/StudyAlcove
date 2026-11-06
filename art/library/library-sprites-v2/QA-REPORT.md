# Independent QA for the pastel Library pack

**Ready for visual inspection · November 6, 2026.** The checks below use the exported PNGs, decoded animation frames and the command-line tool included in this folder.

| Check | Result |
|---|---|
| Source alpha and palette | All 24 cleaned PNGs contain only fully transparent or fully opaque pixels. Transparent pixels have zero RGB. Every isolated prop and avatar layer has genuine transparent space. Floors, walls and doorway tiles fill their cells. The pack uses 28 of the 32 declared pastel swatches and preserves the original source silhouettes. |
| Grid alignment | The entire 960×741 overview, including its outlined lettering, consists of uniform 3×3 pixel blocks. Its background is 84.8% transparent. The room preview also passes the exact 3× check, the animation and contrast sheets pass at 4×, and the seating detail passes at 6×. Reducing each to its logical grid and enlarging it again reproduced every RGBA value. |
| Avatar and atlas | Compositing body, outfit and hair reproduces the composed sheet exactly. All 36 poses fit their 24×32 cells with transparent margins and a common (12, 29) pivot. Each multi-frame action has distinct poses in each direction. The seven atlas cells match their native 16×16 tiles. |
| APNG playback | All 32 directional frame views decoded from the three transparent loops match 4× copies of their source cells, including alpha. Idle has two 500 ms frames, walk has four 125 ms frames, and focus has two 333 ms frames. The loops repeat indefinitely and clear moving edges cleanly. |
| Snap tool | Ran the public CLI on a synthetic 24×32 sprite enlarged to 96×128. It restored the original pixels exactly. It also removed two isolated subcell defects, including a stray opaque pixel in transparent space, and rejected a mismatched aspect ratio and a request to overwrite its input. These tests use the documented canvas origin and padding. |

## Visual review

The muted mint cardigan, apricot wood and dusty rose rug are distinguishable in the room. Both seating closeups show the hands reaching the desktop, with the chair overlapping the lower body. The cream background gives the plum silhouette a 6.50:1 contrast ratio. On the dark test background the same outline measures 1.56:1, so the hair and shoes have less separation. The contrast sheets show this tradeoff directly.

The initial transparent overview had dark lettering that became hard to read on a dark surface. The revised overview and animation contact sheet use a one-pixel cream outline around plum lettering. Both final files pass the hard-edge alpha and integer-grid checks after the correction.

The room and contrast images include their intended backgrounds. The overview, individual sprites, animation contact sheet and three APNGs have transparent backgrounds. Validation covers the art pack and its previews. Runtime collision and pathfinding are outside this review.
