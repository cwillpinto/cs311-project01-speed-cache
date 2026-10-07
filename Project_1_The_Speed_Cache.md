# 🗄️ CS 311 Project 1: The Speed Cache (Fall 2026)

**Starter repository (GitHub template):** [https://github.com/cwillpinto/cs311-project01-speed-cache](https://github.com/cwillpinto/cs311-project01-speed-cache)

**Objective:** Design and implement a thread-safe **LRU (Least Recently Used) Cache**. A Content Delivery Network (CDN) edge server uses caching to avoid some requests to a distant origin server. You will combine a **Hash Map** (for expected O(1) key lookup) with a **Doubly Linked List** (for O(1) reordering of a known node), and keep both structures consistent under concurrent access.

---

## 🌐 The Technical Challenge
A CDN edge server can only hold a small slice of the internet in fast memory at once. When a request comes in:
- If the page is already cached (**a hit**), serve it instantly and mark it as the most recently used.
- If it isn't (**a miss**), fetch it, insert it into the cache, and evict the **least recently used** page if the cache is full.

Both operations — lookup and "mark as most recent" — must happen in **O(1)** time, no matter how many pages are cached. A Python `dict` alone gives you O(1) lookup but no ordering; a Python `list` alone gives you ordering but O(n) reordering. The LRU Cache solves this by wiring a hash map's *keys* directly to *nodes* inside a doubly linked list, so both structures update in lockstep.

Your starter `LRUCache` class already has the skeleton:
```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}
        self.list = DoublyLinkedList()
```
Your job is to finish it — correctly, efficiently, and safely under multiple threads.

---

## 🛠️ Detailed Student Tasks

1. **Phase 1: Architecture Design**
   Sketch (on paper or in a `DESIGN.md`) exactly how a `map` entry and a linked-list node relate to each other. What does the hash map's value actually store — the data itself, or a pointer to the list node? Get this right before you write a single line of the core logic.

2. **Phase 2: Core Build**
   Implement `get(key)` and `put(key, value)`:
   - `get(key)`: return the value if present (and move that entry to the "most recently used" end of the list), or the supplied `_MISSING` sentinel if absent — both in **O(1)**. A stored `None` is a valid hit and must remain distinct from a miss.
   - `put(key, value)`: insert or update a key, moving it to the "most recently used" end. If the cache is at `capacity`, evict the least recently used entry **before** inserting the new one.
   - Your Doubly Linked List needs `add_to_front`, `remove`, and `move_to_front` operations, all O(1) using direct node pointers (no scanning the list to find a node).

3. **Phase 3: Thread-Safety Hardening**
   Wrap `get` and `put` with a `threading.Lock` so that concurrent readers/writers cannot corrupt the map-to-node relationship. Write a stress test that spins up multiple threads hammering `get`/`put` on the same cache instance simultaneously, and confirm no `KeyError`, no orphaned nodes, and no map/list desynchronization occurs.

4. **Phase 4: Verification & Benchmarking**
   - Run `python -m unittest test_lru.py` — every test must pass.
   - Run the supplied `simulate_hitrate.py` with the **same sequence** of simulated page requests at several `capacity` values. Report each hit rate and explain the observed difference. You may extend the script, but a hit-rate result is workload evidence, not proof of O(1) operation cost.

**Complete Project 1 is due Friday, October 16, 2026 at 11:59 PM Central.** Tuesday, October 6 is Fall Break. Tuesday and Thursday have no required on-campus class; you may work on Project 1 in the classroom or elsewhere, or be absent. Thursday includes a brief optional wiring demonstration and project handoff.

---

## 💡 Pro-Tips & Implementation Hints
- **Sentinel nodes:** Give your Doubly Linked List permanent `head` and `tail` sentinel nodes (never holding real data). This eliminates almost every null-check edge case in `add_to_front`/`remove`.
- **Map stores nodes, not values:** `self.map[key]` should point directly at the linked-list `Node` object, not just the raw value. That's what makes `get` able to relocate the node in O(1) — no searching required.
- **Lock granularity:** A single lock around the entire `get`/`put` method body is simpler and safer than fine-grained locking. Don't over-engineer this — correctness first, optimization only if you have time left.
- **Don't forget eviction order:** Evicting must always remove the node adjacent to the `tail` sentinel (least recently used), never the node adjacent to `head`.
- **Test concurrency honestly:** A stress test that "usually passes" is not a passing stress test. Run it multiple times, and consider adding a small `time.sleep(0)` inside critical sections during testing to intentionally widen race windows.

---

## ⚖️ Grading Rubric (CS 311 — Project 1)

| Category | Weight | Description |
| :--- | :--- | :--- |
| **Correctness (get/put)** | 35% | `get` and `put` behave correctly, including eviction, on all standard and edge-case inputs. |
| **True O(1) Operations** | 20% | No hidden O(n) scans in `get`, `put`, or eviction — verified via code review and Big-O justification. |
| **Thread Safety** | 20% | Lock usage correctly prevents corruption under the concurrent stress test. |
| **Verification & Benchmarking** | 15% | All `unittest` cases pass; hit-rate CLI simulation runs and produces sensible output. |
| **Design and Terminal Evidence** | 10% | `DESIGN.md`, reproducible commands, invariant evidence, complete transcript, and Success Token. |

---

## 📅 Project Timeline and Submission

| Date | Goal |
| :--- | :--- |
| Tuesday, October 6 | Fall Break — no required class. Optional classroom or independent Project 1 work; attendance is not required. |
| Thursday, October 8 | Optional classroom Project 1 work after a brief wiring demonstration; work elsewhere or be absent if preferred. |
| Friday, October 16, 11:59 PM Central | Complete 100-point Project 1 due in Course Projects. |

Submit `README.md`, `DESIGN.md`, `doubly_linked_list.py`, `lru_cache.py`, your hit-rate evidence for multiple capacities, a complexity justification for `get`, `put`, and eviction, and the full `python verify_project1.py` transcript including map/list invariant and contention checks and the Success Token. Include any modified `simulate_hitrate.py` and `test_lru.py`.

---

**Terminal check:** The documented commands must run from the submitted files without an IDE. Include enough setup instructions in `README.md` for a reviewer to reproduce your results; the rubric above governs scoring.
