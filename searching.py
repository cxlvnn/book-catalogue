def search_records(records, keyword):
    term = keyword.strip().casefold()
    matches = []
    for record in records:
        if (
            term in record["title"].casefold()
            or term in record["author"].casefold()
            or term in record["genre"].casefold()
        ):
            matches.append(record)
    return matches


def filter_records(records, field, value):
    wanted = value.strip().casefold()
    if field == "price":
        try:
            target = float(wanted)
        except ValueError:
            return []
        return [record for record in records if abs(record["price"] - target) < 0.005]
    if field == "year":
        return [record for record in records if str(record["year"]) == wanted]
    return [record for record in records if str(record[field]).casefold() == wanted]


def shorten(text, limit=30):
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def show_records(records, term):
    if not records:
        print(f'No records match "{term}". Try a different word or value.')
        return
    print(f'{len(records)} record(s) match "{term}":')
    print(f"{'#':<4}{'Title':<34}{'Author':<26}{'Year':<6}{'Price':>7}  Genre")
    for number, record in enumerate(records, start=1):
        title = shorten(record["title"], 32)
        author = shorten(record["author"], 24)
        price = f"{record['price']:.2f}"
        print(f"{number:<4}{title:<34}{author:<26}{record['year']:<6}{price:>7}  {record['genre']}")
