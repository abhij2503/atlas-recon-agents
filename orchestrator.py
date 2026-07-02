import sys
sys.path.append("agents")

import report_agent
import repo_agent1
import repo_agent2
import repo_agent3
import repo_agent4

print("Running the recon committee...\n")

findings = {}

print("Agent 1 (files) working...")
result = repo_agent1.run()
findings["files"] = {
    "atlas_id": "AML.T0004",
    "atlas_name": "Search Application Repositories",
    "evidence": result["evidence"],
    "finding": result["finding"]
}

print("Agent 2 (bias) working...")
result = repo_agent2.run()
findings["bias"] = {
    "atlas_id": "AML.T0001",
    "atlas_name": "Search Open AI Vulnerability Analysis",        # <-- YOU fill
    "evidence": result["evidence"],
    "finding": result["finding"]
}

print("Agent 3 (owners) working...")
result = repo_agent3.run()
findings["owners"] = {
    "atlas_id": "AML.T0087",          # <-- YOU fill
    "atlas_name": "Gather Victim Identity Information",        # <-- YOU fill
    "evidence": result["evidence"],
    "finding": result["finding"]
}

print("Agent 4 (demos) working...")
result = repo_agent4.run()
findings["demos"] = {
    "atlas_id": "AML.T0003",          # <-- YOU fill
    "atlas_name": "Search Victim-Owned Websites",        # <-- YOU fill
    "evidence": result["evidence"],
    "finding": result["finding"]
}

print("\n=== ALL FINDINGS (ATLAS-mapped) ===\n")
for name, data in findings.items():
    print(f"[{data['atlas_id']}] {data['atlas_name']}")
    print(data["finding"])
    print()
report_agent.write_report(findings)