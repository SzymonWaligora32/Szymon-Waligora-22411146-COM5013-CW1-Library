from library import Book, HashTable, TitleIndexBst


def main() -> None:
    test_book = Book("B001", "Algorithms", "Sedgewick", "CS")
    print(test_book)


if __name__ == "__main__":
    main()

def main() -> None:
    # create the hash table index for books
    id_index = HashTable()

    # create a few example books
    book1 = Book("B001", "Algorithms", "Sedgewick", "CS")
    book2 = Book("B002", "Introduction to Algorithms", "Cormen", "CS")

    # store books in the hash table using book_id as the key
    id_index.put(book1.book_id, book1)
    id_index.put(book2.book_id, book2)

    # retrieve a book by id
    fetched = id_index.get("B001")
    print("Fetched B001:", fetched)

    # try a non-existing id
    missing = id_index.get("B999")
    print("Fetched B999 (should be None):", missing)


if __name__ == "__main__":
    main()

def main() -> None:
    # create indexes
    id_index = HashTable()
    title_index = TitleIndexBst()

    # create some example books
    book1 = Book("B001", "Algorithms", "Sedgewick", "CS")
    book2 = Book("B002", "Introduction to Algorithms", "Cormen", "CS")
    book3 = Book("B003", "Algebra", "Stewart", "Maths")
    book4 = Book("B004", "Artificial Intelligence", "Russell", "CS")

    # add books to both indexes
    for book in (book1, book2, book3, book4):
        id_index.put(book.book_id, book)
        title_index.insert(book.title, book)

    # test exact search
    print("Exact title search for 'Algorithms':")
    results_exact = title_index.search_exact("Algorithms")
    for b in results_exact:
        print("  ", b)

    # test prefix search
    print("\nPrefix search for 'Al':")
    results_prefix = title_index.search_prefix("Al")
    for b in results_prefix:
        print("  ", b)

    # still show an ID-based lookup using hash table
    print("\nLookup by ID 'B003':")
    fetched = id_index.get("B003")
    print("  ", fetched)


if __name__ == "__main__":
    main()
