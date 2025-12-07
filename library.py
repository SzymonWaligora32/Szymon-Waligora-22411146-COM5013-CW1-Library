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
class BstNode:
    """
    Node in a binary search tree (BST) for indexing books by title.
    key: lowercase title string
    books: list of Book objects that share that title
    """

    def __init__(self, key: str, books: List["Book"]) -> None:
        self.key = key
        self.books = books
        self.left: Optional["BstNode"] = None
        self.right: Optional["BstNode"] = None


class TitleIndexBst:
    """
    Binary search tree index for book titles.
    Allows exact title searches and simple prefix searches.
    """

    def __init__(self) -> None:
        self.root: Optional[BstNode] = None

    def insert(self, title: str, book: Book) -> None:
        """Insert a book into the BST using its title as the key."""
        key = title.lower()
        self.root = self._insert_recursive(self.root, key, book)

    def _insert_recursive(
        self,
        node: Optional[BstNode],
        key: str,
        book: Book,
    ) -> BstNode:
        if node is None:
            return BstNode(key, [book])

        if key < node.key:
            node.left = self._insert_recursive(node.left, key, book)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, book)
        else:
            # same title: add book to this node's list
            node.books.append(book)

        return node

    def search_exact(self, title: str) -> List[Book]:
        """Find all books whose title exactly matches the given title."""
        key = title.lower()
        return self._search_exact_recursive(self.root, key)

    def _search_exact_recursive(
        self,
        node: Optional[BstNode],
        key: str,
    ) -> List[Book]:
        if node is None:
            return []

        if key < node.key:
            return self._search_exact_recursive(node.left, key)
        if key > node.key:
            return self._search_exact_recursive(node.right, key)
        return node.books

    def search_prefix(self, prefix: str) -> List[Book]:
        """
        Find all books whose title starts with the given prefix
        (case-insensitive).
        """
        prefix_key = prefix.lower()
        found: List[Book] = []
        self._search_prefix_recursive(self.root, prefix_key, found)
        return found

    def _search_prefix_recursive(
        self,
        node: Optional[BstNode],
        prefix: str,
        found: List[Book],
    ) -> None:
        if node is None:
            return

        # In-order style traversal, checking for prefix matches
        if node.key.startswith(prefix):
            found.extend(node.books)

        if prefix <= node.key:
            self._search_prefix_recursive(node.left, prefix, found)
        if prefix >= node.key:
            self._search_prefix_recursive(node.right, prefix, found)
