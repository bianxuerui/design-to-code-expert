# Style System Mapping

Translate source HTML visual tokens into the detected or overridden style system.

## Mapping Priority

1. Explicit `--style` option.
2. Detected style system.
3. Plain `css` fallback.

## Tailwind

- Map recurring spacing to nearest spacing scale classes.
- Map typography to standard utility classes.
- Use arbitrary values only when no close utility exists.
- Keep class lists readable and grouped.

## CSS Modules

- Create `*.module.css` with locally scoped class names.
- Keep structural and visual classes separated.
- Import module classes into component/page file.

## SCSS and LESS

- Keep tokens centralized in local variables when repeating.
- Nest selectors conservatively to avoid specificity issues.
- Preserve source hierarchy without deep selector chains.

## Styled Components or Emotion

- Keep styled blocks grouped by semantic section.
- Avoid runtime-heavy dynamic styling unless required.
- Reuse shared tokens across styled blocks.

## Plain CSS

- Keep deterministic class naming and section comments only when needed.
- Group declarations by layout, typography, and state.
- Ensure hover/focus states do not cause layout shift.

## Universal Requirements

- Preserve token intent for color, font size, spacing, radius, and shadow.
- Preserve interactive states where source implies behavior.
- Prefer minimal style surface needed for faithful restoration.
