---
module: 02-algorithms
topic: Sql
subtopic: 
status: unread
tags: [algorithms, sql]
---

← [Algorithms index](./README.md) · [Algorithm decision tree](./algorithm_tree.md)
## First-Principles Map

```text
WHY SQL exists
├── Structured data lives in relations (tables) — need declarative retrieval
│   ├── Ad-hoc filtering over millions of rows without writing loops
│   └── Multi-table joins replace manual cross-referencing
WHAT it is
├── A declarative set-based language evaluated by a query planner
│   ├── Logical order: FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
│   └── Physical order decided by optimizer (indexes, hash joins, sort-merge joins)
HOW it works
├── Aggregation pipeline
│   ├── GROUP BY partitions rows; aggregate functions (COUNT, SUM, AVG, MAX, MIN) collapse each partition
│   └── HAVING filters after aggregation; WHERE filters before
├── Window functions
│   ├── OVER (PARTITION BY col ORDER BY col) — retains row granularity while computing group stats
│   ├── ROW_NUMBER / RANK / DENSE_RANK — deduplicate, top-N per group
│   └── LAG / LEAD / SUM OVER frame — running totals, delta between adjacent rows
├── Joins
│   ├── INNER — intersection; rows must match in both tables
│   ├── LEFT/RIGHT OUTER — preserve all rows from one side, NULL-fill the other
│   └── SELF JOIN / cross apply — hierarchies, consecutive-row comparisons
├── CTEs (WITH clause)
│   ├── Break multi-step logic into named subqueries — no performance penalty vs inline subquery
│   └── Recursive CTEs — traverse trees/graphs (org charts, BOM)
WHEN to use
├── "top N per group" → ROW_NUMBER() + OVER(PARTITION BY) + WHERE rn = 1
├── "running total / moving average" → SUM/AVG OVER (ORDER BY ... ROWS BETWEEN ...)
├── "find duplicates" → COUNT(*) > 1 GROUP BY key columns
├── "consecutive rows / gaps" → LAG/LEAD or self-join on row_number delta
└── "hierarchy / recursive path" → recursive CTE WITH RECURSIVE
WHAT can go wrong
├── NULL propagation — NULL in JOIN key silently drops rows; NULL in aggregate is ignored
├── HAVING vs WHERE confusion — filtering aggregated result needs HAVING, not WHERE
└── Window function in WHERE — illegal; must wrap in subquery or CTE
DECISION
└── Need per-row context + group stat simultaneously → window function (not GROUP BY, which collapses rows)
```

## First-Principles Breakdown

- **Root problem**: Relational data requires multi-table, multi-condition retrieval without imperative loops.
- **Core insight**: SQL is evaluated as set operations; the optimizer chooses physical execution — write for correctness, let the planner choose the join strategy.
- **Invariant**: Logical evaluation order (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY) is fixed; aliases defined in SELECT are invisible to WHERE/HAVING.
- **Why it works**: Window functions compute aggregates over a partition while preserving row identity, enabling top-N, running totals, and delta patterns in a single pass.
- **Where it breaks**: NULL semantics, implicit type coercion in joins, and applying filters at the wrong pipeline stage (WHERE vs HAVING) produce silent wrong-answer bugs.

---

# SQL — Interview Quick Reference

```
[SQL — MINDMAP]
├── WHY IT EXISTS
│   ├── Problem it solves: query and transform structured relational data without imperative loops
│   ├── Declarative: you describe WHAT you want, the engine decides HOW to fetch it
│   └── Analogy: SQL is to tables what math notation is to numbers — a universal language for set operations
├── WHAT IT IS (First Principles)
│   ├── Core model: relations (tables) = sets of tuples; SQL = relational algebra + aggregation + ordering
│   ├── Key property: set-based operations — no row order guaranteed unless ORDER BY is explicit
│   ├── NULL semantics: three-valued logic (TRUE / FALSE / UNKNOWN); NULL != NULL
│   └── Execution order: FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
├── HOW IT WORKS
│   ├── Joins
│   │   ├── INNER JOIN: only matching rows from both sides
│   │   ├── LEFT JOIN: all rows from left, NULLs for non-matching right
│   │   ├── FULL OUTER JOIN: all rows from both sides, NULLs where no match
│   │   └── SELF JOIN: join table to itself (e.g., employee → manager hierarchy)
│   ├── Aggregation
│   │   ├── GROUP BY partitions rows; aggregate functions collapse each group
│   │   ├── HAVING filters after aggregation (WHERE cannot reference aggregates)
│   │   └── DISTINCT inside COUNT(DISTINCT col) — common interview pattern
│   ├── Window Functions
│   │   ├── ROW_NUMBER() / RANK() / DENSE_RANK(): ranking within partition
│   │   ├── LAG(col, n) / LEAD(col, n): access previous/next row without self-join
│   │   ├── SUM/AVG OVER (PARTITION BY ... ORDER BY ... ROWS/RANGE ...): running totals
│   │   └── PARTITION BY: like GROUP BY but keeps all rows visible
│   ├── Subqueries & CTEs
│   │   ├── Correlated subquery: references outer query — runs once per outer row (expensive)
│   │   ├── WITH (CTE): named, reusable inline view — improves readability, sometimes performance
│   │   └── EXISTS vs IN: EXISTS short-circuits; prefer EXISTS when subquery result is large
│   ├── Set Operations
│   │   ├── UNION: deduplicated rows from both queries
│   │   ├── UNION ALL: all rows including duplicates (faster)
│   │   └── INTERSECT / EXCEPT: common rows / rows in left not in right
│   └── String / Date Functions
│       ├── LIKE 'prefix%': pattern match; % = any chars, _ = one char
│       ├── DATE_DIFF / DATEDIFF / TIMESTAMPDIFF: date arithmetic
│       └── COALESCE(a, b, c): first non-NULL value
├── COMPLEXITY SUMMARY
│   ├── Full table scan: O(N)
│   ├── Index seek: O(log N)
│   ├── Hash join: O(N + M) average
│   ├── Sort-merge join: O(N log N + M log M)
│   └── Window function: O(N log N) — sort + scan
├── WHEN TO USE
│   ├── Signal: "find top-N per group" → RANK() / ROW_NUMBER() with PARTITION BY
│   ├── Signal: "running total / moving average" → SUM OVER with ORDER BY + frame
│   ├── Signal: "users who did X but not Y" → LEFT JOIN + WHERE right.id IS NULL, or EXCEPT
│   ├── Signal: "consecutive rows / streaks" → LAG/LEAD or self-join with row offset trick
│   ├── Signal: "second highest / Nth rank" → DENSE_RANK or LIMIT + OFFSET
│   └── Avoid correlated subqueries when: table is large — rewrite as JOIN or window function
└── COMMON MISTAKES / GOTCHAS
    ├── Filtering on window function result: must wrap in subquery/CTE — window runs after WHERE
    ├── NULL in aggregates: COUNT(*) counts rows; COUNT(col) skips NULLs — different answers
    ├── GROUP BY column list: every non-aggregate SELECT column must appear in GROUP BY
    ├── HAVING vs WHERE: WHERE before aggregation, HAVING after — mixing them causes wrong results
    ├── RANK() skips numbers after ties; DENSE_RANK() does not — pick the right one
    └── JOIN on nullable columns: NULL = NULL is FALSE in SQL — rows silently disappear
```

Covers the SQL patterns that appear most in data engineering, analytics, and backend SDE interviews at Google, Meta, and similar companies.

---

## Execution Order (mental model — memorize this)

```
FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
```

Write queries in this order mentally; filters before grouping are `WHERE`, filters after are `HAVING`.

**Why this matters in interviews:**
- You cannot use a `SELECT` alias in `WHERE` (alias doesn't exist yet at that stage)
- You CAN use a `SELECT` alias in `ORDER BY` (it's evaluated after)
- `HAVING` can reference aggregate functions; `WHERE` cannot

```sql
-- WRONG: alias used in WHERE
SELECT salary * 1.1 AS adjusted
FROM employees
WHERE adjusted > 50000;   -- error: 'adjusted' unknown

-- RIGHT: wrap in subquery or repeat expression
SELECT salary * 1.1 AS adjusted
FROM employees
WHERE salary * 1.1 > 50000;
```

---

## Core Clauses Cheatsheet

| Clause | Use | Gotcha |
|--------|-----|--------|
| `WHERE` | Filter rows before aggregation | Cannot reference aliases defined in `SELECT` |
| `HAVING` | Filter after `GROUP BY` | Can use aggregate functions; `WHERE` cannot |
| `GROUP BY` | Aggregate per group | Every non-aggregate `SELECT` column must appear here |
| `DISTINCT` | Deduplicate output | Applied after `SELECT`, before `ORDER BY` |
| `ORDER BY` | Sort result | Default `ASC`; use `DESC` explicitly |
| `LIMIT n OFFSET k` | Pagination | `OFFSET` is 0-indexed |

---

## JOINs — Pick the Right One

```
Table A: {1, 2, 3}    Table B: {2, 3, 4}

INNER JOIN  → {2, 3}            (intersection)
LEFT JOIN   → {1, 2, 3}         (all A, NULLs for B misses)
RIGHT JOIN  → {2, 3, 4}         (all B, NULLs for A misses)
FULL JOIN   → {1, 2, 3, 4}      (union, NULLs on both sides)
CROSS JOIN  → all pairs (N×M)   (no ON clause)
SELF JOIN   → join table to itself (use alias)
```

### Anti-pattern detection with LEFT JOIN
```sql
-- Find rows in A with no match in B
SELECT a.*
FROM a LEFT JOIN b ON a.id = b.a_id
WHERE b.a_id IS NULL;

-- Real example: users who never placed an order
SELECT u.user_id, u.name
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.user_id IS NULL;
```

### SELF JOIN — tricky and common
```sql
-- Find employees who earn more than their manager
SELECT e.name AS employee, e.salary, m.name AS manager, m.salary AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;

-- Find all pairs of students in the same class
SELECT a.name, b.name, a.class
FROM students a
JOIN students b ON a.class = b.class AND a.id < b.id;  -- a.id < b.id avoids (A,B) and (B,A) duplicates
```

### Multiple JOIN conditions
```sql
-- Match on two columns (composite key)
SELECT *
FROM orders o
JOIN shipments s ON o.order_id = s.order_id AND o.region = s.region;
```

---

## Aggregates

| Function | Returns | NULL behavior |
|----------|---------|---------------|
| `COUNT(*)` | all rows including NULLs | never NULL |
| `COUNT(col)` | non-NULL values in col | skips NULLs |
| `SUM(col)` | sum of non-NULLs | NULL if all NULL |
| `AVG(col)` | avg of non-NULLs | skips NULLs; ≠ SUM/COUNT(*) |
| `MAX/MIN` | extremes | skips NULLs |

### The AVG trap
```sql
-- These are NOT the same when col has NULLs
SELECT AVG(score) FROM results;            -- skips NULLs
SELECT SUM(score) / COUNT(*) FROM results; -- treats NULLs as 0 effectively

-- To treat NULLs as 0:
SELECT AVG(COALESCE(score, 0)) FROM results;
```

### Conditional aggregation (pivot without PIVOT keyword)
```sql
-- Count of orders by status in one row
SELECT
    COUNT(CASE WHEN status = 'pending'   THEN 1 END) AS pending_count,
    COUNT(CASE WHEN status = 'shipped'   THEN 1 END) AS shipped_count,
    COUNT(CASE WHEN status = 'cancelled' THEN 1 END) AS cancelled_count
FROM orders;

-- Revenue by product category
SELECT
    SUM(CASE WHEN category = 'electronics' THEN revenue ELSE 0 END) AS electronics,
    SUM(CASE WHEN category = 'clothing'    THEN revenue ELSE 0 END) AS clothing
FROM sales;
```

---

## Window Functions (the most-tested SQL topic)

```sql
function() OVER (
    PARTITION BY col      -- optional: like GROUP BY per window
    ORDER BY col          -- required for ranking / running totals
    ROWS BETWEEN ...      -- optional: frame specification
)
```

### Ranking
```sql
ROW_NUMBER()   -- unique sequential (1,2,3,4) — no ties
RANK()         -- gaps on ties (1,2,2,4)
DENSE_RANK()   -- no gaps on ties (1,2,2,3)
NTILE(n)       -- distribute rows into n buckets (for percentiles)
```

**When to use which:**
- `ROW_NUMBER` → deduplicate (want exactly one row per group)
- `DENSE_RANK` → "top N" with ties included
- `RANK` → sports-style ranking where ties cause gaps
- `NTILE(4)` → quartiles; `NTILE(100)` → percentiles

```sql
-- Top 3 salaries per department (ties included → DENSE_RANK)
WITH ranked AS (
    SELECT name, dept, salary,
           DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT * FROM ranked WHERE rnk <= 3;

-- Deduplicate: keep one row per user (latest event → ROW_NUMBER)
WITH deduped AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time DESC) AS rn
    FROM events
)
SELECT * FROM deduped WHERE rn = 1;
```

### Offset functions
```sql
LAG(col, n, default)   -- value n rows before current (default if no row)
LEAD(col, n, default)  -- value n rows after current
FIRST_VALUE(col)       -- first in the window frame
LAST_VALUE(col)        -- last in window frame (watch RANGE default!)
NTH_VALUE(col, n)      -- nth value in frame
```

**LAG/LEAD gotcha** — the `default` argument prevents NULLs at boundaries:
```sql
-- Day-over-day change; LAG returns NULL for first row unless default given
SELECT date, revenue,
       revenue - LAG(revenue, 1, 0) OVER (ORDER BY date) AS daily_change
FROM daily_sales;
```

**LAST_VALUE gotcha** — default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, so `LAST_VALUE` just returns the current row. Fix:
```sql
-- WRONG: returns current row's value, not partition's last
SELECT name, LAST_VALUE(salary) OVER (PARTITION BY dept ORDER BY salary) AS last_sal
FROM employees;

-- RIGHT: extend frame to end of partition
SELECT name,
       LAST_VALUE(salary) OVER (
           PARTITION BY dept ORDER BY salary
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS last_sal
FROM employees;
```

### Aggregate over window (no GROUP BY collapse)
```sql
-- Show each employee's salary alongside dept average
SELECT name, dept, salary,
       AVG(salary) OVER (PARTITION BY dept) AS dept_avg,
       salary - AVG(salary) OVER (PARTITION BY dept) AS diff_from_avg
FROM employees;

-- Running total reset per month
SELECT date, amount,
       SUM(amount) OVER (PARTITION BY DATE_TRUNC('month', date) ORDER BY date) AS monthly_running
FROM transactions;

-- Percent of total (each row / grand total)
SELECT name, revenue,
       ROUND(100.0 * revenue / SUM(revenue) OVER (), 2) AS pct_of_total
FROM products;
```

### Frame specification
```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW   -- cumulative (common default)
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW           -- 3-row rolling average
ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING           -- centered 3-row window
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING  -- entire partition

-- 7-day rolling average
SELECT date, revenue,
       AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_7d
FROM daily_sales;
```

---

## Subqueries vs CTEs

**CTE (WITH clause)** — prefer for readability and reuse:
```sql
WITH
dept_avg AS (
    SELECT dept, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY dept
),
above_avg AS (
    SELECT e.name, e.dept, e.salary, d.avg_sal
    FROM employees e
    JOIN dept_avg d ON e.dept = d.dept
    WHERE e.salary > d.avg_sal
)
SELECT * FROM above_avg ORDER BY dept, salary DESC;
```

**Correlated subquery** — runs once per outer row; expensive but sometimes the only option:
```sql
-- Employees earning above their own department's average
SELECT e.name
FROM employees e
WHERE e.salary > (SELECT AVG(salary) FROM employees WHERE dept = e.dept);

-- Second highest salary per department (correlated)
SELECT DISTINCT dept,
    (SELECT MAX(salary) FROM employees e2
     WHERE e2.dept = e1.dept AND e2.salary < MAX(e1.salary)) AS second_highest
FROM employees e1
GROUP BY dept;
```

**EXISTS vs IN:**
- `EXISTS` stops at first match → faster for large subqueries
- `IN` evaluates all → avoid with NULLs (NULL in list → no rows returned)
- `NOT EXISTS` is safer than `NOT IN` when subquery can return NULLs

```sql
-- Users who have placed at least one order (EXISTS)
SELECT u.user_id, u.name
FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.user_id);

-- The NULL trap with NOT IN
-- If orders has even one NULL user_id, this returns ZERO rows
SELECT * FROM users WHERE user_id NOT IN (SELECT user_id FROM orders);

-- Safe version
SELECT * FROM users WHERE user_id NOT IN (SELECT user_id FROM orders WHERE user_id IS NOT NULL);
-- Or better: use NOT EXISTS
SELECT * FROM users u WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.user_id);
```

---

## NULL Gotchas

```sql
NULL = NULL   → NULL  (not TRUE — use IS NULL / IS NOT NULL)
NULL != 1     → NULL
NOT NULL      → NULL
COUNT(*)      → counts NULLs; COUNT(col) does not

COALESCE(a, b, c)   -- first non-NULL
NULLIF(a, b)        -- returns NULL if a = b (avoids division by zero)
```

**Division by zero:**
```sql
-- Safe division
SELECT revenue / NULLIF(users, 0) AS revenue_per_user FROM metrics;
-- NULLIF returns NULL when users=0, making the result NULL instead of error

-- With fallback
SELECT COALESCE(revenue / NULLIF(users, 0), 0) AS revenue_per_user FROM metrics;
```

**Sorting with NULLs:**
```sql
-- NULLs sort first in ASC (PostgreSQL/MySQL default), last in DESC
-- Force NULLs last in ASC:
ORDER BY CASE WHEN col IS NULL THEN 1 ELSE 0 END, col ASC

-- PostgreSQL: NULLS LAST / NULLS FIRST
ORDER BY col ASC NULLS LAST
```

---

## Canonical Interview Patterns

### Nth highest value
```sql
-- Method 1: OFFSET (simple but slow on large tables)
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET N-1;

-- Method 2: DENSE_RANK (handles ties correctly — interview preferred)
WITH ranked AS (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT MIN(salary) FROM ranked WHERE rnk = N;

-- Method 3: correlated subquery (classic, no window functions)
SELECT MAX(salary)
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);  -- for 2nd highest
```

### Running total
```sql
SELECT date, amount,
       SUM(amount) OVER (ORDER BY date) AS cumulative,
       SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS same_thing
FROM transactions;
```

### Month-over-month growth
```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date) AS month,
           SUM(revenue) AS revenue
    FROM orders
    GROUP BY 1
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
          / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2) AS pct_change
FROM monthly;
```

### Deduplicate — keep latest per group
```sql
-- Method 1: ROW_NUMBER (most flexible)
WITH deduped AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
    FROM events
)
SELECT * FROM deduped WHERE rn = 1;

-- Method 2: self-join on max (classic)
SELECT e.*
FROM events e
JOIN (
    SELECT user_id, MAX(created_at) AS latest
    FROM events GROUP BY user_id
) m ON e.user_id = m.user_id AND e.created_at = m.latest;
```

### Find gaps in sequential IDs
```sql
-- Method 1: NOT IN
SELECT id + 1 AS gap_start
FROM t
WHERE id + 1 NOT IN (SELECT id FROM t)
  AND id + 1 <= (SELECT MAX(id) FROM t);

-- Method 2: LAG (more efficient)
SELECT prev_id + 1 AS gap_start, curr_id - 1 AS gap_end
FROM (
    SELECT id AS curr_id, LAG(id) OVER (ORDER BY id) AS prev_id
    FROM t
) sub
WHERE curr_id - prev_id > 1;
```

### Pivot (conditional aggregation)
```sql
-- Monthly revenue by product — rows to columns
SELECT
    user_id,
    SUM(CASE WHEN product = 'A' THEN revenue END) AS product_A,
    SUM(CASE WHEN product = 'B' THEN revenue END) AS product_B,
    SUM(CASE WHEN product = 'C' THEN revenue END) AS product_C
FROM sales
GROUP BY user_id;
```

### Consecutive login days (streak)
```sql
-- The classic "date - row_number" trick: consecutive dates form the same group
WITH dated AS (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM (SELECT DISTINCT user_id, DATE(login_time) AS login_date FROM logins) d
),
grouped AS (
    SELECT user_id, login_date,
           login_date - INTERVAL (rn - 1) DAY AS grp
    FROM dated
)
SELECT user_id, MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end,
       COUNT(*) AS streak_length
FROM grouped
GROUP BY user_id, grp
ORDER BY streak_length DESC;
```

### Retention / cohort analysis
```sql
-- Day-1 retention: users who came back the day after signup
WITH first_visit AS (
    SELECT user_id, MIN(DATE(event_time)) AS signup_date
    FROM events
    GROUP BY user_id
)
SELECT
    f.signup_date,
    COUNT(DISTINCT f.user_id) AS cohort_size,
    COUNT(DISTINCT e.user_id) AS retained_day1,
    ROUND(100.0 * COUNT(DISTINCT e.user_id) / COUNT(DISTINCT f.user_id), 2) AS retention_rate
FROM first_visit f
LEFT JOIN events e
    ON f.user_id = e.user_id
    AND DATE(e.event_time) = f.signup_date + INTERVAL 1 DAY
GROUP BY f.signup_date
ORDER BY f.signup_date;
```

### Rolling active users (DAU / 7-day MAU)
```sql
-- 7-day rolling unique users per day
SELECT
    d.date,
    COUNT(DISTINCT e.user_id) AS rolling_7d_users
FROM (SELECT DISTINCT DATE(event_time) AS date FROM events) d
JOIN events e
    ON DATE(e.event_time) BETWEEN d.date - INTERVAL 6 DAY AND d.date
GROUP BY d.date
ORDER BY d.date;
```

### Median
```sql
-- Method 1: PERCENTILE_CONT (standard SQL)
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary
FROM employees;

-- Method 2: row_number trick (works everywhere)
WITH ordered AS (
    SELECT salary,
           ROW_NUMBER() OVER (ORDER BY salary) AS rn,
           COUNT(*) OVER () AS total
    FROM employees
)
SELECT AVG(salary) AS median
FROM ordered
WHERE rn IN (FLOOR((total + 1) / 2.0), CEIL((total + 1) / 2.0));
```

### Employees with salary above company average AND above department average
```sql
WITH averages AS (
    SELECT
        dept,
        AVG(salary) OVER () AS company_avg,
        AVG(salary) OVER (PARTITION BY dept) AS dept_avg
    FROM employees
)
SELECT DISTINCT e.name, e.dept, e.salary
FROM employees e
JOIN averages a ON e.dept = a.dept
WHERE e.salary > a.company_avg AND e.salary > a.dept_avg;
```

### Find the most recent record before a given event
```sql
-- Most recent login before each purchase
SELECT
    p.purchase_id,
    p.user_id,
    p.purchase_time,
    MAX(l.login_time) AS last_login_before_purchase
FROM purchases p
LEFT JOIN logins l
    ON l.user_id = p.user_id
    AND l.login_time < p.purchase_time
GROUP BY p.purchase_id, p.user_id, p.purchase_time;
```

### Running total that resets (e.g. monthly)
```sql
SELECT
    date,
    amount,
    SUM(amount) OVER (
        PARTITION BY DATE_FORMAT(date, '%Y-%m')
        ORDER BY date
    ) AS monthly_cumulative
FROM transactions;
```

---

## Tricky Interview Questions & Tricks

### 1. Delete duplicates, keep one
```sql
-- Keep the row with the lowest id for each email
DELETE FROM users
WHERE id NOT IN (
    SELECT MIN(id)
    FROM users
    GROUP BY email
);

-- Safer (some DBs don't allow subquery on same table in DELETE):
WITH to_keep AS (SELECT MIN(id) AS id FROM users GROUP BY email)
DELETE FROM users WHERE id NOT IN (SELECT id FROM to_keep);
```

### 2. Update from another table
```sql
-- Update salary in employees based on a raises table
UPDATE employees e
SET salary = salary * (1 + r.pct / 100.0)
FROM raises r
WHERE e.dept = r.dept;

-- MySQL syntax (different):
UPDATE employees e
JOIN raises r ON e.dept = r.dept
SET e.salary = e.salary * (1 + r.pct / 100.0);
```

### 3. Rank within group without window functions (classic correlated subquery)
```sql
-- Rank salary within dept (SDE-2 era trick, still asked)
SELECT
    e1.name, e1.dept, e1.salary,
    COUNT(e2.salary) + 1 AS rank_in_dept
FROM employees e1
LEFT JOIN employees e2
    ON e1.dept = e2.dept AND e2.salary > e1.salary
GROUP BY e1.name, e1.dept, e1.salary
ORDER BY e1.dept, rank_in_dept;
```

### 4. "At least N" vs "exactly N" pattern
```sql
-- Customers who ordered at least 3 times
SELECT customer_id, COUNT(*) AS orders
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 3;

-- Customers who ordered exactly 3 distinct products
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING COUNT(DISTINCT product_id) = 3;
```

### 5. Matching across two conditions in the same table (tricky)
```sql
-- Users who have BOTH a 'click' AND a 'purchase' event
SELECT user_id
FROM events
WHERE event_type IN ('click', 'purchase')
GROUP BY user_id
HAVING COUNT(DISTINCT event_type) = 2;

-- Alternative with EXISTS
SELECT DISTINCT user_id
FROM events e1
WHERE event_type = 'click'
  AND EXISTS (SELECT 1 FROM events e2
              WHERE e2.user_id = e1.user_id AND e2.event_type = 'purchase');
```

### 6. First event of each type per user
```sql
WITH first_events AS (
    SELECT user_id, event_type, event_time,
           ROW_NUMBER() OVER (PARTITION BY user_id, event_type ORDER BY event_time) AS rn
    FROM events
)
SELECT user_id, event_type, event_time
FROM first_events
WHERE rn = 1;
```

### 7. Difference between consecutive rows (stock prices, readings)
```sql
SELECT
    date,
    price,
    price - LAG(price) OVER (ORDER BY date) AS daily_change,
    ROUND(100.0 * (price - LAG(price) OVER (ORDER BY date))
          / NULLIF(LAG(price) OVER (ORDER BY date), 0), 2) AS pct_change
FROM stock_prices;
```

### 8. Longest continuous sequence where condition holds
```sql
-- Longest run of consecutive days with positive revenue
WITH flagged AS (
    SELECT date, revenue,
           CASE WHEN revenue > 0 THEN 1 ELSE 0 END AS positive,
           ROW_NUMBER() OVER (ORDER BY date) AS rn
    FROM daily_revenue
),
grouped AS (
    SELECT date, positive,
           rn - ROW_NUMBER() OVER (PARTITION BY positive ORDER BY date) AS grp
    FROM flagged
)
SELECT MAX(cnt) AS longest_positive_streak
FROM (
    SELECT COUNT(*) AS cnt
    FROM grouped
    WHERE positive = 1
    GROUP BY grp
) streaks;
```

### 9. Cross join for generating date ranges
```sql
-- Generate all dates in a range (useful for filling gaps)
WITH RECURSIVE date_series AS (
    SELECT '2024-01-01'::date AS d
    UNION ALL
    SELECT d + INTERVAL 1 DAY FROM date_series WHERE d < '2024-12-31'
)
-- Left join against this to fill missing dates with 0
SELECT ds.d AS date, COALESCE(SUM(o.revenue), 0) AS revenue
FROM date_series ds
LEFT JOIN orders o ON DATE(o.created_at) = ds.d
GROUP BY ds.d
ORDER BY ds.d;
```

### 10. The "Trips and Users" / cancellation rate pattern
```sql
-- Cancellation rate for unbanned users per day
SELECT
    t.request_at AS day,
    ROUND(
        SUM(CASE WHEN t.status LIKE 'cancelled%' THEN 1.0 ELSE 0 END)
        / COUNT(*),
        2
    ) AS cancellation_rate
FROM trips t
JOIN users u_client ON t.client_id = u_client.users_id AND u_client.banned = 'No'
JOIN users u_driver ON t.driver_id = u_driver.users_id AND u_driver.banned = 'No'
WHERE t.request_at BETWEEN '2013-10-01' AND '2013-10-03'
GROUP BY t.request_at;
```

---

## String Functions (common in interviews)

```sql
UPPER(s), LOWER(s)            -- case conversion
LENGTH(s), CHAR_LENGTH(s)     -- byte length vs char length
SUBSTRING(s, start, len)      -- 1-indexed: SUBSTRING('hello', 2, 3) → 'ell'
LEFT(s, n), RIGHT(s, n)       -- first/last n chars
TRIM(s), LTRIM(s), RTRIM(s)   -- remove whitespace
REPLACE(s, old, new)          -- replace all occurrences
CONCAT(a, b, c)               -- concatenate (NULL-safe: use CONCAT_WS)
CONCAT_WS(',', a, b, c)       -- join with separator, skips NULLs
LIKE '%pattern%'              -- wildcard match (slow, full scan)
REGEXP / RLIKE                -- regex match
POSITION('x' IN s)            -- find position of substring
SPLIT_PART(s, delim, n)       -- PostgreSQL: split and take nth part
```

```sql
-- Extract domain from email
SELECT SUBSTRING(email, POSITION('@' IN email) + 1) AS domain FROM users;

-- Pad with leading zeros
SELECT LPAD(CAST(id AS VARCHAR), 6, '0') AS padded_id FROM orders;

-- Group by first letter of name
SELECT LEFT(name, 1) AS initial, COUNT(*) FROM users GROUP BY 1 ORDER BY 1;
```

---

## Date Functions (frequently tested)

```sql
-- Current date/time
NOW(), CURRENT_TIMESTAMP       -- timestamp with time
CURRENT_DATE, CURDATE()        -- date only

-- Extracting parts
YEAR(d), MONTH(d), DAY(d)
DATE_PART('year', d)           -- PostgreSQL
EXTRACT(YEAR FROM d)           -- standard SQL

-- Truncating
DATE_TRUNC('month', d)         -- PostgreSQL: truncate to start of month
DATE_FORMAT(d, '%Y-%m')        -- MySQL: format as string

-- Arithmetic
d + INTERVAL 7 DAY             -- add days
DATEDIFF(d1, d2)               -- d1 - d2 in days (MySQL)
d1 - d2                        -- PostgreSQL: returns interval
DATE_ADD(d, INTERVAL 1 MONTH)  -- MySQL

-- Day of week
DAYOFWEEK(d)  -- 1=Sunday in MySQL
EXTRACT(DOW FROM d)  -- 0=Sunday in PostgreSQL
```

```sql
-- Users who signed up in the last 30 days
SELECT * FROM users WHERE created_at >= CURRENT_DATE - INTERVAL 30 DAY;

-- Transactions in the same month as today
SELECT * FROM transactions
WHERE YEAR(created_at) = YEAR(CURRENT_DATE)
  AND MONTH(created_at) = MONTH(CURRENT_DATE);

-- Age calculation
SELECT name, TIMESTAMPDIFF(YEAR, dob, CURRENT_DATE) AS age FROM users;
```

---

## Performance Signals (mention in interviews)

| Situation | What to say |
|-----------|-------------|
| Filter early | Push `WHERE` before `JOIN`; use indexed columns in `ON` |
| Avoid `SELECT *` | Name columns; reduces I/O |
| `IN` vs `EXISTS` | `EXISTS` for large subqueries; short-circuits |
| Correlated subquery | O(N) executions → rewrite as `JOIN` or CTE if possible |
| Window vs GROUP BY | Window keeps all rows; GROUP BY collapses — choose by output need |
| Index use | `WHERE`, `JOIN ON`, `ORDER BY` benefit from indexes; functions on columns defeat them |
| `LIKE '%pattern'` | Leading wildcard defeats index → full table scan; `LIKE 'pattern%'` can use index |
| `DISTINCT` vs `GROUP BY` | `GROUP BY` allows aggregation; `DISTINCT` is simpler for dedup only |
| Partition pruning | Filter on partition column in `WHERE` — avoids scanning all partitions |

---

## Common Mistakes to Avoid

| Mistake | Why wrong | Fix |
|---------|-----------|-----|
| `WHERE salary = NULL` | `= NULL` always returns NULL | `WHERE salary IS NULL` |
| `NOT IN (subquery with NULLs)` | Returns zero rows | Use `NOT EXISTS` or filter NULLs in subquery |
| Using alias in `WHERE` | Alias not yet defined | Repeat expression or use subquery/CTE |
| `AVG` treating NULLs as 0 | `AVG` skips NULLs; `SUM/COUNT(*)` doesn't | Use `COALESCE` explicitly |
| Off-by-one in `OFFSET` | `OFFSET 0` = first row | `OFFSET N-1` for Nth row |
| `LAST_VALUE` with default frame | Returns current row | Explicit `ROWS BETWEEN ... UNBOUNDED FOLLOWING` |
| `RANK()` gaps vs `DENSE_RANK()` | Wrong for "top N" with ties | Know which semantics the problem wants |
| Joining on nullable FK | Rows with NULL never match | Use `COALESCE` or handle NULL explicitly |

---

## Quick Drill — Pattern → Query Template

| Pattern keyword | Template |
|-----------------|----------|
| "top N per group" | `RANK() / ROW_NUMBER() OVER (PARTITION BY … ORDER BY …)` + `WHERE rnk <= N` |
| "running / cumulative" | `SUM() OVER (ORDER BY …)` |
| "year-over-year / MoM" | `LAG()` + arithmetic |
| "deduplicate / latest" | `ROW_NUMBER() OVER (PARTITION BY … ORDER BY …)` + `WHERE rn = 1` |
| "no match / missing" | `LEFT JOIN … WHERE b.key IS NULL` or `NOT EXISTS` |
| "count distinct per group" | `COUNT(DISTINCT col)` inside `GROUP BY` |
| "percent of total" | `SUM(col) * 1.0 / SUM(SUM(col)) OVER ()` |
| "conditional count" | `SUM(CASE WHEN … THEN 1 ELSE 0 END)` |
| "median" | `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY col)` |
| "consecutive / streak" | `date - ROW_NUMBER()` grouping trick |
| "first event per user" | `ROW_NUMBER() OVER (PARTITION BY user ORDER BY time) = 1` |
| "compare to previous row" | `LAG(col) OVER (ORDER BY …)` |
| "fill date gaps" | `RECURSIVE CTE` date series + `LEFT JOIN` |
| "both condition A and B" | `GROUP BY … HAVING COUNT(DISTINCT type) = 2` |
| "rank without window functions" | `COUNT(*) + 1` correlated self-join |
| "pivot rows to columns" | `SUM(CASE WHEN cat = 'X' THEN val END) AS X` |
| "retention / cohort" | `MIN(date)` per user → `LEFT JOIN` on `date + interval N` |
| "rolling window (7d MAU)" | `JOIN` on date range or `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` |
