# Stack Detection Rules

## Detection Inputs

The detector scans project signals in this order:

1. `package.json` dependencies and devDependencies.
2. Framework-specific config files.
3. Directory conventions.
4. Source file extensions.
5. Lock files for package manager.

## Framework Scoring

- `next`: `next` dependency, `next.config.*`, `app/` or `pages/` patterns.
- `react`: `react` dependency without stronger framework signals.
- `nuxt`: `nuxt` dependency, `nuxt.config.*`.
- `vue`: `vue` dependency without stronger framework signals.
- `taro`: `@tarojs/*` dependency, `config/index.*` with Taro patterns.
- `svelte`: `svelte` or `@sveltejs/kit` dependency.
- `vanilla`: fallback when no framework scores exceed threshold.

## Style System Scoring

- `tailwind`: `tailwindcss` dependency or Tailwind config file.
- `css-modules`: `.module.css/.module.scss/.module.less` presence.
- `styled-components`: dependency match.
- `emotion`: `@emotion/react` or `@emotion/styled` dependency match.
- `scss`: `.scss` files or `sass` dependency.
- `less`: `.less` files or `less` dependency.
- `css`: fallback.

## Language Detection

- `typescript` if `tsconfig.json` exists or TS source files dominate.
- `javascript` otherwise.

## Confidence Thresholds

- `>= 0.75`: high confidence, proceed.
- `0.50 - 0.74`: medium confidence, proceed with explicit note.
- `< 0.50`: low confidence, require user confirmation unless explicit overrides exist.

## Fallback Policy

- If framework confidence is low and user did not override:
  - Default to `vanilla` strategy planning.
  - Ask user to confirm framework before implementation.
- If style system confidence is low:
  - Default to plain `css` mapping.
  - Ask user to confirm style preference.

## Required Output Fields

- `framework`
- `language`
- `style_system`
- `package_manager`
- `confidence`
- `evidence`
