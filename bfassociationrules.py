import pandas as pd
import numpy as np
import mlxtend as ml


#used to create the item lists of k items
def createKItemsets (items, k):
    itemSets = []
    def backtrack(start, current):
        if len(current) == k:
            itemSets.append(current[:])
            return
        for i in range(start, len(items)):
            current.append(items[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return itemSets



def assocRules(items,dataTable,support_Val, confidence_Val):
    rules = []
    supported = True
    k=1
    current_set = {}
    while supported:
        kSets = {}
        itemSets = createKItemsets(items,k)
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

    rule_preview= {i:[] for i in items}

    for i in items:
        for cSet in current_set:
            if i in cSet:
                rule_preview[i].append(cSet - {i})

    rule_tracker = {s : 0 for s in createKItemsets(items,2)}

    for {a,b} in rule_tracker.keys():
        for s in rule_preview[a]:
            if b in s:
                rule_tracker[(a,b)] +=1

    for (a,b), count in rule_tracker.items():
        confidence = count / len(rule_preview[a])
        if confidence >= confidence_Val:
            rules.append((a,b,confidence))
    return rules


