import pandas as pd
import numpy as np
import mlxtend as ml


#used to create the item lists of k items
def itemLists (items, k):

    ilists = []


    def backtrack(start, current):
        if len(current) == k:
            ilists.append(current[:])
            return
        for i in range(start, len(items)):
            current.append(items[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return ilists



def assocRules(dataTable,support_Val, confidence_Val):
    rules = []
    supported = True
    k=1
    items =[]   #fill 
    current_set = {}
    while supported:
        kSets = {}
        itemSets = itemLists(items,k)
        for s in itemSets:
            count =0
            for row in dataTable:
                if s.issubset(row):
                    count+=1
            if count/len(dataTable) >= support_Val:
                kSets.add(s)
        if len(kSets) == 0:
            supported = False
        current_set.union(kSets)
        k+=1


