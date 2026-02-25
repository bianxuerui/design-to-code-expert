# Framework Mapping: Taro

## Scope Mapping

- `page` scope:
  - Preferred: `src/pages/<route>/index.tsx` or `.jsx`.
- `component` or `section` scope:
  - Preferred: `src/components/<Name>/index.tsx` or `.jsx`.

## Taro-Specific Rules

- Use Taro-compatible primitives where required by project conventions.
- Avoid browser-only APIs unless wrapped with platform checks.
- Keep event and interaction handling aligned with Taro runtime behavior.

## Styling Rules

- Prefer project-standard style files (`.scss`, `.less`, or utility classes).
- Keep style token mapping deterministic using `references/style-system-mapping.md`.

## Interaction and Accessibility

- Preserve button and link intent.
- Ensure touch targets are appropriately sized.
- Preserve form semantics and labels where supported.

## Output Guardrails

- Avoid adding cross-platform abstractions not needed for the restored scope.
- Keep changed files limited to approved targets.
