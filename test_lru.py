"""
Project 1: The Speed Cache -- unittest suite (non-concurrent correctness).

Run: python -m unittest test_lru.py
See verify_project1.py for the full check (this suite + the
concurrency stress test + the hit-rate simulation + the Success Token).
"""

import unittest

from lru_cache import _MISSING, LRUCache


class TestLRUCacheBasics(unittest.TestCase):
    def assert_invariant(self, cache):
        """Every map entry is the exact reachable node and all links agree."""
        seen = {}
        previous = cache.list.head
        node = previous.next
        while node is not cache.list.tail:
            self.assertIs(node.prev, previous)
            self.assertIs(previous.next, node)
            self.assertNotIn(node.key, seen)
            self.assertIs(cache.map[node.key], node)
            seen[node.key] = node
            previous, node = node, node.next
            self.assertLessEqual(len(seen), cache.capacity)
        self.assertIs(cache.list.tail.prev, previous)
        self.assertEqual(set(seen), set(cache.map))

    def test_invariants_after_every_mutation(self):
        cache = LRUCache(capacity=3)
        for operation, key, value in [
            ("put", "a", 1), ("put", "b", 2), ("get", "a", None),
            ("put", "a", 3), ("put", "c", 4), ("put", "d", 5),
            ("get", "b", None), ("put", "e", 6),
        ]:
            if operation == "put": cache.put(key, value)
            else: cache.get(key)
            self.assert_invariant(cache)

    def test_put_then_get(self):
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        self.assertEqual(cache.get("a"), 1)

    def test_get_missing_key_returns_sentinel(self):
        cache = LRUCache(capacity=2)
        self.assertIs(cache.get("nope"), _MISSING)

    def test_put_updates_existing_key(self):
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.put("a", 2)
        self.assertEqual(cache.get("a"), 2)

    def test_eviction_removes_least_recently_used(self):
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)  # capacity 2, should evict "a" (never touched since insert)
        self.assertIs(cache.get("a"), _MISSING)
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)

    def test_get_marks_entry_as_recently_used(self):
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")       # touching "a" should protect it from the next eviction
        cache.put("c", 3)    # should now evict "b", not "a"
        self.assertEqual(cache.get("a"), 1)
        self.assertIs(cache.get("b"), _MISSING)
        self.assertEqual(cache.get("c"), 3)

    def test_put_marks_entry_as_recently_used(self):
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("a", 10)   # re-putting "a" should also protect it
        cache.put("c", 3)    # should evict "b", not "a"
        self.assertEqual(cache.get("a"), 10)
        self.assertIs(cache.get("b"), _MISSING)

    def test_capacity_one(self):
        cache = LRUCache(capacity=1)
        cache.put("a", 1)
        cache.put("b", 2)
        self.assertIs(cache.get("a"), _MISSING)
        self.assertEqual(cache.get("b"), 2)

    def test_repeated_eviction_sequence(self):
        cache = LRUCache(capacity=3)
        for i in range(10):
            cache.put(i, i * 10)
        # only the last 3 keys (7, 8, 9) should remain
        for i in range(7):
            self.assertIs(cache.get(i), _MISSING)
        for i in range(7, 10):
            self.assertEqual(cache.get(i), i * 10)


if __name__ == "__main__":
    unittest.main()
