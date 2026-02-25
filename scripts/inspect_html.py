#!/usr/bin/env python3
"""Inspect local HTML draft and extract structural and visual signals."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List

SEMANTIC_TAGS = {"header", "main", "section", "footer", "nav", "article", "aside", "form"}
INTERACTIVE_TAGS = {"button", "a", "input", "select", "textarea", "summary"}


class DraftInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tag_counter: Counter[str] = Counter()
        self.class_counter: Counter[str] = Counter()
        self.semantic_sections: Counter[str] = Counter()
        self.interactive_elements: List[Dict[str, str]] = []
        self.images: List[str] = []
        self.stylesheets: List[str] = []
        self.scripts: List[str] = []
        self.inline_styles: List[str] = []
        self.style_blocks: List[str] = []
        self._in_style = False
        self._style_buffer: List[str] = []
        self.stack: List[str] = []
        self.root_children: List[Dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs):
        attrs_dict = {k: v for k, v in attrs}

        self.tag_counter[tag] += 1

        class_attr = attrs_dict.get("class")
        if class_attr:
            for cls in class_attr.split():
                self.class_counter[cls] += 1

        if tag in SEMANTIC_TAGS:
            self.semantic_sections[tag] += 1

        if tag in INTERACTIVE_TAGS or attrs_dict.get("onclick") or attrs_dict.get("role") == "button":
            self.interactive_elements.append(
                {
                    "tag": tag,
                    "id": attrs_dict.get("id", ""),
                    "class": attrs_dict.get("class", ""),
                    "role": attrs_dict.get("role", ""),
                }
            )

        if tag == "img" and attrs_dict.get("src"):
            self.images.append(attrs_dict["src"])
        if tag == "link" and attrs_dict.get("href"):
            rel = (attrs_dict.get("rel") or "").lower()
            if "stylesheet" in rel:
                self.stylesheets.append(attrs_dict["href"])
        if tag == "script" and attrs_dict.get("src"):
            self.scripts.append(attrs_dict["src"])

        style_attr = attrs_dict.get("style")
        if style_attr:
            self.inline_styles.append(style_attr)

        parent = self.stack[-1] if self.stack else ""
        if parent == "body" and len(self.root_children) < 30:
            self.root_children.append(
                {
                    "tag": tag,
                    "id": attrs_dict.get("id", ""),
                    "class": attrs_dict.get("class", ""),
                }
            )

        if tag == "style":
            self._in_style = True
            self._style_buffer = []

        self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_endtag(self, tag: str):
        if tag == "style" and self._in_style:
            self._in_style = False
            text = "".join(self._style_buffer).strip()
            if text:
                self.style_blocks.append(text)
            self._style_buffer = []

        for idx in range(len(self.stack) - 1, -1, -1):
            if self.stack[idx] == tag:
                del self.stack[idx]
                break

    def handle_data(self, data: str):
        if self._in_style:
            self._style_buffer.append(data)


def unique_limited(items: List[str], limit: int = 40) -> List[str]:
    seen = set()
    result = []
    for item in items:
        normalized = item.strip()
        if not normalized:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
        if len(result) >= limit:
            break
    return result


def extract_tokens(css_text: str) -> Dict[str, List[str]]:
    colors = re.findall(r"#(?:[0-9a-fA-F]{3,8})\b|rgba?\([^)]*\)|hsla?\([^)]*\)", css_text)
    font_sizes = re.findall(r"font-size\s*:\s*([^;}{]+)", css_text, flags=re.IGNORECASE)
    spacings = re.findall(
        r"(?:margin|padding|gap|row-gap|column-gap)\s*:\s*([^;}{]+)",
        css_text,
        flags=re.IGNORECASE,
    )
    radii = re.findall(r"border-radius\s*:\s*([^;}{]+)", css_text, flags=re.IGNORECASE)
    shadows = re.findall(r"box-shadow\s*:\s*([^;}{]+)", css_text, flags=re.IGNORECASE)

    return {
        "colors": unique_limited(colors),
        "font_sizes": unique_limited(font_sizes),
        "spacings": unique_limited(spacings),
        "radii": unique_limited(radii),
        "shadows": unique_limited(shadows),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect local HTML design draft")
    parser.add_argument("--html", required=True, help="Path to local HTML file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    html_path = Path(args.html).expanduser().resolve()

    if not html_path.exists() or not html_path.is_file():
        print(json.dumps({"error": f"html file not found: {html_path}"}, ensure_ascii=True))
        return 2

    if html_path.suffix.lower() != ".html":
        print(json.dumps({"error": "input must be a .html file"}, ensure_ascii=True))
        return 2

    try:
        raw_html = html_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(json.dumps({"error": f"failed to read html: {exc}"}, ensure_ascii=True))
        return 2

    inspector = DraftInspector()
    inspector.feed(raw_html)

    combined_css = "\n".join(inspector.inline_styles + inspector.style_blocks)
    tokens = extract_tokens(combined_css)

    repeated_classes = [
        {"class": cls, "count": count}
        for cls, count in inspector.class_counter.most_common(30)
        if count >= 2
    ]

    top_tags = [{"tag": tag, "count": count} for tag, count in inspector.tag_counter.most_common(15)]
    semantic_sections = [
        {"tag": tag, "count": count} for tag, count in inspector.semantic_sections.most_common()
    ]

    output = {
        "html_path": str(html_path),
        "summary": {
            "element_count": sum(inspector.tag_counter.values()),
            "unique_tags": len(inspector.tag_counter),
            "top_tags": top_tags,
            "semantic_sections": semantic_sections,
            "interactive_elements": len(inspector.interactive_elements),
            "external_assets": {
                "images": unique_limited(inspector.images, limit=50),
                "stylesheets": unique_limited(inspector.stylesheets, limit=50),
                "scripts": unique_limited(inspector.scripts, limit=50),
            },
        },
        "tokens": tokens,
        "structure": {
            "root_children": inspector.root_children,
            "repeated_classes": repeated_classes,
            "sample_interactive": inspector.interactive_elements[:20],
        },
    }

    print(json.dumps(output, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
