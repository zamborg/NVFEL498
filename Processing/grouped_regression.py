import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv('../../../Data/Processed/ICE_trips/alltrips.csv')
print(df)
num_trips = len(df)
split1 = num_trips * 7 // 10
split2 = split1 + num_trips * 3 // 20

pke = df['Aggressiveness']
pf = df['Aggressivity']
fuel = df['Fuel Economy[mpg]']

idx = pke.isna() | pf.isna() | fuel.isna() | np.isinf(pke) | np.isinf(pf) | np.isinf(fuel)
print('any true', idx.any())
pke = pke[~idx]
pf = pf[~idx]
fuel = fuel[~idx]

print(pke[pke.isna()])
print(pf[pf.isna()])
print(fuel[fuel.isna()])

print(sum(pke))
print(sum(pf))
print(sum(fuel))

X_train = np.array(pke[:split1]).reshape(-1, 1)
X_val = np.array(pke[split1:split2]).reshape(-1, 1)
X_test = np.array(pke[split2:]).reshape(-1, 1)

y_train = np.array(fuel[:split1]).reshape(-1, 1)
y_val = np.array(fuel[split1:split2]).reshape(-1, 1)
y_test = np.array(fuel[split2:]).reshape(-1, 1)

reg = LinearRegression().fit(X_train, y_train)

train_score = reg.score(X_train, y_train)
val_score = reg.score(X_val, y_val)

y_pred = reg.predict(X_val)

print('Train Scores')
print(f'PKE: {train_score}')
print('Val Scores')
print(f'PKE: {val_score}')

plt.scatter(X_val, y_val, color='black')
plt.plot(X_val, y_pred, color='blue', linewidth=3)

plt.xticks((np.arange(0, 500000, 100000)))
plt.yticks((np.arange(0, 65, 5)))
plt.xlabel('PKE Aggressiveness Score (unitless)')
plt.ylabel('Fuel Economy[mpg]')
plt.title('Preliminary Regression on PKE Aggressiveness Score')

plt.savefig('grouped_regression.png')

