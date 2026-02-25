# Framework Mapping: Vanilla HTML CSS JS

## Scope Mapping

- `page` scope:
  - Preferred: `src/pages/<name>.html` or project-specific static page directory.
- `component` scope:
  - Preferred: split into `*.html`, `*.css`, and optional `*.js` files.
- `section` scope:
  - Add section markup/styles into confirmed host page file.

## Structure Rules

- Preserve semantic tags from source HTML.
- Keep class naming stable and predictable.
- Avoid global selectors that can leak styles across unrelated pages.

## Styling Rules

- Keep style tokens explicit and grouped by component/section.
- Use CSS variables only if repository already follows tokenized styles.

## Interaction Rules

- Preserve click and form interactions with unobtrusive JavaScript.
- Keep event listeners scoped and removable.
- Preserve keyboard and focus accessibility.

## Output Guardrails

- Do not add build tooling or framework code.
- Keep output deterministic and bounded to requested scope.
