import pandas as pd
import csv
import os
from i2b2_cdi.config.config import Config
from loguru import logger
import random
from time import time
import datetime
import string
import i2b2_cdi.concept.runner as concept_runner
import i2b2_cdi.fact.runner as fact_runner
from .fact_count import get_fact_records_count
import matplotlib.pyplot as plt
import plotly.express as px
from i2b2_cdi.common.utils import *
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.common.py_bcp import PyBCP
from pathlib import Path
import glob
import shutil


numberOfFacts=''
def fact_benchmark(options):
    conceptFactsList = [(concepts,facts,partitions) for concepts in options.num_of_concepts for facts in options.num_of_facts for partitions in options.num_of_partitions]
    
    for i in range(0,options.times):
        for index,tuple in enumerate(conceptFactsList):
            no_of_concepts = tuple[0]
            no_of_facts = tuple[1]
            no_of_partitions = tuple[2]
            run(no_of_concepts,no_of_facts,no_of_partitions)

    path = '/usr/src/app/tmp/benchmark/fact_benchmark_result.csv'
    generate_plot(path)

def run(num_of_concepts,num_of_facts,num_of_partions):
    global numberOfFacts
    numberOfFacts = num_of_facts
    logger.info('Running fact benchmark for {0} concepts and {1} facts'.format(num_of_concepts,num_of_facts))
    demoType = ['assertion','integer','largestring','string','float']

    conceptArr = []
    factArr = []
    conceptHash = {}
    conceptDict = {}
    patientMrn = []
    partitions = []
    indexes = []
    timeArr = []

    benchmarkPath = "/usr/src/app/tmp/benchmark"
    if  os.path.exists(benchmarkPath):
        shutil.rmtree(benchmarkPath)
        os.makedirs(benchmarkPath)
    else:
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
    
    typeMap = conceptDf.set_index('code')['type'].to_dict()
    conceptCodes = [k for k in typeMap.keys()]

    valueMap = { 'integer' : 100,'string' : 'string',
                 'largestring' : 'largestring','float': 10.10,'assertion': ''}

    #Generate patient mrns
    for count in range(0, int(num_of_facts/10000)):
        mrnNos = range(1,int(num_of_facts/1000)+1)
        mrn = random.choice(mrnNos)
        patientMrn.append(mrn)


    #Generate facts.csv using concepts
    factCsvHeaders = ['mrn','start-date','code','value']
    factFilename = benchmarkPath + "/sample_facts.csv"

    for count in range(1,num_of_facts+1):
        mrn = random.choice(patientMrn)
        startDate = '2021-02-15'
        code = random.choice(conceptCodes)
        conceptType = typeMap[code]
        value = valueMap[conceptType]

        rowList = [mrn,startDate,code,value]
        factArr.append(rowList)
        if len(factArr) == 100000:
            write_csv(factFilename,factCsvHeaders,factArr)
            logger.info('Copied {} rows to file'.format(count))
            factArr.clear()

    # #Time analysis
    config=Config().new_config(argv=['concept','delete'])
    concept_runner.mod_run(config)

    config=Config().new_config(argv=['fact','delete'])
    fact_runner.mod_run(config)

    config=Config().new_config(argv=['concept','load','-i', 'tmp/benchmark/'])
    concept_runner.mod_run(config)

    #Partitioning observation_fact table
    if num_of_partions > 0:
        create_partitoned_table = Path('i2b2_cdi/resources/sql') / \
        'create_partitoned_table_observation_facts_pg.sql'

        execute_partitions(create_partitoned_table)
        logger.info('Created new partitioned observation_fact table with {} partitons'.format(num_of_partions))

        for i in range(0,num_of_partions):
            createPartition = "CREATE TABLE patient_{0} PARTITION OF OBSERVATION_FACT FOR VALUES WITH (MODULUS {1},REMAINDER {0});".format(i,num_of_partions)
            createIndex = "CREATE INDEX pt{0}_index on patient_{0} USING btree(PATIENT_NUM);".format(i)
            partitions.append(createPartition)
            indexes.append(createIndex)

        execute_partitions(partitions)
        
        index_file_path = Path('i2b2_cdi/resources/sql') / \
        'create_indexes_observation_fact_pg.sql'
        
        with open(index_file_path,'w') as f:
            for line in indexes:
                f.write(f"{line}\n")

    startTime = time()
    config=Config().new_config(argv=['fact','load', '-i', 'tmp/benchmark/'])
    fact_runner.mod_run(config)
    timeDiff = time() - startTime

    factsDbCount = get_fact_records_count()
    resultList = [num_of_concepts,num_of_facts,int(num_of_facts/10000),factsDbCount,timeDiff,str(datetime.datetime.now())]
    logger.debug('Result list is:-', resultList)
    
    resultCsvHeaders = ['No_of_concepts','No_of_facts','No_of_patients','Records in DB','Time','Timestamp'] #RC:KW Add no_of_concepts,no of patients and timestamp in result.csv
    resultFileName = benchmarkPath + "/fact_benchmark_result.csv"
    write_csv(resultFileName,resultCsvHeaders,resultList)
    numberOfFacts = num_of_facts
    # time_analysis()

    #Query time analysis
    if num_of_partions > 0:
        for file in glob.glob('/usr/src/app/i2b2_cdi/resources/sql/benchmark_queries/*.sql'):
            arr = get_query_analysis(file,num_of_partions,num_of_facts)
            timeArr.append(arr)
        
        with open('/usr/src/app/tmp/timeAnalysis.csv','a',newline="") as f:
            writer = csv.writer(f)
            writer.writerows(timeArr)


def write_csv(path,header,arr):
    if path == '/usr/src/app/tmp/benchmark/fact_benchmark_result.csv':
        with open(path,'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvfile.seek(0,2)
            if csvfile.tell() == 0:
                csvwriter.writerow(header)
            csvwriter.writerow(arr)
    else:
        with open(path,'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            if csvfile.tell() == 0:
                csvwriter.writerow(header)
            csvwriter.writerows(arr)

def get_query_analysis(path,num_of_partions,num_of_facts,config=Config().new_config(argv=['fact','load'])):
    try:
        with I2b2crcDataSource(config) as cursor:
            query = open(path,'r').read()
            stime = time()
            cursor.execute(query)
            timeTaken = time() - stime
        return [os.path.basename(path).split('/')[-1],timeTaken,'Partitions:{}'.format(num_of_partions),'Num of facts:{}'.format(num_of_facts)]
    except Exception as e:
        logger.exception('Failed to execute query:{}'.format(e))


def time_analysis():
    df = pd.read_csv("tmp/timeAnalysis.csv")
    df.columns=["functionName","timeTakenInSec"]
    
    df["time_taken_in_percentage"]=(100 * df["timeTakenInSec"] / df["timeTakenInSec"].sum()).round(1).astype(str)
    df["number_of_factrecords"]=numberOfFacts
    resultFilePath="tmp/final_result.csv"
    if os.path.isfile(resultFilePath):
        df_result=result_analysis()
        df=pd.concat([df_result,df])
        df.to_csv("tmp/final_result.csv",index=False)
    else:
        df.to_csv("tmp/final_result.csv",index=False)
    path="tmp/timeAnalysis.csv"
    delete_file_if_exists(path)
    gragh(df)

def result_analysis():
    df = pd.read_csv("tmp/final_result.csv")
    return df
def gragh(df):
    fig = px.line(df, x="functionName", y="time_taken_in_percentage", color="number_of_factrecords", title="time taken for each function")
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    fig.write_image("time_taken_for_functions.png")


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

def execute_partitions(query,config=Config().new_config(argv=['fact','load'])):
    try:
        if type(query) is list:
            with I2b2crcDataSource(config) as cursor:
                for query in query:
                    cursor.execute(query)
        else:
            dbparams = I2b2crcDataSource(config)
            with dbparams as cursor:
                cursor.execute("set search_path to "+dbparams.database)
                cursor.execute(open(query, 'r').read())
    except Exception as e:
        logger.exception('Failed to execute query:{}'.format(e))

