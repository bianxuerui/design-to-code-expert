#!/usr/bin/env python3
"""Detect project framework, language, style system, and package manager."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

EXCLUDED_DIRS = {
    "node_modules",
    ".git",
    ".next",
    ".nuxt",
    "dist",
    "build",
    "coverage",
    "out",
    ".turbo",
}


def error(message: str, code: int = 2) -> int:
    print(json.dumps({"error": message}, ensure_ascii=True))
    return code


def load_package_json(project_root: Path) -> Dict[str, object]:
    package_json = project_root / "package.json"
    if not package_json.exists():
        return {}

    try:
        return json.loads(package_json.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def gather_source_stats(project_root: Path, max_files: int = 4000) -> Dict[str, int]:
    counts = {
        "ts": 0,
        "tsx": 0,
        "js": 0,
        "jsx": 0,
        "vue": 0,
        "svelte": 0,
        "scss": 0,
        "less": 0,
        "css": 0,
        "module_css": 0,
        "module_scss": 0,
        "module_less": 0,
    }

    scanned = 0
    for current_root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for filename in files:
            if scanned >= max_files:
                return counts
            scanned += 1

            path = Path(current_root) / filename
            suffix = path.suffix.lower()
            lower_name = filename.lower()

            if suffix == ".ts":
                counts["ts"] += 1
            elif suffix == ".tsx":
                counts["tsx"] += 1
            elif suffix == ".js":
                counts["js"] += 1
            elif suffix == ".jsx":
                counts["jsx"] += 1
            elif suffix == ".vue":
                counts["vue"] += 1
            elif suffix == ".svelte":
                counts["svelte"] += 1
            elif suffix == ".scss":
                counts["scss"] += 1
            elif suffix == ".less":
                counts["less"] += 1
            elif suffix == ".css":
                counts["css"] += 1

            if lower_name.endswith(".module.css"):
                counts["module_css"] += 1
            elif lower_name.endswith(".module.scss"):
                counts["module_scss"] += 1
            elif lower_name.endswith(".module.less"):
                counts["module_less"] += 1

    return counts


def detect_framework(project_root: Path, deps: Dict[str, str]) -> Tuple[str, float, List[str], Dict[str, float]]:
    scores = {
        "next": 0.0,
        "react": 0.0,
        "nuxt": 0.0,
        "vue": 0.0,
        "taro": 0.0,
        "svelte": 0.0,
        "vanilla": 0.2,
    }
    evidence = {name: [] for name in scores}

    def add(name: str, points: float, reason: str) -> None:
        scores[name] += points
        evidence[name].append(reason)

    dep_names = set(deps.keys())

    if "next" in dep_names:
        add("next", 1.2, "dependency: next")
    if "react" in dep_names:
        add("react", 0.9, "dependency: react")
    if "react-dom" in dep_names:
        add("react", 0.3, "dependency: react-dom")
    if "react-router" in dep_names or "react-router-dom" in dep_names:
        add("react", 0.2, "dependency: react-router")

    if "nuxt" in dep_names:
        add("nuxt", 1.2, "dependency: nuxt")
    if "vue" in dep_names:
        add("vue", 0.9, "dependency: vue")
    if "vue-router" in dep_names:
        add("vue", 0.2, "dependency: vue-router")

    if any(dep.startswith("@tarojs/") for dep in dep_names):
        add("taro", 1.3, "dependency: @tarojs/*")

    if "svelte" in dep_names:
        add("svelte", 1.0, "dependency: svelte")
    if "@sveltejs/kit" in dep_names:
        add("svelte", 0.5, "dependency: @sveltejs/kit")

    if (project_root / "next.config.js").exists() or (project_root / "next.config.mjs").exists():
        add("next", 0.4, "config: next.config.*")
    if (project_root / "nuxt.config.ts").exists() or (project_root / "nuxt.config.js").exists():
        add("nuxt", 0.4, "config: nuxt.config.*")
    if (project_root / "src/app").exists() or (project_root / "app").exists():
        add("next", 0.3, "dir: app router structure")
    if (project_root / "pages").exists() or (project_root / "src/pages").exists():
        add("next", 0.1, "dir: pages structure")
        add("react", 0.1, "dir: pages structure")
        add("nuxt", 0.1, "dir: pages structure")

    if (project_root / "config/index.ts").exists() or (project_root / "config/index.js").exists():
        add("taro", 0.3, "config: taro-like config/index.*")

    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_name, top_score = ordered[0]
    second_score = ordered[1][1] if len(ordered) > 1 else 0.0

    confidence = 0.35
    if top_name == "vanilla":
        confidence = 0.55 if top_score > 0.2 else 0.35
    else:
        confidence = min(0.98, 0.45 + top_score * 0.28)
        if top_score - second_score < 0.25:
            confidence -= 0.12

    confidence = max(0.1, round(confidence, 2))
    return top_name, confidence, evidence[top_name], scores


def detect_language(project_root: Path, source_stats: Dict[str, int]) -> Tuple[str, List[str]]:
    evidence: List[str] = []
    ts_total = source_stats["ts"] + source_stats["tsx"]
    js_total = source_stats["js"] + source_stats["jsx"]

    if (project_root / "tsconfig.json").exists():
        evidence.append("file: tsconfig.json")
        return "typescript", evidence

    if ts_total > js_total:
        evidence.append(f"source: ts files {ts_total} > js files {js_total}")
        return "typescript", evidence

    evidence.append(f"source: js files {js_total} >= ts files {ts_total}")
    return "javascript", evidence


def detect_style_system(project_root: Path, deps: Dict[str, str], source_stats: Dict[str, int]) -> Tuple[str, List[str], float]:
    dep_names = set(deps.keys())
    scores = {
        "tailwind": 0.0,
        "css-modules": 0.0,
        "scss": 0.0,
        "less": 0.0,
        "styled-components": 0.0,
        "emotion": 0.0,
        "css": 0.2,
    }
    evidence = {name: [] for name in scores}

    def add(name: str, points: float, reason: str) -> None:
        scores[name] += points
        evidence[name].append(reason)

    if "tailwindcss" in dep_names:
        add("tailwind", 1.0, "dependency: tailwindcss")
    if (project_root / "tailwind.config.js").exists() or (project_root / "tailwind.config.ts").exists():
        add("tailwind", 0.5, "config: tailwind.config.*")

    module_total = (
        source_stats["module_css"]
        + source_stats["module_scss"]
        + source_stats["module_less"]
    )
    if module_total > 0:
        add("css-modules", 0.9, f"source: module style files {module_total}")

    if source_stats["scss"] > 0 or "sass" in dep_names:
        add("scss", 0.7, "source/dependency: scss or sass")

    if source_stats["less"] > 0 or "less" in dep_names:
        add("less", 0.7, "source/dependency: less")

    if "styled-components" in dep_names:
        add("styled-components", 1.0, "dependency: styled-components")

    if "@emotion/react" in dep_names or "@emotion/styled" in dep_names:
        add("emotion", 1.0, "dependency: emotion")

    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_name, top_score = ordered[0]
    second_score = ordered[1][1] if len(ordered) > 1 else 0.0

    confidence = min(0.98, 0.45 + top_score * 0.35)
    if top_score - second_score < 0.2:
        confidence -= 0.1
    confidence = max(0.1, round(confidence, 2))

    return top_name, evidence[top_name], confidence


def detect_package_manager(project_root: Path) -> Tuple[str, List[str]]:
    if (project_root / "pnpm-lock.yaml").exists():
        return "pnpm", ["file: pnpm-lock.yaml"]
    if (project_root / "yarn.lock").exists():
        return "yarn", ["file: yarn.lock"]
    if (project_root / "package-lock.json").exists():
        return "npm", ["file: package-lock.json"]
    if (project_root / "bun.lockb").exists() or (project_root / "bun.lock").exists():
        return "bun", ["file: bun lock"]
    return "npm", ["fallback: no lockfile"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect project stack metadata")
    parser.add_argument("--project-root", default=".", help="Project root path")
    parser.add_argument(
        "--framework",
        default="auto",
        choices=["auto", "next", "react", "nuxt", "vue", "taro", "svelte", "vanilla"],
        help="Framework override",
    )
    parser.add_argument(
        "--style",
        default="auto",
        choices=["auto", "tailwind", "css-modules", "scss", "less", "styled-components", "emotion", "css"],
        help="Style system override",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.exists() or not project_root.is_dir():
        return error(f"project root not found: {project_root}")

    package_data = load_package_json(project_root)
    deps = {}
    if isinstance(package_data, dict):
        for key in ("dependencies", "devDependencies", "peerDependencies"):
            block = package_data.get(key, {})
            if isinstance(block, dict):
                deps.update({str(k): str(v) for k, v in block.items()})

    source_stats = gather_source_stats(project_root)
    framework, fw_confidence, fw_evidence, fw_scores = detect_framework(project_root, deps)
    language, language_evidence = detect_language(project_root, source_stats)
    style_system, style_evidence, style_confidence = detect_style_system(project_root, deps, source_stats)
    package_manager, pm_evidence = detect_package_manager(project_root)

    overrides = {}
    if args.framework != "auto":
        framework = args.framework
        overrides["framework"] = args.framework
        fw_evidence = [f"override: framework={args.framework}"]
        fw_confidence = 0.99

    if args.style != "auto":
        style_system = args.style
        overrides["style_system"] = args.style
        style_evidence = [f"override: style={args.style}"]
        style_confidence = 0.99

    if not fw_evidence:
        fw_evidence = [f"fallback: framework={framework}"]
    if not style_evidence:
        style_evidence = [f"fallback: style_system={style_system}"]

    confidence = round(min(0.99, (fw_confidence + style_confidence) / 2.0), 2)

    output = {
        "framework": framework,
        "language": language,
        "style_system": style_system,
        "package_manager": package_manager,
        "confidence": confidence,
        "evidence": {
            "framework": fw_evidence,
            "language": language_evidence,
            "style_system": style_evidence,
            "package_manager": pm_evidence,
        },
        "diagnostics": {
            "framework_scores": {k: round(v, 2) for k, v in fw_scores.items()},
            "source_stats": source_stats,
        },
    }

    if overrides:
        output["overrides"] = overrides

    print(json.dumps(output, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
