# Framework Mapping: Svelte

## Scope Mapping

- `page` scope:
  - SvelteKit preferred: `src/routes/<route>/+page.svelte`.
  - Fallback: project page conventions if non-SvelteKit.
- `component` or `section` scope:
  - Preferred: `src/lib/<Name>.svelte` or `src/components/<Name>.svelte`.

## Component Rules

- Preserve source semantic structure in markup.
- Keep logic minimal; avoid introducing derived state unless needed for interaction.
- Use idiomatic Svelte bindings only where source interaction requires them.

## Styling Rules

- Prefer local component styles unless project uses global utility patterns.
- Map visual tokens using `references/style-system-mapping.md`.

## Interaction Rules

- Preserve keyboard accessibility and focus behavior.
- Keep event handlers explicit and scoped.

## Output Guardrails

- Avoid adding routing/data loading logic unless requested.
- Keep implementation strictly within confirmed files and scope.
