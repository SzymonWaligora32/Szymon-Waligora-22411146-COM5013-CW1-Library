from datetime import date
from typing import Optional, Any, List, Tuple


class Book:
    def __init__(self, book_id: str, title: str, author: str, subject: str) -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.subject = subject

        self.is_on_loan = False
        self.due_date: Optional[date] = None
        self.borrower_id: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"Book(book_id={self.book_id!r}, "
            f"title={self.title!r}, "
            f"author={self.author!r}, "
            f"is_on_loan={self.is_on_loan})"
        )
class Book:
    def __init__(self, book_id: str, title: str, author: str, subject: str) -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.subject = subject

        self.is_on_loan = False
        self.due_date: Optional[date] = None
        self.borrower_id: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"Book(book_id={self.book_id!r}, "
            f"title={self.title!r}, "
            f"author={self.author!r}, "
            f"is_on_loan={self.is_on_loan})"
        )


class HashTable:
    """
    Simple hash table with separate chaining.
    Key: string (e.g. book_id)
    Value: any Python object (e.g. Book instance)
    """

    def __init__(self, capacity: int = 101) -> None:
        # capacity is the number of buckets
        self.capacity = capacity
        self.buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(capacity)]

    def _bucket_index(self, key: str) -> int:
        """Compute index of bucket for the given key."""
        return hash(key) % self.capacity

    def put(self, key: str, value: Any) -> None:
        """Insert or update a key-value pair."""
        index = self._bucket_index(key)
        bucket = self.buckets[index]

        # Check if key already exists → update it
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return

        # Otherwise append new key-value pair
        bucket.append((key, value))

    def get(self, key: str) -> Optional[Any]:
        """Retrieve value for the given key, or None if not found."""
        index = self._bucket_index(key)
        bucket = self.buckets[index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value
        return None

    def delete(self, key: str) -> bool:
        """Delete entry with given key, return True if deleted, False if not found."""
        index = self._bucket_index(key)
        bucket = self.buckets[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                return True
        return False
