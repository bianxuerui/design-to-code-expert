# Framework Mapping: React and Next

## Scope Mapping

### React

- `page` scope:
  - Preferred: `src/pages/<Name>.tsx` or `.jsx`.
  - If router conventions differ, follow existing `src/routes` pattern.
- `component` or `section` scope:
  - Preferred: `src/components/<Name>.tsx` or `.jsx`.

### Next

- `page` scope:
  - App Router first: `src/app/<route>/page.tsx` or `.jsx`.
  - If app router missing, fallback to `pages/<route>.tsx` or `.jsx`.
- `component` or `section` scope:
  - Preferred: `src/components/<Name>.tsx` or `.jsx`.

## Component Rules

- Preserve semantic HTML structure from source draft.
- Keep one primary component per file for restoration target.
- Extract repeated blocks into subcomponents only when they repeat three times or more.
- Keep props minimal and infer only from source structure.

## Styling Rules

- Delegate style translation to `references/style-system-mapping.md`.
- Prefer local, deterministic styles over global side effects.
- Keep spacing, typography, color, radius, and shadow tokens consistent with source tokens.

## Interaction Rules

- Preserve button/link semantics.
- Preserve form label/input associations.
- Add keyboard-focus visibility for interactive elements.

## Output Guardrails

- Do not invent data-fetching logic unless user asks.
- Do not introduce unrelated refactors.
- Keep file changes scoped to approved target paths.
