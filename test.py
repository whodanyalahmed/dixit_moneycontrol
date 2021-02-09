import pandas as pd


name = "ARUNA HOTELS LTD"
nameList = name.split(" ")

for e in reversed(nameList):
    print(name.replace(e," "))