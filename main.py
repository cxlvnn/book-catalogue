from os import makedirs
from os.path import dirname

from catalogue import FIELD_NAMES, check_price, check_text, check_year, load_records, save_records
from cleaning import remove_duplicates, standardise_records
from searching import filter_records, search_records, show_records
from summaries import build_summary, summary_lines, write_summary

DATA_FILE = "books.csv"

MENU = """
===== Book catalogue =====
1. Add a record
2. Import records from a file
3. Clean and standardise records
4. Remove duplicates
5. Search records
6. Filter by field
7. Show summary
8. Export records
9. Export summary
0. Exit
"""


def ask(prompt):
    return input(f"{prompt}: ").strip()


def save_now(records):
    save_records(records, DATA_FILE)
    print(f"Saved {len(records)} records to {DATA_FILE}")


def get_str_field(prompt, field_name):
    while True:
        try:
            return check_text(input(f"{prompt}: "), field_name)
        except ValueError as error:
            print(error)


def get_year_field(prompt):
    while True:
        try:
            return check_year(input(f"{prompt}: "))
        except ValueError as error:
            print(error)


def get_price_field(prompt):
    while True:
        try:
            return check_price(input(f"{prompt}: "))
        except ValueError as error:
            print(error)


def add_record(records):
    record = {
        "title": get_str_field("Enter book title", "title"),
        "author": get_str_field("Enter book author", "author"),
        "year": get_year_field("Enter the year in which it was written"),
        "price": get_price_field("Enter the book price"),
        "genre": get_str_field("Enter the book genre", "genre"),
    }
    records.append(record)
    print(
        f'Added "{record["title"]}" by {record["author"]}, {record["year"]}, '
        f'{record["price"]:.2f}, {record["genre"]}'
    )
    save_now(records)


def import_records(records):
    path = ask("Path of the file to import")
    if path.lower()[-4:] != ".csv":
        print("Only .csv files can be imported")
        return
    try:
        new_records, problems = load_records(path)
    except FileNotFoundError:
        print(f'Can\'t find "{path}"')
        return
    records.extend(new_records)
    print(f"Imported {len(new_records)} records from {path}")
    if problems:
        print(f"Skipped {len(problems)} rows:")
        for problem in problems:
            print(f"  {problem}")
    if new_records:
        save_now(records)


def clean_records(records):
    cleaned, changes = standardise_records(records)
    if not changes:
        print("Nothing to clean. Every field is already standardised.")
        return records
    print(f"Fixed {len(changes)} fields:")
    for change in changes:
        print(f"  {change}")
    save_now(cleaned)
    return cleaned


def deduplicate(records):
    unique, removed = remove_duplicates(records)
    if not removed:
        print("No duplicates found.")
        return records
    print(f"Removed {len(removed)} duplicate records:")
    for record in removed:
        print(f'  "{record["title"]}" by {record["author"]} ({record["year"]})')
    save_now(unique)
    return unique


def search(records):
    keyword = ask("Keyword to search for in title, author or genre")
    if keyword == "":
        print("Type a word to search for.")
        return
    show_records(search_records(records, keyword), keyword)


def filter_by_field(records):
    print("Fields: " + ", ".join(FIELD_NAMES))
    field = ask("Field to filter on").lower()
    if field not in FIELD_NAMES:
        print("That field doesn't exist.")
        return
    value = ask(f"Value to match in {field}")
    if value == "":
        print("Type a value to match.")
        return
    show_records(filter_records(records, field, value), f"{field} = {value}")


def show_summary(records):
    for line in summary_lines(build_summary(records)):
        print(line)


def export_records(records):
    path = ask("File to save records to, press enter for exports/records.csv")
    if path == "":
        path = "exports/records.csv"
    make_folder(path)
    save_records(records, path)
    print(f"Saved {len(records)} records to {path}")


def export_summary(records):
    path = ask("File to save the summary to, press enter for exports/summary.txt")
    if path == "":
        path = "exports/summary.txt"
    make_folder(path)
    write_summary(records, path)
    print(f"Saved the summary to {path}")


def make_folder(path):
    folder = dirname(path)
    if folder:
        makedirs(folder, exist_ok=True)


def load_starting_records():
    try:
        records, problems = load_records(DATA_FILE)
    except FileNotFoundError:
        print(f"No {DATA_FILE} found. Starting with an empty catalogue.")
        return []
    print(f"Loaded {len(records)} records from {DATA_FILE}")
    for problem in problems:
        print(f"  {problem}")
    if not records:
        print("The catalogue is empty. Use option 2 to import a file.")
    return records


def main():
    records = load_starting_records()
    while True:
        print(MENU)
        choice = ask("Choose an option")
        match choice:
            case "1":
                add_record(records)
            case "2":
                import_records(records)
            case "3":
                records = clean_records(records)
            case "4":
                records = deduplicate(records)
            case "5":
                search(records)
            case "6":
                filter_by_field(records)
            case "7":
                show_summary(records)
            case "8":
                export_records(records)
            case "9":
                export_summary(records)
            case "0":
                break
            case _:
                print("That's not an option. Pick a number from the menu.")


if __name__ == "__main__":
    main()
