from collections import deque
from datetime import date, timedelta
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
        self.reservation_queue = deque()  # queue of user_ids

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
class Library:
    """
    Main library class that uses:
    - HashTable for fast lookup by book_id
    - TitleIndexBst for searching by title
    """

    loan_period_days = 14

    def __init__(self) -> None:
        self.id_index = HashTable()
        self.title_index = TitleIndexBst()

    # --- catalogue operations ---

    def add_book(self, book_id: str, title: str, author: str, subject: str) -> None:
        """Add a new book to the library catalogue."""
        if self.id_index.get(book_id) is not None:
            raise ValueError(f"Book with id {book_id} already exists")

        book = Book(book_id, title, author, subject)
        self.id_index.put(book_id, book)
        self.title_index.insert(title, book)

    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """Return a book by its ID, or None if not found."""
        return self.id_index.get(book_id)

    def search_title_exact(self, title: str) -> List[Book]:
        """Return a list of books with exactly this title."""
        return self.title_index.search_exact(title)

    def search_title_prefix(self, prefix: str) -> List[Book]:
        """Return a list of books whose titles start with this prefix."""
        return self.title_index.search_prefix(prefix)

    # --- loan operations ---

    def borrow_book(self, book_id: str, user_id: str) -> str:
        """Borrow a book or join the reservation queue if it is on loan."""
        book = self.get_book_by_id(book_id)
        if book is None:
            return "Book not found."

        if not book.is_on_loan:
            book.is_on_loan = True
            book.borrower_id = user_id
            book.due_date = date.today().replace() + timedelta(days=self.loan_period_days)
            return f"Book borrowed successfully. Due date: {book.due_date}"

        # already on loan → add to reservation queue
        book.reservation_queue.append(user_id)
        return "Book is currently on loan. You have been added to the reservation queue."

    def return_book(self, book_id: str) -> str:
        """Return a book and possibly issue it to the next user in the reservation queue."""
        book = self.get_book_by_id(book_id)
        if book is None:
            return "Book not found."

        if not book.is_on_loan:
            return "Book is not currently on loan."

        book.is_on_loan = False
        book.borrower_id = None
        book.due_date = None

        if book.reservation_queue:
            next_user = book.reservation_queue.popleft()
            book.is_on_loan = True
            book.borrower_id = next_user
            book.due_date = date.today().replace() + timedelta(days=self.loan_period_days)
            return (
                "Book returned and issued to next user in queue: "
                f"{next_user}, due on {book.due_date}"
            )

        return "Book returned and is now available."

    # --- reporting/lists ---

    def list_all_books(self) -> List[Book]:
        """Return a list of all books in the library (unsorted)."""
        all_books: List[Book] = []
        for bucket in self.id_index.buckets:
            for _, book in bucket:
                all_books.append(book)
        return all_books

    def list_books_sorted_by_title(self) -> List[Book]:
        """Return all books sorted by title."""
        books = self.list_all_books()
        return sorted(books, key=lambda b: b.title.lower())

    def list_overdue_books(self) -> List[Book]:
        """Return a list of all overdue books, sorted by due date."""
        today = date.today()
        overdue: List[Book] = []

        for book in self.list_all_books():
            if book.is_on_loan and book.due_date is not None and book.due_date < today:
                overdue.append(book)

        return sorted(overdue, key=lambda b: b.due_date)
