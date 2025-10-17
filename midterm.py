def main_menu():
    while True:
        print("\n=== Main Menu ===")
        print("1. Add item")
        print("2. View items")
        print("3. Delete item")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")


stores = ["Alice's Bakery", "Bob's Breakfasts", "Charlie's Cafe", "Desayuno de David","Eddie's Eatery"]


def view_items():
    if not stores:
        print("No items found.")
    else:
        print("\nItems:")
        for i, store in enumerate(stores, 1):
            print(f"{i}. {store}")



if __name__ == "__main__":
    main_menu()
