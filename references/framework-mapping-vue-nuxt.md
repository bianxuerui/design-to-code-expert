# Framework Mapping: Vue and Nuxt

## Scope Mapping

### Vue

- `page` scope:
  - Preferred: `src/views/<Name>.vue` or project-specific page directory.
- `component` or `section` scope:
  - Preferred: `src/components/<Name>.vue`.

### Nuxt

- `page` scope:
  - Preferred: `pages/<route>.vue`.
- `component` or `section` scope:
  - Preferred: `components/<Name>.vue`.

## SFC Structure Rules

- Use Single File Component structure:
  - `template`
  - `script setup` unless repository uses classic script style.
  - `style` according to detected style system.
- Keep template hierarchy aligned with source HTML semantic structure.

## Styling Rules

- Delegate style translation to `references/style-system-mapping.md`.
- Use scoped styles unless repository conventions prefer global utility classes.

## Interaction Rules

- Preserve interactive semantics and accessible labels.
- Keep event handlers minimal and deterministic.

## Output Guardrails

- Do not add stores, plugins, or API calls unless user requests them.
- Keep implementation bounded to approved scope and files.
