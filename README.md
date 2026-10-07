# Project 1: The Speed Cache

Full assignment: `Project_1_The_Speed_Cache.md` (course handout; copy alongside this starter when staging the repository).

## GitHub workflow
Use **Use this template** to create your own repository, clone it, complete the
starter TODOs, and commit and push your work. Submit the files and evidence
listed in the assignment through Blackboard.

Complete 100-point Course Project due Friday, October 16, 2026 at 11:59 PM Central. Tuesday, October 6 is Fall Break. Neither Tuesday nor Thursday requires on-campus attendance: you may work on Project 1 in the classroom or elsewhere, or be absent. Thursday offers a brief optional wiring demonstration and project handoff.

## Files
- `doubly_linked_list.py` -- sentinel-based DLL: complete `add_to_front`, `remove`, `move_to_front`
- `lru_cache.py` -- `LRUCache`: complete `get`, `put`, and lock usage
- `test_lru.py` -- non-concurrent correctness suite (`python -m unittest test_lru.py`)
- `simulate_hitrate.py` -- supplied CLI hit-rate simulation; run the same workload at several capacities and explain the result
- `verify_project1.py` -- runs everything above plus a concurrency stress test, then prints the Success Token

## Run
```bash
python -m unittest test_lru.py
python verify_project1.py         # full check, including thread-safety -- run this for the token
```

## Submit
1. `README.md` with reproducible setup and commands, and `DESIGN.md`
2. `doubly_linked_list.py`, `lru_cache.py`
3. Hit-rate evidence at multiple capacities
4. Full `python verify_project1.py` transcript, including invariant and contention checks, and Success Token
5. Complexity justification for `get`, `put`, and eviction
6. Any modified `simulate_hitrate.py` and `test_lru.py`
