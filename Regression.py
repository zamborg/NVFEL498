# lets make our goal dataset:
data = pd.read_csv('./NVFEL498/alltrips_final.csv')
# remeber to do our NAN check:
mask = [~(np.isnan(data.iloc[i,:]).sum()>0) for i in range(len(data))]
data = data.loc[mask]

features = [
    'Aggressiveness',
    'Weight',
    'Displacement',
    'Air Temperature[F]',
    'Precipitation Level[mm]',
    'SpeedAverage',
    'Aggressiveness*SpeedAverage',
    'Aggressiveness*Weight',
    'Aggressiveness*Displacement',
    'Displacement/Weight'
]

def transform_data(data, features, out = 'Fuel Rate[gpm]'):
    d = pd.DataFrame(columns = features)
    
    for f in features:
        if '*' in f:
            f1, f2 = f.split('*')
            d[f] = data[f1] * data[f2]
        elif '/' in f:
            f1, f2 = f.split('/')
            d[f] = data[f1] / data[f2]
        else:
            d[f] = data[f]
            
    return np.array(d), np.array(data[out]), {f:i for i,f in enumerate(features)}

X, y, features = transform_data(data, features)

model = LinearRegression().fit(X,y)

# now lets compute r^2:
# WOW WE have an almost 0 impact on r^2 -- surprising
preds = model.predict(X)
r_2 = 1 - (((y - preds)**2).sum())/((y - y.mean())**2).sum()
print(r_2)

# lets see which value has the highest average impact on our regression:

print('Impact = MEAN * Coef')
for i, vals in enumerate(zip(features.keys(), model.coef_)):
    feature, coef = vals
    print(f"{feature}: {X[:,i].mean()*coef}")
    
# we can actually get the relative percentages here:
print('========= PERCENTAGES =========')

impact = np.array([np.abs(coef * X[:,i].mean()) for i, coef in enumerate(model.coef_)])
for feature, i in zip(features.keys(), (impact*100)/impact.sum()):
    print(f"{feature}: {i}")
