# Copyright 2023 Massachusetts General Hospital.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
from glob import glob
from pathlib import Path
from loguru import logger

def getConcatCsvAsDf(dirPath,fileSuffix,delimiter=','):
    """Globs files with fileSuffix from dirPath, merges them into a single pandas DataFrame

    Arguments:
        dirPath {string} -- absolute path to input directory e.g. /user/home/data
        fileSuffix {[type]} -- suffix pattern of the files to be globbed e.g. '_concepts.csv'

    Returns:
        [type] -- pandas data frame with an additional column (source_file) containing name of file from which the row originated 
    """
    '''
        Reads all columns as string
    '''
    res=pd.DataFrame()
    #provide trailing slash
    dirPath=str(Path(dirPath))
    globPath=dirPath+"/**/*"
    logger.trace('globPath:{}',globPath)
    arr=[]

    for x in glob(globPath,recursive = True):
        if fileSuffix.lower() in x.lower():
            logger.trace('reading csv:'+x)
            #stripping whitespace
            df=pd.read_csv(x,delimiter=delimiter, dtype=str, encoding='utf-8-sig')
            df.columns=[x.lower().strip() for x in df.columns]
            for col in df.columns:
                df[col] = df[col].apply(lambda x: '' if pd.isnull(x) else  str(x).strip())
            df['input_file']=[x for i in range(0,len(df))]
            df['line_num']=[i for i in range(0,len(df))]
            arr.append((x,df))
    if len(arr)>0:
        res=pd.concat([x[1] for x in arr])
    logger.trace('res columns {}',res.columns)
    logger.trace(res)
    return res

def dirGlob(dirPath,fileSuffixList):
    """Globs files with fileSuffix from dirPath
    Arguments:
        dirPath {string} -- dir containing the files
        fileSuffixList {list{string}} list of file suffixes to include
    Returns:
        [dictionary] -- filePaths as keys and content  
    """
    #provide trailing slash
    dirPath=str(Path(dirPath))

    d={}
    for fileSuffix in fileSuffixList:
        globPath=dirPath+"/**/*"+fileSuffix
        logger.trace('globbing:{}',globPath)
    return [ p for p in glob(globPath,recursive = True) if '/deid/' not in p and '/logs/' not in p ]

def str_to_file(oFilePath,textContent):
    try:     
        logger.trace('writing to file:'+oFilePath)  
        with open(oFilePath, "w") as the_file:
            the_file.write(textContent)
    except Exception as e:
        msg='Error writing to file :'+oFilePath        
        logger.error(msg,e)
        raise Exception(msg,e)

def str_from_file(oFilePath):
    try: 
        logger.trace('reading file:'+oFilePath)  
        with open(oFilePath, "r") as the_file:
            return the_file.read()
    except Exception as e:
        msg='Error reading from file :'+oFilePath        
        logger.error(msg,e)
        raise Exception(msg,e)
    
if __name__=='__main__':
    logger.trace()
