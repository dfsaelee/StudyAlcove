# Library sprite pack, revision 2

START-HERE.png shows the cutouts together on a transparent canvas. Use the native PNGs in cleaned for your game. The room scene and the two contrast tests have intentional backgrounds. The 4x PNG loops use animated PNG with transparency. Open them in an APNG-capable viewer or browser.

The revision uses the original native silhouettes with a daylight palette of mint, apricot, pale oak and dusty plum. The original concept and visual references remain in the preceding pack and project folder. Animation order, pivots, prop footprints and seats are recorded in metadata.

## Aligning an export

Run the following from this folder with Python and Pillow. Give the tool a cropped export whose outer edges match the original frame or atlas boundaries. Width and height are the full logical canvas dimensions, including transparent padding.

    python align_sprites.py enlarged.png aligned.png --size 24 32

The script samples one color per logical cell, snaps it to the pack palette and makes alpha fully transparent or opaque. It keeps the canvas origin. A shifted crop requires correcting the crop first. For display, use nearest-neighbor scaling at whole-number zoom. Running the script without arguments rebuilds the pack from the sibling library-sprites-v1 native sources.
