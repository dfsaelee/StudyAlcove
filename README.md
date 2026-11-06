# StudyAlcove

StudyAlcove is a shared pixel-art study room. A guest can choose a desk and focus alongside other people. The [roadmap](docs/roadmap.md) describes the planned app and backend. See [AGENTS.md](AGENTS.md) for the project conventions.

Start in the folder that owns the decision. For a change that crosses the interface and the room, use the [shared handoff guide](docs/design/shared/UI-UX-AND-PIXEL-ART.md). It follows one Library desk from sprite placement to a keyboard-accessible seat claim and a confirmed focus session.

| Folder | What belongs here | Where to start |
|---|---|---|
| **UI** | What people see and operate in React. Color tokens, type, spacing, HUD layout, buttons and component states. | [Design system](docs/design/ui/DESIGN-SYSTEM.md) · [UI components](docs/design/ui/UI-COMPONENTS.md) |
| **UX** | What people are trying to do and what happens next. Navigation, interaction order, keyboard paths, loading, errors and recovery. | [Direction and priorities](docs/design/ux/DESIGN-DIRECTION-AND-UX.md) · [Screens and flows](docs/design/ux/SCREENS-AND-FLOWS.md) |
| **Pixel art** | How rooms, tiles, props, avatars and animations are drawn, exported and checked for PixiJS. | [Production pipeline](docs/design/pixel-art/PIXEL-ART-PIPELINE.md) · [Library art walkthrough](docs/design/pixel-art/library-sprites-v1/REVIEW.md) · [Library QA](docs/design/pixel-art/library-sprites-v1/QA-REPORT.md) |
| **Shared** | Product direction, which artwork each surface needs, cross-discipline decisions and review gates. | [Visual brief](docs/design/shared/DESIGN-BRIEF.md) · [Asset manifest](docs/design/shared/ASSET-MANIFEST.md) · [Review plan](docs/design/shared/DESIGN-REVIEW-PLAN.md) |

For example, changing the **color of a desk prompt** belongs in UI. Changing **what happens when two people choose the same desk** belongs in UX. Changing **where the seated avatar’s feet land** belongs in pixel art. If a revised chair changes where a player can stand and which desk the prompt names, update the shared handoff and link to the affected specifications.

The original [interface inspiration notes](docs/design/ui/references/designthoughts.md) and [image-design workflow template](docs/design/shared/references/Designandspritedesign.md) are filed with their respective disciplines. The template’s sample paths describe its own example project. The [Library sprite pack](art/library/library-sprites-v1/START-HERE.png) contains the corresponding image and metadata files.

The [pastel Library revision](art/library/library-sprites-v2/REVIEW.md) and [avatar authoring guide](art/library/library-avatar-proof-v3/authoring/GUIDE.md) are kept alongside the original Library pack.
