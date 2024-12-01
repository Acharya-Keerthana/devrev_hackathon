import json
import pandas as pd

# Load the JSON file
file_path = 'new_response_data.json'  # Replace with your JSON file path
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract relevant data from the "works" key
works_data = data.get("works", [])

# Prepare a list to store extracted data
extracted_data = []

# Loop through each work item and extract fields
for work in works_data:
    extracted_data.append({
        "Title": work.get("title", ""),
        "Type": work.get("type", ""),
        "Severity": work.get("severity", ""),
        "Created By": work.get("created_by", {}).get("full_name", ""),
        "Created Date": work.get("created_date", ""),
        "Applies To Feature": work.get("applies_to_part", {}).get("name", ""),
        "Stage": work.get("stage", {}).get("name", ""),
        "Needs Response": work.get("needs_response", ""),
        "Body": work.get("body", ""),
    })

# Convert to a Pandas DataFrame for tabular representation
df = pd.DataFrame(extracted_data)

# Save to a CSV file or print
output_path = 'extracted_data.csv'
df.to_csv(output_path, index=False)
print(df)