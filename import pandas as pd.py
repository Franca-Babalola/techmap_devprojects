import pandas as pd

# -------------------------------------------------
# 1. Load DataStage Job Inventory Excel
# -------------------------------------------------
excel_file = "Comprehensive_DataStage_Job_Inventory.xlsx"
df = pd.read_excel(excel_file, sheet_name="DataStage Job Inventory")

# -------------------------------------------------
# 2. Effort Roll-ups
# -------------------------------------------------
effort_by_wave = (
    df.groupby("Migration Wave")["Estimated Effort (Days)"]
    .sum()
    .reset_index()
)

effort_by_platform = (
    df.groupby("Target Platform (IDMC/AWS)")["Estimated Effort (Days)"]
    .sum()
    .reset_index()
)

effort_by_readiness = (
    df.groupby("Migration Readiness")["Estimated Effort (Days)"]
    .sum()
    .reset_index()
)

# -------------------------------------------------
# 3. Generate Jira Subtasks (Bulk Upload)
# -------------------------------------------------
jira_subtasks = []

for _, row in df.iterrows():
    jira_subtasks.append({
        "Issue Type": "Sub-task",
        "Summary": f"Migrate DataStage Job - {row['Job Name']}",
        "Description": (
            f"Job Type: {row['Job Type']}\n"
            f"Source: {row['Source System']} → Target: {row['Target System']}\n"
            f"Complexity: {row['Complexity']}\n"
            f"Migration Platform: {row['Target Platform (IDMC/AWS)']}"
        ),
        "Migration Wave": row["Migration Wave"],
        "Estimated Effort (Days)": row["Estimated Effort (Days)"],
        "Risk Level": row["Risk Level"]
    })

jira_df = pd.DataFrame(jira_subtasks)
jira_df.to_csv("Jira_Subtasks_From_DataStage_Inventory.csv", index=False)

# -------------------------------------------------
# 4. Generate Management Summary Report
# -------------------------------------------------
summary_report = f"""
DataStage Migration – Assessment Summary
=======================================

Total Jobs Assessed: {len(df)}
Total Migration Effort (Days): {df['Estimated Effort (Days)'].sum()}

--- Effort by Migration Wave ---
{effort_by_wave.to_string(index=False)}

--- Effort by Target Platform ---
{effort_by_platform.to_string(index=False)}

--- Effort by Migration Readiness ---
{effort_by_readiness.to_string(index=False)}

Key Observations:
- High complexity jobs are primarily Fact Loads
- AWS-target jobs require higher redesign effort
- IDMC jobs are mostly migration-ready
"""

with open("DataStage_Migration_Executive_Summary.txt", "w") as f:
    f.write(summary_report)

# -------------------------------------------------
# 5. Generate Confluence-ready Table
# -------------------------------------------------
columns = df.columns.tolist()

confluence_table = "| " + " | ".join(columns) + " |\n"
confluence_table += "| " + " | ".join(["---"] * len(columns)) + " |\n"

for _, row in df.iterrows():
    confluence_table += "| " + " | ".join(str(row[col]) for col in columns) + " |\n"

with open("Confluence_DataStage_Job_Inventory_Table.txt", "w") as f:
    f.write(confluence_table)

print("✔ DataStage migration artifacts generated successfully.")
