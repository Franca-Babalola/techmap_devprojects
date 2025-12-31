import xml.etree.ElementTree as ET
import pandas as pd

# Parse XML
tree = ET.parse("DataStage_Job_Inventory.xml")
root = tree.getroot()

rows = []

for job in root.findall("Job"):
    rows.append({
        "Job ID": job.findtext("JobID"),
        "Job Name": job.findtext("JobName"),
        "Job Type": job.findtext("JobType"),
        "Category": job.findtext("Category"),
        "Source System": job.find("Source/System").text,
        "Source Type": job.find("Source/Type").text,
        "Target System": job.find("Target/System").text,
        "Target Type": job.find("Target/Type").text,
        "Transformations Used": job.find("TechnicalDetails/Transformations").text,
        "Stages Used": job.find("TechnicalDetails/StagesUsed").text,
        "Dependencies": job.find("Operations/Dependencies").text,
        "Scheduling Tool": job.find("Operations/SchedulingTool").text,
        "Frequency": job.find("Operations/Frequency").text,
        "Avg Runtime (mins)": job.find("Operations/AverageRuntimeMinutes").text,
        "Data Volume": job.find("Operations/DataVolume").text,
        "Target Platform": job.find("Migration/TargetPlatform").text,
        "Migration Readiness": job.find("Migration/Readiness").text,
        "Estimated Effort (Days)": job.find("Migration/EstimatedEffortDays").text,
        "Migration Wave": job.find("Migration/MigrationWave").text,
        "Risk Level": job.find("Migration/RiskLevel").text,
        "Remarks": job.findtext("Remarks")
    })

# Create Excel
df = pd.DataFrame(rows)
df.to_excel("Parsed_DataStage_Job_Inventory.xlsx", index=False)

print("Excel file created successfully")
