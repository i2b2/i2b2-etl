from loguru import logger
import csv
import glob

def get_type(value):
    if(value==None or value==''): 
        return('assertion')
    else:      
        try:
            if(value.isdigit()):
                return('integer')
        except Exception as  e:
                pass
        try:
            if(float(value)):
                return('float')             
        except Exception as e:
            if(len(value)<=255): #TVAL_CHAR
                return ('string')             
            else:
                return ('largestring') #OBSERVATION_BLOB

def determine_concept_type(args):     
    code2type={}
    try:
        fact_files = glob.glob(args.fact_file_dir+'/*facts.csv')      
        for file_name in fact_files:
            with open(file_name) as file:
                csv_file = csv.reader(file)
                header_line=next(csv_file)
                header_line=[header.lower() for header in header_line]
                code_index=header_line.index("code")
                value_index=header_line.index("value")

                for row in csv_file:
                    if row[code_index] not in code2type.keys():
                        code2type[row[code_index]]=get_type(row[value_index])
    
        filePath=args.fact_file_dir+"/concepts_type.csv"
        with open(filePath, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['code','type'])
            for key, value in code2type.items():
                writer.writerow([key, value])

    except Exception as e:
        logger.exception(e)


 
