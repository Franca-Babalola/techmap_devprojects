import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------
XML_FILE = "DataStage_Job_Inventory.xml"
OUTPUT_FILE = "comprehensive_parsed_Datastage_Inventory.xlsx"

# -----------------------------
# Validate input file
# -----------------------------
xml_path = Path(XML_FILE)
if not xml_path.exists():
    raise FileNotFoundError(f"XML file not found: {XML_FILE}")

# -----------------------------
# Parse XML
# -----------------------------
tree = ET.parse(xml_path)
root = tree.getroot()

jobs = []
stages = []
links = []
parameters = []

# -----------------------------
# Extract Data
# -----------------------------
for job in root.findall(".//Job"):
    job_name = job.get("name")
    job_type = job.get("type")

    jobs.append({
        "Job Name": job_name,
        "Job Type": job_type
    })

    for param in job.findall(".//Parameter"):
        parameters.append({
            "Job Name": job_name,
            "Parameter Name": param.get("name"),
            "Default Value": param.get("default")
        })

    for stage in job.findall(".//Stage"):
        stage_name = stage.get("name")
        stage_type = stage.get("type")

        stages.append({
            "Job Name": job_name,
            "Stage Name": stage_name,
            "Stage Type": stage_type
        })

        for link in stage.findall(".//Link"):
            links.append({
                "Job Name": job_name,
                "Stage Name": stage_name,
                "Link Name": link.get("name"),
                "Direction": link.get("direction")
            })

# -----------------------------
# Write to Excel
# -----------------------------
with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    pd.DataFrame(jobs).to_excel(writer, sheet_name="Jobs", index=False)
    pd.DataFrame(stages).to_excel(writer, sheet_name="Stages", index=False)
    pd.DataFrame(links).to_excel(writer, sheet_name="Links", index=False)
    pd.DataFrame(parameters).to_excel(writer, sheet_name="Parameters", index=False)

print("✔ DataStage inventory parsed successfully")
print(f"✔ Output written to {OUTPUT_FILE}")
