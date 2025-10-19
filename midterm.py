import os
import pandas as pd
import numpy as np
import mlxtend as ml
from bfassociationrules import assocRules


def main_menu():
    keepgoing = "y"
    dbfile = ""
    stores = ["Alice's Bakery", "Bob's Breakfast", "Charlie's Cafe", "Desayuno de David", "Eddie's Eatery"]
    supportValue, confidenceValue = 0, 0

    # 👇 locate the "tables" folder next to this script
    base_dir = os.path.dirname(__file__)
    tables_dir = os.path.join(base_dir, "tables")

    while keepgoing == "y":
        storeChoice = ""
        print("\n==================Welcome to the Midterm Baking District==============")
        print("Please Select a Store")
        for i, store in enumerate(stores, 1):
            print(f"{i}. {store}")

        while storeChoice == "":
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
                break
            else:
                print("Invalid choice. Please choose a number 1-5.")

        print(f"Welcome to {storeChoice}!")

        # input validation
        while True:
            sV = input("Please enter the minimum support % you want (0-100): ")
            try:
                supportValue = float(sV) / 100
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
                confidenceValue = float(cV) / 100
            except ValueError:
                print("Please input a numeric value")
                continue
            if 0.0 <= confidenceValue <= 1.0:
                break
            else:
                print("Invalid selection")
        print("Support {} %".format(supportValue * 100))
        print("Confidence {} %".format(confidenceValue * 100))
        transactions = pd.read_csv(dbfile, usecols=["ItemsPurchased"])

        transactions_set = transactions["ItemsPurchased"].apply(
            lambda x: set(item.strip() for item in x.split(","))
        ).tolist()

        unique_items = set().union(*transactions_set)


        if supportValue != 0:
            [bfsets,bfrules] = assocRules(unique_items, transactions_set, supportValue, confidenceValue)
            print("=================================Results=============================")
            print(f"Frequent Itemsets:\n {bfsets}")
            print("==================================Rules==============================")
            i = 1
            for (a, b, c) in bfrules:
                print(f"Rule {i}: {a} ===> {b} \t Confidence :{c}")
                print("\n")
                i += 1
        if supportValue == 0:
            print(
                "At 0% support I have to look at possible menu pairing as a rule even if it happens only once. "
                "So in other words, you're trying to waste my time so here is the whole list of transactions."
            )
            # print(transactions)

        if supportValue != 0 and len(bfrules) == 0:
            print("There are no rules that satisfy these minimum values")

        print("=====================================================================")
        print("\n")
        choice = input("Do you want to try another store or settings? (y/n): ").lower()
        while choice not in ("y", "n"):
            choice = input("Please enter y or n:\n").lower()
        keepgoing = choice

    print("Thank You!")


if __name__ == "__main__":
    main_menu()
