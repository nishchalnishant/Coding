from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "google-sde2" / "PROBLEM_DETAILS.md"


def slugify(title: str) -> str:
    s = title.strip().lower()
    s = s.replace("&", "and")
    s = re.sub(r"[’']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s


def normalize_key(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"\s+", " ", s)
    # normalize common separators
    s = re.sub(r"\s*/\s*", "/", s)
    s = re.sub(r"\s+—\s+", " — ", s)
    return s


def iter_md_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*.md"):
        if ".git" in p.parts:
            continue
        if "books" in p.parts:
            continue
        yield p


def parse_catalog_titles(catalog_text: str) -> Dict[str, str]:
    """
    Return mapping title_lower -> anchor_id derived from catalog headings.
    """
    mapping: Dict[str, str] = {}
    for m in re.finditer(r"^###\s+(.+?)\s*$", catalog_text, re.M):
        title = m.group(1).strip()
        mapping[normalize_key(title)] = slugify(title)
    return mapping


def ensure_explicit_anchors(catalog_text: str) -> str:
    """
    Insert <a id="..."></a> line above each ### heading if missing.
    Id is derived from heading text (slugify).
    """
    lines = catalog_text.splitlines(True)
    out: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(###)\s+(.+?)\s*$", line.rstrip("\n"))
        if m:
            title = m.group(2).strip()
            anchor = slugify(title)
            prev = out[-1] if out else ""
            if not re.match(rf'^<a id="{re.escape(anchor)}"></a>\s*$', prev.strip()):
                out.append(f'<a id="{anchor}"></a>\n')
            out.append(line)
            i += 1
            continue
        out.append(line)
        i += 1
    return "".join(out)


def rel_catalog_link(from_file: Path, anchor_id: str) -> str:
    rel = os.path.relpath(CATALOG_PATH, start=from_file.parent).replace(os.sep, "/")
    return f"{rel}#{anchor_id}"


def linkify_bold_titles(text: str, title_to_id: Dict[str, str], link_prefix: str) -> str:
    """
    Replace **Title** with **[Title](...#id)** when Title matches catalog.
    """

    def repl(m: re.Match[str]) -> str:
        title = m.group(1)
        key = normalize_key(title)
        if key not in title_to_id:
            return m.group(0)
        # already linkified?
        if title.startswith("[") or "](" in title:
            return m.group(0)
        anchor_id = title_to_id[key]
        return f"**[{title}]({link_prefix}{anchor_id})**"

    # Only replace bold tokens that are likely used as a "title" (not arbitrary emphasis).
    # Heuristic: Title Case-ish or contains digits/roman, but still avoid huge replacements:
    pattern = r"\*\*([^\*\n\|]{2,80}?)\*\*"
    return re.sub(pattern, repl, text)


def linkify_bullets(text: str, title_to_id: Dict[str, str], link_prefix: str) -> str:
    """
    Linkify bullet items like:
      - Two Sum
      - Two Sum — trick: ...
      - Trapping Rain Water (Hard / Stretch)
    """
    out_lines: List[str] = []
    for raw in text.splitlines():
        line = raw
        m = re.match(r"^(\s*[-*]\s+)(.+)$", line)
        if not m:
            out_lines.append(line)
            continue
        prefix, rest = m.group(1), m.group(2)
        if "](" in rest:
            out_lines.append(line)
            continue
        # Split off trailing commentary "— ..." (em dash) if present
        main, sep, tail = rest.partition("—")
        tail = (sep + tail) if sep else ""

        main_stripped = main.strip()
        qual = ""

        # Try matching with parentheses first (some titles include them),
        # otherwise treat as qualifier and strip.
        main_clean_full = re.sub(r"^\*\*(.+)\*\*$", r"\1", main_stripped).strip()
        key_full = normalize_key(main_clean_full)
        if key_full in title_to_id:
            anchor_id = title_to_id[key_full]
            linked = f"[{main_clean_full}]({link_prefix}{anchor_id})"
            out_lines.append(f"{prefix}{linked} {tail}".rstrip())
            continue

        qm = re.match(r"^(.*?)(\s*\([^)]*\)\s*)$", main_stripped)
        if qm:
            main_stripped = qm.group(1).strip()
            qual = qm.group(2)

        # Remove surrounding bold markers in bullet (rare)
        main_clean = re.sub(r"^\*\*(.+)\*\*$", r"\1", main_stripped).strip()

        key = normalize_key(main_clean)
        if key in title_to_id:
            anchor_id = title_to_id[key]
            linked = f"[{main_clean}]({link_prefix}{anchor_id})"
            # restore original emphasis if it was bold-only bullet
            out_lines.append(f"{prefix}{linked}{qual} {tail}".rstrip())
        else:
            out_lines.append(line)
    return "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")


def main() -> int:
    if not CATALOG_PATH.exists():
        raise SystemExit(f"Catalog not found: {CATALOG_PATH}")

    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")
    catalog_text2 = ensure_explicit_anchors(catalog_text)
    if catalog_text2 != catalog_text:
        CATALOG_PATH.write_text(catalog_text2, encoding="utf-8")
        catalog_text = catalog_text2

    title_to_id = parse_catalog_titles(catalog_text)

    changed_files = 0
    for md in iter_md_files(REPO_ROOT):
        if md == CATALOG_PATH:
            continue
        text = md.read_text(encoding="utf-8")
        # Build a file-specific link prefix (path + '#')
        rel = os.path.relpath(CATALOG_PATH, start=md.parent).replace(os.sep, "/")
        link_prefix = f"{rel}#"

        new = text
        new = linkify_bullets(new, title_to_id, link_prefix)
        new = linkify_bold_titles(new, title_to_id, link_prefix)

        if new != text:
            md.write_text(new, encoding="utf-8")
            changed_files += 1

    print(f"Updated {changed_files} markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
