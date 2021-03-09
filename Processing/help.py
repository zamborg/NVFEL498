import pandas as pd

df = pd.read_csv("ICE_trip7636.csv")
print(len(df['Latitude[deg]']))
