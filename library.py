from datetime import date
from typing import Optional


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
