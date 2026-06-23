import csv

with open("C:/Users/jaide/Downloads/nc_water_quality.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

print(f"Loaded {len(rows)} rows")

cleaned = []

for row in rows:
    utility = row[0]
    contaminant = row[1].replace("*", "").strip()
    raw_level= row[2]
    raw_guideline = row[3]
    times_above = row[4].strip()

    level_text = raw_level.replace("This Utility: ", "")

    legal_limit = ""
    if "No Legal Limit" in level_text:
        level_text = level_text.replace("No Legal Limit", "")
        legal_limit = "No Legal Limit"
    elif "Proposed Legal Limit:" in level_text:
        parts = level_text.split("Proposed Legal Limit:")
        level_text = parts[0]
        legal_limit = "Proposed: " + parts[1].strip()
    elif "Legal Limit:" in level_text:
        parts = level_text.split("Legal Limit:")
        level_text = parts[0]
        legal_limit = parts[1].strip()
    
    level_text = level_text.strip()
    level_value = ""
    level_unit = ""
    if level_text:
        pieces = level_text.split(" ")
        if len(pieces) >= 2:
            level_value = pieces[0]
            level_unit = pieces[1]
        else:
            level_value = pieces[0]

    guideline_text = raw_guideline.strip()
    guideline_value = ""
    guideline_unit = ""

    if guideline_text == "No EWG Health Guideline":
        guideline_value = ""
        guideline_unit = ""
    else:
        guideline_text = guideline_text.replace("EWG's Health Guideline: ", "")
        pieces = guideline_text.split(" ")
        if len(pieces) >= 2:
            guideline_value = pieces[0]
            guideline_unit = pieces[1]
        else:
            guideline_value = pieces[0]
    
    cleaned.append([
        utility,
        contaminant,
        level_value,
        level_unit,
        legal_limit,
        guideline_value,
        guideline_unit,
        times_above
    ])

with open("C:/Users/jaide/Downloads/nc_water_quality_clean.csv", "w", newline="", encoding="utf-8") as f:
    writer =csv.writer(f)
    writer.writerow(["Utility", "Contaminant", "Level", "Unit", "Legal Limit", "EWG Guideline", "Guideline Unit", "Time Above"])
    writer.writerows(cleaned)

print(f"Done. {len(cleaned)} clean rows saved to nc_water_quality_clean.csv")


