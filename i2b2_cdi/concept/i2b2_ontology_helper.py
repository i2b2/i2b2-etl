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
from loguru import logger
import re
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
import hashlib 

def getAncestorPaths(norm_path="/A/B/C"):
    """
    Args:
        path (str): Path in the form "/A/B/C".

    Returns:
        array(str): The array of string pathLk

    """
    arr=[]
    for x in norm_path.split('/')[1:-1]:
        if len(arr)==0:
            arr.append('/'+x)
        else:
            arr.append(arr[-1]+'/'+x)      
    return arr

def get_code_concept_path(concept_path,codeLookup):
    """ancestor pathLk of concept_path are required in codeLookup

    Arguments:
        concept_path {string} -- like file path
        codeLookup {dict} -- dictionary of concept_codes that are already used

    Returns:
        [string] -- like file path
    """    
    path=''
    ancestor_path=''
    
    for n in concept_path.split('/')[1:]:
        
        ancestor_path+='/'+n
        logger.trace('lookup ancestor Path:{} {}',ancestor_path,codeLookup)
        if ancestor_path in codeLookup:
            logger.trace('FOUND {}:{}',ancestor_path,codeLookup[ancestor_path])
        path+='/'+codeLookup[ancestor_path]
    logger.trace('resolved {}: {}',concept_path,path)
    return path

def get_duplicate_rows(conceptDef):
    '''Fetching duplicate rows from csv if any and returning the row that have duplicate concept path'''
    #Validation for duplicates concept path in csv
    dup_path = conceptDef["path"]
    dt_duplicate=conceptDef[dup_path.isin(dup_path[dup_path.duplicated()])]
    dt_duplicate=dt_duplicate[dt_duplicate.columns[0:3]]#Omitting the last column as it is file path
    dt_duplicate= dt_duplicate.drop_duplicates(subset=['path'], keep='last')# This is keeping only the duplicate path those are omitted
    return dt_duplicate


#print(get_short_concept_path('/covid/lab/hematocrit/NHHCT',codeLk))
    

def getAutoParentCode(name):
    code=name
    if len(name)>50:
        code=name[-39:]+'~'+str(hashlib.sha256(str(name).encode('utf-8')).hexdigest())[0:10]
    return code
 

#final codeLK:{'/B/C/E': 'E', '/A': 'A', '/A/B': 'B', '/B~a7d60b7242': 'B~a7d60b7242', '/B~a7d60b7242/C': 'C', '/B~a7d60b7242/C/D': 'D', '/B': 'B~a7d60b7242', '/B/C': 'C~1fa2e198cd'}




def isRootPath(conceptPath,lk):
    try:
        arr=conceptPath.split('/')
        if len(arr)==1:
            return True
        
        parentPath='/'.join(conceptPath.split('/')[0:-1])
        return parentPath not in lk
        #ancestorPaths=getAncestorPaths(conceptPath)
        #if len(ancestorPaths)==0:
        #    return True
        #logger.trace('ancestor {}-{} {}',conceptPath,ancestorPaths[-1],lk.keys())
        #return ancestorPaths[-1] not in lk
    except Exception as e:
        #logger.error('in {}',conceptPath)
        logger.exception(e)

def isLeafPath(conceptPath,parentlk):
    try:
        #return False
        return conceptPath not in parentlk
        cpp=str(conceptPath)+'/'
        for x in lk.keys():
            if len(cpp) < len(x) and cpp in x:
                return False
        return True
    except Exception as e:
        #logger.error('in {}',conceptPath)
        logger.error(e)

def normalizePath(path):
    """converts to linux style slash and removes ending slash

    Arguments:
        path {string} -- folder path like string

    Returns:
        string -- normalize folder path like strings
    """    

    path=path.replace("\\",'/')
    path=path.replace('^/','')
    path=path.replace('/$','')
    path=re.sub("/$","",path)
    path='/'+path
    path=path.replace('//','/')
    return path

def i2b2Path(path):
    """converts linux style slash to i2b-sql '\\' delimiter and adds ending slash

    Arguments:
        path {string} -- folder path like string

    Returns:
        string -- i2b2-sql folder path like strings
    """    
    path=path.replace("/",'\\')+'\\'
    return path

def i2b2metadata_dsv_to_conceptcsv(dsv,concept_map_df=None):
    """generates concept path

       --TODO validates length and type of elements

    Arguments:
        dsv {[type]} -- '|' seperated file : .dsv

    Returns:
        pandas.DataFrame -- abstraction that is malleable
    """    
    if len(dsv)==0:
        msg='No metadata found. perhaps .dsv has no rows'
        logger.warning(msg)
        return pd.DataFrame()
    ##TODO handle visit dimension seperately
    m=dsv[dsv['c_tablename'].apply(lambda x:x.lower())=='concept_dimension']

    m.columns
    m=m.rename(columns={'c_fullname':'short_path',\
        'c_basecode':'code',\
        'c_dimcode':'code_path',\
        'c_name':'concept_name',\
        'c_tooltip':'description'})\
        [['short_path','concept_name','code','code_path','description']]

    m['short_path']=m['short_path'].apply(lambda x: normalizePath(x))
    m['code_path']=m['code_path'].apply(lambda x: normalizePath(x))

    pathMap={}
    codeMap={}
    for idx,row in m.iterrows():
        if pd.isnull(row['concept_name']) or pd.isnull(row['short_path'])\
            or row['concept_name']=='nan' or row['short_path']=='nan':
            logger.warning('invalid row: {}',row)
        else:
            pathMap[row['short_path']]=row['concept_name']
            codeMap[row['code']]=True

    #creating concept pathLk ##and concepts codes (latter may be useful)
    arr=[]
    codearr=[]
    for idx,row in m.iterrows():
        shortp=row['short_path']
        parents=getAncestorPaths(shortp)
        tup=[(x,pathMap[x]) if x in pathMap else (x,'-' ) for x in parents ]
        cpath='/'+'/'.join([str(x[1]) for x in tup])+'/'+row['concept_name']
        arr.append(cpath)


    m['path']=arr

    return m



def find_error_in_row(row):
    
    if len(row['concept_name'])>2000:
        return 'concept name is >2000'

    if len(row['code'])>50:
        return 'length of concept code is >50'
    
    if row['code'] == '':
        return 'concept_code is missing'

    if row['path']=='' or row['path']=='/':
        return 'concept_path is missing'

    if row['concept_type'] is not None:
        if row['concept_type'].lower() not in ['largestring','posinteger','float','integer','posfloat','string','assertion']\
            and 'enum' not in row['concept_type'].lower()\
            and len(row['concept_type'])!=0:
            return 'concept_type is incorrect'

    # if row['definition_type'] is not None:
    #     if row['definition_type'] and row['definition_type'].lower():
    #         return 'definition_type is incorrect'

    regex = r"([\\\\,\\,/,//]+)"
    if re.findall(regex,row['code']):
        return 'Slash was found in the concept code.'

    # if row['definition_type'] is not None and row['definition_type'].lower()=='derived' :
    #     if row['blob'] is None or row['blob']=='':
    #         return 'derived concept has no blob'


    return None



def get_existing_Ont2(config):
    """This method generates Hash from sql
        Args:
            args: options namespace     

    """
  
    logger.debug('getting concepts from crc')
    try:
        conn = I2b2crcDataSource(config)
        with conn as conn:            
            lkDf = pd.read_sql_query("select distinct concept_path, concept_cd from concept_dimension",conn.connection) 

            logger.debug("DF from database {}",lkDf)

            lk={}
            for idx,r in lkDf.iterrows():
                lk[normalizePath(r['concept_path'])]=r['concept_cd']
             
            return lk
           
    except Exception as e:
        logger.exception(e)

def get_concept_ontology_from_i2b2metadata(config,conceptDef,concept_map_df=None):
    """
        Tranforms the conceptDefintion pandas dataframe into one which has the elements to display an Ontology
    
    Arguments:
        conceptDef {pandas data frame} -- dataFrame having concept_path and concept_code

    Returns:
        pandas DataFrame -- has autocreated rows for parents and columns for diffirent path transforms
    """
    '''The resulting dataframe has one child level (including concept_code in path)
    and all required levels of parents'''

    '''
    use case 1 code_concept_path given , orphans should be displayed using table access
    
    use case2: parents are auto generated , along with code-concept pathLk'''
    #code for duplicate path omission from csv and process other 
    conceptDef= conceptDef.drop_duplicates(subset=['path'], keep='first')
    if 'unit' not in conceptDef:
        conceptDef['concept_unit']=['' for x in conceptDef['path']]
    df=conceptDef.rename(columns={"path":"concept_path","code":"concept_code",\
        "type":"concept_type","name":"concept_name",\
            "description":"concept_description",\
                "unit":"concept_unit", "blob":"concept_blob", "definition_type":"definition_type"})
    logger.debug("df:",df)
    logger.debug('cols:{}',df.columns)
    
    df['concept_path']=df.apply(lambda x: normalizePath(x['concept_path']), axis=1)

    #make parent rows
    pathLk={path:True for path in df['concept_path'].to_list()}
    codes={code:True for code in df['concept_code'].to_list()}
    codeLk={x['concept_path']:x['concept_code'] for idx,x in df.iterrows()}
    pathMap={}

    existing_ont=get_existing_Ont2(config)
    for k in existing_ont:
        v=existing_ont[k]

        pathLk[k]=True
        codes[v]=True
        codeLk[k]=v #overwriting codes of provided paths


    arr=[]
    count=0
    onetenth=round(len(df)/10)
    for idx,r in df.iterrows():
        count+=1
        if onetenth>0 and (count % onetenth ==0):
            logger.debug('..{}%',str(int(count*100/len(df))))
        path=r['concept_path']
        code=r['concept_code']
        ctype=r['concept_type']
        # line_num=r['line_num']
        # input_file=r['input_file']

        line_num=idx+1          #Updating line_num to make consistent for summarize function
        # input_file=idx
        input_file = r['input_file']

        if('definition_type' in df.columns and r['definition_type']=='DERIVED' and r['concept_blob']==''):
            logger.warning("Concept blob is empty for Derived concept")
            pathLk.pop(path)
            codes.pop(code)
            codeLk.pop(path)
            continue

        if 'concept_name' in df.columns:
            cname=r['concept_name']
        else:
            cname=r['concept_path'].split('/')[-1]
        
        if 'concept_description' in df.columns:
            cdesc=r['concept_description']
        else:
            cdesc=''

        if ctype=='':
            ctype='assertion'
            
        if 'concept_blob' in df.columns:
            cblob=r['concept_blob']
        else:
            cblob=''

        if 'definition_type' in df.columns:
            cdefinition_type=r['definition_type']
        else:
            cdefinition_type=''

        #already_present_parent_paths=[normalizePath(x) for x in db_concepts['path']]
        #logger.trace('db_concepts[\'path\']:{}',already_present_parent_paths)
        
       
        logger.trace("Starting codeLK:{}",codeLk)

        for p in getAncestorPaths(path):
            n=p.split('/')[-1]
            #processing ancestors that are not defined in the input file 
            
            if p not in pathLk:
                pathLk[p]=True
                #cd='auto-parent:'+n #?should use short path
                
                #e.g. /covid/lab/test1 /diabetes/lab/test2
                cd=''
                if p in codeLk:
                    cd=codeLk[p]
                else:
                    cd=getAutoParentCode(n)
                
                    logger.trace("..adding {}:{} {}",p,cd,codeLk)
                    pathLk[p]=True
                    codes[cd]=True
                    codeLk[p]=cd 
                
                sp=get_code_concept_path(p,codeLk)         
                cp=sp
                #pathLk[cp]=True
                is_root=isRootPath(p,pathLk)
                ccdesc=""
                ccunit=""

                arr.append([p,cd,'',n,sp,cp,False,is_root,ccdesc,ccunit,'','',line_num,input_file])

        ccpath=get_code_concept_path(path,codeLk)
        spath=ccpath
        #pathLk[spath]=True
        codeLk[path]=code
        is_leaf=False
        is_root=False

        logger.trace("final codeLK:{}",codeLk)

        arr.append([path,code,ctype,cname,spath,ccpath,is_leaf,is_root,cdesc,r['concept_unit'], cblob, cdefinition_type,line_num,input_file])
        if count%1000==0:
            logger.trace('completed {} of {}', count, len(df))
    df1=pd.DataFrame(arr,columns=["path","code","concept_type","concept_name","short_path","code_path","is_leaf","is_root","description","concept_unit","concept_blob","definition_type",'line_num','input_file'])
    
    df1,errDf=filterErrors(df1)
    #logger.trace('ERROR:{}',errDf)
    
    df2=addMapToConceptDef(df1,concept_map_df)
    df2=processLeafRoot(df2,existing_ont)
    #filter by existing ontology
    arr=[]
    for idx,r in df2.iterrows():
        _path=r['code_path']
        if _path in existing_ont:
            pass
        else:
            arr.append(r)
    df3=pd.DataFrame(arr,columns=df2.columns)
    df3=df3.drop_duplicates('code_path')
    return (df3,errDf)

def filterErrors(df):
    (arrIdx,errors)=([],[])
    logger.debug("df header:{}",list(df))
    
    for idx,r in df.iterrows():
        logger.debug('filtering')
        logger.debug(r)
        error=find_error_in_row(r)
        if error is not None:
            a=[]
            a.append(error)
            for x in list(df):
                a.append(r[x]) 
            errors.append(a)
            arrIdx.append(False)
        else:
           arrIdx.append(True)
    return df[arrIdx],pd.DataFrame(errors,columns=['error']+list(df))



def processLeafRoot(conceptDef,existing_ont):
    logger.debug('..processing leaves and root')
    if conceptDef.empty:
        return conceptDef
    df=conceptDef
    pathLk={path:True for path in df['path'].to_list()}
    parentpathLk={}
    for path in df['path'].to_list():
        _a=path.split('/')
        if (len(_a))>2:
            if path.endswith('/'):
                parentpathLk['/'.join(_a[0:-2])]=True #-2 If it ends with slash then there is space and last node so we have to do -2
            else:
               parentpathLk['/'.join(_a[0:-1])]=True #-1 will only omit the last node of the path which is actually the child node.
    
    #for k in existing_ont:
    #    pathLk=True
    #print('\n'.join(pathLk.keys()))
    #print()
    #print('>>>parent')
    #print()
    #print('\n'.join(parentpathLk.keys()))

    arr=[]
    
    for idx,r in df.iterrows():
        spath=r['path']
        r['is_leaf']=isLeafPath(spath,parentpathLk)
        sspath=spath.split('/')
        #is root must be for the first node only.if it starts with slash the length must be 2 
        if len(sspath)==2:
            r['is_root']=True
        else:
            r['is_root']=False
        #r['is_root']=isRootPath(spath,pathLk)
        arr.append(r)
    return pd.DataFrame(arr,columns=df.columns)


def add_codes_as_child(conceptDef):
    df=conceptDef
    arr=[]
    for idx,r in df.iterrows():
        arr.append(r)
        c=r.copy()
        if pd.isnull(c['code']) or c['code']=='nan' or c['code']=='':
            pass
        else:
            c['concept_name']=c['code']
            c['short_path']=c['short_path']+'/'+c['code']
            logger.trace(c)
            arr.append(c)
    return pd.DataFrame(arr,columns=df.columns)


def addMapToConceptDef(resolved_concept_df,concept_map_df=None):
    """integrated concept mappings CSV into concept definition CSV

    Arguments:
        concept_df {[pandas.DataFrame]} -- concept CSV

    Keyword Arguments:
        concept_map_df {[pandas.DataFrame]} -- concept_map CSV(default: {None})

    Returns:
        [pandas.DataFrame] -- concept CSV after merging the mappings
    """ 
    logger.debug('..processing concept maps')
    concept_df=resolved_concept_df
    if concept_map_df is None:
        return concept_df

    concept_df['code']=concept_df['code'].apply(lambda x:str(x))
    arr=[]
    ignore=[]
    logger.trace('adding concept map')

    mapLk={}
    for idx,m in concept_map_df.iterrows():
        std=str(m['standard_code'])
        local=str(m['local_code'])

        if pd.isnull(std) or std is None or std=='' or std=='nan':
            ignore.append(local)
        
        if std not in mapLk:
            mapLk[std]=[]
        if local not in mapLk[std]:
            mapLk[std].append(local)

    logger.trace('created map of size {}',len(mapLk))
    
    for idx,c in concept_df.iterrows():
        arr.append(c)
        std=c['code']
        if std in mapLk:
            for local in mapLk[std]:
                m=c.copy()
                m['path']=m['path']+'/'+local
                m['short_path']=c['code_path']+'/'+local#c['short_path']+'/'+local
                m['concept_name']=local
                m['code']=local
                m['code_path']=c['code_path']+'/'+local
                arr.append(m)

    if len(ignore)>0:
        logger.warning('ignored {} mappings that had no standard code',len(ignore))
    logger.trace('completed adding concept map')
    return pd.DataFrame(arr,columns=concept_df.columns)


def get_existing_Ont():
    return pd.DataFrame()
    


