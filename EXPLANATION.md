# Data structure choices and AI collaboration

## Why each collection type is used

**List — the records, and every result.**
All the records live in one list, in the order they came from the file. Cleaning, searching
and duplicate removal all hand back a list, so the user sees the records in a stable order.
A list keeps duplicates and the original order, which is what a catalogue needs: order
matters for reading, and only the duplicate rule is allowed to drop a record.

**Dictionary — one record, and the frequency counts.**
Each record is `{"title": ..., "author": ..., "year": ..., "price": ..., "genre": ...}`.
Named fields mean the code reads as `record["year"]` instead of `record[2]`, a wrong or
missing field is caught by name, and adding a field later does not change every position in
the code. Dictionaries also carry the counts: the summary builds `{"Science Fiction": 3}`
style maps, then sorts them into pairs for display.

**Set — uniqueness.**
Two jobs. In `remove_duplicates()` a `seen` set holds the key of every record already kept,
so the duplicate test is just `key in seen`, and a set cannot hold the same key twice. In
the summary, `{record["genre"] for record in records}` gives the unique genres, because a
set throws repeats away by design. A list would have to be searched by hand to do the same
job.

**Tuple — fixed groups of values.**
The duplicate key is `(title.casefold(), author.casefold(), year)`: three values that belong
together and never change, so a tuple is a natural fit and it can go straight into a set.
Sorted counts also arrive as tuples from `dict.items()`, so each summary line is a pair such
as `("Science Fiction", 3)` waiting to be printed.

**String methods and slicing — cleaning, checking and presenting.**
Cleaning uses `strip()`, `split()`, `join()`, `capitalize()` and `casefold()`. The results
table shortens long titles with `text[:limit] + "..."` so rows line up. The import check
looks at the last four characters, `path.lower()[-4:]`, to reject files that are not CSV.
`casefold()` makes searches case insensitive without changing the stored record.

## AI collaboration record

**Tools used**

1. **ChatGPT** — used at the start, for planning only: choosing a context for the project
   (a book catalogue out of the suggested list) and sketching the broad shape (a menu, CSV
   storage, cleaning, search, summary, export). It is not used any more for this project.
2. **Google searches** — used while writing the first version of `main.py` to look up
   Python details, for example how to append a dictionary to a CSV with `csv.DictWriter`
   and how `match` statements work.
3. **OpenCode (Big Pickle model)** — used for this version: reading the existing code,
   writing the modules, the test dataset, the test runner and these documents, and debugging.

**Prompts and what I did with the answers**

| Prompt | What came back | What I accepted, changed or rejected |
| --- | --- | --- |
| Asked ChatGPT to suggest a suitable context for a records project and the broad shape of it | Book catalogue with a menu over a CSV file | Accepted the context and the menu/CSV shape. Rejected its sample code and wrote my own version |
| Told the AI to look through the folder first, keep the good parts of my `main.py`, drop the bad ones, no comments, plain English, and to ask before deciding anything | It read `main.py`, `books.csv` and the git history, then proposed 5 modules, 5 fields and a duplicate rule | Accepted the module split and the duplicate rule (title + author + year after cleaning). Changed the field list by adding `genre`, because the brief needs categories and frequency counts |
| Asked which fields a record should have | title, author, year, price, genre | Accepted. The original 4 fields stay, genre was added |
| Asked how the testing evidence table should be produced | A script that writes the table with the real actual results | Accepted. Nothing in the table is typed by hand |
| Asked whether price should be whole numbers or money | Decimal money such as 12.99 | Accepted |
| Asked about the demo recording | It cannot record video, offered a written demo script | Changed: recording left for later, code first |
| Told it the earlier `clean_records()` behaviour and my writing habits | It pointed out that the old function wrote an empty string over `books.csv`, and that `str.title()` turns `it's` into `It'S` | Accepted both. Cleaning now works in memory, and capitalisation is done word by word |

**How I checked the work**

The expected results in `testing_evidence.md` were written down before the tests were run,
so they come from working the answers out by hand, not from copying what the code printed.
`run_tests.py` then prints the actual result next to them. I also ran the menu end to end
with a script of keystrokes (import, clean, remove duplicates, search, filter, summary,
export) and re-imported the exported file to confirm the export round trip works.
49 out of 49 checks pass. The faults found on the way are listed under
"Faults found and corrections" in `testing_evidence.md`.
