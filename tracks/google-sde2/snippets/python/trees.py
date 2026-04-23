from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def inorder(root: Optional[TreeNode]) -> List[int]:
    out: List[int] = []
    stack: List[TreeNode] = []
    cur = root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        out.append(cur.val)
        cur = cur.right
    return out


def validate_bst(root: Optional[TreeNode]) -> bool:
    def dfs(node: Optional[TreeNode], lo: int, hi: int) -> bool:
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return dfs(node.left, lo, node.val) and dfs(node.right, node.val, hi)

    return dfs(root, -10**30, 10**30)


def lca_binary_tree(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    if not root or root == p or root == q:
        return root
    left = lca_binary_tree(root.left, p, q)
    right = lca_binary_tree(root.right, p, q)
    if left and right:
        return root
    return left or right


def max_path_sum(root: Optional[TreeNode]) -> int:
    best = float("-inf")

    def dfs(node: Optional[TreeNode]) -> int:
        nonlocal best
        if not node:
            return 0
        left = max(0, dfs(node.left))
        right = max(0, dfs(node.right))
        best = max(best, node.val + left + right)
        return node.val + max(left, right)

    dfs(root)
    return int(best)


def serialize_preorder(root: Optional[TreeNode]) -> str:
    out: List[str] = []

    def dfs(node: Optional[TreeNode]) -> None:
        if not node:
            out.append("#")
            return
        out.append(str(node.val))
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return ",".join(out)


def deserialize_preorder(data: str) -> Optional[TreeNode]:
    tokens = data.split(",")
    i = 0

    def build() -> Optional[TreeNode]:
        nonlocal i
        if tokens[i] == "#":
            i += 1
            return None
        node = TreeNode(int(tokens[i]))
        i += 1
        node.left = build()
        node.right = build()
        return node

    return build()

