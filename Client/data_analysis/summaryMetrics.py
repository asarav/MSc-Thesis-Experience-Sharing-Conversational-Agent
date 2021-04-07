import pandas as pd

data = pd.read_csv("output_files/summary.csv")

print(data["priorEfficacy"].std())
print(data["priorEfficacy"].mean())
print(data["postEfficacy"].std())
print(data["postEfficacy"].mean())

condition1 = data.loc[data['condition'] == 0]
condition2 = data.loc[data['condition'] == 1]
condition3 = data.loc[data['condition'] == 2]

print(condition1.head())
print(condition2.head())
print(condition3.head())