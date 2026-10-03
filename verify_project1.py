"""
Project 1: The Speed Cache -- full verification (unittest suite +
concurrency stress test + hit-rate simulation sanity check).

Run: python verify_project1.py
Prints the Success Token only if every check below passes.
"""

import base64
import hashlib
import io
import random
import sys
import threading
import unittest

from lru_cache import _MISSING, LRUCache
from simulate_hitrate import simulate

ASSIGNMENT_ID = "PROJECT1"


def get_student_id() -> str:
    """Prompt for the student's USI username; baked into the Success Token
    so a copied/shared token decodes to someone else's name, not yours."""
    student_id = input("Enter your USI username (e.g. cwill): ").strip()
    while not student_id:
        student_id = input("Username cannot be blank. Enter your USI username: ").strip()
    return student_id


def generate_token(assignment_id: str, student_id: str) -> str:
    digest = hashlib.sha256(f"CS311-{assignment_id}-{student_id}-VERIFIED".encode()).hexdigest()[:16]
    raw = f"CS311|{assignment_id}|{student_id}|PASS|{digest}"
    return base64.b64encode(raw.encode()).decode()


def print_success_banner(assignment_id: str) -> None:
    student_id = get_student_id()
    token = generate_token(assignment_id, student_id)
    print("\n" + "=" * 60)
    print(f"  ALL CHECKS PASSED -- {assignment_id}")
    print(f"  STUDENT: {student_id}")
    print("  SUCCESS TOKEN (paste this into Blackboard):")
    print(f"  {token}")
    print("=" * 60 + "\n")


def check(label: str, condition: bool, failures: list) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}")
    if not condition:
        failures.append(label)


def run_unittest_suite(failures: list) -> None:
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=".", pattern="test_lru.py")
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    check(f"unittest suite: {result.testsRun} tests run, {len(result.failures) + len(result.errors)} failed", result.wasSuccessful(), failures)


def concurrency_stress_test(failures: list, num_threads: int = 20, ops_per_thread: int = 500) -> None:
    cache = LRUCache(capacity=100)
    crash_flags = [False] * num_threads
    rng_seed_base = 311

    def worker(worker_id: int) -> None:
        rng = random.Random(rng_seed_base + worker_id)
        try:
            for _ in range(ops_per_thread):
                key = rng.randint(0, 150)  # overlapping key space -> real contention
                if rng.random() < 0.5:
                    cache.get(key)
                else:
                    cache.put(key, key * 2)
        except Exception:
            crash_flags[worker_id] = True

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    check("concurrency stress test: no thread raised an exception", not any(crash_flags), failures)

    # Structural consistency: every map entry must be reachable by walking
    # the list, and the list's real length must match the map's length.
    node = cache.list.head.next
    seen_nodes = []
    steps = 0
    while node is not cache.list.tail and steps <= len(cache.map) + 5:
        seen_nodes.append(node)
        node = node.next
        steps += 1
    check("post-stress: list traversal reaches exactly as many nodes as map entries", len(seen_nodes) == len(cache.map), failures)
    check("post-stress: every list node is the exact mapped node and links agree",
          all(node.key in cache.map and cache.map[node.key] is node and node.prev.next is node and node.next.prev is node for node in seen_nodes) and
          len({node.key for node in seen_nodes}) == len(seen_nodes) and
          cache.list.head.next.prev is cache.list.head and
          cache.list.tail.prev.next is cache.list.tail, failures)
    check("post-stress: cache never exceeded its capacity", len(cache.map) <= cache.capacity, failures)


def hitrate_sanity_check(failures: list) -> None:
    rng = random.Random(311)
    popular_pages = [f"page-{i}" for i in range(20)]
    rare_pages = [f"page-{i}" for i in range(20, 500)]
    requests = [rng.choice(popular_pages) if rng.random() < 0.8 else rng.choice(rare_pages) for _ in range(5000)]

    small_hit_rate = simulate(5, requests)
    large_hit_rate = simulate(200, requests)
    print(f"  hit rate at capacity=5:   {small_hit_rate:.2%}")
    print(f"  hit rate at capacity=200: {large_hit_rate:.2%}")
    check("hit rate improves as capacity grows", large_hit_rate > small_hit_rate, failures)


def main() -> int:
    failures: list = []

    print("Running non-concurrent unittest suite (test_lru.py)...\n")
    run_unittest_suite(failures)
    if failures:
        print(f"\n{len(failures)} check(s) failed -- fix correctness before the stress test. No token issued.")
        return 1

    print("\nRunning concurrency stress test (20 threads x 500 ops)...\n")
    concurrency_stress_test(failures)
    if failures:
        print(f"\n{len(failures)} check(s) failed. No token issued.")
        return 1

    print("\nRunning hit-rate simulation sanity check...\n")
    hitrate_sanity_check(failures)

    print()
    if failures:
        print(f"{len(failures)} check(s) failed. No token issued.")
        return 1

    print_success_banner(ASSIGNMENT_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
