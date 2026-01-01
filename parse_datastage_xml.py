import pandas as pd
from lxml import etree
from pathlib import Path

# -----------------------------
# File paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
xml_file = BASE_DIR / "DataStage_Job_Inventory.xml"
excel_file = BASE_DIR / "comprehensive_parsed_Datastage_Inventory.xlsx"

if not xml_file.exists():
    raise FileNotFoundError(f"XML file not found: {xml_file}")

# -----------------------------
# Parse XML
# -----------------------------
tree = etree.parse(str(xml_file))
root = tree.getroot()

# -----------------------------
# Prepare data lists
# -----------------------------
jobs_data = []
stages_data = []
links_data = []
parameters_data = []
sources_targets_data = []

# -----------------------------
# Extract Jobs
# -----------------------------
for project in root.findall("Project"):
    project_name = project.get("projectName")
    environment = project.get("environment")
    platform = project.get("platform")
    source_system = project.get("sourceSystem")

    for job in project.findall("Job"):
        job_dict = {
            "Project": project_name,
            "Environment": environment,
            "Platform": platform,
            "Source System": source_system,
            "Job ID": job.get("jobId"),
            "Job Name": job.get("jobName"),
            "Job Category": job.get("jobCategory"),
            "Job Type": job.get("jobType"),
            "Job Status": job.get("jobStatus"),
            "Job Enabled": job.get("jobEnabled"),
            "Developer": job.get("developer"),
            "Last Modified": job.get("lastModified"),
            "Schedule": job.get("schedule"),
            "Frequency": job.get("frequency"),
            "Criticality": job.get("criticality"),
            "Wave": job.get("wave"),
            "Target Platform": job.get("targetPlatform"),
            "Description": job.findtext("Description", default="")
        }
        jobs_data.append(job_dict)

        # -----------------------------
        # Extract Stages
        # -----------------------------
        for stage in job.findall("Stages/Stage"):
            stages_data.append({
                "Job Name": job.get("jobName"),
                "Stage ID": stage.get("stageId"),
                "Stage Name": stage.get("stageName"),
                "Stage Type": stage.get("stageType"),
                "Stage Category": stage.get("stageCategory"),
                "Technology": stage.get("technology"),
                "Parallelism": stage.get("parallelism")
            })

        # -----------------------------
        # Extract Links
        # -----------------------------
        for link in job.findall("Links/Link"):
            links_data.append({
                "Job Name": job.get("jobName"),
                "Link Name": link.get("linkName"),
                "From Stage": link.get("fromStage"),
                "To Stage": link.get("toStage"),
                "Link Type": link.get("linkType")
            })

        # -----------------------------
        # Extract Parameters
        # -----------------------------
        for param in job.findall("Parameters/Parameter"):
            parameters_data.append({
                "Job Name": job.get("jobName"),
                "Parameter Name": param.get("name"),
                "Type": param.get("type"),
                "Default Value": param.get("defaultValue")
            })

        # -----------------------------
        # Extract Sources
        # -----------------------------
        for source in job.findall("Sources/Source"):
            sources_targets_data.append({
                "Job Name": job.get("jobName"),
                "Role": "Source",
                "System": source.get("system"),
                "Object Name": source.get("objectName"),
                "Object Type": source.get("objectType")
            })

        # -----------------------------
        # Extract Targets
        # -----------------------------
        for target in job.findall("Targets/Target"):
            sources_targets_data.append({
                "Job Name": job.get("jobName"),
                "Role": "Target",
                "System": target.get("system"),
                "Object Name": target.get("objectName"),
                "Object Type": target.get("objectType")
            })

# -----------------------------
# Convert to DataFrames
# -----------------------------
df_jobs = pd.DataFrame(jobs_data)
df_stages = pd.DataFrame(stages_data)
df_links = pd.DataFrame(links_data)
df_parameters = pd.DataFrame(parameters_data)
df_sources_targets = pd.DataFrame(sources_targets_data)

# -----------------------------
# Write to Excel with multiple sheets
# -----------------------------
with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
    df_jobs.to_excel(writer, sheet_name="Jobs", index=False)
    df_stages.to_excel(writer, sheet_name="Stages", index=False)
    df_links.to_excel(writer, sheet_name="Links", index=False)
    df_parameters.to_excel(writer, sheet_name="Parameters", index=False)
    df_sources_targets.to_excel(writer, sheet_name="Sources_Targets", index=False)

print(f"✅ Comprehensive Excel file created: {excel_file}")
