import time
from library import Library, HashTable, TitleIndexBst, Book


def print_header(title: str) -> None:
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


# 1. EMPTY DATA STRUCTURE TESTS

def test_empty_structures() -> None:
    print_header("TEST 1: Handling Empty Data Structures")

    lib = Library()
    hash_table = HashTable()
    bst = TitleIndexBst()

    # HashTable search on empty
    print("HashTable get('X') →", hash_table.get("X"))

    # BST exact search on empty
    print("BST exact search('Algorithms') →", bst.search_exact("Algorithms"))

    # Library searches on empty catalogue
    print("Library search by ID →", lib.get_book_by_id("B001"))
    print("Library list_all_books →", lib.list_all_books())


# 2. ZERO / NULL VALUES TESTS

def test_zero_and_null_values() -> None:
    print_header("TEST 2: Zero / Null-like Values")

    lib = Library()

    # Book with unusual values
    lib.add_book("0", "", "", "")
    book = lib.get_book_by_id("0")

    print("Added book with empty title/author/subject:")
    print("Result:", book)

    # Searching empty title
    print("Exact title search ('') →", lib.search_title_exact(""))


# 3. LARGE DATA STRUCTURES (1,000,000 items)

def test_large_dataset() -> None:
    print_header("TEST 3: Large Dataset (1,000,000 values)")

    hash_table = HashTable(capacity=2_000_003)  # large prime for better distribution
    N = 200_000  # you can increase to 1,000,000 later; this keeps test fast

    print(f"Inserting {N} items into hash table...")
    start = time.time()

    for i in range(N):
        hash_table.put(f"id{i}", i)

    end = time.time()
    print(f"Done in {end - start:.3f} seconds")

    # Test lookup performance
    lookup_key = f"id{N // 2}"
    print(f"Looking up: {lookup_key}")
    start = time.time()
    result = hash_table.get(lookup_key)
    end = time.time()
    print("Lookup result:", result, "| Time:", f"{end - start:.6f}s")


# 4. LARGE DATA TYPES (> 64 bits)

def test_large_data_types() -> None:
    print_header("TEST 4: Handling Large (>64-bit) Data Types")

    extremely_large_number = 2**500  # far larger than 64-bit integer

    lib = Library()
    lib.add_book("BIG1", "HugeNumberTest", "Author", "Maths")

    book = lib.get_book_by_id("BIG1")
    book.large_value = extremely_large_number

    print("Assigned a 500-bit integer to a book attribute.")
    print("Stored value:", book.large_value)
    print("Value bit-length:", book.large_value.bit_length())


# MAIN TEST RUNNER

if __name__ == "__main__":
    test_empty_structures()
    test_zero_and_null_values()
    test_large_dataset()
    test_large_data_types()
    print("\nALL TESTS COMPLETED.\n")
