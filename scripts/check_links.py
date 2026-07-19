#!/usr/bin/env python3
"""Check relative Markdown links and heading anchors across the repo.

Usage: python3 scripts/check_links.py [root]
Exits 1 if any broken file links or anchors are found.

Anchor rules mirror GitHub's slugger closely enough for this repo:
- explicit `{#custom-id}` heading attributes are honored
- code spans in headings contribute their text to the slug
- emoji are stripped; punctuation removed; whitespace -> hyphens
- comparison collapses hyphen runs on both sides (em-dash headings
  produce double hyphens on GitHub) and allows prefix matches
"""
import os
import re
import sys
import unicodedata

LINK_RE = re.compile(r'\]\(([^)\s]+)\)')
HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)$')
EXPLICIT_ID_RE = re.compile(r'\{#([A-Za-z0-9_-]+)\}\s*$')


def slugify(heading: str) -> str:
    h = EXPLICIT_ID_RE.sub('', heading)
    h = re.sub(r'`([^`]*)`', r'\1', h)  # code spans keep their text
    h = ''.join(c for c in h if not unicodedata.category(c).startswith('So'))
    h = h.strip().lower()
    h = re.sub(r'[^\w\s-]', '', h)
    return re.sub(r'\s+', '-', h).strip('-')


def norm(s: str) -> str:
    return re.sub(r'-+', '-', s)


def anchors_of(path: str, cache: dict) -> set:
    if path in cache:
        return cache[path]
    anchors = set()
    in_fence = False
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                if line.lstrip().startswith('```'):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                m = HEADING_RE.match(line.rstrip())
                if not m:
                    continue
                text = m.group(2)
                em = EXPLICIT_ID_RE.search(text)
                if em:
                    anchors.add(em.group(1).lower())
                anchors.add(slugify(text))
    except OSError:
        pass
    cache[path] = anchors
    return anchors


def anchor_ok(frag: str, anchors: set) -> bool:
    f = norm(frag.lower())
    for a in anchors:
        na = norm(a)
        if f == na or na.startswith(f) or f.startswith(na):
            return True
    return False


def main() -> int:
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
    cache = {}
    errors = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in ('.git', 'node_modules', '.claude')]
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            src = os.path.join(dirpath, fn)
            with open(src, encoding='utf-8') as f:
                text = f.read()
            for link in LINK_RE.findall(text):
                if link.startswith(('http://', 'https://', 'mailto:')):
                    continue
                link = link.split('?')[0]
                if link.startswith('#'):
                    target, frag = src, link[1:]
                else:
                    part, _, frag = link.partition('#')
                    target = os.path.normpath(
                        os.path.join(dirpath, part.replace('%20', ' ')))
                    if not os.path.exists(target):
                        errors.append(f'{os.path.relpath(src, root)}: '
                                      f'missing file -> {link}')
                        continue
                    if not target.endswith('.md'):
                        continue
                if frag and not anchor_ok(frag, anchors_of(target, cache)):
                    errors.append(f'{os.path.relpath(src, root)}: '
                                  f'missing anchor -> {link}')
    for e in errors:
        print(e)
    print(f'{len(errors)} broken link(s)' if errors else 'all links OK')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
