import math
import csv

class DecisionNode:
    def __init__(self, attribute=None, threshold=None, value=None, class_label=None):
        self.attribute = attribute
        self.threshold = threshold
        self.children = {}
        self.value = value
        self.class_label = class_label

def entropy(data):
    labels = {}
    for record in data:
        label = record[-1]
        if label not in labels:
            labels[label] = 0
        labels[label] += 1
    total = len(data)
    entropy = 0
    for label in labels:
        probability = labels[label] / total
        entropy -= probability * math.log2(probability)
    return entropy

def gain(data, attribute):
    values = {}
    for record in data:
        value = record[attribute]
        if value not in values:
            values[value] = []
        values[value].append(record)
    total = len(data)
    remainder = 0
    for value in values:
        probability = len(values[value]) / total
        remainder += probability * entropy(values[value])
    return entropy(data) - remainder, remainder, entropy(data)

def j48(data, attributes, attributes_labels=None):
    labels = set([record[-1] for record in data])
    if len(labels) == 1:
        leaf = DecisionNode(None)
        leaf.class_label = labels.pop()
        return leaf
    if not attributes:
        leaf = DecisionNode(None)
        leaf.class_label = max(set([record[-1] for record in data]), key=[record[-1] for record in data].count)
        return leaf
    best_attribute = max(attributes, key=lambda attribute: gain(data, attribute)[0])
    node = DecisionNode(best_attribute)
    values = set([record[best_attribute] for record in data])
    print("Atributo \t Entropia \t Remainder \t Ganancia")
    for att in attributes:
        gain_temp = gain(data, att)
        if attributes_labels[att] == "moroso":
            print(attributes_labels[att], "\t\t", round(gain_temp[2], 2), "\t \t", round(gain_temp[1], 2), "\t \t", round(gain_temp[0], 2))
        else:
            print(attributes_labels[att], "\t", round(gain_temp[2], 2), "\t \t", round(gain_temp[1], 2), "\t \t", round(gain_temp[0], 2))
    print("\n")
    print("Best attribute: ", attributes_labels[best_attribute])
    print(values)
    print("====================================")
    for value in values:
        subset = [record for record in data if record[best_attribute] == value]
        if not subset:
            leaf = DecisionNode(None)
            leaf.class_label = max(set([record[-1] for record in data]), key=[record[-1] for record in data].count)
            node.children[value] = leaf
        else:
            new_attributes = [attribute for attribute in attributes if attribute != best_attribute]
            node.children[value] = j48(subset, new_attributes, attributes_labels=attributes_labels)
    return node

with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

    attributes = data[0]
    data = data[1:]

    root = j48(data, list(range(len(attributes) - 1)), attributes_labels=attributes[:-1])

    #test_data = [
    #    ["M","High","Single"],
    #    ["F","Low","Married"],
    #    ["M","Medium","Single"],
    #    ["F","Low","Single"],
    #    ["M","High","Married"],
    #    ["F","High","Married"],
    #    ["F","Medium","Single"],
    #    ["M","Low","Married"],
    #    ["F", "Low", "Married"],
    #    ["M", "Medium", "Married"],
    #    ["F", "Medium", "Single"],
    #    ["M", "Low", "Married"],
    #    ["M", "Low", "Single"],
    #]
    #
    #for record in test_data:
    #    node = root
    #    while node.class_label is None:
    #        value = record[node.attribute]
    #        node = node.children[value]
    #    if (not node.class_label):
    #        print(node.attribute)
    #    else:
    #        print(node.class_label)





    
