import pandas as pd



df = pd.read_csv('TSLA.csv',parse_dates = True, index_col=0)

value = df['Adj Close'].shift(-1)
value1 = df['Adj Close']

print(value1)
print(value)
