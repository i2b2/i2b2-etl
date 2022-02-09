#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
from config import config
from pathlib import Path

class Warn():
    """Service to buffer writing IO_warning to log
    """    
    def __init__(self,logFile,bufferSize=10):    
        """[summary]

        Args:
            logFile ([type]): name of logFile
            bufferSize (int, optional): Number of lines to keep in memomery before flushing to disk. Defaults to 10.
        """            
        self.logFile=logFile
        Path(config.log_dir).mkdir(parents=True, exist_ok=True)
        self.file=open(config.log_dir+'/'+self.logFile, "w")
        self.buffer=[]
        self.bufferSize=bufferSize


    def __exit__(self, type, value, traceback):
        """Close the file handle and write buffer to file
        Args:
            type (:obj:`type`, mandatory): Type of the exception
            value (:obj:`value`, mandatory): Value of the exception
            traceback (:obj:`traceback`, mandatory): traceback of the exception
            
        """
        self.flush()
        self.file.close()

    def flush(self):
        for x in buffer:
            self.logFile.write(x)
    

    def warn(warning,task='-',inputLineNumber='-',inputLine='-')
        warning='etl-pipeline-error: (' +
            task +
            '), - ' +
            traceback.format_exc()
        self.buffer.append('\t'.join([warning,inputLineNumber,inputLine))
        if len(self.buffer)>10:
            self.flush()

        