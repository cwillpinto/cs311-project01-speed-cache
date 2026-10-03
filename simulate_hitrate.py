"""
Project 1: The Speed Cache -- Phase 4 hit-rate CLI simulation.

Run: python simulate_hitrate.py
Replays a simulated sequence of page requests against the cache at a
few different capacities and reports the hit rate for each, showing
that hit rate improves as capacity grows.
"""

import random

from lru_cache import _MISSING, LRUCache


def simulate(capacity: int, requests: list) -> float:
    cache = LRUCache(capacity=capacity)
    hits = 0
    for page in requests:
        if cache.get(page) is not _MISSING:
            hits += 1
        else:
            cache.put(page, f"content-of-{page}")
    return hits / len(requests)


def main() -> None:
    rng = random.Random(311)
    # A Zipf-ish workload: a small set of "popular" pages requested far
    # more often than a long tail of rare ones -- this is what makes
    # hit rate meaningfully improve as capacity grows, instead of being
    # flat regardless of capacity like a uniform-random workload would be.
    popular_pages = [f"page-{i}" for i in range(20)]
    rare_pages = [f"page-{i}" for i in range(20, 500)]
    requests = []
    for _ in range(20_000):
        if rng.random() < 0.8:
            requests.append(rng.choice(popular_pages))
        else:
            requests.append(rng.choice(rare_pages))

    print("Simulating page requests across cache capacities...\n")
    for capacity in [5, 10, 20, 50, 100]:
        hit_rate = simulate(capacity, requests)
        print(f"  capacity={capacity:4d}  hit rate={hit_rate:.2%}")


if __name__ == "__main__":
    main()
