menu_msg = """
===== Book catalogue =====
1. Add/import records
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
            print("add")
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
