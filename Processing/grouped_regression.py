import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv('../../../Data/Processed/ICE_trips/alltrips_with_weight_and_disp.csv')

X = df[['Aggressiveness', 'Weight', 'Displacement']]
Y = df['Fuel Economy[mpg]']

pke = X['Aggressiveness']
w = X['Weight']
d = X['Displacement']
fuel = Y

idx = pke.isna() | fuel.isna() | w.isna() | d.isna() | np.isinf(pke) | np.isinf(fuel) | np.isinf(w) | np.isinf(d)
print('any true', idx.any())

X = X[~idx]
Y = Y[~idx]

num_trips = len(X)
split1 = num_trips * 7 // 10
split2 = split1 + num_trips * 3 // 20

X_train = np.array(X[:split1]).reshape(-1, 3)
X_val = np.array(X[split1:split2]).reshape(-1, 3)
X_test = np.array(X[split2:]).reshape(-1, 3)

print(X_train.shape)
print(X_val.shape)
y_train = np.array(Y[:split1]).reshape(-1, 1)
y_val = np.array(Y[split1:split2]).reshape(-1, 1)
y_test = np.array(Y[split2:]).reshape(-1, 1)

reg = LinearRegression().fit(X_train, y_train)

train_score = reg.score(X_train, y_train)
val_score = reg.score(X_val, y_val)

y_pred = reg.predict(X_val)

print('Train Scores')
print(f'PKE: {train_score}')
print('Val Scores')
print(f'PKE: {val_score}')

plt.scatter(X_val[:, 0], y_val, color='black')
plt.plot(X_val[:, 0], y_pred, color='blue', linewidth=3)

plt.xticks((np.arange(0, 500000, 100000)))
plt.yticks((np.arange(0, 65, 5)))
plt.xlabel('PKE Aggressiveness Score (unitless)')
plt.ylabel('Fuel Economy[mpg]')
plt.title('Grouped Regression')

plt.savefig('grouped_regression.png')

plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_val[:, 0], X_val[:, 2] / X_val[:, 1], y_val, marker='.', color='red')
ax.set_xlabel('PKE')
ax.set_ylabel('Dispalcement / Weight')
ax.set_zlabel('Fuel Economy[mpg]')

ax.plot_surface(X_val[:, 0], X_val[:, 2] / X_val[:, 1], y_pred)
plt.savefig('grouped_regression_3d.png')
