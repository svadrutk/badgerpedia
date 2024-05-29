# remove id column from thing
import pandas as pd

df = pd.read_csv('grades.csv')
df.drop('id', axis=1, inplace=True)
print(df.head())

# Save the cleaned data to a new CSV file
df.to_csv('grades2.csv', index=False)