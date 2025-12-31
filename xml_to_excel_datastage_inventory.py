import xml.etree.ElementTree as ET
import pandas as pd

# -----------------------------
# INPUT / OUTPUT FILES
# -----------------------------
XML_FILE = "DataStage_Job_Inventory.xml"
EXCEL_FILE = "Parsed_DataStage_Job_Inventory.xlsx"

# -----------------------------
# PARSE XML
# -----------------------------
tree = ET.parse(XML_FILE)
root = tree.getroot()

records = []

for job in root.findall("Job"):
    records.append({
        "Job ID": job.findtext("JobID"),
        "Job Name": job.findtext("JobName"),
        "Job Type": job.findtext("JobType"),
        "Category": job.findtext("Category"),

        "Source System": job.find("Source/System").text if job.find("Source/System") is not None else "",
        "Source Type": job.find("Source/Type").text if job.find("Source/Type") is not None else "",

        "Target System": job.find("Target/System").text if job.find("Target/System") is not None else "",
        "Target Type": job.find("Target/Type").text if job.find("Target/Type") is not None else "",

        "Transformations Used": job.find("TechnicalDetails/Transformations").text if job.find("TechnicalDetails/Transformations") is not None else "",
        "Stages Used": job.find("TechnicalDetails/StagesUsed").text if job.find("TechnicalDetails/StagesUsed") is not None else "",
        "Reusable Components": job.find("TechnicalDetails/ReusableComponents").text if job.find("TechnicalDetails/ReusableComponents") is not None else "",
        "Error Handling": job.find("TechnicalDetails/ErrorHandling").text if job.find("TechnicalDetails/ErrorHandling") is not None else "",

        "Dependencies": job.find("Operations/Dependencies").text if job.find("Operations/Dependencies") is not None else "",
        "Scheduling Tool": job.find("Operations/SchedulingTool").text if job.find("Operations/SchedulingTool") is not None else "",
        "Frequency": job.find("Operations/Frequency").text if job.find("Operations/Frequency") is not None else "",
        "Avg Runtime (mins)": job.find("Operations/AverageRuntimeMinutes").text if job.find("Operations/AverageRuntimeMinutes") is not None else "",
        "Data Volume": job.find("Operations/DataVolume").text if job.find("Operations/DataVolume") is not None else "",

        "Target Platform": job.find("Migration/TargetPlatform").text if job.find("Migration/TargetPlatform") is not None else "",
        "Migration Readiness": job.find("Migration/Readiness").text if job.find("Migration/Readiness") is not None else "",
        "Estimated Effort (Days)": job.find("Migration/EstimatedEffortDays").text if job.find("Migration/EstimatedEffortDays") is not None else "",
        "Migration Wave": job.find("Migration/MigrationWave").text if job.find("Migration/MigrationWave") is not None else "",
        "Risk Level": job.find("Migration/RiskLevel").text if job.find("Migration/RiskLevel") is not None else "",

        "Remarks": job.findtext("Remarks")
    })

# -----------------------------
# WRITE TO EXCEL
# -----------------------------
df = pd.DataFrame(records)
df.to_excel(EXCEL_FILE, index=False, sheet_name="DataStage Job Inventory")

print("✅ Excel file generated successfully")
print(f"📄 Output file: {EXCEL_FILE}")
