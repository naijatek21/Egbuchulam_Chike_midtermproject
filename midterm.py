import os
import pandas as pd
import numpy as np
import mlxtend as ml
from bfassociationrules import assocRules

def main_menu():
    storeChoice = ""
    dbfile = ""
    stores = [
        "Alice's Bakery",
        "Bob's Breakfast",
        "Charlie's Cafe",
        "Desayuno de David",
        "Eddie's Eatery"
    ]
    
    # 👇 define the folder where your CSVs are stored
    base_dir = os.path.dirname(__file__)               # directory where midterm.py is located
    tables_dir = os.path.join(base_dir, "tables")      # tables subfolder path

    print("\n==================Welcome to the Midterm Baking District==============")
    print("Please Select a Store")
    for i, store in enumerate(stores, 1):
        print(f"{i}. {store}")
    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        storeChoice = "Alice's Bakery"
        dbfile = os.path.join(tables_dir, "alicebakery001.csv")
    elif choice == "2":
        storeChoice = "Bob's Breakfast"
        dbfile = os.path.join(tables_dir, "bobsbreakfast001.csv")
    elif choice == "3":
        storeChoice = "Charlie's Cafe"
        dbfile = os.path.join(tables_dir, "charliescafe001.csv")
    elif choice == "4":
        storeChoice = "Desayuno de David"
        dbfile = os.path.join(tables_dir, "desayunodedavid001.csv")
    elif choice == "5":
        storeChoice = "Eddie's Eatery"
        dbfile = os.path.join(tables_dir, "eddieseats001.csv")
    else:
        print("Invalid choice. Please choose a number 1-5.")
        return

    print(f"Welcome to {storeChoice}!")

    # Input validation for support and confidence
    while True:
        sV = input("Please enter the minimum support % you want (0-100): ")
        try:
            supportValue = int(sV) / 100
        except ValueError:
            print("Please input a numeric value")
            continue
        if 0.0 <= supportValue <= 1.00:
            break
        else:
            print("Invalid selection")

    while True:
        cV = input("Please enter the minimum confidence % you want (0-100): ")
        try:
            confidenceValue = int(cV) / 100
        except ValueError:
            print("Please input a numeric value")
            continue
        if 0.0 <= confidenceValue <= 1.0:
            break
        else:
            print("Invalid selection")

    # ✅ now reads from tables/<filename>.csv
    transactions = pd.read_csv(dbfile, usecols=["ItemsPurchased"])

    transactions_set = transactions['ItemsPurchased'].apply(
        lambda x: set(item.strip() for item in x.split(','))
    ).tolist()

    unique_items = set().union(*transactions_set)

    bfrules = assocRules(unique_items, transactions_set, supportValue, confidenceValue)


if __name__ == "__main__":
    main_menu()
