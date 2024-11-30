import pandas as pd
from myapp.models import SafetyReport

# Correct file path to the Excel file
file_path = '/Users/william/Downloads/aspirinAlgo.xlsx'

try:
    # Load the Excel file
    data = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Error: File not found at {file_path}. Please verify the file path.")
    raise

# Iterate over rows and create SafetyReport objects
for _, row in data.iterrows():
    # Replace NaN with None for nullable fields
    SafetyReport.objects.create(
        occur_country=row.get('safetyreport/occurcountry/text') if pd.notna(row.get('safetyreport/occurcountry/text')) else None,
        active_substance=row.get('safetyreport/patient/drug/activesubstance/activesubstancename/text') if pd.notna(row.get('safetyreport/patient/drug/activesubstance/activesubstancename/text')) else None,
        drug_dosage_form=row.get('safetyreport/patient/drug/drugdosageform/text') if pd.notna(row.get('safetyreport/patient/drug/drugdosageform/text')) else None,
        drug_dosage_text=row.get('safetyreport/patient/drug/drugdosagetext/text') if pd.notna(row.get('safetyreport/patient/drug/drugdosagetext/text')) else None,
        drug_indication=row.get('safetyreport/patient/drug/drugindication/text') if pd.notna(row.get('safetyreport/patient/drug/drugindication/text')) else None,
        medicinal_product=row.get('safetyreport/patient/drug/medicinalproduct/text') if pd.notna(row.get('safetyreport/patient/drug/medicinalproduct/text')) else None,
        patient_age=int(row.get('safetyreport/patient/patientonsetage/text')) if pd.notna(row.get('safetyreport/patient/patientonsetage/text')) else None,
        patient_sex=int(row.get('safetyreport/patient/patientsex/text')) if pd.notna(row.get('safetyreport/patient/patientsex/text')) else None,
        reporter_country=row.get('safetyreport/primarysource/reportercountry/text') if pd.notna(row.get('safetyreport/primarysource/reportercountry/text')) else None,
        seriousness_death=int(row.get('safetyreport/seriousnessdeath/text')) if pd.notna(row.get('safetyreport/seriousnessdeath/text')) else None,
        seriousness_disabling=int(row.get('safetyreport/seriousnessdisabling/text')) if pd.notna(row.get('safetyreport/seriousnessdisabling/text')) else None,
    )

print("Data imported successfully!")
