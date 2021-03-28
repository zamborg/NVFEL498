import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv('../../alltrips.csv')


pke = df['Aggressiveness']
weight = df['Weight']
disp = df['Displacement']
fuel = df['Fuel Rate[gpm]']
tmp = df['Fuel Economy[mpg]']

vars = [pke, weight, disp, fuel, tmp]

valid_data = fuel.isna()
for var in vars:
    valid_data = valid_data | var.isna() | np.isinf(var)

valid_data = np.array(~valid_data)

minW = float(input('Enter a minimum weight (in lbs): '))
maxW = float(input('Enter a maximum weight (in lbs): '))
minD = float(input('Enter a minimum displacement (in L): '))
maxD = float(input('Enter a maximum displacement (in L): '))

a = (weight <= maxW)
b = (weight >= minW)
c = (disp <= maxD)
d = (disp >= minD)
grouping = np.array(a & b & c & d)
idx = np.logical_and(valid_data, grouping)

X = pke[idx]
Y = fuel[idx]

num_trips = len(Y)
split1 = num_trips * 7 // 10
split2 = split1 + num_trips * 3 // 20

X_train = np.array(X.iloc[:split1]).reshape(-1, 1)
X_val = np.array(X.iloc[split1:split2]).reshape(-1, 1)
X_test = np.array(X.iloc[split2:]).reshape(-1, 1)


y_train = np.array(Y.iloc[:split1]).reshape(-1, 1)
y_val = np.array(Y.iloc[split1:split2]).reshape(-1, 1)
y_test = np.array(Y.iloc[split2:]).reshape(-1, 1)

reg = LinearRegression().fit(X_train, y_train)

train_score = reg.score(X_train, y_train)
val_score = reg.score(X_val, y_val)

y_pred = reg.predict(X_val)

print(f'Train Score: {train_score}')
print(f'Val Score: {val_score}')

plt.scatter(X_val, y_val, color='black')
plt.plot(X_val, y_pred, color='blue', linewidth=2)

max_x = X.max()
max_y = Y.max()

plt.xticks((np.arange(0, max_x, max_x / 10)))
plt.yticks((np.arange(0, max_y, max_y / 10)))
plt.xlabel('PKE Aggressiveness Score (unitless)')
plt.ylabel('Fuel Rate[gpm]')
plt.title(f'Regression Grouped by {minW} <= Weight <= {maxW} \nand {minD} <= Disp <= {maxD}, R2 = {val_score}')

plt.savefig(f'{minW}<=w<={maxW}, {minD}<=d<={maxD}, r2={val_score}.png')
