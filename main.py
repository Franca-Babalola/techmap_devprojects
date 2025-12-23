# Write your code here and merge with main branch 
import xml.etree.ElementTree as ET

# Load and parse the XML file
tree = ET.parse("sample.xml")
root = tree.getroot()

# Print root element
print("Root tag:", root.tag)

# Loop through elements
for employee in root.findall("employee"):
    emp_id = employee.get("id")
    name = employee.find("name").text
    department = employee.find("department").text
    salary = employee.find("salary").text

    print(f"ID: {emp_id}, Name: {name}, Department: {department}, Salary: {salary}")


# Parse Excel Using Pandas

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
