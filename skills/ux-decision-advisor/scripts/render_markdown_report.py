#!/usr/bin/env python3
"""Render localized Markdown as a single offline H5 report.

Standard library only. Supports headings, paragraphs, lists, blockquotes,
tables, inline/fenced code, safe links, and a small acyclic Mermaid flowchart
subset. Raw HTML is escaped and remote assets are never fetched.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import os
import re
import sys
import unicodedata
from collections import defaultdict, deque
from pathlib import Path
from urllib.parse import urlsplit

BASE = Path(__file__).resolve().parents[1]
SHELL = BASE / "assets" / "markdown-report-shell.html"
MAX_INPUT_BYTES = 2_000_000


class InputIssue(ValueError):
    pass


def read_markdown(path: Path) -> tuple[dict[str, str], str]:
    if not path.is_file():
        raise InputIssue("INPUT_NOT_A_FILE")
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise InputIssue("INPUT_TOO_LARGE")
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    metadata: dict[str, str] = {}
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            for line in text[4:end].splitlines():
                if ":" in line and not line.lstrip().startswith("#"):
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip().strip('"').strip("'")
            text = text[end + 5:]
    if not text.strip():
        raise InputIssue("EMPTY_MARKDOWN")
    return metadata, text


def safe_link(url: str) -> bool:
    try:
        parsed = urlsplit(url)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https", "mailto"} or (not parsed.scheme and url.startswith("#"))


def inline_markdown(text: str, language: str = "zh") -> str:
    tokens: list[str] = []

    def token(value: str) -> str:
        tokens.append(value)
        return f"\x00{len(tokens) - 1}\x00"

    def code_repl(match: re.Match) -> str:
        return token("<code>" + html.escape(match.group(1)) + "</code>")

    def image_repl(match: re.Match) -> str:
        alt, url = match.group(1), match.group(2)
        if re.match(r"^data:image/(png|jpeg|jpg|webp|gif);base64,", url, re.I):
            return token(f'<img src="{html.escape(url, quote=True)}" alt="{html.escape(alt, quote=True)}">')
        message = f"外部图片未嵌入：{alt}（{url}）" if language == "zh" else f"External image not embedded: {alt} ({url})"
        return token(f'<span class="external-image">{html.escape(message)}</span>')

    def link_repl(match: re.Match) -> str:
        label, url = match.group(1), match.group(2)
        if safe_link(url):
            return token(f'<a href="{html.escape(url, quote=True)}" rel="noopener noreferrer">{html.escape(label)}</a>')
        message = f"链接未启用：{url}" if language == "zh" else f"Link disabled: {url}"
        return token(f'<code>{html.escape(label)}</code> <span class="small">（{html.escape(message)}）</span>' if language == "zh" else f'<code>{html.escape(label)}</code> <span class="small">({html.escape(message)})</span>')

    text = re.sub(r"`([^`]+)`", code_repl, text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image_repl, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, text)
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    for index, value in enumerate(tokens):
        escaped = escaped.replace(f"\x00{index}\x00", value)
    return escaped


def split_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith(r"\|"):
        line = line[:-1]
    cells = re.split(r"(?<!\\)\|", line)
    return [cell.strip().replace(r"\|", "|") for cell in cells]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


NODE_ID_RE = re.compile(r"[A-Za-z0-9_]+")
NODE_RE = re.compile(r"([A-Za-z0-9_]+)(?:\[(.*?)\]|\((.*?)\)|\{(.*?)\})")
EDGE_SPLIT_RE = re.compile(r"\s*(-->|-\.->|==>)(?:\|([^|]*)\|\s*)?")


def parse_mermaid(source: str) -> tuple[str, dict[str, str], dict[str, str], list[tuple[str, str, str, str]]] | None:
    lines = [line.strip() for line in source.splitlines() if line.strip() and not line.strip().startswith("%%")]
    if not lines:
        return None
    match = re.fullmatch(r"(?:flowchart|graph)\s+(TD|LR)", lines[0], re.I)
    if not match:
        return None
    direction = match.group(1).upper()
    nodes: dict[str, str] = {}
    shapes: dict[str, str] = {}
    edges: list[tuple[str, str, str, str]] = []
    for line in lines[1:]:
        if any(arrow in line for arrow in ("-->", "-.->", "==>")):
            for node in NODE_RE.finditer(line):
                node_id = node.group(1)
                labels = node.groups()[1:]
                label = next((value for value in labels if value is not None), "")
                nodes[node_id] = label or node_id
                shapes[node_id] = "diamond" if labels[2] is not None else "rect"
            clean_line = NODE_RE.sub(lambda match: match.group(1), line)
            parts = re.split(EDGE_SPLIT_RE, clean_line)
            if len(parts) < 4 or (len(parts) - 1) % 3 != 0:
                return None
            for index in range(0, len(parts) - 1, 3):
                src = parts[index].strip()
                arrow = parts[index + 1]
                label = (parts[index + 2] or "").strip()
                target = parts[index + 3].strip()
                if not NODE_ID_RE.fullmatch(src) or not NODE_ID_RE.fullmatch(target):
                    return None
                nodes.setdefault(src, src)
                nodes.setdefault(target, target)
                edges.append((src, arrow, label, target))
            continue
        node = NODE_RE.fullmatch(line)
        if not node:
            return None
        node_id = node.group(1)
        labels = node.groups()[1:]
        label = next((value for value in labels if value is not None), "")
        nodes[node_id] = label or node_id
        shapes[node_id] = "diamond" if labels[2] is not None else "rect"
    if not nodes:
        return None
    return direction, {key: nodes[key] for key in nodes}, shapes, edges


def display_width(value: str) -> int:
    return sum(2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1 for char in value)


def wrap_label(value: str, max_units: int = 24) -> list[str]:
    lines: list[str] = []
    current = ""
    current_units = 0
    for char in value:
        units = 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
        if current and current_units + units > max_units:
            lines.append(current)
            current = ""
            current_units = 0
        current += char
        current_units += units
    if current:
        lines.append(current)
    return lines or [""]


def mermaid_svg(source: str, language: str = "zh") -> str | None:
    parsed = parse_mermaid(source)
    if parsed is None:
        return None
    direction, nodes, shapes, edges = parsed
    adjacency: dict[str, list[str]] = defaultdict(list)
    indegree = {node: 0 for node in nodes}
    for src, _, _, target in edges:
        adjacency[src].append(target)
        indegree[target] += 1
    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    levels = {node: 0 for node in nodes}
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for target in adjacency[node]:
            levels[target] = max(levels[target], levels[node] + 1)
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if visited != len(nodes):
        return None

    by_level: dict[int, list[str]] = defaultdict(list)
    for node in sorted(nodes):
        by_level[levels[node]].append(node)
    label_lines = {node: wrap_label(nodes[node]) for node in nodes}
    sizes: dict[str, tuple[float, float]] = {}
    for node, lines in label_lines.items():
        node_width = max(118.0, 34.0 + max(display_width(line) for line in lines) * 7.8)
        node_height = max(46.0, 18.0 * len(lines) + 16.0)
        sizes[node] = (node_width, node_height)
    positions: dict[str, tuple[float, float, float, float]] = {}
    if direction == "TD":
        row_widths = {
            level: sum(sizes[node][0] for node in items) + 36.0 * (len(items) - 1)
            for level, items in by_level.items()
        }
        max_row_width = max(row_widths.values())
        level_heights = {level: max(sizes[node][1] for node in items) for level, items in by_level.items()}
        y_offsets: dict[int, float] = {}
        cursor_y = 28.0
        for level in sorted(by_level):
            y_offsets[level] = cursor_y
            cursor_y += level_heights[level] + 46.0
        for level, items in by_level.items():
            cursor_x = 40.0 + (max_row_width - row_widths[level]) / 2.0
            for node in items:
                node_width, node_height = sizes[node]
                positions[node] = (cursor_x, y_offsets[level], node_width, node_height)
                cursor_x += node_width + 36.0
    else:
        column_widths = {level: max(sizes[node][0] for node in items) for level, items in by_level.items()}
        x_offsets: dict[int, float] = {}
        cursor_x = 34.0
        for level in sorted(by_level):
            x_offsets[level] = cursor_x
            cursor_x += column_widths[level] + 70.0
        for level, items in by_level.items():
            cursor_y = 28.0
            for node in items:
                node_width, node_height = sizes[node]
                positions[node] = (x_offsets[level], cursor_y, node_width, node_height)
                cursor_y += node_height + 40.0
    width = max(480.0, max(x + w for x, y, w, h in positions.values()) + 40.0)
    height = max(180.0, max(y + h for x, y, w, h in positions.values()) + 36.0)
    marker_id = "arrow-" + hashlib.sha1(source.encode("utf-8")).hexdigest()[:10]
    aria_label = "Markdown Mermaid 流程图" if language == "zh" else "Markdown Mermaid flowchart"
    parts = [
        f'<svg class="mermaid-svg" viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="{aria_label}">',
        f'<defs><marker id="{marker_id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" class="mermaid-arrow"/></marker></defs>',
    ]
    for src, arrow, label, target in edges:
        sx, sy, sw, sh = positions[src]
        tx, ty, tw, th = positions[target]
        if direction == "TD":
            x1, y1 = sx + sw / 2, sy + sh
            x2, y2 = tx + tw / 2, ty
            cx1, cy1 = x1, (y1 + y2) / 2
            cx2, cy2 = x2, (y1 + y2) / 2
        else:
            x1, y1 = sx + sw, sy + sh / 2
            x2, y2 = tx, ty + th / 2
            cx1, cy1 = (x1 + x2) / 2, y1
            cx2, cy2 = (x1 + x2) / 2, y2
        dash = ' stroke-dasharray="6 5"' if arrow == "-.->" else ""
        marker = "" if arrow == "-.->" else f' marker-end="url(#{marker_id})"'
        parts.append(f'<path d="M {x1:.1f} {y1:.1f} C {cx1:.1f} {cy1:.1f}, {cx2:.1f} {cy2:.1f}, {x2:.1f} {y2:.1f}" class="mermaid-edge"{dash}{marker}/>')
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 7
            parts.append(f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" class="mermaid-edge-label">{html.escape(label)}</text>')
    for node, (x, y, w, h) in positions.items():
        if shapes.get(node) == "diamond":
            points = f"{x + w / 2:.1f},{y:.1f} {x + w:.1f},{y + h / 2:.1f} {x + w / 2:.1f},{y + h:.1f} {x:.1f},{y + h / 2:.1f}"
            parts.append(f'<polygon points="{points}" class="mermaid-node"/>')
        else:
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="9" class="mermaid-node"/>')
        lines = label_lines[node]
        start_y = y + h / 2 - (len(lines) - 1) * 9 + 5
        for line_index, line in enumerate(lines):
            parts.append(f'<text x="{x + w / 2:.1f}" y="{start_y + line_index * 18:.1f}" text-anchor="middle" class="mermaid-label">{html.escape(line)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def render_mermaid(source: str, language: str = "zh") -> str:
    svg = mermaid_svg(source, language)
    if svg:
        caption = "Markdown Mermaid 流程图 · 本地 SVG" if language == "zh" else "Markdown Mermaid flowchart · local SVG"
        return f'<figure class="diagram">{svg}<figcaption>{caption}</figcaption></figure>'
    fallback = "当前图表未转为 SVG，以下保留可读 Mermaid 源文本。" if language == "zh" else "This diagram was not converted to SVG; readable Mermaid source follows."
    return (
        f'<figure class="diagram fallback"><figcaption>{fallback}</figcaption>'
        f'<pre><code>{html.escape(source)}</code></pre></figure>'
    )


def markdown_to_html(markdown: str, language: str = "zh") -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        fence = re.match(r"^```([A-Za-z0-9_-]*)\s*$", stripped)
        if fence:
            fence_language = fence.group(1).lower()
            index += 1
            block: list[str] = []
            while index < len(lines) and not re.match(r"^```\s*$", lines[index].strip()):
                block.append(lines[index])
                index += 1
            if index >= len(lines):
                raise InputIssue("UNCLOSED_CODE_FENCE")
            index += 1
            source = "\n".join(block)
            if fence_language == "mermaid":
                output.append(render_mermaid(source, language))
            else:
                output.append(f'<pre><code class="language-{html.escape(fence_language)}">{html.escape(source)}</code></pre>')
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            output.append(f"<h{level}>{inline_markdown(heading.group(2), language)}</h{level}>")
            index += 1
            continue
        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", stripped):
            output.append("<hr>")
            index += 1
            continue
        if stripped.startswith(">"):
            quote: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote.append(lines[index].strip()[1:].lstrip())
                index += 1
            output.append("<blockquote>" + "<br>".join(inline_markdown(item, language) for item in quote) + "</blockquote>")
            continue
        if "|" in line and index + 1 < len(lines) and is_table_separator(lines[index + 1]):
            headers = split_table_row(line)
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                rows.append(split_table_row(lines[index]))
                index += 1
            output.append('<div class="table-wrap"><table><thead><tr>' + "".join(f'<th scope="col">{inline_markdown(cell, language)}</th>' for cell in headers) + "</tr></thead><tbody>")
            for row in rows:
                padded = row + [""] * (len(headers) - len(row))
                output.append("<tr>" + "".join(f"<td>{inline_markdown(cell, language)}</td>" for cell in padded[:len(headers)]) + "</tr>")
            output.append("</tbody></table></div>")
            continue
        if re.match(r"^(?:[-*+]|\d+\.)\s+", stripped):
            ordered = bool(re.match(r"^\d+\.\s+", stripped))
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            while index < len(lines):
                item = re.match(r"^(?:[-*+]|\d+\.)\s+(.+)$", lines[index].strip())
                if not item:
                    break
                items.append("<li>" + inline_markdown(item.group(1), language) + "</li>")
                index += 1
            output.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        paragraph = [stripped]
        index += 1
        while index < len(lines):
            nxt = lines[index].strip()
            if not nxt or re.match(r"^(#{1,6})\s+", nxt) or nxt.startswith(">") or nxt.startswith("```") or re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", nxt):
                break
            if "|" in lines[index] and index + 1 < len(lines) and is_table_separator(lines[index + 1]):
                break
            if re.match(r"^(?:[-*+]|\d+\.)\s+", nxt):
                break
            paragraph.append(nxt)
            index += 1
        output.append("<p>" + " ".join(inline_markdown(part, language) for part in paragraph) + "</p>")
    return "\n".join(output)


def detect_language(markdown: str) -> str:
    chinese = len(re.findall(r"[\u4e00-\u9fff]", markdown))
    english = len(re.findall(r"[A-Za-z]", markdown))
    return "zh" if chinese > english * 0.25 else "en"


def first_heading(markdown: str) -> str:
    for line in markdown.splitlines():
        match = re.match(r"^#\s+(.+)$", line.strip())
        if match:
            return re.sub(r"[*_`]", "", match.group(1)).strip()
    return "UXDA research report"


def render_page(title: str, subtitle: str, language: str, content: str, source: str) -> str:
    template = SHELL.read_text(encoding="utf-8")
    for marker in ("__CONTENT__", "__SOURCE__"):
        if template.count(marker) != 1:
            raise InputIssue("TEMPLATE_MARKER_INVALID:" + marker)
    for marker in ("__TITLE__", "__SUBTITLE__", "__LANG__", "__NOTE__", "__PRINT_LABEL__", "__SOURCE_LABEL__", "__FOOTER__"):
        if template.count(marker) < 1:
            raise InputIssue("TEMPLATE_MARKER_INVALID:" + marker)
    if language == "zh":
        note = "本地离线报告 · 无外部资源 · 内容真实性需人工复核"
        print_label = "打印 / 存为 PDF"
        source_label = "查看原始 Markdown"
        footer = "由 UXDA render_markdown_report.py 在本地生成。渲染器不验证内容真实性、引用或研究结论。"
    else:
        note = "Offline local report · no external assets · claims require human review"
        print_label = "Print / Save PDF"
        source_label = "View source Markdown"
        footer = "Generated locally by UXDA render_markdown_report.py. The renderer does not verify claims, citations, or research conclusions."
    return (
        template.replace("__TITLE__", html.escape(title))
        .replace("__SUBTITLE__", html.escape(subtitle))
        .replace("__CONTENT__", content)
        .replace("__SOURCE__", html.escape(source))
        .replace("__LANG__", "zh-CN" if language == "zh" else "en")
        .replace("__NOTE__", html.escape(note))
        .replace("__PRINT_LABEL__", html.escape(print_label))
        .replace("__SOURCE_LABEL__", html.escape(source_label))
        .replace("__FOOTER__", html.escape(footer))
    )


def run(input_path: Path, output_path: Path, *, title: str | None = None, subtitle: str | None = None, language: str | None = None) -> dict:
    output = output_path.resolve()
    source = BASE.resolve()
    if output == input_path.resolve():
        raise InputIssue("OUTPUT_OVERWRITES_INPUT")
    if output.exists() and input_path.exists() and os.path.samefile(output, input_path):
        raise InputIssue("OUTPUT_OVERWRITES_INPUT")
    if output == source or source in output.parents:
        raise InputIssue("OUTPUT_INSIDE_SKILL_SOURCE")
    metadata, markdown = read_markdown(input_path)
    selected_language = language or metadata.get("language") or detect_language(markdown)
    if selected_language not in {"zh", "en"}:
        raise InputIssue("LANGUAGE_MUST_BE_ZH_OR_EN")
    selected_title = title or metadata.get("title") or first_heading(markdown)
    selected_subtitle = subtitle if subtitle is not None else metadata.get("subtitle", "")
    content = markdown_to_html(markdown, selected_language)
    page = render_page(selected_title, selected_subtitle, selected_language, content, markdown)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    return {"title": selected_title, "language": selected_language, "bytes": output.stat().st_size}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--title")
    parser.add_argument("--subtitle", default=None)
    parser.add_argument("--language", choices=["zh", "en"], default=None)
    args = parser.parse_args()
    try:
        result = run(args.input, args.output, title=args.title, subtitle=args.subtitle, language=args.language)
    except Exception as exc:
        code = str(exc) if isinstance(exc, InputIssue) else "MARKDOWN_RENDERING_ERROR"
        print("MARKDOWN_REPORT_FAIL:", code, file=sys.stderr)
        return 2
    print(f"MARKDOWN_REPORT_OK language={result['language']} bytes={result['bytes']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
