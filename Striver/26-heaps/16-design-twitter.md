---
module: striver/26-heaps
lesson: 16
topic: Design twitter
difficulty: Medium
source: https://takeuforward.org/learning/dsa/design-twitter?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, design, k-way-merge]
---
# 16. Design twitter

← [Hand of Straights](15-hand-of-straights.md) · [Part 26 index](README.md) · Next → [Minimum cost to connect sticks](17-minimum-cost-to-connect-sticks.md)

> [!abstract] Problem at a glance
> **Task:** Design `postTweet`, `follow`, `unfollow` and `getNewsFeed(userId)` returning the 10 most recent tweet ids from the user and their followees.
> **Key insight:** Each user's tweets are already sorted by time (append-only). The feed is a **k-way merge** of the followees' lists, newest first, stopped after 10. Use a max-heap seeded with each list's last tweet. Cost per feed: O(f + 10 log f) for f followees.
> **Difficulty:** Medium · **Pattern:** K-way merge (heap) + hash maps · **Also on:** [LC 355](https://leetcode.com/problems/design-twitter/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/design-twitter?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Collect all, sort, take 10](#3-collect-all-sort-take-10) · [4. Heap-based k-way merge](#4-heap-based-k-way-merge) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`postTweet(userId, tweetId)` composes a new tweet (ids unique). `getNewsFeed(userId)` returns up to 10 tweet ids from the user and the users they follow, most recent first. `follow(a, b)` / `unfollow(a, b)`: `a` starts/stops following `b`.

| Input | Output | Why |
|---|---|---|
| `post(1,5); feed(1); follow(1,2); post(2,6); feed(1); unfollow(1,2); feed(1)` | `[5], [6,5], [5]` |  |

**Constraints:** `1 ≤ userId, followeeId ≤ 500`, up to `3·10⁴` calls in total.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Collect all, sort, take 10 | gather every followee tweet; sort by time | feed O(T log T) | O(T) |
| Heap-based k-way merge | max-heap of (time, user, idx); pop ≤ 10, push predecessor | feed O(f + 10 log f) | O(users + tweets) |

> [!tip] Interview angle
> Drive it like a mini system design: data model first (`tweets[user] = [(time, id)]`, `follows[user] = set`), then the feed as merge-k. Mention fan-out-on-write vs fan-out-on-read: this is read-time merge; celebrities make write-time fan-out expensive, and real systems mix the two.

---

## 3. Collect all, sort, take 10

**Intuition.** Simple and correct, but cost grows with the total number of tweets, not with the 10 you need.

```python
from collections import defaultdict
class TwitterSort:
    def __init__(self):
        self.t, self.tw, self.fl = 0, defaultdict(list), defaultdict(set)
    def postTweet(self, u, tid):
        self.t += 1
        self.tw[u].append((self.t, tid))
    def getNewsFeed(self, u):
        allt = [x for v in self.fl[u] | {u} for x in self.tw[v]]
        return [tid for _, tid in sorted(allt, reverse=True)[:10]]
    def follow(self, a, b):
        self.fl[a].add(b)
    def unfollow(self, a, b):
        self.fl[a].discard(b)
```

**Complexity:** time **feed O(T log T)**, space **O(T)**.

---

## 4. Heap-based k-way merge

**Intuition.** Seed a max-heap with the newest tweet of each followee (and self). Pop the newest overall; push that user's next-older tweet. Stop after 10 pops.

**Algorithm**

1. Global counter `time` increments per tweet.
2. `tweets[u]` appends `(time, id)`; `follows[u]` is a set (self handled separately).
3. Feed: for each `v` in `follows[u] ∪ {u}` with tweets, push `(lastTime, v, lastIdx)`.
4. Pop up to 10 times; after popping `(_, v, i)` push `(tweets[v][i−1], v, i−1)` if `i > 0`.

**Dry run** — User 4 follows 3 (tweets 100…111) and posted 200 last. Heap {(200,4), (111,3)} → 200; push nothing for 4 → 111, push 110 → … → 10 ids: 200, 111…103.

**C++**
```cpp
class Twitter {
    int time = 0;
    unordered_map<int, vector<pair<int, int>>> tweets;   // user -> (time, id)
    unordered_map<int, unordered_set<int>> follows;
public:
    void postTweet(int u, int id) { tweets[u].push_back({++time, id}); }
    vector<int> getNewsFeed(int u) {
        priority_queue<tuple<int, int, int>> pq;          // (time, user, idx)
        auto seed = [&](int v) {
            auto it = tweets.find(v);
            if (it != tweets.end() && !it->second.empty())
                pq.push({it->second.back().first, v, (int)it->second.size() - 1});
        };
        seed(u);
        for (int v : follows[u]) if (v != u) seed(v);
        vector<int> res;
        while (!pq.empty() && res.size() < 10) {
            auto [t, v, i] = pq.top(); pq.pop();
            res.push_back(tweets[v][i].second);
            if (i > 0) pq.push({tweets[v][i - 1].first, v, i - 1});
        }
        return res;
    }
    void follow(int a, int b) { follows[a].insert(b); }
    void unfollow(int a, int b) { follows[a].erase(b); }
};
```

**Java**
```java
static class Twitter {
    private int time = 0;
    private final Map<Integer, List<int[]>> tweets = new HashMap<>();   // user -> [time, id]
    private final Map<Integer, Set<Integer>> follows = new HashMap<>();
    void postTweet(int u, int id) { tweets.computeIfAbsent(u, x -> new ArrayList<>()).add(new int[]{++time, id}); }
    List<Integer> getNewsFeed(int u) {
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(b[0], a[0]));  // [time, user, idx]
        Set<Integer> src = new HashSet<>(follows.getOrDefault(u, Collections.emptySet()));
        src.add(u);
        for (int v : src) {
            List<int[]> l = tweets.get(v);
            if (l != null && !l.isEmpty()) pq.offer(new int[]{l.get(l.size() - 1)[0], v, l.size() - 1});
        }
        List<Integer> res = new ArrayList<>();
        while (!pq.isEmpty() && res.size() < 10) {
            int[] e = pq.poll();
            List<int[]> l = tweets.get(e[1]);
            res.add(l.get(e[2])[1]);
            if (e[2] > 0) pq.offer(new int[]{l.get(e[2] - 1)[0], e[1], e[2] - 1});
        }
        return res;
    }
    void follow(int a, int b) { follows.computeIfAbsent(a, x -> new HashSet<>()).add(b); }
    void unfollow(int a, int b) { Set<Integer> s = follows.get(a); if (s != null) s.remove(b); }
}
```

**Python**
```python
import heapq
from collections import defaultdict
class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)      # user -> [(time, id)]
        self.follows = defaultdict(set)
    def postTweet(self, u, tid):
        self.time += 1
        self.tweets[u].append((self.time, tid))
    def getNewsFeed(self, u):
        h = []
        for v in self.follows[u] | {u}:
            if self.tweets[v]:
                i = len(self.tweets[v]) - 1
                h.append((-self.tweets[v][i][0], v, i))
        heapq.heapify(h)
        res = []
        while h and len(res) < 10:
            _, v, i = heapq.heappop(h)
            res.append(self.tweets[v][i][1])
            if i:
                heapq.heappush(h, (-self.tweets[v][i - 1][0], v, i - 1))
        return res
    def follow(self, a, b):
        self.follows[a].add(b)
    def unfollow(self, a, b):
        self.follows[a].discard(b)
```

**Complexity:** time **feed O(f + 10 log f)**, space **O(users + tweets)** — heapify f seeds in O(f); 10 pops/pushes of O(log f).

---

## Edge cases

- User follows themself: dedupe the self source (set union / `v != u`).
- Unfollow someone not followed: no-op.
- User with no tweets and no followees → `[]`.
- Ordering must use a global timestamp, not tweet ids.

---

## Common mistakes

1. Sorting by tweet id instead of post time.
2. Seeding the heap with *every* tweet instead of one per user.
3. Letting `unfollow(u, u)` remove the user's own tweets from their feed.

---

## Follow-ups

1. Millions of users, celebrities?
2. Paginate the feed?

<details><summary>Answer sketches</summary>

**#1:** Hybrid fan-out: push tweets into followers' cached feeds for normal users, pull and merge for celebrities at read time.

**#2:** Return a cursor `(time)`; next page = same merge restricted to tweets older than the cursor.
</details>

---

## Flashcards

**Design Twitter feed algorithm?** #flashcard
K-way merge of followees' tweet lists with a max-heap, stop at 10.

**Twitter: what orders tweets?** #flashcard
A global increasing timestamp.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
