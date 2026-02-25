---
name: design-to-code-expert
description: "HTML design-to-code restoration skill for local .html mockups. Use when users ask to restore, replicate, rebuild, or pixel-match a design draft into the current project stack and language. Triggers include: 还原设计稿, HTML还原, 复刻页面, 像素级还原, design to code, restore UI, replicate page, convert html mockup, implement from html file, React, Next.js, Vue, Nuxt, Taro, Svelte, vanilla frontend." 
---

# Design to Code Expert

## Overview

Execute a deterministic, confirmation-first workflow to restore a local HTML design draft into the current project codebase.

- Start with analysis, not code generation.
- Auto-detect project stack and language first.
- Ask for confirmation at required checkpoints unless the user explicitly chooses `--quick`.
- Keep implementation consistent by using scripts and reference files.

## Inputs and Options

Required input:

- `design_html_path`: local `.html` file path.

Optional options (full spec in `references/argument-spec.md`):

- `--target <path>`: explicit output file path.
- `--scope <page|component|section>`: implementation scope.
- `--framework <auto|next|react|nuxt|vue|taro|svelte|vanilla>`: framework override.
- `--style <auto|tailwind|css-modules|scss|less|styled-components|emotion|css>`: style system override.
- `--mode <strict|balanced|quick>`: fidelity mode.
- `--name <ComponentName>`: component/page naming hint.
- `--overwrite <ask|replace|patch|new>`: file conflict behavior.
- `--dry-run`: analyze and plan only.
- `--check-only`: run checks only; no file edits.

Parse and conflict rules:

- Load `references/argument-spec.md` before parsing options.
- Precedence: explicit option overrides auto-detection, and auto-detection overrides defaults.

## Workflow

Copy this checklist and mark items while executing:

- [ ] Step 0: Validate local HTML input `BLOCKING`
- [ ] Step 1: Detect project stack `BLOCKING`
- [ ] Step 2: Inspect HTML structure and tokens
- [ ] Step 3: Build restoration strategy from mappings
- [ ] Step 4: Confirm plan with user `REQUIRED`
- [ ] Step 5: Implement restoration in target files
- [ ] Step 6: Run quality gates
- [ ] Step 7: Run pre-delivery checklist `REQUIRED`
- [ ] Step 8: Produce structured delivery output
- [ ] Step 9: Ask next-step fix scope `REQUIRED`

### Step 0: Validate local HTML input `BLOCKING`

- Verify `design_html_path` exists and is readable.
- Verify file extension is `.html`.
- If invalid, stop and ask user for a valid local HTML file.
- If `--check-only` is set, continue with analysis but do not write code.

### Step 1: Detect project stack `BLOCKING`

- Run:

```bash
python3 scripts/detect_stack.py --project-root .
```

- If user passes framework/style overrides, apply them after detection.
- Read detection output fields: `framework`, `language`, `style_system`, `package_manager`, `confidence`, `evidence`.
- Load `references/stack-detection.md` for confidence thresholds and fallback behavior.
- If confidence is low and no explicit override exists, require user confirmation before coding.

### Step 2: Inspect HTML structure and tokens

- Run:

```bash
python3 scripts/inspect_html.py --html "<design_html_path>"
```

- Parse output fields for:
  - Structural summary (`top_tags`, `semantic_sections`, repeated classes).
  - Visual tokens (`colors`, `font_sizes`, `spacings`, `radii`, `shadows`).
  - Interaction points (`buttons`, links, form controls, click targets).
- Load `references/html-analysis-questions.md` and answer the questions explicitly before coding.

### Step 3: Build restoration strategy from mappings

- Select framework mapping file based on detected or overridden framework:
  - `references/framework-mapping-react-next.md`
  - `references/framework-mapping-vue-nuxt.md`
  - `references/framework-mapping-taro.md`
  - `references/framework-mapping-svelte.md`
  - `references/framework-mapping-vanilla.md`
- Load `references/style-system-mapping.md` to map styles into target styling approach.
- Run target path suggestion:

```bash
python3 scripts/suggest_target_path.py --project-root . --scope <scope> --framework <framework> --name <name> --overwrite <overwrite>
```

- Convert analysis into a concrete file-level implementation plan.

### Step 4: Confirm plan with user `REQUIRED`

- Load `references/confirmation-gates.md`.
- Present and confirm all required items:
  - Detected stack and style system.
  - Target file path(s) and overwrite mode.
  - Scope and fidelity mode.
  - Any known limitations from HTML source.
- Skip this step only when user explicitly passes `--quick` and mode is not `strict`.

### Step 5: Implement restoration in target files

- Implement only after Step 4 is confirmed (unless valid `--quick` path).
- Follow selected framework mapping and style system mapping.
- Respect scope:
  - `page`: full page structure.
  - `component`: reusable component extraction.
  - `section`: bounded section implementation.
- If `--dry-run` or `--check-only` is set, output intended changes without writing files.

### Step 6: Run quality gates

- Run available checks based on project toolchain:
  - Lint if configured.
  - Type check if TypeScript is used.
  - Build or compile check if available.
- If checks fail, summarize blocker issues first, then non-blockers.

### Step 7: Run pre-delivery checklist `REQUIRED`

- Load:
  - `references/pre-delivery-checklist.md`
  - `references/severity-matrix.md`
- Evaluate output and classify deviations as P0-P3.
- P0 or unresolved P1 requires explicit user sign-off before completion.

### Step 8: Produce structured delivery output

- Load `references/output-template.md`.
- Report:
  - Stack detection result and confidence.
  - HTML analysis summary.
  - Changed file list.
  - Fidelity deviations with severity.
  - Risks, assumptions, and follow-up actions.

### Step 9: Ask next-step fix scope `REQUIRED`

After delivery, ask user how to proceed:

1. Fix all deviations.
2. Fix P0/P1 only.
3. Fix specific items.
4. Stop with current result.

Do not continue modifications until user selects one option.

## Output Contract

Always output in this order:

1. Detection summary.
2. Implementation plan.
3. Files changed or planned.
4. Deviation grading P0-P3.
5. Next-step decision request.

## Resource Loading Index

| Resource | Load When |
| --- | --- |
| `references/argument-spec.md` | Before option parsing in Inputs phase |
| `references/workflow-checklist.md` | At workflow start for progress tracking |
| `references/stack-detection.md` | Step 1 confidence and fallback decisions |
| `references/html-analysis-questions.md` | Step 2 analysis before coding |
| `references/framework-mapping-react-next.md` | Step 3 when framework is React or Next |
| `references/framework-mapping-vue-nuxt.md` | Step 3 when framework is Vue or Nuxt |
| `references/framework-mapping-taro.md` | Step 3 when framework is Taro |
| `references/framework-mapping-svelte.md` | Step 3 when framework is Svelte |
| `references/framework-mapping-vanilla.md` | Step 3 when framework is Vanilla |
| `references/style-system-mapping.md` | Step 3 style mapping |
| `references/confirmation-gates.md` | Step 4 confirmation checkpoint |
| `references/pre-delivery-checklist.md` | Step 7 quality verification |
| `references/severity-matrix.md` | Step 7 severity grading |
| `references/output-template.md` | Step 8 structured result output |

## Resources

- references/
  - `argument-spec.md`
  - `workflow-checklist.md`
  - `stack-detection.md`
  - `html-analysis-questions.md`
  - `framework-mapping-react-next.md`
  - `framework-mapping-vue-nuxt.md`
  - `framework-mapping-taro.md`
  - `framework-mapping-svelte.md`
  - `framework-mapping-vanilla.md`
  - `style-system-mapping.md`
  - `confirmation-gates.md`
  - `pre-delivery-checklist.md`
  - `severity-matrix.md`
  - `output-template.md`
- scripts/
  - `detect_stack.py`
  - `inspect_html.py`
  - `suggest_target_path.py`
