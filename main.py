# Write your code here and merge with main branch 
import pandas as pd

# Read Excel file
df = pd.read_excel("employees.xlsx")

# Show first rows
print(df.head())

# Access columns
print(df["Name"])

# Iterate through rows
for index, row in df.iterrows():
    print(row["ID"], row["Name"], row["Department"], row["Salary"])
