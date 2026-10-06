from csv import DictWriter


def add_record():
    title = input("Enter book title: ").strip().lower().title()
    author = input("Enter book author: ").strip().lower().title()
    print(f"{title} - {author} .")

    headers = ["title", "author"]
    data = {"title": title, "author": author}

    with open("books.csv", "a", newline="") as f:
        dict_writer = DictWriter(f, fieldnames=headers)
        dict_writer.writerow(data)


menu_msg = """
===== Book catalogue =====
1. Add records
2. Clean records
3. Search records
4. Show summary
5. Export results
6. Exit
"""

while True:
    print(menu_msg)
    choice = input(": ")

    match choice:
        case "1":
            add_record()
        case "2":
            print("clean")
        case "3":
            print("search")
        case "4":
            print("show")
        case "5":
            print("export")
        case "6":
            break
        case _:
            print("Make sure you entered a valid input")
