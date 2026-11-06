# How the Library artwork, interface and interactions fit together

The Library sprite pack gives the team a desk, chair and seated pose to design around. UX defines how Robin finds that desk and learns whether it is available. React presents the choices and feedback. PixiJS draws the room from its art and the latest confirmed room state.

## One desk from artwork to interaction

| Step | What to hand off |
|---|---|
| Place the seat | The pack's `seat-3` pairs `writing_desk` with `slat_chair`. Its standing point is (220, 109) and its seated foot position is (220, 94), measured in native room pixels from the upper left. Align the north-facing frame's (12, 29) foot pivot there. Redraw the chair's foreground rows over the lower body. [Seat metadata](../../../art/library/library-sprites-v1/metadata/seats.json) · [Seated art detail](../../../art/library/library-sprites-v1/previews/seated-detail.png) |
| Inspect and claim it | The proposed world target and keyboard-accessible **Desks** list identify the same seat. Both open the DOM seat prompt. For an available seat, “Sit here” sends one request under the same movement and occupancy rules. Show “Taking seat…” while it is pending. When the server confirms Robin owns the seat, draw the seated pose and offer “Start focus.” If another player got there first, update both views and offer another desk. [Screen behavior](../ux/SCREENS-AND-FLOWS.md) · [RoomCanvas, GameHUD and SeatPrompt](../ui/UI-COMPONENTS.md) |
| Follow a focus session | A confirmed start supplies the timer's start/end times. PixiJS can play the avatar's two focus frames at the pack's 3 fps. React displays the countdown and announces meaningful state changes. At zero, “Checking your session…” precedes credited minutes. A sprite loop or elapsed display cannot award credit. [Avatar metadata](../../../art/library/library-sprites-v1/metadata/avatar.json) |

The pack contains **eight authored seat records**. “3 of 10 online” in the screen proposal is illustrative presence data. For a playable build, match seat IDs to the actual room map and read occupancy and capacity from the server. Check any location label, such as “Window”, against that map before using it in the desk list.

## When the same scene appears in two themes

Keep the honey-colored floor, lamps and avatar on the Library's authored palette. Change the DOM panel, label, border and keyboard ring through the theme tokens. Put the prompt on a solid plate and move it beside the desk or into the outer rail when it would cover Robin. Use a labelled seat status that works through keyboard, pointer and touch. With reduced motion, communicate focusing through text and a still pose where appropriate. Keep timer ticks out of the announcement stream. [UI tokens and motion](../ui/DESIGN-SYSTEM.md) · [World palette and animation](../pixel-art/PIXEL-ART-PIPELINE.md)

## Review at handoff

- **Art evidence today.** The pack includes source sprites, frame metadata and static layout previews. Its QA report covers palette/alpha, layer alignment, seat positions and seated occlusion. Use the manifest to identify the remaining artwork for each screen. [Library QA report](../pixel-art/library-sprites-v1/QA-REPORT.md) · [Asset manifest](ASSET-MANIFEST.md)
- **Prototype checks after implementation.** Claim the same desk from two clients, one through the keyboard list. Verify one confirmed owner, matching chair/pose and DOM feedback. Reconnect and compare both views to a fresh room snapshot. In both themes, check that focus returns to the desk control, the prompt clears the avatar and a screen reader hears the claim result once. Collision, reachability and multiplayer behavior need this live check.
