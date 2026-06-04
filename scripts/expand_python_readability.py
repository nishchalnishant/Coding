#!/usr/bin/env python3
"""Expand dense Python in coding/ blocks: split semicolons, unwrap any/all."""

from __future__ import annotations

import re
from pathlib import Path

CODING = Path(__file__).resolve().parents[1] / "coding"

DIRECTIONS = "((0, 1), (0, -1), (1, 0), (-1, 0))"


def split_semicolon_line(line: str) -> list[str]:
    if not line.startswith("> "):
        return [line]
    code = line[2:].rstrip("\n")
    if ";" not in code:
        return [line]
    stripped = code.lstrip()
    if stripped.startswith("#"):
        return [line]

    indent = code[: len(code) - len(stripped)]
    parts: list[str] = []
    current = ""
    in_str: str | None = None
    for ch in stripped:
        if in_str:
            current += ch
            if ch == in_str:
                in_str = None
        elif ch in "\"'":
            in_str = ch
            current += ch
        elif ch == ";":
            if current.strip():
                parts.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current.strip())

    if len(parts) <= 1:
        return [line]
    return [f"> {indent}{part}\n" for part in parts]


def expand_any_all_line(line: str) -> list[str]:
    """Expand any/all one-liners into explicit loops."""
    if not line.startswith("> "):
        return [line]
    code = line[2:].rstrip("\n")
    stripped = code.lstrip()
    indent = code[: len(code) - len(stripped)]

    # found = any(dfs(...) for dr, dc in directions)
    m = re.match(
        r"(\w+) = any\((.+?) for dr, dc in (\([^)]+\)|\[[^\]]+\]|\(\([^)]+\)(?:,\s*\([^)]+\))*)\)\s*\)",
        stripped,
    )
    if m:
        var, call, dirs = m.group(1), m.group(2).strip(), m.group(3)
        return [
            f"> {indent}{var} = False\n",
            f"> {indent}for dr, dc in {dirs}:\n",
            f"> {indent}    if {call}:\n",
            f"> {indent}        {var} = True\n",
            f"> {indent}        break\n",
        ]

    # return any(... for dr, dc in ...)
    m = re.match(
        r"return any\((.+?) for dr, dc in (\([^)]+\)|\[[^\]]+\]|\(\([^)]+\)(?:,\s*\([^)]+\))*)\)\s*\)",
        stripped,
    )
    if m:
        call, dirs = m.group(1).strip(), m.group(2)
        return [
            f"> {indent}for dr, dc in {dirs}:\n",
            f"> {indent}    if {call}:\n",
            f"> {indent}        return True\n",
            f"> {indent}return False\n",
        ]

    # return any(f(...) for r in range(...) for c in range(...))
    m = re.match(
        r"return any\((.+?) for (\w+) in range\((.+?)\) for (\w+) in range\((.+?)\)\)",
        stripped,
    )
    if m:
        call, v1, r1, v2, r2 = m.groups()
        return [
            f"> {indent}for {v1} in range({r1}):\n",
            f"> {indent}    for {v2} in range({r2}):\n",
            f"> {indent}        if {call.strip()}:\n",
            f"> {indent}            return True\n",
            f"> {indent}return False\n",
        ]

    # return any(dfs(node) for node in range(n) if cond)
    m = re.match(r"return any\((.+?) for (\w+) in range\((.+?)\) if (.+)\)", stripped)
    if m:
        call, v, rng, cond = m.groups()
        return [
            f"> {indent}for {v} in range({rng}):\n",
            f"> {indent}    if {cond}:\n",
            f"> {indent}        if {call.strip()}:\n",
            f"> {indent}            return True\n",
            f"> {indent}return False\n",
        ]

    # return all(expr for x in iterable) — e.g. s[:length] == prefix for s in strs[1:]
    m = re.match(r"return all\((.+?) for (\w+) in (\w+(?:\[[^\]]+\])?)\)", stripped)
    if m:
        expr, v, it = m.groups()
        return [
            f"> {indent}for {v} in {it}:\n",
            f"> {indent}    if not ({expr.strip()}):\n",
            f"> {indent}        return False\n",
            f"> {indent}return True\n",
        ]

    # var = any(matrix[0][j] == 0 for j in range(n))
    m = re.match(r"(\w+) = any\((.+?) for (\w+) in range\((.+?)\)\)", stripped)
    if m:
        var, expr, v, rng = m.groups()
        return [
            f"> {indent}{var} = False\n",
            f"> {indent}for {v} in range({rng}):\n",
            f"> {indent}    if {expr.strip()}:\n",
            f"> {indent}        {var} = True\n",
            f"> {indent}        break\n",
        ]

    # return any(self._dfs(...) for child in node.children.values())
    m = re.match(r"return any\((.+?) for (\w+) in (.+)\)", stripped)
    if m:
        call, v, it = m.groups()
        if " for " in it:  # skip nested fors handled above
            return [line]
        return [
            f"> {indent}for {v} in {it}:\n",
            f"> {indent}    if {call.strip()}:\n",
            f"> {indent}        return True\n",
            f"> {indent}return False\n",
        ]

    # has_negative_cycle = any(cond for u, v, w in edges)
    m = re.match(r"(\w+) = any\((.+?) for (\w+, \w+, \w+) in (\w+)\)", stripped)
    if m:
        var, cond, loop_vars, it = m.groups()
        return [
            f"> {indent}{var} = False\n",
            f"> {indent}for {loop_vars} in {it}:\n",
            f"> {indent}    if {cond.strip()}:\n",
            f"> {indent}        {var} = True\n",
            f"> {indent}        break\n",
        ]

    # tmp, board[r][c] = board[r][c], '#'
    m = re.match(r"(\w+), (\w+\[[^\]]+\]) = \2, (.+)", stripped)
    if m:
        tmp, cell, mark = m.group(1), m.group(2), m.group(3)
        return [
            f"> {indent}{tmp} = {cell}\n",
            f"> {indent}{cell} = {mark}\n",
        ]

    return [line]


def merge_multiline_any(block: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Collapse multiline any(...) into one logical line, then expand."""
    out: list[tuple[int, str]] = []
    i = 0
    while i < len(block):
        _, line = block[i]
        stripped = line[2:].strip() if line.startswith("> ") else line.strip()
        if re.search(r"\bany\(", stripped) and not stripped.rstrip().endswith(")"):
            merged = stripped
            j = i + 1
            while j < len(block) and ")" not in merged:
                nxt = block[j][1]
                part = nxt[2:].strip() if nxt.startswith("> ") else nxt.strip()
                merged += " " + part
                j += 1
            indent = line[2:][: len(line[2:]) - len(line[2:].lstrip())] if line.startswith("> ") else ""
            expanded = expand_any_all_line(f"> {indent}{merged}\n")
            if len(expanded) > 1 or expanded[0] != f"> {indent}{merged}\n":
                out.extend((block[i][0], ln) for ln in expanded)
                i = j
                continue
        out.append(block[i])
        i += 1
    return out


def process_block(block: list[tuple[int, str]]) -> list[str]:
    block = merge_multiline_any(block)
    result: list[str] = []
    for _, line in block:
        expanded = expand_any_all_line(line)
        for el in expanded:
            result.extend(split_semicolon_line(el))
    return result


def process_file(path: Path) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []
    i = 0
    changed = False

    while i < len(lines):
        line = lines[i]
        if line.startswith("> ```python"):
            out.append(line)
            i += 1
            block: list[tuple[int, str]] = []
            while i < len(lines) and not lines[i].startswith("> ```"):
                block.append((i, lines[i]))
                i += 1
            new_block = process_block(block)
            if new_block != [l for _, l in block]:
                changed = True
            out.extend(new_block)
            if i < len(lines):
                out.append(lines[i])
                i += 1
            continue
        out.append(line)
        i += 1

    if changed:
        path.write_text("".join(out), encoding="utf-8")
    return changed


def main() -> None:
    n = 0
    for path in sorted(CODING.rglob("*.md")):
        if process_file(path):
            n += 1
            print(f"updated {path.relative_to(CODING.parents[0])}")
    print(f"Done — {n} files updated")


if __name__ == "__main__":
    main()
