import pandas as pd
import numpy as np
import mlxtend as ml
from bfassociationrules import assocRules


def main_menu():
    keepgoing = "y"
    storeChoice = ""
    dbfile = ""
    stores = ["Alice's Bakery", "Bob's Breakfast", "Charlie's Cafe", "Desayuno de David","Eddie's Eatery"]
    supportValue,confidenceValue=0,0
    while keepgoing =="y":
        print("\n==================Welcome to the Midterm Baking District==============")
        print("Please Select a Store")
        for i, store in enumerate(stores, 1):
                print(f"{i}. {store}")
        choice = input("Enter your choice (1-5): ")
        
        while storeChoice=="":
            if choice == "1":
                storeChoice="Alice's Bakery"
                dbfile='alicebakery001.csv'
            elif choice == "2":
                storeChoice="Bob's Breakfast"
                dbfile='bobsbreakfast001.csv'
            elif choice == "3":
                storeChoice="Charlie's Cafe"
                dbfile='charliescafe001.csv'
            elif choice == "4":
                storeChoice="Desayuno de David"
                dbfile='desayunodedavid001.csv'
            elif choice == "5":
                storeChoice="Eddie's Eatery"
                dbfile='eddieseats001.csv'
                break
            else:
                print("Invalid choice. Please choose a number 1-5.")

        print("Welcome to "+storeChoice+"!")

        # input validation
        while True:
            sV=input("Please enter the minimum support %% you want (0-100): ")
            try:
                supportValue = (int(sV))/100
            except ValueError:
                print("Please input a numeric value")
                continue
            if 0.0<=supportValue<=1.00:
                break
            else:
                print("Invalid selection")


        while True:
            cV=input("Please enter the minimum support %% you want (0-100): ")
            try:
                confidenceValue = (int(cV))/100
            except ValueError:
                print("Please input a numeric value")
                continue
            if 0.0<=confidenceValue<=1.0:
                break
            else:
                print("Invalid selection")

        transactions= pd.read_csv(dbfile,usecols=["ItemsPurchased"])

        transactions_set = transactions['ItemsPurchased'].apply(lambda x: set(item.strip() for item in x.split(','))).tolist()

        unique_items = set().union(*transactions_set)

        print("=================================Results=============================")
        print("Support {} %".format(supportValue*100))
        print("Confidence {} %".format(confidenceValue*100))

        if supportValue!=0:
            bfrules=assocRules(unique_items,transactions_set,supportValue,confidenceValue)
            print("==================================Rules==============================")
            i=1
            for (a,b,c) in bfrules:
                print(f"Rule {i}: {a} ===> {b} \t Confidence :{c}")
                print('\n')
                i+=1
        if supportValue==0:
            print("At 0%/ support I have to look at possible menu pairing as a rule even if it happens only once. So in other words you're trying to waste my time so here is the whole ist of transactions.")
            print(transactions)

        if len(bfrules)==0:
            print("There are no rules that saitisfy these minimum values")
        print("=====================================================================")
        print("\n")
        choice =""
        choice = input("Do you want to try another store or settings? (y/n)")
        choice=choice.lower()
        while choice != "y" and choice!="n" :
            choice = input("Please enter y or n:\n")
            choice=choice.lower()
        keepgoing=choice
    print("Thank You!")

            
           

        


    
'''
 te = TransactionEncoder()
 te_array = te.fit(transactions).transform(transactions)
 df_encoded = pd.DataFrame(te_array, columns=te.columns_)
 frequent_items = apriori(df_encoded, min_support=s upportValue, use_colnames=True)
 aRules = association_rules(frequent_items, metric="confidence", min_threshold=confidenceValue)
 rules = rules[rules['antecedents'].apply(lambda x: len(x) >= 1) & rules['consequents'].apply(lambda x: len(x) >= 1)]




 treeRes=fpgrowth(df, min_support=supportValue)
 fpRules = association_rules(frequent_itemsets, metric='confidence', min_threshold=confidenceValue)


'''
 


    






if __name__ == "__main__":
    main_menu()
