# #!/bin/bash
 
facts_file="diabetes_facts.csv"
mrn_start=10001
mrn_end=11000
 
unique_codes=$(awk -F "," 'NR>1 {print $2}' "$facts_file" | sort | uniq | grep -v -E "positive|negative")
echo "mrn,code,start_date,value"
for (( mrn=mrn_start; mrn<=mrn_end; mrn++ )); do
  # Iterate through each unique code for the patient
  while read -r code; do
    # Extract all rows with the selected code and randomly choose a start date and value
    start_date=$(awk -F "," -v selected_code="$code" 'NR>1 && $2 == selected_code {print $3}' "$facts_file" | shuf -n 1)
    value=$(awk -F "," -v selected_code="$code" 'NR>1 && $2 == selected_code {print $4}' "$facts_file" | shuf -n 1)
 
    # Output the new record in the same format: mrn,code,start_date,value
    echo "$mrn,$code,$start_date,$value"
  done <<< "$unique_codes"
done

value=""
code="target"
start_date="2024-03-03"
for (( mrn=mrn_start; mrn<=mrn_end; mrn++ )); do
  echo "$mrn,$code,$start_date,$value"
done