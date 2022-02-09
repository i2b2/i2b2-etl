import pandas as pd
import csv
import time
import os
from i2b2_cdi.config.config import Config
from loguru import logger
import random
import time
import datetime
import string
import i2b2_cdi.concept.runner as concept_runner
import i2b2_cdi.fact.runner as fact_runner
from .fact_count import get_fact_records_count
import matplotlib.pyplot as plt

def fact_benchmark(options):
    conceptFactsList = [(concepts,facts) for concepts in options.num_of_concepts for facts in options.num_of_facts]
    for i in range(0,options.times):
        for index,tuple in enumerate(conceptFactsList):
            no_of_concepts = tuple[0]
            no_of_facts = tuple[1]
            run(no_of_concepts,no_of_facts)

    path = '/usr/src/app/tmp/benchmark/fact_benchmark_result.csv'
    generate_plot(path)

def run(num_of_concepts,num_of_facts):
    logger.info('Running fact benchmark for {0} concepts and {1} facts'.format(num_of_concepts,num_of_facts))
    demoType = ['assertion','integer','largestring','string','float']

    conceptArr = []
    factArr = []
    conceptHash = {}
    conceptDict = {}
    patientMrn = []

    benchmarkPath = "/usr/src/app/tmp/benchmark"
    if not os.path.exists(benchmarkPath):
        os.makedirs(benchmarkPath)

    for count in range(1,num_of_concepts+1):
        type = random.choice(demoType)
        code = random.choice(list(string.ascii_lowercase)) + str(count)
        path = get_path(conceptHash,code)
        
        rowList = [type,path,code]
        conceptArr.append(rowList)
        conceptHash[path] = True
    
    conceptCsvHeaders = ['type','path','code']
    conceptFilename = benchmarkPath + "/demo_new_concepts.csv"
    write_csv(conceptFilename,conceptCsvHeaders,conceptArr)

    conceptDf = pd.read_csv(conceptFilename, usecols=["code","type"])
    conceptDict = conceptDf.set_index('code')['type'].to_dict()
    typeDict = { 'integer' : random.randint(10,100),'string' : ''.join(random.choices(string.ascii_lowercase + string.digits, k = 5)),
                 'largestring' : ''.join(random.choices(string.ascii_lowercase + string.digits, k = 15)),'float': round(random.uniform(10.1219,100.9121),4),'assertion': ''}

    #Generate patient mrns
    for count in range(0, int(num_of_facts/10000)):
        mrn = random.randint(10,1000)
        patientMrn.append(mrn)

    #Generate facts.csv using concepts
    for count in range(1,num_of_facts+1):
        mrn = random.choice(patientMrn)
        startDate = datetime.date(random.randint(2010,2021), random.randint(1,12),random.randint(1,28))
        code = random.choice(list(conceptDict))
        type = conceptDict[code]
        value = typeDict[type]

        rowList = [mrn,startDate,code,value]
        factArr.append(rowList)

    factCsvHeaders = ['mrn','start-date','code','value']
    factFilename = benchmarkPath + "/demo_new_facts.csv"
    write_csv(factFilename,factCsvHeaders,factArr)

    #Time analysis
    config=Config().new_config(argv=['concept','delete'])
    concept_runner.mod_run(Config.config)

    config=Config().new_config(argv=['fact','delete'])
    fact_runner.mod_run(Config.config)

    config=Config().new_config(argv=['concept','load','-i', 'tmp/benchmark/'])
    concept_runner.mod_run(Config.config)

    startTime = time.time()
    config=Config().new_config(argv=['fact','load', '-i', 'tmp/benchmark/'])
    fact_runner.mod_run(Config.config)
    timeDiff = time.time() - startTime

    factsDbCount = get_fact_records_count()
    resultList = [num_of_concepts,num_of_facts,int(num_of_facts/10000),factsDbCount,timeDiff,str(datetime.datetime.now())]
    logger.debug('Result list is:-', resultList)
    resultCsvHeaders = ['No_of_concepts','No_of_facts','No_of_patients','Records in DB','Time','Timestamp'] #RC:KW Add no_of_concepts,no of patients and timestamp in result.csv
    resultFileName = benchmarkPath + "/fact_benchmark_result.csv"
    write_csv(resultFileName,resultCsvHeaders,resultList)
    
def write_csv(path,header,arr):
    if path == '/usr/src/app/tmp/benchmark/fact_benchmark_result.csv':
        with open(path,'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvfile.seek(0,2)
            if csvfile.tell() == 0:
                csvwriter.writerow(header)
            csvwriter.writerow(arr)
    else:
        with open(path,'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(header)
            csvwriter.writerows(arr)
    logger.info('Data written to file successfully')   

def get_path(conceptHash,code):
    if len(conceptHash) == 0:
        return 'a'
    else:
        parentPath = random.choice(list(conceptHash.keys()))
        path = parentPath + '/' + code
        if len(path.split('/')) > 20:
            return get_path(conceptHash,code)
        return path

def generate_plot(path):
    df = pd.read_csv(path)
    groups = df.groupby('No_of_concepts')
    for name,group in groups:
        plt.plot(group.No_of_facts,group.Time, marker='o', linestyle='dashed', label=name)
    plt.xlabel('No of facts')
    plt.ylabel('Time')
    plt.legend()
    plt.show()
    plt.savefig('/usr/src/app/tmp/fact_benchmark.png')