"""
Project 1: The Speed Cache -- LRUCache starter.

See the assignment for full phase-by-phase requirements.
Thread-safety (Phase 3) belongs here too -- wrap get/put bodies in a
single threading.Lock. Don't over-engineer with finer-grained locking.
"""

import threading
from typing import Any, Optional

from doubly_linked_list import DoublyLinkedList, Node

_MISSING = object()  # sentinel distinguishing "not found" from a legitimately-stored None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.map = {}
        self.list = DoublyLinkedList()
        # TODO (Phase 3): add a threading.Lock and wrap get/put bodies in it.
        self._lock = threading.Lock()

    def get(self, key: Any) -> Any:
        """
        Return the value for `key` and move it to the most-recently-used
        end, or return the _MISSING sentinel if absent. Both in O(1).
        """
        # TODO
        raise NotImplementedError

    def put(self, key: Any, value: Any) -> None:
        """
        Insert or update `key`, moving it to the most-recently-used end.
        If at capacity, evict the least-recently-used entry BEFORE
        inserting the new one. O(1).
        """
        # TODO
        raise NotImplementedError
