from csv import DictWriter, reader
from datetime import date

FIELD_NAMES = ["title", "author", "year", "price", "genre"]
MIN_YEAR = 1450
MAX_TEXT_LENGTH = 60


def check_text(value, field_name):
    text = value.strip()
    if text == "":
        raise ValueError(f"{field_name} can't be empty")
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(f"{field_name} can't be longer than {MAX_TEXT_LENGTH} characters")
    return text


def check_year(value):
    text = value.strip()
    if not text.isdigit():
        raise ValueError("year must be a whole number, for example 1998")
    year = int(text)
    if year < MIN_YEAR or year > date.today().year:
        raise ValueError(f"year must be between {MIN_YEAR} and {date.today().year}")
    return year


def check_price(value):
    text = value.strip()
    if text == "":
        raise ValueError("price can't be empty")
    try:
        price = float(text)
    except ValueError:
        raise ValueError("price must be a number, for example 12.99") from None
    if price < 0:
        raise ValueError("price can't be negative")
    if round(price, 2) != price:
        raise ValueError("price can't have more than 2 decimal places")
    return price


def load_records(path):
    records = []
    problems = []
    with open(path, newline="", encoding="utf-8") as file:
        for line_number, row in enumerate(reader(file), start=1):
            if line_number == 1 and [cell.strip().lower() for cell in row] == FIELD_NAMES:
                continue
            if not row or all(cell.strip() == "" for cell in row):
                continue
            if len(row) != len(FIELD_NAMES):
                problems.append(f"line {line_number}: found {len(row)} values, need {len(FIELD_NAMES)}")
                continue
            values = dict(zip(FIELD_NAMES, row))
            try:
                record = {
                    "title": check_text(values["title"], "title"),
                    "author": check_text(values["author"], "author"),
                    "year": check_year(values["year"]),
                    "price": check_price(values["price"]),
                    "genre": check_text(values["genre"], "genre"),
                }
            except ValueError as error:
                problems.append(f"line {line_number}: {error}")
                continue
            records.append(record)
    return records, problems


def save_records(records, path):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["price"] = f"{record['price']:.2f}"
            writer.writerow(row)
