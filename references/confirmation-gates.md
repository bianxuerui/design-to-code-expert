# Confirmation Gates

Use this checkpoint before writing implementation files.

## Required Confirmation Payload

Report and confirm:

1. Detected stack summary:
   - framework
   - language
   - style system
   - package manager
   - confidence
2. Input analysis summary:
   - major structure blocks
   - core visual tokens
   - interaction points
3. Target output:
   - target path(s)
   - scope
   - overwrite policy
   - mode
4. Known assumptions and limitations.

## Confirmation Prompt Template

Use this exact structure:

- Detected stack: `...`
- Planned output path: `...`
- Scope and mode: `...`
- Overwrite behavior: `...`
- Assumptions: `...`

Question:

- Continue with implementation?
  - 1. Continue as planned
  - 2. Adjust path or scope
  - 3. Adjust framework or style mapping
  - 4. Stop

## Quick Mode Rules

- If `--quick` is set and mode is not `strict`, confirmation may be skipped.
- If confidence is low or overwrite conflict exists, still request confirmation even in quick mode.
