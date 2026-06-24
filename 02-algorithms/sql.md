---
module: 02-algorithms
topic: Sql
subtopic: 
status: awareness-only
tags: [algorithms, sql]
---

← [Algorithms index](./README.md) · [Algorithm decision tree](./algorithm_tree.md)

> [!warning] **Amazon SDE-2 scope: awareness only.**
> SQL does not appear in SDE-2 algorithm coding rounds. Skip detailed study; skim for system design conversations.

## One-Liner Reference

- **JOINs**: INNER (intersection), LEFT/RIGHT (one side all rows), FULL OUTER (union with nulls), CROSS (cartesian).
- **Window functions**: `ROW_NUMBER() / RANK() / DENSE_RANK() OVER (PARTITION BY x ORDER BY y)` — running totals, ranking within group.
- **CTEs**: `WITH cte AS (SELECT ...)` — readable multi-step queries; recursive CTEs for hierarchies.
- **Aggregation**: `GROUP BY` + `HAVING` (filter after aggregation vs `WHERE` before).
- **Indexes**: B-tree default; composite index leftmost-prefix rule; covering index avoids table scan.
- **EXPLAIN**: check for `Seq Scan` vs `Index Scan`; use to validate query plan.
- **N+1 problem**: symptom of lazy-loading in ORM loops; fix with JOIN or batch fetch.

If SQL appears in a system design discussion: mention indexing strategy, query optimization, read replicas for read-heavy workloads, and connection pooling.
