# Library review files

Open [START-HERE.png](../../../../art/library/library-sprites-v1/START-HERE.png) first. The room uses the [cleaned sprites](../../../../art/library/library-sprites-v1/cleaned/) at 3×. The [light inventory](../../../../art/library/library-sprites-v1/previews/inventory-light.png) and [dark inventory](../../../../art/library/library-sprites-v1/previews/inventory-dark.png) include all four directions. The [idle](../../../../art/library/library-sprites-v1/previews/idle-4x.gif), [walk](../../../../art/library/library-sprites-v1/previews/walk-4x.gif) and [focus](../../../../art/library/library-sprites-v1/previews/focus-4x.gif) GIFs preview each animated action at 4×. See the [QA report](QA-REPORT.md) for checks and findings.

## Art and provenance

The built-in image generator produced [the Library direction sheet](../../../../art/library/library-sprites-v1/raw/library-direction.png) from the following prompt.

> Original StudyAlcove sprite art direction sheet, orthographic straight-on three-quarter top-down cozy 16-bit RPG library, dark walnut shelves with rhythmically clustered books, cream plaster, honey plank floor, sage bankers lamps, restrained autumn textiles, terracotta foliage pots, central clear classroom aisle, eight study places. Small original avatar with dark side swept hair, green cardigan and gold scarf. Exact square pixel clusters; no isometry, UI, lettering or gradients. Wide 16:9 environmental concept reference.

The reference files informed the written direction and native sprite drawing. Each production layer, pose, tile and prop was drawn on its logical grid using the shared 32-color palette. The generated concept is preserved at its original resolution.

| Supplied reference | Applied detail |
|---|---|
| [3rBkNR.gif](../../../../art/references/3rBkNR.gif) | Classroom desk spacing, seat access and central aisle |
| [D8ZJRJ.gif](../../../../art/references/D8ZJRJ.gif) | Wood shelves, alternating book spines and warm shadows |
| [o0Sf8r.gif](../../../../art/references/o0Sf8r.gif) | Interior wall edges and clear sightlines |
| [MP5Mfe.gif](../../../../art/references/MP5Mfe.gif) | Compact avatar proportions and readable hair silhouette |
| [char free/global.png](../../../../art/references/char%20free/global.png) | Reusable body, outfit and hair alignment |
| [char free/char_walk_left.gif](../../../../art/references/char%20free/char_walk_left.gif) | Left-facing gait and planted foot |
| [char free/char_walk_right.gif](../../../../art/references/char%20free/char_walk_right.gif) | Right-facing gait and baseline |
| [chairsprites.jpg](../../../../art/references/chairsprites.jpg) | Upholstered seats, visible writing surfaces and reading lamps |
| [decoration.jpg](../../../../art/references/decoration.jpg) | Front-aligned shelving, potted foliage and desk footprints |
| [backgroundcafecozy.jpg](../../../../art/references/backgroundcafecozy.jpg) | Leafy greens against honey-colored timber |
| [images.jpg](../../../../art/references/images.jpg) | Autumn upholstery and layered warm materials |

## Using the sheets

The [four avatar sheets](../../../../art/library/library-sprites-v1/cleaned/avatars/) share a 9-column by 4-row grid. Frame indices in [avatar.json](../../../../art/library/library-sprites-v1/metadata/avatar.json) are zero-based within each row. Composite the layers in the listed order. In [seats.json](../../../../art/library/library-sprites-v1/metadata/seats.json) both coordinates are native room pixels measured from the upper left. Align the north-facing seated frame by its foot pivot. Draw the chair behind the character, then draw chair rows 12 through 17 over the seated body. [Props](../../../../art/library/library-sprites-v1/metadata/props.json) with zero footprint are decorative or mounted on another object. The [atlas](../../../../art/library/library-sprites-v1/cleaned/tiles/interior_atlas.png) uses one horizontal row with no padding. Use nearest-neighbor sampling at integer zoom.

