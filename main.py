from library import Book, HashTable


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
