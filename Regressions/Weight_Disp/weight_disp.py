import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv('../../alltrips.csv')


pke = df['Aggressiveness']
weight = df['Weight']
disp = df['Displacement']
fuel = df['Fuel Rate[gpm]']

vars = [pke, weight, disp, fuel, disp/weight]

d = {'pke': pke, 'weight/disp': weight / disp}
X = pd.DataFrame(d)
Y = fuel

idx = fuel.isna()
for var in vars:
    idx |= (var.isna() | np.isinf(var) | var == 0)


idx = np.array(~idx)
X = X[idx]
Y = Y[idx]

d = X['weight/disp']
idx = d.isna()

idx = np.array(~idx)
X = X[idx]
Y = Y[idx]

print(X, Y)

num_trips = len(Y)
split1 = num_trips * 7 // 10
split2 = split1 + num_trips * 3 // 20

X_train = np.array(X.iloc[:split1]).reshape(-1, 2)
X_val = np.array(X.iloc[split1:split2]).reshape(-1, 2)
X_test = np.array(X.iloc[split2:]).reshape(-1, 2)


y_train = np.array(Y.iloc[:split1]).reshape(-1, 1)
y_val = np.array(Y.iloc[split1:split2]).reshape(-1, 1)
y_test = np.array(Y.iloc[split2:]).reshape(-1, 1)

reg = LinearRegression().fit(X_train, y_train)

train_score = reg.score(X_train, y_train)
val_score = reg.score(X_val, y_val)

y_pred = reg.predict(X_val)



print('Train Scores')
print(f'PKE: {train_score}')
print('Val Scores')
print(f'PKE: {val_score}')

p, f = np.meshgrid(X_val[:, 0] , X_val[:, 1])
fig = plt.figure()
ax = fig.gca(projection='3d')

print(X_val[:, 0].reshape(-1).shape)
print(X_val[:, 1].reshape(-1).shape)
print(y_val.reshape(-1).shape)

a = X_val[:, 0].reshape(-1)
b = X_val[:, 1].reshape(-1)
c = y_val.reshape(-1)

ax.scatter(a, b, c, color='black')
surf = ax.plot_surface(p, f, y_pred, cmap=matplotlib.cm.hot)

ax.set_xlabel('PKE')
ax.set_ylabel('Weight/Dsisp Ratio')
ax.set_zlabel('Fuel Rate[GPM]')

plt.title('Regression with PKE and Weight/Disp Ratio')
plt.savefig('weight_disp_3d.png')
plt.clf()

plt.scatter(a, c)
plt.plot(a, y_val, color='blue', linewidth=2)
plt.xlabel('PKE')
plt.ylabel('Fuel Rate')
plt.title('PKE vs Fuel')
plt.savefig('pke_vs_fuel.png')
plt.clf()

plt.scatter(b, c)
plt.plot(b, y_val, color='blue', linewidth=2)
plt.xlabel('Disp/Weight Ratio')
plt.ylabel('Fuel Rate')
plt.title('Disp/Weight vs Fuel')
plt.savefig('weight_disp_vs_fuel.png')
plt.clf()