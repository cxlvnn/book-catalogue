SHORT_WORDS = {"a", "an", "the", "of", "in", "on", "at", "to", "and", "but", "or", "for", "with", "from", "by"}


def squeeze_spaces(text):
    return " ".join(text.split())


def standardise_title(text):
    words = squeeze_spaces(text).split(" ")
    fixed = []
    for index, word in enumerate(words):
        lowered = word.lower()
        if index not in (0, len(words) - 1) and lowered in SHORT_WORDS:
            fixed.append(lowered)
        else:
            fixed.append(word.capitalize())
    return " ".join(fixed)


def standardise_person(text):
    words = squeeze_spaces(text).split(" ")
    fixed = []
    for word in words:
        letters = word.replace(".", "")
        if "." in word and letters.isalpha() and len(letters) <= 4:
            fixed.append(word.upper())
        else:
            fixed.append(word.capitalize())
    return " ".join(fixed)


def standardise_records(records):
    cleaned = []
    changes = []
    for number, record in enumerate(records, start=1):
        new_record = {
            "title": standardise_title(record["title"]),
            "author": standardise_person(record["author"]),
            "year": record["year"],
            "price": record["price"],
            "genre": standardise_title(record["genre"]),
        }
        for field in ("title", "author", "genre"):
            if new_record[field] != record[field]:
                changes.append(f'record {number}: {field} "{record[field]}" is now "{new_record[field]}"')
        cleaned.append(new_record)
    return cleaned, changes


def record_key(record):
    return (record["title"].casefold(), record["author"].casefold(), record["year"])


def remove_duplicates(records):
    unique = []
    removed = []
    seen = set()
    for record in records:
        key = record_key(record)
        if key in seen:
            removed.append(record)
        else:
            seen.add(key)
            unique.append(record)
    return unique, removed
