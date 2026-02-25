# Argument Specification

## Required

- `design_html_path`: local `.html` input file.

## Optional Flags

| Option | Values | Default | Notes |
| --- | --- | --- | --- |
| `--target` | file path | auto | Explicit output path |
| `--scope` | `page`, `component`, `section` | `component` | Affects path strategy and implementation granularity |
| `--framework` | `auto`, `next`, `react`, `nuxt`, `vue`, `taro`, `svelte`, `vanilla` | `auto` | Overrides detection |
| `--style` | `auto`, `tailwind`, `css-modules`, `scss`, `less`, `styled-components`, `emotion`, `css` | `auto` | Overrides style detection |
| `--mode` | `strict`, `balanced`, `quick` | `balanced` | Fidelity and interaction behavior |
| `--name` | string | inferred | Component or page name hint |
| `--overwrite` | `ask`, `replace`, `patch`, `new` | `ask` | Existing file behavior |
| `--dry-run` | flag | off | Plan only, no write |
| `--check-only` | flag | off | Checks only, no write |
| `--quick` | flag | off | Skip required confirmation when allowed |

## Precedence

1. Explicit option value.
2. Auto-detected value from scripts.
3. Skill default value.

## Conflict Resolution

- `--check-only` implies no file write regardless of other flags.
- `--dry-run` implies no file write regardless of other flags.
- `--mode strict` disables `--quick` shortcut and keeps Step 4 confirmation required.
- `--overwrite new` requires non-conflicting file path generation.
- If `--target` is provided, path suggestion is advisory only.

## Parsing Notes

- Resolve `design_html_path` before any other action.
- Treat unknown option values as blocking input errors.
- Report resolved runtime config in output before implementation.
