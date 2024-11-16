import numpy as np
import time

def load_data():
    traindata = np.genfromtxt('train.csv', delimiter=',')[1:, 1:]
    income_data = traindata[:, -1]
    return income_data

income_data = load_data()
income_sum = 0
for num in income_data:
    income_sum += num

income_percent = income_sum / len(income_data)

print(income_data)
print()
print(f"Number of rows: {len(income_data)}, Points with income: {income_sum}")
print(f"Percent >50k: {income_percent}")

