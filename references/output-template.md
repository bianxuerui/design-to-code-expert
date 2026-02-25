# Output Template

Use this output structure after Step 7.

```markdown
## Design Restoration Summary

**Input HTML**: <path>
**Scope**: <page|component|section>
**Mode**: <strict|balanced|quick>

---

## Stack Detection

- Framework: <value>
- Language: <value>
- Style system: <value>
- Package manager: <value>
- Confidence: <value>
- Evidence: <bulleted list>

---

## HTML Analysis

- Structure summary: <key points>
- Visual tokens: <key points>
- Interaction points: <key points>

---

## Implementation Plan / Changes

- Target file(s):
  - `<path>`
- Actions performed:
  - <item>

---

## Fidelity Deviations (P0-P3)

### P0
- <none or items>

### P1
- <none or items>

### P2
- <none or items>

### P3
- <none or items>

---

## Risks and Assumptions

- <item>

---

## Next Step

Choose one:
1. Fix all deviations
2. Fix P0/P1 only
3. Fix specific items
4. Stop
```
