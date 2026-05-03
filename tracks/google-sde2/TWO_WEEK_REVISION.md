# Google SDE-2 (L4) — Two-Week Revision Plan

Use this **14-day** schedule when your interview is **~2 weeks away**. It compresses the broader plan in [ROADMAP.md](ROADMAP.md) and points to **internal notes** in this repo so you revise from one place.

**Your loop (as shared by the team):** **two DSA rounds** — one **virtual on Google EET** (video), one **in person** — plus **one AI / ML–focused interview**. This file is tuned to that shape: DSA prep stays primary; **system design** is optional unless you learn it is still on the loop; **AI-ML** gets a dedicated revision block (this repo has no separate AI-ML `.md` — that section lists topics and external references below).

---

## How the three rounds differ (prep angle)

| Round | Format | What to train |
|--------|--------|----------------|
| **DSA #1 — virtual (recruiter: “Google EET”)** | Camera + audio, shared doc or IDE in browser | Same DSA skills as below, plus **remote hygiene**: stable link, second monitor, quiet room, test **mic/camera/screen share** once, **think out loud** clearly. **Clarify** whether **EET** is the **time zone (Europe / Eastern European Time)** or a **specific meeting product / internal name**; either way, rehearse the **link and tooling** they send. |
| **DSA #2 — In person** | Whiteboard and/or laptop per site norms | Same patterns; practice **writing code legibly** or **typing** as you’ll do on the day. If you travel, plan rest and **arrive with buffer**. |
| **AI / ML** | Often: ML fundamentals, past projects, tradeoffs, sometimes a small modeling or data problem — *confirm with recruiter* | See **AI / ML revision checklist** below; do at least one **60–90 min** “talk through resume ML + one open-ended design” session. |

---

## Targets for 2 weeks (realistic, 3-round loop)

| Area | Target |
|------|--------|
| **DSA (both rounds)** | ~30–40 **high-quality** problems (Medium-heavy; Easy for speed; a few Hard if strong). Same bar for virtual and on-site — only the **medium** changes (doc vs keyboard). |
| **DSA mocks** | **4–6** sessions of **45–60 min** (1–2 problems). Make **≥2** of them **video** (share screen, no extra paper) to mimic **EET**; make **≥1** “on-site style” (single screen, or paper) to mimic **in person**. |
| **AI / ML** | **6–10** hours of focused revision + **2–3** deep-dive sessions (see checklist); **1** full mock / discussion. |
| **System design (general software)** | **Optional** unless your recruiter confirmed a separate SD round. If not in the loop, skip or cap at **0–2** light reads of [SYSTEM_DESIGN_L4.md](SYSTEM_DESIGN_L4.md) — which now includes 3 worked walkthroughs (URL shortener, rate limiter, news feed). |
| **AI / ML** | [AIML_PREP.md](AIML_PREP.md) — core ML, metrics, data issues, ML system design, STAR story templates. |
| **Behavioral / Googliness** | Still often embedded in every round — **6–8** STAR stories, said out loud; [BEHAVIORAL_GOOGLINESS.md](BEHAVIORAL_GOOGLINESS.md). |
| **Polish** | One **mistake log** ([PRACTICE_TRACKER.md](PRACTICE_TRACKER.md)); redo failures cold in week 2. |

---

## Master revision checklist (touch these topics)

### Must be fluent (highest interview frequency)

| Topic | What to nail | Internal notes | Practice in repo |
|-------|----------------|----------------|------------------|
| Arrays, prefix sums, hashing | Two pointers, prefix + map, frequency | [../foundations/data-structures/array.md](../foundations/data-structures/array.md), [../foundations/data-structures/hashing.md](../foundations/data-structures/hashing.md) | [PROBLEM_SET.md](PROBLEM_SET.md) — arrays |
| Two pointers + sliding window | Variable/fixed window, invariants | [../../reference/patterns/patterns-master.md](../../reference/patterns/patterns-master.md) | [PROBLEM_SET.md](PROBLEM_SET.md) — two pointers, sliding window |
| Strings | Windows, anagrams, often same as array patterns | [../foundations/algorithms/string.md](../foundations/algorithms/string.md) | [PROBLEM_SET.md](PROBLEM_SET.md) |
| Trees & BST | Traversals, LCA, validate BST, tree DP | [../foundations/data-structures/tree.md](../foundations/data-structures/tree.md) | [PROBLEM_SET.md](PROBLEM_SET.md) — trees |
| Graphs | BFS/DFS, grid problems, topo, when to use BFS vs DFS | [../foundations/data-structures/graphs.md](../foundations/data-structures/graphs.md), [../foundations/algorithms/graph.md](../foundations/algorithms/graph.md) | [PROBLEM_SET.md](PROBLEM_SET.md) — graphs |
| Binary search | Bounds, rotated array, binary search on answer | [../foundations/algorithms/searching.md](../foundations/algorithms/searching.md) | [PROBLEM_SET.md](PROBLEM_SET.md) — binary search |
| Heaps / priority queue | Top-K, merge K lists, scheduling | [../foundations/data-structures/heap.md](../foundations/data-structures/heap.md) | [PROBLEM_SET.md](PROBLEM_SET.md) — heaps |
| Stack / queue | Monotonic stack, deque for sliding max | [../foundations/data-structures/stack.md](../foundations/data-structures/stack.md), [../foundations/data-structures/queue.md](../foundations/data-structures/queue.md) | [PROBLEM_SET.md](PROBLEM_SET.md) — stack/queue |
| Linked lists | Dummy node, fast/slow, reverse, merge | [../foundations/data-structures/linked-list.md](../foundations/data-structures/linked-list.md) | [PROBLEM_SET.md](PROBLEM_SET.md) — linked list |

### Core SDE-2 “second line” (must recognize + implement common forms)

| Topic | Internal notes | Practice |
|-------|----------------|----------|
| **DP** (1D/2D, LIS/LCS, knapsack/coin) | [../foundations/algorithms/dynamic-programming/README.md](../foundations/algorithms/dynamic-programming/README.md), [../../reference/patterns/patterns-master.md](../../reference/patterns/patterns-master.md) | [PROBLEM_SET.md](PROBLEM_SET.md) — DP |
| **Backtracking** | [../foundations/algorithms/backtracking.md](../foundations/algorithms/backtracking.md) | [PROBLEM_SET.md](PROBLEM_SET.md) — backtracking |
| **Union-Find** (connectivity) | [../foundations/algorithms/union-find.md](../foundations/algorithms/union-find.md) | [COVERAGE_MAP.md](COVERAGE_MAP.md) |
| **Greedy** (intervals, scheduling) | [../foundations/algorithms/greedy.md](../foundations/algorithms/greedy.md) | [PROBLEM_SET.md](PROBLEM_SET.md) |
| **Bit manipulation** | [../foundations/algorithms/bit-manipulation.md](../foundations/algorithms/bit-manipulation.md) | Optional: See `../foundations/` for bit logic. |

### Interview process (non-optional polish)

| Area | File |
|------|------|
| **Coding round flow (7 steps, edge cases, debugging)** | [CODING_ROUNDS.md](CODING_ROUNDS.md) |
| **One-page pattern recall** | [../../reference/quick-sheets/quick-recall.md](../../reference/quick-sheets/quick-recall.md) |
| **Full foundations revision (Parts A–D)** | [../../reference/quick-sheets/revision-guide.md](../../reference/quick-sheets/revision-guide.md) |
| **Topic ↔ canonical problems index** | [../../reference/problem-bank/canonical-questions.md](../../reference/problem-bank/canonical-questions.md) |
| **Copy/paste templates (coding + mock)** | [TEMPLATES.md](TEMPLATES.md) |
| **Language snippets (BFS, DFS, topo, DSU, …)** | [LANGUAGE_TEMPLATES.md](LANGUAGE_TEMPLATES.md), [snippets/python/README.md](snippets/python/README.md) |
| **Quick pseudocode for named problems** | [PROBLEM_DETAILS.md](PROBLEM_DETAILS.md) |
| **Tricks + question bank** | [QUESTION_BANK.md](QUESTION_BANK.md), [SNIPPETS.md](SNIPPETS.md) |
| **System design (L4)** | [SYSTEM_DESIGN_L4.md](SYSTEM_DESIGN_L4.md) — *use if SD is on your loop* |
| **Behavioral / Googliness** | [BEHAVIORAL_GOOGLINESS.md](BEHAVIORAL_GOOGLINESS.md) |
| **Coverage sanity check** | [COVERAGE_MAP.md](COVERAGE_MAP.md) |

---

## AI / ML interview — what to touch

Full prep guide: **[AIML_PREP.md](AIML_PREP.md)** — covers core ML, evaluation metrics, data issues, ML system design, and STAR story templates.

Summary checklist (quick orientation): **Ask the recruiter** whether the round is: theory-only, **ML system design** (serving, training, data), or **stats/coding** (e.g. simple modeling). Cover all three lightly if unknown.

| Theme | Revision points |
|--------|-----------------|
| **Core ML** | Supervised vs unsupervised; bias–variance; train/val/test; overfitting, regularization; common metrics (accuracy, precision/recall, F1, AUC, log loss) and when they mislead. |
| **Models** | Linear models, trees/ensembles (RF, GBDT) at a high level; when you’d use what. Neural nets: **forward/backward intuition**, activations, vanishing gradients (name only if not research role). |
| **Deep learning (if your resume has it)** | CNNs (locality, pooling) vs RNN/Transformer for sequences; **attention** in one clear sentence. Training: batching, learning rate, batch norm / dropout (purpose). |
| **Data & features** | Missing values, class imbalance, leakage, train-serving skew, **feature stores** (conceptually). |
| **Production / scale** | Batch vs online inference; **latency vs throughput**; model monitoring (drift); A/B and shadow deployment — enough to discuss one past project. |
| **ML “system design” (common at Google)** | End-to-end: data sources → training pipeline → **evaluation** → deployment → **monitoring**; GPU vs CPU; **Google-flavored** topics may include TPUs, BigQuery/Spark-style batch (speak at requirements level). |
| **Honesty** | If you only used an API, say so; be ready for **“how you’d improve it”** and **what you’d verify in production**. |

**Practice:** walk two **STAR** stories for ML or data-heavy work (problem → metrics → what you built → result → what you’d do next). For one open-ended, try: “**Design a system to recommend YouTube/Search–style content**” or “**How would you debug a 5% quality drop?**” out loud, 20 minutes.

**External references (add your own):** *Hands-On Machine Learning* (Géron) for breadth; *Designing Machine Learning Systems* (Huyen) for production; distillation-style notes on **Transformer** if NLP is on your resume.

---

### Optional: structured 30-day program (if a day maps to a weak area)

The [../../archive/30-day/README.md](../../archive/30-day/README.md) program aligns by theme: week 1 (DS basics), week 2 (BST, heaps, graphs, DP intro), week 3 (backtracking, greedy, bit, mocks), week 4 (problem-solving, Google-focused day, final mocks, relaxation). For **Google-tagged review**, see [../../archive/30-day/week-4/ay-24-focus-on-google-specific-questions.md](../../archive/30-day/week-4/ay-24-focus-on-google-specific-questions.md).

---

## Week 1 (Days 1–7) — DSA speed + first **video (EET-style) mock** + start AI-ML

**Theme:** Core DSA coverage; **1 video mock** to mirror the **Google EET** DSA round; start **AI / ML** revision early so it is not a cram in week 2.

| Day | Focus | Actions |
|-----|--------|---------|
| **1** | Setup + arrays / hashing + windows | Skim [CODING_ROUNDS.md](CODING_ROUNDS.md); [../../reference/quick-sheets/revision-guide.md](../../reference/quick-sheets/revision-guide.md) Part A + B1–B2; solve **3–4** from [PROBLEM_SET.md](PROBLEM_SET.md) (arrays, two pointers, window). Confirm **EET time** in your local time + **interview order** (which day is EET vs on-site). |
| **2** | Arrays + strings (speed) | [../../reference/patterns/patterns-master.md](../../reference/patterns/patterns-master.md); **3–4** problems; log mistakes in [PRACTICE_TRACKER.md](PRACTICE_TRACKER.md). |
| **3** | Trees + BST | [../foundations/data-structures/tree.md](../foundations/data-structures/tree.md); **3–4** tree problems; verbalize traversals and LCA cases. |
| **4** | Binary search + heap + **AI-ML (first pass)** | [../foundations/algorithms/searching.md](../foundations/algorithms/searching.md), [../foundations/data-structures/heap.md](../foundations/data-structures/heap.md); **3** problems. **~90 min:** skim the **AI / ML revision checklist** above; write **3** bullet “definitions you could say in 60s” (e.g. train/val, precision/recall, overfitting). |
| **5** | Stack / queue, linked lists | [../foundations/data-structures/stack.md](../foundations/data-structures/stack.md); monotonic / parentheses; **2–3** problems; **1** list problem. |
| **6** | **Mock #1 (video / EET-style)** + graphs | **Timed DSA mock** in **45–60 min** with **camera + screen share** (1–2 problems) — this is your **EET** rehearsal. Then BFS/DFS: [../foundations/algorithms/graph.md](../foundations/algorithms/graph.md), [../foundations/data-structures/graphs.md](../foundations/data-structures/graphs.md); **2** graph/grid problems. |
| **7** | AI-ML + week review + optional SD | **2 h:** one **STAR** ML story + one **open-ended** ML question out loud (see AI / ML section). Re-read [../../reference/quick-sheets/quick-recall.md](../../reference/quick-sheets/quick-recall.md). Re-do **1** failed problem cold. *Only if* a **general** SD round is on your schedule: **1** pass [SYSTEM_DESIGN_L4.md](SYSTEM_DESIGN_L4.md) (else skip). |

**Week 1 goal:** you can name the **pattern in 30–60 seconds** (see [../foundations/GOOGLE_INTERVIEW_REVISION.md](../foundations/GOOGLE_INTERVIEW_REVISION.md)); you have done **at least one** DSA session under **virtual** conditions.

---

## Week 2 (Days 8–14) — Graphs, DP, **second DSA style** (on-site), **AI-ML deep dive**

**Theme:** Graphs + DP + backtracking; **2 more DSA mocks** — at least one **in-person or whiteboard / single-laptop** style to contrast with **EET**; **1 AI-ML–focused** session; **no** heavy new DSA on day 14.

| Day | Focus | Actions |
|-----|--------|---------|
| **8** | Graphs (BFS, DFS, topo) | **3–4** problems (grid BFS, Course Schedule–style, clone graph, etc. per [PROBLEM_SET.md](PROBLEM_SET.md)). |
| **9** | DP core | [../foundations/algorithms/dynamic-programming/README.md](../foundations/algorithms/dynamic-programming/README.md) + [../../reference/patterns/patterns-master.md](../../reference/patterns/patterns-master.md) skim; **3–4** DP problems (1D, 2D, one LIS/LCS-style). |
| **10** | Backtracking + greedy + **AI-ML (production + metrics)** | [../foundations/algorithms/backtracking.md](../foundations/algorithms/backtracking.md), [../foundations/algorithms/greedy.md](../foundations/algorithms/greedy.md); **2–3** problems. **~2 h:** train/serve skew, monitoring, one **ML system design** outline (15 min talk) from the AI / ML section. |
| **11** | **Mock #2 (on-site / whiteboard style)** + behavioral | **Timed DSA mock** **without** “full remote” setup if possible: one screen, or **paper** + pen, 45–60 min — to mirror the **in-person** DSA round. Tighten **STAR** drafts [BEHAVIORAL_GOOGLINESS.md](BEHAVIORAL_GOOGLINESS.md). |
| **12** | Mixed DSA + **AI-ML mock** | [COVERAGE_MAP.md](COVERAGE_MAP.md) gaps + [QUESTION_BANK.md](QUESTION_BANK.md); **2–3** DSA problems. **60 min:** **AI-ML** — resume deep dive + one scenario (“debug quality drop” or “design a retraining trigger”). |
| **13** | **Mock #3 (video again)** + polish | **EET-style** DSA **video mock** again (screen + audio) to stay sharp for **whichever** DSA is virtual. Review [CODING_ROUNDS.md](CODING_ROUNDS.md) debugging. Practice **1** ML and **1** collaboration story. |
| **14** | Light revision + rest | [../../reference/quick-sheets/revision-guide.md](../../reference/quick-sheets/revision-guide.md) Part A + [../../reference/quick-sheets/quick-recall.md](../../reference/quick-sheets/quick-recall.md) only. **0** new topics. Optional: [../../archive/30-day/week-4/day-28-relaxation-techniques-before-interviews.md](../../archive/30-day/week-4/day-28-relaxation-techniques-before-interviews.md). **Logistics:** charge laptop, test **EET** link, **ID / badge** for on-site, sleep. Prepare **2–3** questions for interviewers (team + **ML/infra** if relevant). |

**Week 2 goal:** you can run the DSA **flow** the same in **virtual** and **in-person** settings; you can spend **20 minutes** on coherent ML **tradeoffs and experience** without notes.

---

## If you have only 7 days left

Use the **7-day table** in [../foundations/GOOGLE_INTERVIEW_REVISION.md](../foundations/GOOGLE_INTERVIEW_REVISION.md) (Part D) and add: **2 DSA mocks** (one **video / EET-style**, one **in-person or paper**), **1** focused **AI-ML** block (see checklist), **3** behavioral/STAR stories, and **0–1** general SD passes **only** if a separate system-design round is confirmed.

---

## If you have 48 hours left

Follow **Part D — If you have 48 hours** in [../../reference/quick-sheets/revision-guide.md](../../reference/quick-sheets/revision-guide.md), plus [../../reference/quick-sheets/quick-recall.md](../../reference/quick-sheets/quick-recall.md) and [CODING_ROUNDS.md](CODING_ROUNDS.md). **Skim** the **AI / ML** checklist once; **do not** start new ML theory. Re-run a **45 min EET-style** block (audio + screen share) if the **virtual** DSA is still ahead of you.

---

## Related repo index (optional depth)

- **Top 20–style curated list:** [../sde3-dsa/sde-3-guide.md](../sde3-dsa/sde-3-guide.md)
- **LeetCode pattern list:** [../../archive/leetcode-patterns.md](../../archive/leetcode-patterns.md)
- **System design + algorithms (advanced):** [../sde3-dsa/system-design-algorithms.md](../sde3-dsa/system-design-algorithms.md)
- **Repository audit / orientation:** [../../archive/GOOGLE_SDE2_AUDIT.md](../../archive/GOOGLE_SDE2_AUDIT.md)

**Good luck.** For **DSA**: daily work on [PROBLEM_SET.md](PROBLEM_SET.md) + [PROBLEM_DETAILS.md](PROBLEM_DETAILS.md), and [GOOGLE_INTERVIEW_REVISION.md](../foundations/GOOGLE_INTERVIEW_REVISION.md) + [CODING_ROUNDS.md](CODING_ROUNDS.md) for communication. For **AI-ML** and for **EET vs on-site** logistics, this doc’s two dedicated sections are your home base — the repo’s other `.md` files are DSA/foundations centric.
