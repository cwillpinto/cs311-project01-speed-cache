"""
Project 1: The Speed Cache -- DoublyLinkedList starter.

Sentinel-based design (Pro-Tip from the project doc): head/tail never
hold real data, which eliminates most null-check edge cases. Complete
add_to_front, remove, and move_to_front -- all must be O(1) using
direct node pointers, never scanning the list.
"""

from typing import Any, Optional


class Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: Any = None, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head = Node()  # sentinel -- never holds real data
        self.tail = Node()  # sentinel -- never holds real data
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_to_front(self, node: Node) -> None:
        """Insert `node` immediately after the head sentinel (the 'most recently used' end). O(1)."""
        # TODO
        raise NotImplementedError

    def remove(self, node: Node) -> None:
        """Unlink `node` from wherever it currently sits. O(1)."""
        # TODO
        raise NotImplementedError

    def move_to_front(self, node: Node) -> None:
        """Move an already-linked `node` to the front. O(1) -- should just be remove() + add_to_front()."""
        # TODO
        raise NotImplementedError

    def least_recently_used(self) -> Optional[Node]:
        """Given: the node adjacent to the tail sentinel, or None if the list is empty."""
        return self.tail.prev if self.tail.prev is not self.head else None
