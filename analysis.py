import csv

with open("C:/Users/jaide/Downloads/nc_water_quality_clean.csv", "r", encoding = "utf=8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Loaded {len(rows)} records")

utilities = {}
for row in rows:
    name = row["Utility"]
    if name not in utilities:
        utilities[name] = []
    utilities[name].append(row)


above_guideline = {}
for name, records in utilities.items():
    count = 0
    for r in records:
        if r["Time Above"] and r["Time Above"] != "":
            count += 1
    above_guideline[name] = count

# Sorting most contaminants above guidelines first
worst_by_count = sorted(above_guideline.items(), key=lambda x: x[1], reverse=True)

# Looking for the highest Times Above values across all data
extreme_violations = []
for row in rows:
    ta = row["Time Above"].replace(",","").replace("x", "").strip()
    if ta:
        try:
            val = float(ta)
            extreme_violations.append({
                "utility": row["Utility"],
                "contaminant": row["Contaminant"],
                "level": row["Level"],
                "unit": row["Unit"],
                "times_above": val
            })
        except ValueError:
            pass

extreme_violations.sort(key=lambda x: x["times_above"], reverse=True)

# Find PFAS analysis and utilities with PFOS and PFOA
pfas_data = []
for row in rows:
    contam = row["Contaminant"].lower()
    if "pfos" in contam or "pfoa" in contam or "pfas" in contam or "genx" in contam:
        ta = row["Time Above"].replace(",", "").replace("x", "").strip()
        if ta:
            try:
                pfas_data.append({
                    "utility": row["Utility"],
                    "contaminant": row["Contaminant"],
                    "level": row["Level"],
                    "unit": row["Unit"],
                    "times_above": float(ta)
                })
            except ValueError:
                pass

pfas_data.sort(key=lambda x: x["times_above"], reverse=True)

# Cleanest utilities
cleanest = sorted(above_guideline.items(), key=lambda x: x[1])

# Looking for Fayetteville's rank
fay_count = above_guideline.get("Fayetteville Public Works Commission", 0)
fay_rank = 1
for name, count in worst_by_count:
    if count > fay_count:
        fay_rank += 1
    else:
        break

# Most common contaminants
contam_frequency = {}
for row in rows:
    contam = row["Contaminant"]
    utility = row["Utility"]
    if contam not in contam_frequency:
        contam_frequency[contam] = set()
    contam_frequency[contam].add(utility)

most_common = sorted(contam_frequency.items(), key=lambda x: len(x[1]), reverse=True)

# Generating the markdown report

report = []
report.append("# NC Water Quality Analysis Report")
report.append("")
report.append(f"**Data source:** EWG Tap Water Database")
report.append(f"**Utilities analyzed:** {len(utilities)}")
report.append(f"**Total contaminant records:** {len(rows)}")
report.append("")

# Most contaminated utilities
report.append("## Most Contaminated Utilities")
report.append("")
report.append("Ranked by number of contaminants exceeding EWG health guidelines:")
report.append("")
report.append("| Rank | Utility | Contaminants Above EWG Guideline |")
report.append("|------|---------|----------------------------------|")
for i, (name, count) in enumerate(worst_by_count[:20]):
    report.append(f"| {i+1} | {name} | {count} |")
report.append("")

# extreme violations
report.append("## Most Extreme Violations")
report.append("")
report.append("Contaminants found at the highest multiples above EWG health guidelines")
report.append("")
report.append("| Utility | Contaminant | Level | Time Above Guideline |")
report.append("|---------|-------------|-------|-----------------------|")
for v in extreme_violations[:20]:
    report.append(f"| {v['utility']} | {v['contaminant']} | {v['level']} {v['unit']} | {v['times_above']}x |")
report.append("")

# PFAS
report.append("## PFAS Contamination (PFOS, PFOA, GenX)")
report.append("")
report.append("PFAS are persistent chemicals linked to cancer, immune system damage, and developmental issues.")
report.append("")
report.append("| Utility | Chemical | Level | Time Above Guideline |")
report.append("|---------|----------|-------|-----------------------|")
for p in pfas_data[:20]:
    report.append(f"| {p['utility']} | {p['contaminant']} | {p['level']} {p['unit']} | {p['times_above']}x |")
report.append("")

# Fayetteville Ranked
report.append("## Fayetteville Spotlight")
report.append("")
report.append(f"Fayetteville Public Works Commission ranks **#{fay_rank}** out of {len(utilities)} utilities")
report.append(f"with **{fay_count}** contaminants exceeding EWG health guidelines.")
report.append("")
fay_records = utilities.get("Fayetteville Public Works Commission", [])
fay_above = []
for r in fay_records:
    ta = r["Time Above"].replace(",", "").replace("x", "").strip()
    if ta:
        try:
            fay_above.append({"contaminant": r["Contaminant"], "level": r["Level"], "unit": r["Unit"], "times": float(ta)})
        except ValueError:
            pass
fay_above.sort(key=lambda x: x["times"], reverse=True)
report.append("| Contaminant | Level | Time Above Guideline |")
report.append("|-------------|-------|-----------------------|")
for f in fay_above[:10]:
    report.append(f"| {f['contaminant']} | {f['level']} {f['unit']} | {f['times']}x |")
report.append("")

# Cleanest Utilities
report.append("## Cleanest Utilities")
report.append("")
report.append("Utilities with the fewest contaminants above EWG guidelines:")
report.append("")
report.append("| Rank | Utility | Contaminants Above EWG Guideline |")
report.append("|------|---------|---------------------------------|")
for i, (name, count) in enumerate(cleanest[:10]):
    report.append(f"| {i+1} | {name} | {count} |")
report.append("")

# Most common contaminants
report.append("## Most Widespread Contaminants")
report.append("")
report.append("Contaminants found in the most NC utilities:")
report.append("")
report.append("| Contaminant | Found In (utilities) |")
report.append("|-------------|----------------------|")
for contam, utils in most_common[:15]:
    report.append(f"| {contam} | {len(utils)} |")
report.append("")
report.append("---")
report.append("*Report generated by nc-water-quality-scraper | Data from EWG Tap Water Database*")


# Save the report
with open("C:/Users/jaide/Downloads/nc_water_quality_report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print(f"Report saved to nc_water_quality_report.md")