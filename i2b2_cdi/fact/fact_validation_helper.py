from loguru import logger
from i2b2_cdi.common.utils import parse_date
import hashlib

def validate_header(columns):
    columns = [c.replace('-','').replace('_','').replace(' ','').lower() for c in columns]
    headers = columns
    missingColumns = []
    
    if 'mrn' not in headers:
        missingColumns.append('mrn')

    if 'startdate' not in headers:
        missingColumns.append('start-date')

    if 'code' not in headers:
        missingColumns.append('code')

    return missingColumns


def validate_fact_row(row, patient_map, concept_map, config, code_type_lookup):
    if not row['mrn']:
        return 'MRN is Missing'
    else:
        if len(row['mrn'])>200:
            return 'Length of MRN >200 '
        else:
            salt = config.mrn_hash_salt
            mrnSalt = salt + str(row['mrn'])

            hashedMrn = hashlib.sha512(mrnSalt.encode('utf-8')).hexdigest()
            patient_num = patient_map.get(hashedMrn)
            if patient_num is None:
               return 'Patient mapping not found'
            else:
                row['mrn'] = patient_num
                
    if not row['startdate']:
        return "start-date is Missing"
    else:
        parsed_date = parse_date(row['startdate'])
        if parsed_date is None:
            return "Invalid start date format"
        else:
            row['startdate'] = parsed_date

    if not row['code']:
        return "concept_code is missing"
    else:
        if len(row['code'])>50:
           return 'Length of code >50'
        else:
            if not config.disable_fact_validation and row['code'] not in concept_map:
                return "Concept code doesn't exists for fact"
    
    ctype = code_type_lookup.get(row['code'])

    if ctype=='integer':
        try:
            value = int(row["value"])
        except Exception as e:
            return "Invalid value for "+ row["code"] +" Code of type "+ ctype.capitalize()

    if ctype=='float':
        try:
            value = float(row["value"])
        except Exception as e:
            return "Invalid value for "+ row["code"] +" Code of type "+ ctype.capitalize()

    
    if (ctype=="assertion"):
        if type(row["value"]) is str:
            if len(row["value"]) !=0:
                return "Invalid value for "+ row["code"] +" Code of type "+ ctype.capitalize() +". Value of Assertion should be blank."
        
    if (ctype=="string"):
        if type(row["value"]) is str:
            if len(row["value"]) >255:
                return "Invalid value for code "+ row["code"] +". Concept type of "+ row["code"] +" must be largestring."      
    


def initialize_defaults(columns,row,encounter_map):
    
    if 'encounterid' not in columns or not row['encounterid']:
        row['encounterid'] = 0
    else:
        if len(row['encounterid'])>200:
            return 'Length of encounterId >200'
        else:
            encounter_num = encounter_map.get(row['encounterid'])
            if encounter_num is None:
                return 'Encounter mapping not found'

    if 'providerid' not in columns or not row['providerid']:
        row['providerid'] = 0
    else:
        if len(row['providerid'])>50:
            return 'Length of providerId >50'
    
    if 'modifiercd' not in columns or not row['modifiercd']:
        row['modifiercd'] = '@'
    else:
        if len(row['modifiercd'])>100:
            return 'Length of encounterId >100'

    if 'instancenum' not in columns or not row['instancenum']:
        row['instancenum'] = 1
    
    if 'value' not in columns:
        row['value'] = ''
    
    if 'unitcd' not in columns:
        row['unitcd'] = ''
    else:
        if len(row['unitcd'])>50:
            return 'Length of unitcd >50'