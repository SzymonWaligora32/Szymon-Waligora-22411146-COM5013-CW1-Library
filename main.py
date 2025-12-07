from library import Library


def print_menu() -> None:
    print("\n--- Library Menu ---")
    print("1. Add a new book")
    print("2. Search book by ID")
    print("3. Search book by exact title")
    print("4. Search book by title prefix")
    print("5. Borrow a book")
    print("6. Return a book")
    print("7. List all books")
    print("8. List all books sorted by title")
    print("9. List overdue books")
    print("0. Exit")


def main() -> None:
    print("Starting library program...")  # debug line so we see *something*
    library = Library()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            book_id = input("Enter book ID: ").strip()
            title = input("Enter title: ").strip()
            author = input("Enter author: ").strip()
            subject = input("Enter subject: ").strip()
            try:
                library.add_book(book_id, title, author, subject)
                print("Book added.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "2":
            book_id = input("Enter book ID to search: ").strip()
            book = library.get_book_by_id(book_id)
            if book is None:
                print("Book not found.")
            else:
                print("Found:", book)

        elif choice == "3":
            title = input("Enter exact title to search: ").strip()
            results = library.search_title_exact(title)
            if not results:
                print("No books found.")
            else:
                print("Books found:")
                for book in results:
                    print("  ", book)

        elif choice == "4":
            prefix = input("Enter title prefix to search: ").strip()
            results = library.search_title_prefix(prefix)
            if not results:
                print("No books found.")
            else:
                print("Books found:")
                for book in results:
                    print("  ", book)

        elif choice == "5":
            book_id = input("Enter book ID to borrow: ").strip()
            user_id = input("Enter your user ID: ").strip()
            message = library.borrow_book(book_id, user_id)
            print(message)

        elif choice == "6":
            book_id = input("Enter book ID to return: ").strip()
            message = library.return_book(book_id)
            print(message)

        elif choice == "7":
            books = library.list_all_books()
            if not books:
                print("No books in library.")
            else:
                print("All books:")
                for book in books:
                    print("  ", book)

        elif choice == "8":
            books = library.list_books_sorted_by_title()
            if not books:
                print("No books in library.")
            else:
                print("Books sorted by title:")
                for book in books:
                    print("  ", book)

        elif choice == "9":
            overdue_books = library.list_overdue_books()
            if not overdue_books:
                print("No overdue books.")
            else:
                print("Overdue books:")
                for book in overdue_books:
                    print("  ", book)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
