#!/usr/bin/env python3
"""Convert FLOWCHARTS.md / MINDMAP.md style docs to print PDF via headless Chrome."""

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
MM_TO_PT = 72 / 25.4


@dataclass(frozen=True)
class PrintProfile:
    """Per-document print settings tuned for readability on A4."""

    orientation: str = "portrait"  # portrait | landscape
    margin_mm: float = 12.0
    tree_font_pt: float = 8.0
    tree_line_height: float = 1.2
    body_font_pt: float = 10.0
    wrap_at: int | None = None  # None → auto-fit printable width
    columns: int = 1  # 2 = pack ### topic blocks side-by-side


PRESETS: dict[str, PrintProfile] = {
    "FLOWCHARTS": PrintProfile(
        orientation="portrait",
        tree_font_pt=8.5,
        columns=1,
    ),
    "MINDMAP": PrintProfile(
        orientation="landscape",
        tree_font_pt=7.5,
        columns=2,
    ),
    "MINDMAP-DS": PrintProfile(
        orientation="landscape",
        tree_font_pt=8.0,
        columns=2,
    ),
    "MINDMAP-ALGO": PrintProfile(
        orientation="landscape",
        tree_font_pt=8.0,
        columns=2,
    ),
}


@dataclass
class TopicBlock:
    title: str
    tree: str


@dataclass
class Section:
    title: str
    topics: list[TopicBlock] = field(default_factory=list)
    standalone_tree: str | None = None


def page_width_pt(profile: PrintProfile) -> float:
    w_mm = 297.0 if profile.orientation == "landscape" else 210.0
    margin_pt = profile.margin_mm * MM_TO_PT
    return w_mm * MM_TO_PT - 2 * margin_pt


def char_width_pt(font_pt: float) -> float:
    return font_pt * 0.58


def effective_wrap_at(profile: PrintProfile) -> int:
    if profile.wrap_at is not None:
        return profile.wrap_at
    gap_pt = 10.0 if profile.columns > 1 else 0.0
    col_width = (page_width_pt(profile) - gap_pt * (profile.columns - 1)) / profile.columns
    usable = col_width - 14  # pre padding
    chars = int(usable / char_width_pt(profile.tree_font_pt)) - 1
    return max(52, chars)


def css_for(profile: PrintProfile) -> str:
    page = f"A4 {profile.orientation}"
    cols_css = ""
    if profile.columns > 1:
        cols_css = f"""
.topics.cols-{profile.columns} {{
  column-count: {profile.columns};
  column-gap: 10pt;
  column-fill: balance;
}}
.topic {{
  break-inside: avoid;
  -webkit-column-break-inside: avoid;
  page-break-inside: avoid;
  margin-bottom: 10pt;
}}
.topic h3 {{
  margin-top: 0;
}}
.topic pre.tree {{
  margin-bottom: 0;
}}
"""
    return f"""
@page {{
  size: {page};
  margin: {profile.margin_mm}mm {profile.margin_mm - 2}mm;
}}
* {{ box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: {profile.body_font_pt}pt;
  line-height: 1.35;
  color: #111;
  max-width: 100%;
  margin: 0;
  padding: 0;
}}
h1 {{
  font-size: {profile.body_font_pt + 6}pt;
  margin: 0 0 6pt;
  page-break-after: avoid;
}}
h2 {{
  font-size: {profile.body_font_pt + 2}pt;
  margin: 14pt 0 6pt;
  padding-top: 2pt;
  border-top: 1px solid #ccc;
  page-break-after: avoid;
  column-span: all;
}}
h3 {{
  font-size: {profile.body_font_pt + 0.5}pt;
  margin: 10pt 0 4pt;
  page-break-after: avoid;
}}
p.subtitle, p.nav {{
  font-size: {profile.body_font_pt - 1}pt;
  color: #444;
  margin: 0 0 8pt;
}}
pre.tree {{
  font-family: "Menlo", "Consolas", "Courier New", monospace;
  font-size: {profile.tree_font_pt}pt;
  line-height: {profile.tree_line_height};
  white-space: pre;
  overflow-wrap: normal;
  word-break: normal;
  background: #fafafa;
  border: 1px solid #ddd;
  border-radius: 3px;
  padding: 6pt 7pt;
  margin: 0 0 10pt;
  page-break-inside: auto;
  width: 100%;
}}
{cols_css}
@media print {{
  pre.tree {{ background: #fff; border-color: #bbb; }}
  h2 {{ page-break-before: auto; }}
}}
"""


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def wrap_tree_line(line: str, max_col: int) -> list[str]:
    if len(line) <= max_col:
        return [line]

    m = re.match(r"^([ \t│├└─]*)", line)
    prefix = m.group(1) if m else ""
    text = line[len(prefix) :]
    if not text.strip():
        return [line]

    cont = prefix
    if "├──" in prefix or "└──" in prefix:
        cont = re.sub(r"[├└]──", "│  ", prefix)
    elif prefix.endswith("│"):
        cont = prefix + "  "
    else:
        cont = prefix + "  "

    words = text.split(" ")
    chunks: list[str] = []
    current = ""
    budget = max_col - len(prefix)
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= budget:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = word
    if current:
        chunks.append(current)

    if not chunks:
        return [line[:max_col]]

    out = [prefix + chunks[0]]
    for chunk in chunks[1:]:
        out.append(cont + chunk)
    return out


def wrap_tree_block(text: str, max_col: int) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        lines.extend(wrap_tree_line(line, max_col))
    return "\n".join(lines)


def parse_md(md: str) -> tuple[list[str], list[Section]]:
    """Parse markdown into preamble HTML fragments and structured sections."""
    md = strip_frontmatter(md)
    lines = md.splitlines()

    preamble: list[str] = []
    sections: list[Section] = []
    current_section: Section | None = None
    current_topic: TopicBlock | None = None
    in_fence = False
    fence_buf: list[str] = []
    i = 0

    def flush_fence() -> None:
        nonlocal fence_buf, current_topic, current_section
        if not fence_buf:
            return
        content = "\n".join(fence_buf)
        fence_buf = []
        if current_topic is not None:
            current_topic.tree = content
            current_topic = None
        elif current_section is not None:
            current_section.standalone_tree = content

    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if in_fence:
                flush_fence()
                in_fence = False
            else:
                in_fence = True
            i += 1
            continue

        if in_fence:
            fence_buf.append(line)
            i += 1
            continue

        if not line.strip():
            i += 1
            continue

        if line.startswith("# "):
            preamble.append(f"<h1>{escape_html(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            if current_section is not None:
                sections.append(current_section)
            current_section = Section(title=line[3:].strip())
            current_topic = None
        elif line.startswith("### "):
            if current_section is None:
                current_section = Section(title="")
            current_topic = TopicBlock(title=line[4:].strip(), tree="")
            current_section.topics.append(current_topic)
        elif line.startswith("_") and line.endswith("_"):
            preamble.append(f'<p class="subtitle">{escape_html(line.strip("_"))}</p>')
        elif line.startswith("←"):
            preamble.append(f'<p class="nav">{escape_html(line)}</p>')
        else:
            preamble.append(f"<p>{escape_html(line)}</p>")
        i += 1

    if in_fence:
        flush_fence()
    if current_section is not None:
        sections.append(current_section)

    return preamble, sections


def render_tree(tree: str, profile: PrintProfile, columns: int) -> str:
    wrap = effective_wrap_at(
        PrintProfile(
            orientation=profile.orientation,
            margin_mm=profile.margin_mm,
            tree_font_pt=profile.tree_font_pt,
            tree_line_height=profile.tree_line_height,
            body_font_pt=profile.body_font_pt,
            wrap_at=profile.wrap_at,
            columns=columns,
        )
    )
    return f'<pre class="tree">{escape_html(wrap_tree_block(tree, wrap))}</pre>'


def md_to_html_body(md: str, profile: PrintProfile) -> str:
    preamble, sections = parse_md(md)
    out = list(preamble)

    for section in sections:
        if section.title:
            out.append(f"<h2>{escape_html(section.title)}</h2>")

        if section.topics and profile.columns > 1:
            out.append(f'<div class="topics cols-{profile.columns}">')
            for topic in section.topics:
                out.append('<div class="topic">')
                out.append(f"<h3>{escape_html(topic.title)}</h3>")
                out.append(render_tree(topic.tree, profile, profile.columns))
                out.append("</div>")
            out.append("</div>")
        elif section.topics:
            for topic in section.topics:
                out.append(f"<h3>{escape_html(topic.title)}</h3>")
                out.append(render_tree(topic.tree, profile, 1))
        elif section.standalone_tree:
            out.append(render_tree(section.standalone_tree, profile, 1))

    return "\n".join(out)


def escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_html(md_text: str, title: str, profile: PrintProfile) -> str:
    body = md_to_html_body(md_text, profile)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{escape_html(title)}</title>
<style>{css_for(profile)}</style>
</head>
<body>
{body}
</body>
</html>
"""


def chrome_pdf(html_path: Path, pdf_path: Path) -> None:
    if not CHROME.is_file():
        raise SystemExit(f"Chrome not found at {CHROME}")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not pdf_path.is_file():
        raise SystemExit(
            f"Chrome PDF failed ({result.returncode}):\n{result.stderr}\n{result.stdout}"
        )


def split_mindmap(md_path: Path) -> tuple[str, str]:
    body = strip_frontmatter(md_path.read_text(encoding="utf-8"))
    ds_marker = "## coding/data-structures/"
    algo_marker = "## coding/algorithms/"
    ds_start = body.index(ds_marker)
    algo_start = body.index(algo_marker)
    preamble = body[:ds_start].rstrip() + "\n\n"
    ds = preamble + body[ds_start:algo_start].rstrip() + "\n"
    algo_title = preamble.replace(
        "Mindmap — ASCII only (`coding/`)",
        "Mindmap — Algorithms (`coding/algorithms/`)",
    )
    algo = algo_title + body[algo_start:].rstrip() + "\n"
    return ds, algo


def profile_for(stem: str, args: argparse.Namespace) -> PrintProfile:
    base = PRESETS.get(stem, PrintProfile())
    if args.font_size is not None:
        base = PrintProfile(
            orientation=base.orientation,
            margin_mm=base.margin_mm,
            tree_font_pt=args.font_size,
            tree_line_height=base.tree_line_height,
            body_font_pt=base.body_font_pt,
            wrap_at=base.wrap_at,
            columns=base.columns,
        )
    if args.landscape:
        base = PrintProfile(
            orientation="landscape",
            margin_mm=base.margin_mm,
            tree_font_pt=base.tree_font_pt,
            tree_line_height=base.tree_line_height,
            body_font_pt=base.body_font_pt,
            wrap_at=base.wrap_at,
            columns=base.columns,
        )
    if args.columns is not None:
        base = PrintProfile(
            orientation=base.orientation,
            margin_mm=base.margin_mm,
            tree_font_pt=base.tree_font_pt,
            tree_line_height=base.tree_line_height,
            body_font_pt=base.body_font_pt,
            wrap_at=base.wrap_at,
            columns=args.columns,
        )
    return base


def convert_text(
    md_text: str,
    pdf_path: Path,
    profile: PrintProfile,
    title: str,
) -> Path:
    html = build_html(md_text, title, profile)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(html)
        html_path = Path(tmp.name)
    try:
        chrome_pdf(html_path, pdf_path)
    finally:
        html_path.unlink(missing_ok=True)
    return pdf_path


def convert(md_path: Path, pdf_path: Path | None, profile: PrintProfile) -> Path:
    md_path = md_path.resolve()
    pdf_path = (pdf_path or md_path.with_suffix(".pdf")).resolve()
    text = md_path.read_text(encoding="utf-8")
    return convert_text(text, pdf_path, profile, md_path.stem)


def page_count(pdf_path: Path) -> int | None:
    try:
        from pypdf import PdfReader

        return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        return None


def emit_pdf(
    md_path: Path,
    pdf_path: Path,
    profile: PrintProfile,
    md_text: str | None = None,
) -> None:
    title = pdf_path.stem
    text = md_text if md_text is not None else md_path.read_text(encoding="utf-8")
    pdf = convert_text(text, pdf_path, profile, title)
    size_kb = pdf.stat().st_size / 1024
    pages = page_count(pdf)
    wrap = effective_wrap_at(profile)
    page_note = f", {pages} pages" if pages else ""
    print(
        f"Wrote {pdf} ({size_kb:.0f} KB{page_note}) "
        f"[{profile.orientation}, {profile.tree_font_pt}pt, "
        f"{profile.columns} col, wrap≈{wrap}]"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Markdown ASCII docs → print PDF (per-file presets for readability)"
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="Markdown files")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: same as input)",
    )
    parser.add_argument(
        "--font-size",
        type=float,
        default=None,
        help="Override tree monospace font size (pt)",
    )
    parser.add_argument(
        "--landscape",
        action="store_true",
        help="Force landscape orientation",
    )
    parser.add_argument(
        "--columns",
        type=int,
        default=None,
        help="Number of topic columns (default: preset)",
    )
    parser.add_argument(
        "--split-mindmap",
        action="store_true",
        help="Emit MINDMAP-DS.pdf and MINDMAP-ALGO.pdf instead of one file",
    )
    args = parser.parse_args()

    out_dir = args.output_dir

    for inp in args.inputs:
        inp = inp.resolve()
        if args.split_mindmap and inp.stem == "MINDMAP":
            ds_text, algo_text = split_mindmap(inp)
            base = inp.parent if out_dir is None else out_dir
            ds_profile = profile_for("MINDMAP-DS", args)
            algo_profile = profile_for("MINDMAP-ALGO", args)
            emit_pdf(inp, base / "MINDMAP-DS.pdf", ds_profile, ds_text)
            emit_pdf(inp, base / "MINDMAP-ALGO.pdf", algo_profile, algo_text)
            continue

        profile = profile_for(inp.stem, args)
        out = (
            out_dir / f"{inp.stem}.pdf"
            if out_dir
            else inp.with_suffix(".pdf")
        )
        emit_pdf(inp, out, profile)


if __name__ == "__main__":
    main()
