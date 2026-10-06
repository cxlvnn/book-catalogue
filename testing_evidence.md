# Testing evidence

Every test runs against the shared test dataset in `test_dataset.csv`.
The table was written by `run_tests.py`, so the actual result column is what the code really did when the tests were run.

Tests passed: 49 out of 49.

| Operation | Test input | Expected result | Actual result | Pass/fail |
| --- | --- | --- | --- | --- |
| Add a valid record | The Hobbit / J.R.R. Tolkien / 1937 / 14.99 / Fantasy | 1 record in the list | 1 record in the list | Pass |
| Reject an empty value | title: "" | title can't be empty | title can't be empty | Pass |
| Reject a value that is too long | title: 61 letters | title can't be longer than 60 characters | title can't be longer than 60 characters | Pass |
| Reject a year that is not a number | year: twenty | year must be a whole number, for example 1998 | year must be a whole number, for example 1998 | Pass |
| Reject a year before 1450 | year: 1200 | year must be between 1450 and 2026 | year must be between 1450 and 2026 | Pass |
| Reject a year in the future | year: 3000 | year must be between 1450 and 2026 | year must be between 1450 and 2026 | Pass |
| Reject a price that is not a number | price: abc | price must be a number, for example 12.99 | price must be a number, for example 12.99 | Pass |
| Reject a negative price | price: -4.00 | price can't be negative | price can't be negative | Pass |
| Reject a price with 3 decimal places | price: 12.999 | price can't have more than 2 decimal places | price can't have more than 2 decimal places | Pass |
| Accept a valid price | price: 12.99 | 12.99 | 12.99 | Pass |
| Import the shared test dataset | test_dataset.csv | 10 records loaded, 5 rows skipped | 10 records loaded, 5 rows skipped | Pass |
| Report a row with missing values | test_dataset.csv line 16 (3 values instead of 5) | line 16: found 3 values, need 5 | line 16: found 3 values, need 5 | Pass |
| Report a row with a bad year | test_dataset.csv line 13 (year: twenty) | line 13: year must be a whole number, for example 1998 | line 13: year must be a whole number, for example 1998 | Pass |
| Import a file that does not exist | does_not_exist.csv | FileNotFoundError | FileNotFoundError | Pass |
| Import a file that is not a CSV | notes.txt | Only .csv files can be imported | Only .csv files can be imported | Pass |
| Remove spaces and fix capitalisation in a title | "  the   great gatsby " | The Great Gatsby | The Great Gatsby | Pass |
| Keep short words lowercase in the middle of a title | "the day of the triffids" | The Day of the Triffids | The Day of the Triffids | Pass |
| Keep an apostrophe in a title | "it's a good book" | It's a Good Book | It's a Good Book | Pass |
| Fix initials in an author name | "j.r.r. tolkien" | J.R.R. Tolkien | J.R.R. Tolkien | Pass |
| Fix capitalisation in an author name | "f. scott fitzgerald" | F. Scott Fitzgerald | F. Scott Fitzgerald | Pass |
| Clean the whole shared dataset | 10 records from test_dataset.csv | 11 fields changed | 11 fields changed | Pass |
| Show what was changed | first change reported | record 2: title "the   great gatsby" is now "The Great Gatsby" | record 2: title "the   great gatsby" is now "The Great Gatsby" | Pass |
| Remove duplicate records | 10 cleaned records | 8 records kept, 2 duplicates removed | 8 records kept, 2 duplicates removed | Pass |
| Which records were removed | 10 cleaned records | The Great Gatsby, The Hobbit | The Great Gatsby, The Hobbit | Pass |
| Keep the first record of a duplicate pair | The Great Gatsby (1925) | 1 record kept | 1 record kept | Pass |
| Search with several matches | keyword: "orwell" | 2 records: 1984, Animal Farm | 2 records: 1984, Animal Farm | Pass |
| Search in the genre field | keyword: "science fiction" | 3 records: 1984, Animal Farm, Dune | 3 records: 1984, Animal Farm, Dune | Pass |
| Search with no matches | keyword: "zebra" | No records match "zebra". Try a different word or value. | No records match "zebra". Try a different word or value. | Pass |
| Filter on a field, case-insensitive | genre = science fiction | 3 records: 1984, Animal Farm, Dune | 3 records: 1984, Animal Farm, Dune | Pass |
| Filter on author | author = jane austen | 2 records: Emma, Sense and Sensibility | 2 records: Emma, Sense and Sensibility | Pass |
| Filter on a number | price = 8.99 | 2 records: 1984, Sense and Sensibility | 2 records: 1984, Sense and Sensibility | Pass |
| Filter with no matches | genre = poetry | No records match "genre = poetry". Try a different word or value. | No records match "genre = poetry". Try a different word or value. | Pass |
| Shorten a long title for the table | shorten("The Hitchhiker's Guide to the Galaxy", 20) | The Hitchhiker's Gui... | The Hitchhiker's Gui... | Pass |
| Leave a short title alone | shorten("Dune", 20) | Dune | Dune | Pass |
| Count the records | 10 records after import, 8 after cleaning | 8 | 8 | Pass |
| Count the unique genres | 8 cleaned records | 4 (Classic, Fantasy, Romance, Science Fiction) | 4 (Classic, Fantasy, Romance, Science Fiction) | Pass |
| Count records per genre | 8 cleaned records | Science Fiction: 3, Classic: 2, Romance: 2, Fantasy: 1 | Science Fiction: 3, Classic: 2, Romance: 2, Fantasy: 1 | Pass |
| Count records per author | 8 cleaned records | George Orwell: 2, Jane Austen: 2, F. Scott Fitzgerald: 1, Frank Herbert: 1, Harper Lee: 1, J.R.R. Tolkien: 1 | George Orwell: 2, Jane Austen: 2, F. Scott Fitzgerald: 1, Frank Herbert: 1, Harper Lee: 1, J.R.R. Tolkien: 1 | Pass |
| Summarise the years | 1811, 1815, 1925, 1937, 1945, 1949, 1960, 1965 | lowest 1811, highest 1965, average 1913.4 | lowest 1811, highest 1965, average 1913.4 | Pass |
| Summarise the prices | 12.99, 10.50, 8.99, 7.25, 14.99, 11.50, 9.99, 8.99 | lowest 7.25, highest 14.99, average 10.65, total 85.20 | lowest 7.25, highest 14.99, average 10.65, total 85.20 | Pass |
| Print the summary | 8 cleaned records | first line: Total records: 8 | first line: Total records: 8 | Pass |
| Load a dataset with no records | test_dataset_empty.csv (header row only) | 0 records, 0 rows skipped | 0 records, 0 rows skipped | Pass |
| Summarise an empty collection | empty list | There are no records to summarise. | There are no records to summarise. | Pass |
| Search an empty collection | empty list, keyword anything | No records match "anything". Try a different word or value. | No records match "anything". Try a different word or value. | Pass |
| Filter an empty collection | empty list, genre = Classic | No records match "genre = Classic". Try a different word or value. | No records match "genre = Classic". Try a different word or value. | Pass |
| Export records to a CSV file | exports/test_records.csv | 9 lines: header plus 8 records | 9 lines: header plus 8 records | Pass |
| Export prices with 2 decimal places | prices such as 10.5 and 15.0 | every price written with 2 decimal places | every price written with 2 decimal places | Pass |
| Import the exported file again | exports/test_records.csv | 8 records, 0 rows skipped | 8 records, 0 rows skipped | Pass |
| Export the summary to a text file | exports/test_summary.txt | first line: Total records: 8 | first line: Total records: 8 | Pass |

## Faults found and corrections

The first version of `clean_records()` in main.py opened books.csv for writing and wrote an empty string to it. Cleaning destroyed the catalogue instead of cleaning it. Cleaning now works on the list in memory and returns the fixed list, and books.csv is written after every change (add, import, clean, remove duplicates). Cleaning never opens the file for writing.

books.csv contained rows with only 3 or 4 values (price and genre were missing), so those rows could not be loaded. The missing values were filled in by hand, and load_records() now reports the line number and what it found instead of crashing.

The original get_str_field() ran .strip().lower().title() on everything the user typed. str.title() turns "it's" into "It'S" and "the day of the triffids" into "The Day Of The Triffids", and it also mangles initials such as j.r.r. Replaced with standardise_title() and standardise_person(), which go through the words one by one: short words such as "of" and "the" stay lowercase in the middle of a title, and initials such as "j.r.r." become "J.R.R.".

The exported CSV wrote prices as 15.0 instead of 15.00, because a float drops the trailing zero. Fixed in save_records() by formatting the price to 2 decimal places before it is written, and covered by the test "Export prices with 2 decimal places".
