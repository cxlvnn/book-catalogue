# Book catalogue CLI

A command line toolkit for a small shop or library that keeps its books in a CSV file.
The records are usually typed in by hand, so they end up with extra spaces, mixed up
capitalisation, repeated entries and values that are missing or wrong. This tool cleans
the records up, finds duplicates, searches and summarises them, and exports the result.

## The records

Each record has five fields:

| Field | What it holds | Rule |
| --- | --- | --- |
| title | book title | not empty, max 60 characters |
| author | writer's name | not empty, max 60 characters |
| year | year it was written | whole number, 1450 up to this year |
| price | price in dollars | number with up to 2 decimals, not negative |
| genre | category, e.g. Science Fiction | not empty, max 60 characters |

Wrong values are never accepted quietly. The program tells you which field is wrong and
what is allowed, then asks again.

## How to run it

You need Python 3.10 or newer (the menu uses a `match` statement). From this folder:

```
python3 main.py
```

The program loads `books.csv` on start. If that file is not there it starts with an
empty catalogue.

## The menu

| Option | What it does |
| --- | --- |
| 1. Add a record | Asks for each field, checks it, adds it and saves `books.csv` |
| 2. Import records from a file | Loads a CSV, shows how many rows were loaded and which rows were skipped and why, then saves `books.csv` |
| 3. Clean and standardise records | Removes extra spaces, fixes capitalisation, prints every field it changed |
| 4. Remove duplicates | Drops repeated records and prints which ones went |
| 5. Search records | Keyword search over title, author and genre (part of the word is enough) |
| 6. Filter by field | Exact match on one field, e.g. `genre = science fiction` (not case sensitive) |
| 7. Show summary | Totals, unique genres, records per genre and per author, year and price figures |
| 8. Export records | Saves the records to a CSV file, default `exports/records.csv` |
| 9. Export summary | Saves the summary to a text file, default `exports/summary.txt` |
| 0. Exit | Leaves the program |

Adding, importing, cleaning and removing duplicates all write the result straight to
`books.csv` and print a line saying how many records were saved, so the file always matches
what you see on screen. Search, filter and summary never change anything. Export is for
saving a copy under a different name or in a different folder.

If a search or filter finds nothing you get:

```
No records match "zebra". Try a different word or value.
```

If you summarise an empty collection you get `There are no records to summarise.` instead
of an error.

## Cleaning rules

Cleaning does three things, and it prints every change it makes:

1. Extra spaces are removed from both ends and runs of spaces inside are squeezed down to
   one, so `  the   great gatsby ` becomes `the great gatsby`.
2. Titles and genres are capitalised word by word. Short words such as `a`, `of`, `the`
   and `and` stay lowercase when they are in the middle of a title, so
   `the day of the triffids` becomes `The Day of the Triffids`.
3. Author names are capitalised word by word too, and initials are kept together, so
   `j.r.r. tolkien` becomes `J.R.R. Tolkien`.

## The duplicate rule

Two records are duplicates when the title, the author and the year are all the same
**after** cleaning, with capitalisation ignored. So these two are the same book:

```
  the   great gatsby , f. scott fitzgerald , 1925
The Great Gatsby,F. Scott Fitzgerald,1925
```

The first record is kept, the later ones are removed, and the ones that were removed are
listed on screen. The price and the genre are not part of the rule, because a book can be
sold at two prices and still be the same book.

## Files

| File | What it is |
| --- | --- |
| `main.py` | the menu and the input questions |
| `catalogue.py` | loading, saving and checking the values |
| `cleaning.py` | cleaning and duplicate removal |
| `searching.py` | search, filter and the results table |
| `summaries.py` | summary figures and the summary export |
| `books.csv` | the catalogue the program starts with |
| `test_dataset.csv` | the shared test dataset |
| `test_dataset_empty.csv` | a dataset with no records, header row only |
| `run_tests.py` | runs every test and writes the evidence table |
| `testing_evidence.md` | the test results table and the faults found |
| `EXPLANATION.md` | why each collection type is used, and the AI use record |
| `exports/` | example exported records and summary |

## The test dataset

`test_dataset.csv` has 15 rows: 10 good records, 2 of which are duplicates of other rows
after cleaning, rows with extra spaces and mixed capitalisation, and 5 rows that must be
rejected (empty title, `twenty` as a year, a negative price, an empty price and a row with
only 3 values). Searching for `orwell` returns several records, `zebra` returns none.

## Running the tests

```
python3 run_tests.py
```

This runs every test against `test_dataset.csv`, prints the number of tests passed and
writes `testing_evidence.md` with the operation, the test input, the expected result, the
actual result and a pass/fail column, plus the faults found and how they were fixed.
