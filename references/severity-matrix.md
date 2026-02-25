# Severity Matrix

## P0

- Meaning: Blocking issue that makes output unusable or unsafe.
- Examples: broken build, inaccessible critical interaction, destructive overwrite without approval.
- Action: Must fix before completion.

## P1

- Meaning: High-impact fidelity or correctness issue.
- Examples: major layout mismatch, key interaction mismatch, incorrect semantic structure for core content.
- Action: Fix before merge unless user explicitly defers.

## P2

- Meaning: Medium-impact maintainability or visual consistency issue.
- Examples: spacing inconsistency, minor token drift, non-critical accessibility gap.
- Action: Fix now or track as follow-up.

## P3

- Meaning: Low-impact optimization.
- Examples: naming cleanup, minor style simplification.
- Action: Optional improvement.
