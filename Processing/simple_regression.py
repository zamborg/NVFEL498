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

X1_train = np.array(pke[:split1]).reshape(-1, 1)
X1_val = np.array(pke[split1:split2]).reshape(-1, 1)
X1_test = np.array(pke[split2:]).reshape(-1, 1)

X2_train = np.array(pf[:split1]).reshape(-1, 1)
X2_val = np.array(pf[split1:split2]).reshape(-1, 1)
X2_test = np.array(pf[split2:]).reshape(-1, 1)

y_train = np.array(fuel[:split1]).reshape(-1, 1)
y_val = np.array(fuel[split1:split2]).reshape(-1, 1)
y_test = np.array(fuel[split2:]).reshape(-1, 1)

reg1 = LinearRegression().fit(X1_train, y_train)
reg2 = LinearRegression().fit(X2_train, y_train)

train1_score = reg1.score(X1_train, y_train)
train2_score = reg2.score(X2_train, y_train)
val1_score = reg1.score(X1_val, y_val)
val2_score = reg2.score(X2_val, y_val)

y1_pred = reg1.predict(X1_val)
y2_pred = reg2.predict(X2_val)

print('Train Scores')
print(f'PKE: {train1_score}\tPF: {train2_score}')
print('Val Scores')
print(f'PKE: {val1_score}\tPF: {val2_score}')

plt.scatter(X1_val, y_val, color='black')
plt.plot(X1_val, y1_pred, color='blue', linewidth=3)

plt.xticks((np.arange(0, 500000, 100000)))
plt.yticks((np.arange(0, 65, 5)))
plt.xlabel('PKE Aggressiveness Score (unitless)')
plt.ylabel('Fuel Economy[mpg]')
plt.title('Preliminary Regression on PKE Aggressiveness Score')

plt.savefig('pke_simplereg.png')

plt.clf()
plt.scatter(X2_val, y_val, color='black')
plt.plot(X2_val, y2_pred, color='blue', linewidth=3)

plt.xticks((np.arange(0, 2000, 200)))
plt.yticks((np.arange(0, 65, 5)))
plt.xlabel('PF Aggressiveness Score (unitless)')
plt.ylabel('Fuel Economy[mpg]')
plt.title('Preliminary Regression on PF Aggressiveness Score')

plt.savefig('pf_simplereg.png')