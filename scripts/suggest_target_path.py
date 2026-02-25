#!/usr/bin/env python3
"""Suggest deterministic target path for design restoration output."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List


def load_dependencies(project_root: Path) -> Dict[str, str]:
    package_json = project_root / "package.json"
    if not package_json.exists():
        return {}
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

    deps: Dict[str, str] = {}
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        block = data.get(key, {})
        if isinstance(block, dict):
            deps.update({str(k): str(v) for k, v in block.items()})
    return deps


def infer_framework(project_root: Path, deps: Dict[str, str], framework_opt: str) -> str:
    if framework_opt != "auto":
        return framework_opt

    dep_names = set(deps.keys())
    if "next" in dep_names:
        return "next"
    if "nuxt" in dep_names:
        return "nuxt"
    if any(name.startswith("@tarojs/") for name in dep_names):
        return "taro"
    if "@sveltejs/kit" in dep_names or "svelte" in dep_names:
        return "svelte"
    if "vue" in dep_names:
        return "vue"
    if "react" in dep_names:
        return "react"

    if (project_root / "src/app").exists() or (project_root / "app").exists():
        return "next"
    if (project_root / "pages").exists() and (project_root / "nuxt.config.ts").exists():
        return "nuxt"

    return "vanilla"


def infer_language(project_root: Path, language_opt: str) -> str:
    if language_opt != "auto":
        return language_opt
    if (project_root / "tsconfig.json").exists():
        return "typescript"
    return "javascript"


def to_pascal_case(value: str) -> str:
    chunks = re.split(r"[^a-zA-Z0-9]+", value)
    filtered = [chunk for chunk in chunks if chunk]
    if not filtered:
        return "RestoredDesign"
    return "".join(chunk[:1].upper() + chunk[1:] for chunk in filtered)


def to_kebab_case(value: str) -> str:
    replaced = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value)
    replaced = re.sub(r"[^a-zA-Z0-9]+", "-", replaced)
    normalized = replaced.strip("-").lower()
    return normalized or "restored-design"


def choose_extension(framework: str, language: str) -> str:
    if framework in {"vue", "nuxt"}:
        return "vue"
    if framework == "svelte":
        return "svelte"
    if framework == "vanilla":
        return "html"
    if framework in {"next", "react", "taro"}:
        return "tsx" if language == "typescript" else "jsx"
    return "tsx" if language == "typescript" else "jsx"


def default_path(project_root: Path, framework: str, scope: str, name: str, extension: str) -> Path:
    component_name = to_pascal_case(name)
    route_name = to_kebab_case(name)

    if framework == "next":
        if scope == "page":
            if (project_root / "src/app").exists():
                return Path("src/app") / route_name / f"page.{extension}"
            if (project_root / "app").exists():
                return Path("app") / route_name / f"page.{extension}"
            if (project_root / "src/pages").exists():
                return Path("src/pages") / f"{route_name}.{extension}"
            return Path("pages") / f"{route_name}.{extension}"
        return Path("src/components") / f"{component_name}.{extension}"

    if framework == "react":
        if scope == "page":
            return Path("src/pages") / f"{component_name}.{extension}"
        return Path("src/components") / f"{component_name}.{extension}"

    if framework == "nuxt":
        if scope == "page":
            return Path("pages") / f"{route_name}.vue"
        return Path("components") / f"{component_name}.vue"

    if framework == "vue":
        if scope == "page":
            return Path("src/views") / f"{component_name}.vue"
        return Path("src/components") / f"{component_name}.vue"

    if framework == "taro":
        if scope == "page":
            return Path("src/pages") / route_name / f"index.{extension}"
        return Path("src/components") / component_name / f"index.{extension}"

    if framework == "svelte":
        if scope == "page":
            if (project_root / "src/routes").exists():
                return Path("src/routes") / route_name / "+page.svelte"
            return Path("src/pages") / f"{route_name}.svelte"
        if (project_root / "src/lib").exists():
            return Path("src/lib") / f"{component_name}.svelte"
        return Path("src/components") / f"{component_name}.svelte"

    if scope == "page":
        if (project_root / "src/pages").exists():
            return Path("src/pages") / f"{route_name}.html"
        return Path("pages") / f"{route_name}.html"

    return Path("components") / f"{route_name}.html"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Suggest target output path")
    parser.add_argument("--project-root", default=".", help="Project root path")
    parser.add_argument(
        "--framework",
        default="auto",
        choices=["auto", "next", "react", "nuxt", "vue", "taro", "svelte", "vanilla"],
        help="Framework value or auto",
    )
    parser.add_argument(
        "--language",
        default="auto",
        choices=["auto", "typescript", "javascript"],
        help="Language value or auto",
    )
    parser.add_argument(
        "--scope",
        default="component",
        choices=["page", "component", "section"],
        help="Target implementation scope",
    )
    parser.add_argument("--target", default="", help="Explicit target path")
    parser.add_argument("--name", default="RestoredDesign", help="Name hint")
    parser.add_argument(
        "--overwrite",
        default="ask",
        choices=["ask", "replace", "patch", "new"],
        help="Overwrite behavior",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.exists() or not project_root.is_dir():
        print(json.dumps({"error": f"project root not found: {project_root}"}, ensure_ascii=True))
        return 2

    deps = load_dependencies(project_root)
    framework = infer_framework(project_root, deps, args.framework)
    language = infer_language(project_root, args.language)
    extension = choose_extension(framework, language)

    scope = args.scope
    normalized_scope = "component" if scope == "section" else scope

    reasoning: List[str] = []
    if args.framework == "auto":
        reasoning.append(f"framework inferred as {framework}")
    else:
        reasoning.append(f"framework override applied: {framework}")

    if args.language == "auto":
        reasoning.append(f"language inferred as {language}")
    else:
        reasoning.append(f"language override applied: {language}")

    if args.target:
        suggested = Path(args.target)
        if suggested.is_absolute():
            suggested_abs = suggested
            try:
                suggested_rel = suggested_abs.relative_to(project_root)
            except ValueError:
                suggested_rel = suggested_abs
        else:
            suggested_rel = suggested
            suggested_abs = project_root / suggested_rel
        reasoning.append("explicit target path provided")
    else:
        suggested_rel = default_path(project_root, framework, normalized_scope, args.name, extension)
        suggested_abs = project_root / suggested_rel
        reasoning.append(f"target path suggested from framework={framework} scope={normalized_scope}")

    path_exists = suggested_abs.exists()
    needs_confirmation = False
    confirmation_reasons: List[str] = []

    if framework == "vanilla" and args.framework == "auto":
        needs_confirmation = True
        confirmation_reasons.append("framework fallback to vanilla")

    if path_exists and args.overwrite in {"ask", "new"}:
        needs_confirmation = True
        confirmation_reasons.append(f"target exists and overwrite={args.overwrite}")

    if not path_exists and args.overwrite == "patch":
        needs_confirmation = True
        confirmation_reasons.append("overwrite=patch but target file does not exist")

    output = {
        "framework": framework,
        "language": language,
        "scope": scope,
        "recommended_path": str(suggested_rel),
        "recommended_path_abs": str(suggested_abs),
        "path_exists": path_exists,
        "overwrite": args.overwrite,
        "needs_confirmation": needs_confirmation,
        "confirmation_reasons": confirmation_reasons,
        "reasoning": reasoning,
    }

    print(json.dumps(output, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
