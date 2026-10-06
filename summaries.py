def count_values(records, field):
    counts = {}
    for record in records:
        counts[record[field]] = counts.get(record[field], 0) + 1
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))


def build_summary(records):
    if not records:
        return None
    years = [record["year"] for record in records]
    prices = [record["price"] for record in records]
    return {
        "total": len(records),
        "unique_genres": {record["genre"] for record in records},
        "genres": count_values(records, "genre"),
        "authors": count_values(records, "author"),
        "year": {
            "lowest": min(years),
            "highest": max(years),
            "average": sum(years) / len(years),
        },
        "price": {
            "lowest": min(prices),
            "highest": max(prices),
            "average": sum(prices) / len(prices),
            "total": sum(prices),
        },
    }


def summary_lines(summary):
    if summary is None:
        return ["There are no records to summarise."]
    years = summary["year"]
    prices = summary["price"]
    lines = [
        f"Total records: {summary['total']}",
        f"Unique genres: {len(summary['unique_genres'])} ({', '.join(sorted(summary['unique_genres']))})",
        "",
        "Records per genre:",
    ]
    for genre, count in summary["genres"]:
        lines.append(f"  {genre}: {count}")
    lines.append("")
    lines.append("Records per author:")
    for author, count in summary["authors"]:
        lines.append(f"  {author}: {count}")
    lines.append("")
    lines.append(
        f"Year: lowest {years['lowest']}, highest {years['highest']}, average {years['average']:.1f}"
    )
    lines.append(
        f"Price: lowest {prices['lowest']:.2f}, highest {prices['highest']:.2f}, "
        f"average {prices['average']:.2f}, total {prices['total']:.2f}"
    )
    return lines


def write_summary(records, path):
    lines = summary_lines(build_summary(records))
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")
    return len(lines)
