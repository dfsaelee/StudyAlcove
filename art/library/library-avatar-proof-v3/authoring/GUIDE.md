# Avatar authoring handoff

- Draw on `blank-10frame-240x32.png`: 10 transparent 24×32 cells, left to right. `landmarks-guide.png` is a native-size overlay; `landmarks-guide-4x.png` is the same overlay enlarged 4× for inspection. White links show the pose skeleton. Orange marks head, blue shoulders, cyan elbows/wrists, green waist, purple knees, pink feet, and white pivot. Exact per-frame points and names are in `landmarks.json`.
- Each cell uses local origin (0,0), with pivot (12,29). Read the corresponding frame entry in `landmarks.json`; the base silhouette has varying profile, walk, and seated coordinates, so use its per-frame landmark values.
- `palette.json` lists named shadow/midtone/highlight ramps. The first ramp in each category is the exact replacement-source ramp; preserve its RGB values for automated color replacement. Hair outline is fixed at #463138.
