from contextlib import redirect_stdout
from datetime import date
from io import StringIO
from unittest.mock import patch

from catalogue import check_price, check_text, check_year, load_records, save_records
from cleaning import remove_duplicates, standardise_person, standardise_records, standardise_title
from main import import_records
from searching import filter_records, search_records, show_records, shorten
from summaries import build_summary, summary_lines, write_summary

TEST_DATA = "test_dataset.csv"
EMPTY_DATA = "test_dataset_empty.csv"
EVIDENCE_FILE = "testing_evidence.md"

RESULTS = []

FAULTS = [
    (
        "The first version of `clean_records()` in main.py opened books.csv for writing and "
        "wrote an empty string to it. Cleaning destroyed the catalogue instead of cleaning it. "
        "Cleaning now works on the list in memory and returns the fixed list; the file is only "
        "written when you export."
    ),
    (
        "books.csv contained rows with only 3 or 4 values (price and genre were missing), so "
        "those rows could not be loaded. The missing values were filled in by hand, and "
        "load_records() now reports the line number and what it found instead of crashing."
    ),
    (
        "The original get_str_field() ran .strip().lower().title() on everything the user typed. "
        "str.title() turns \"it's\" into \"It'S\" and \"the day of the triffids\" into "
        "\"The Day Of The Triffids\", and it also mangles initials such as j.r.r. "
        "Replaced with standardise_title() and standardise_person(), which go through the words "
        "one by one: short words such as \"of\" and \"the\" stay lowercase in the middle of a "
        "title, and initials such as \"j.r.r.\" become \"J.R.R.\"."
    ),
    (
        "The exported CSV wrote prices as 15.0 instead of 15.00, because a float drops the "
        "trailing zero. Fixed in save_records() by formatting the price to 2 decimal places "
        "before it is written, and covered by the test \"Export prices with 2 decimal places\"."
    ),
]


def check(operation, test_input, expected, actual):
    expected = str(expected)
    actual = str(actual)
    outcome = "Pass" if expected == actual else "Fail"
    RESULTS.append([operation, test_input, expected, actual, outcome])


def error_from(function, *args):
    try:
        function(*args)
    except ValueError as error:
        return str(error)
    return "no error raised"


def capture(function, *args):
    buffer = StringIO()
    with redirect_stdout(buffer):
        function(*args)
    return buffer.getvalue().strip()


def titles(records):
    return ", ".join(record["title"] for record in records)


def counts(pairs):
    return ", ".join(f"{name}: {count}" for name, count in pairs)


def add_one_record():
    records = [
        {
            "title": check_text("  The Hobbit  ", "title"),
            "author": check_text("J.R.R. Tolkien", "author"),
            "year": check_year("1937"),
            "price": check_price("14.99"),
            "genre": check_text("Fantasy", "genre"),
        }
    ]
    return f"{len(records)} record in the list"


def run_validation_tests():
    check(
        "Add a valid record",
        "The Hobbit / J.R.R. Tolkien / 1937 / 14.99 / Fantasy",
        "1 record in the list",
        add_one_record(),
    )
    check(
        "Reject an empty value",
        'title: ""',
        "title can't be empty",
        error_from(check_text, "   ", "title"),
    )
    check(
        "Reject a value that is too long",
        'title: 61 letters',
        "title can't be longer than 60 characters",
        error_from(check_text, "a" * 61, "title"),
    )
    check(
        "Reject a year that is not a number",
        "year: twenty",
        "year must be a whole number, for example 1998",
        error_from(check_year, "twenty"),
    )
    check(
        "Reject a year before 1450",
        "year: 1200",
        f"year must be between 1450 and {date.today().year}",
        error_from(check_year, "1200"),
    )
    check(
        "Reject a year in the future",
        "year: 3000",
        f"year must be between 1450 and {date.today().year}",
        error_from(check_year, "3000"),
    )
    check(
        "Reject a price that is not a number",
        "price: abc",
        "price must be a number, for example 12.99",
        error_from(check_price, "abc"),
    )
    check(
        "Reject a negative price",
        "price: -4.00",
        "price can't be negative",
        error_from(check_price, "-4.00"),
    )
    check(
        "Reject a price with 3 decimal places",
        "price: 12.999",
        "price can't have more than 2 decimal places",
        error_from(check_price, "12.999"),
    )
    check("Accept a valid price", "price: 12.99", "12.99", check_price("12.99"))


def run_import_tests():
    records, problems = load_records(TEST_DATA)
    check(
        "Import the shared test dataset",
        "test_dataset.csv",
        "10 records loaded, 5 rows skipped",
        f"{len(records)} records loaded, {len(problems)} rows skipped",
    )
    check(
        "Report a row with missing values",
        "test_dataset.csv line 16 (3 values instead of 5)",
        "line 16: found 3 values, need 5",
        problems[4],
    )
    check(
        "Report a row with a bad year",
        "test_dataset.csv line 13 (year: twenty)",
        "line 13: year must be a whole number, for example 1998",
        problems[1],
    )
    try:
        load_records("does_not_exist.csv")
    except FileNotFoundError:
        missing = "FileNotFoundError"
    else:
        missing = "no error raised"
    check(
        "Import a file that does not exist",
        "does_not_exist.csv",
        "FileNotFoundError",
        missing,
    )
    with patch("builtins.input", return_value="notes.txt"):
        message = capture(import_records, [])
    check(
        "Import a file that is not a CSV",
        "notes.txt",
        "Only .csv files can be imported",
        message,
    )
    return records


def run_cleaning_tests(records):
    check(
        "Remove spaces and fix capitalisation in a title",
        '"  the   great gatsby "',
        "The Great Gatsby",
        standardise_title("  the   great gatsby "),
    )
    check(
        "Keep short words lowercase in the middle of a title",
        '"the day of the triffids"',
        "The Day of the Triffids",
        standardise_title("the day of the triffids"),
    )
    check(
        "Keep an apostrophe in a title",
        '"it\'s a good book"',
        "It's a Good Book",
        standardise_title("it's a good book"),
    )
    check(
        "Fix initials in an author name",
        '"j.r.r. tolkien"',
        "J.R.R. Tolkien",
        standardise_person("j.r.r. tolkien"),
    )
    check(
        "Fix capitalisation in an author name",
        '"f. scott fitzgerald"',
        "F. Scott Fitzgerald",
        standardise_person("f. scott fitzgerald"),
    )
    cleaned, changes = standardise_records(records)
    check(
        "Clean the whole shared dataset",
        "10 records from test_dataset.csv",
        "11 fields changed",
        f"{len(changes)} fields changed",
    )
    check(
        "Show what was changed",
        "first change reported",
        'record 2: title "the   great gatsby" is now "The Great Gatsby"',
        changes[0],
    )
    return cleaned, changes


def run_duplicate_tests(cleaned):
    unique, removed = remove_duplicates(cleaned)
    check(
        "Remove duplicate records",
        "10 cleaned records",
        "8 records kept, 2 duplicates removed",
        f"{len(unique)} records kept, {len(removed)} duplicates removed",
    )
    check(
        "Which records were removed",
        "10 cleaned records",
        "The Great Gatsby, The Hobbit",
        titles(removed),
    )
    check(
        "Keep the first record of a duplicate pair",
        "The Great Gatsby (1925)",
        "1 record kept",
        f"{sum(1 for record in unique if record['title'] == 'The Great Gatsby')} record kept",
    )
    return unique


def run_search_tests(records):
    matches = search_records(records, "orwell")
    check(
        "Search with several matches",
        'keyword: "orwell"',
        "2 records: 1984, Animal Farm",
        f"{len(matches)} records: {titles(matches)}",
    )
    matches = search_records(records, "science fiction")
    check(
        "Search in the genre field",
        'keyword: "science fiction"',
        "3 records: 1984, Animal Farm, Dune",
        f"{len(matches)} records: {titles(matches)}",
    )
    check(
        "Search with no matches",
        'keyword: "zebra"',
        'No records match "zebra". Try a different word or value.',
        capture(show_records, search_records(records, "zebra"), "zebra"),
    )
    matches = filter_records(records, "genre", "science fiction")
    check(
        "Filter on a field, case-insensitive",
        "genre = science fiction",
        "3 records: 1984, Animal Farm, Dune",
        f"{len(matches)} records: {titles(matches)}",
    )
    matches = filter_records(records, "author", "jane austen")
    check(
        "Filter on author",
        "author = jane austen",
        "2 records: Emma, Sense and Sensibility",
        f"{len(matches)} records: {titles(matches)}",
    )
    matches = filter_records(records, "price", "8.99")
    check(
        "Filter on a number",
        "price = 8.99",
        "2 records: 1984, Sense and Sensibility",
        f"{len(matches)} records: {titles(matches)}",
    )
    matches = filter_records(records, "genre", "poetry")
    check(
        "Filter with no matches",
        "genre = poetry",
        'No records match "genre = poetry". Try a different word or value.',
        capture(show_records, matches, "genre = poetry"),
    )
    check(
        "Shorten a long title for the table",
        'shorten("The Hitchhiker\'s Guide to the Galaxy", 20)',
        "The Hitchhiker's Gui...",
        shorten("The Hitchhiker's Guide to the Galaxy", 20),
    )
    check(
        "Leave a short title alone",
        'shorten("Dune", 20)',
        "Dune",
        shorten("Dune", 20),
    )


def run_summary_tests(records):
    summary = build_summary(records)
    check("Count the records", "10 records after import, 8 after cleaning", "8", summary["total"])
    check(
        "Count the unique genres",
        "8 cleaned records",
        "4 (Classic, Fantasy, Romance, Science Fiction)",
        f"{len(summary['unique_genres'])} ({', '.join(sorted(summary['unique_genres']))})",
    )
    check(
        "Count records per genre",
        "8 cleaned records",
        "Science Fiction: 3, Classic: 2, Romance: 2, Fantasy: 1",
        counts(summary["genres"]),
    )
    check(
        "Count records per author",
        "8 cleaned records",
        "George Orwell: 2, Jane Austen: 2, F. Scott Fitzgerald: 1, Frank Herbert: 1, "
        "Harper Lee: 1, J.R.R. Tolkien: 1",
        counts(summary["authors"]),
    )
    years = summary["year"]
    check(
        "Summarise the years",
        "1811, 1815, 1925, 1937, 1945, 1949, 1960, 1965",
        "lowest 1811, highest 1965, average 1913.4",
        f"lowest {years['lowest']}, highest {years['highest']}, average {years['average']:.1f}",
    )
    prices = summary["price"]
    check(
        "Summarise the prices",
        "12.99, 10.50, 8.99, 7.25, 14.99, 11.50, 9.99, 8.99",
        "lowest 7.25, highest 14.99, average 10.65, total 85.20",
        f"lowest {prices['lowest']:.2f}, highest {prices['highest']:.2f}, "
        f"average {prices['average']:.2f}, total {prices['total']:.2f}",
    )
    lines = summary_lines(summary)
    check(
        "Print the summary",
        "8 cleaned records",
        "first line: Total records: 8",
        f"first line: {lines[0]}",
    )


def run_empty_tests():
    records, problems = load_records(EMPTY_DATA)
    check(
        "Load a dataset with no records",
        "test_dataset_empty.csv (header row only)",
        "0 records, 0 rows skipped",
        f"{len(records)} records, {len(problems)} rows skipped",
    )
    check(
        "Summarise an empty collection",
        "empty list",
        "There are no records to summarise.",
        "\n".join(summary_lines(build_summary(records))),
    )
    check(
        "Search an empty collection",
        "empty list, keyword anything",
        'No records match "anything". Try a different word or value.',
        capture(show_records, search_records(records, "anything"), "anything"),
    )
    check(
        "Filter an empty collection",
        "empty list, genre = Classic",
        'No records match "genre = Classic". Try a different word or value.',
        capture(show_records, filter_records(records, "genre", "Classic"), "genre = Classic"),
    )


def run_export_tests(records):
    save_records(records, "exports/test_records.csv")
    with open("exports/test_records.csv", encoding="utf-8") as file:
        lines = file.read().splitlines()
    check(
        "Export records to a CSV file",
        "exports/test_records.csv",
        "9 lines: header plus 8 records",
        f"{len(lines)} lines: header plus {len(lines) - 1} records",
    )
    prices = [line.split(",")[3] for line in lines[1:]]
    with_two_decimals = all(len(price.split(".")[-1]) == 2 for price in prices)
    check(
        "Export prices with 2 decimal places",
        "prices such as 10.5 and 15.0",
        "every price written with 2 decimal places",
        "every price written with 2 decimal places" if with_two_decimals else str(prices),
    )
    reloaded, reloaded_problems = load_records("exports/test_records.csv")
    check(
        "Import the exported file again",
        "exports/test_records.csv",
        "8 records, 0 rows skipped",
        f"{len(reloaded)} records, {len(reloaded_problems)} rows skipped",
    )
    write_summary(records, "exports/test_summary.txt")
    with open("exports/test_summary.txt", encoding="utf-8") as file:
        summary_file = file.read().splitlines()
    check(
        "Export the summary to a text file",
        "exports/test_summary.txt",
        "first line: Total records: 8",
        f"first line: {summary_file[0]}",
    )


def clean_cell(text):
    return str(text).replace("|", "\\|").replace("\n", "<br>")


def write_evidence():
    passed = sum(1 for row in RESULTS if row[4] == "Pass")
    lines = [
        "# Testing evidence",
        "",
        "Every test runs against the shared test dataset in `test_dataset.csv`.",
        "The table was written by `run_tests.py`, so the actual result column is what the code "
        "really did when the tests were run.",
        "",
        f"Tests passed: {passed} out of {len(RESULTS)}.",
        "",
        "| Operation | Test input | Expected result | Actual result | Pass/fail |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in RESULTS:
        lines.append("| " + " | ".join(clean_cell(cell) for cell in row) + " |")
    lines += ["", "## Faults found and corrections", ""]
    for fault in FAULTS:
        lines += [fault, ""]
    with open(EVIDENCE_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    return passed


def main():
    run_validation_tests()
    records = run_import_tests()
    cleaned, changes = run_cleaning_tests(records)
    unique = run_duplicate_tests(cleaned)
    run_search_tests(unique)
    run_summary_tests(unique)
    run_empty_tests()
    run_export_tests(unique)
    passed = write_evidence()
    print(f"{passed} out of {len(RESULTS)} tests passed. Evidence written to {EVIDENCE_FILE}")
    for row in RESULTS:
        if row[4] == "Fail":
            print(f"FAIL: {row[0]}")
            print(f"  expected: {row[2]}")
            print(f"  actual:   {row[3]}")


if __name__ == "__main__":
    main()
