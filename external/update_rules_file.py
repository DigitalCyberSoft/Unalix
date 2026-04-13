import json
import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
submodule_path = os.path.join(script_dir, "clearurls-rules")
submodule_rules = os.path.join(submodule_path, "data.min.json")
rules_path = os.path.join(script_dir, "..", "unalix", "package_data", "rulesets", "data.min.json")

# Update the submodule to latest upstream
print("Updating ClearURLs/Rules submodule...")
subprocess.run(["git", "submodule", "update", "--remote", "external/clearurls-rules"], check=True)

print(f"Reading rules from {submodule_rules}...")

with open(file=submodule_rules, mode="r") as file:
    rules = json.loads(file.read())

print(f"Loaded {len(rules['providers'])} providers")

with open(file=rules_path, mode="w") as file:
    file.write(json.dumps(rules, indent=4))

print(f"Written to {rules_path}")
