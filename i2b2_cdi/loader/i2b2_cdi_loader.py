#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`i2b2-loader` -- Perform various operations in data pipeline
=================================================================

.. module:: loader
    :platform: Linux/Windows
    :synopsis: module contains methods for performs various operations in data pipeline



"""
# __since__ = "2020-05-08"

from os.path import dirname, realpath, sep, pardir
import os,sys
sourceDir=dirname(realpath(__file__)) + sep + pardir + sep + pardir
sys.path.insert(0,sourceDir) 

import argparse
import os
from i2b2_cdi.log import logger
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.fact import perform_fact
from i2b2_cdi.concept import perform_concept
from i2b2_cdi.patient import perform_patient
from i2b2_cdi.encounter import perform_encounter
from i2b2_cdi.common.constants import *
from i2b2_cdi.encounter import perform_encounter
from i2b2_cdi.config import config
from i2b2_cdi.concept import concept_load_from_dir
from i2b2_cdi.project import addI2b2ProjectWrapper
import unittest

def delete_concepts():
    """Delete the concepts. It's wrapper method"""
    perform_concept.delete_concepts()


def delete_facts():
    """Delete the facts. It's wrapper method"""
    perform_fact.delete_facts()


def load_concepts(input_dir):
    """Load the concepts. It's wrapper method

    Args:
        file_path (:obj:`str`, mandatory):

    """
    concept_load_from_dir(input_dir)


def load_facts(obs_file_path):
    """Load the facts. It's wrapper method.

    Args:
        file_path (:obj:`str`, mandatory):

    """
    factErrorFiles = perform_fact.load_facts(obs_file_path)


def delete_encounters():
    """Delete the encounters. It's wrapper method.
    """
    perform_encounter.delete_encounters()


def delete_encounter_mappings():
    """Delete the encounter mapping. It's wrapper method.
    """
    perform_encounter.delete_encounter_mappings()


def load_encounters(file_path):
    """Load the encounters. It's wrapper method.
    Args:
        file_path (:obj:`str`, mandatory): Input encounter file.
    """
    perform_encounter.load_encounters(file_path)


def delete_patient_mappings():
    """Delete patient mapping. It's wrapper method.
    """
    perform_patient.delete_patient_mappings()


def delete_patients():
    """Delete patients. It's wrapper method.
    """
    perform_patient.delete_patient_dimensions()

def load_patient_mapping(file_path):
    """Load patient mapping. It's wrapper method.
    Args:
        file_path (:obj:`str`, mandatory): Path to the mrn file.
    """
    perform_patient.load_patient_mapping(file_path)

def load_patients(file_path):
    """Load patients. It's wrapper method.
    Args:
        file_path (:obj:`str`, mandatory): Input patient file.
    """
    perform_patient.load_patient_dimension(file_path)
    
def dir_path(dir):
    if os.path.isdir(dir):
        return dir
    else:
        raise argparse.ArgumentTypeError(
            "'{0}' is not a valid directory".format(dir))

def delete_data():
    """Delete the concepts, facts, encounters patients etc. It's wrapper method.
    """
    # Cleanup i2b2
    try:
        delete_concepts()
        delete_patient_mappings()
        delete_patients()
        delete_encounter_mappings()
        delete_encounters()
        delete_facts()
    except Exception as e:
        logger.error("Failed to delete data : {}", e)
    finally:
        logger.info("Delete data : operation completed !!") 


def load_data(dir_path):
    """Load the concepts, facts, encounters etc. It's wrapper method.
    Args:
        dir_path (:obj:`str`, mandatory): Path to the directory where files are placed to load.
    """
    try:
        mrn_file = 'mrn.csv'
        encounter_file = 'encounters.csv'
        fact_file = 'facts.csv'
        patient_file = 'patients.csv'
        data_files_map = {mrn_file: False, encounter_file: False,
                        fact_file: False, patient_file: False}
        # Get all files in a folder
        files = os.listdir(dir_path)
        for file in files:
            if file in data_files_map:
                data_files_map[file] = True
        # Import concepts
        if any(File.endswith("concepts.csv") for File in os.listdir(dir_path)):
            load_concepts(dir_path)

        # Import facts, encounters, patients and mrns
        if data_files_map.get(mrn_file):
            load_patient_mapping(dir_path + '/' + mrn_file)
        if data_files_map.get(patient_file):
            load_patients(dir_path + '/' + patient_file)
        if data_files_map.get(encounter_file):
            load_encounters(dir_path + '/' + encounter_file)
        if data_files_map.get(fact_file):
            load_facts(dir_path + '/' + fact_file)

        # Delete csv files after import
        for file in files:
            if file.endswith(".csv"):
                os.remove(os.path.join(dir_path, file))
        
    except Exception as e:
        logger.error("Failed to load data : {}", e)
        raise(e)
    finally:
        logger.info("Load data : operation completed !!") 

def test_fact_load():
        try:
            suite = unittest.TestLoader().discover("i2b2_cdi/test/integration", pattern="test_fact.py")
            unittest.TextTestRunner(verbosity=2).run(suite)
        except Exception as e:
            logger.error("Issue in test cases : {}", e)
            raise

if __name__ == "__main__":
    args = config
    level_per_module = {"": "TRACE",
    "i2b2_cdi": "TRACE"}

    logger.debug("config:{}",config)

    #elif args.delete_data:
    #    delete_data()
    #elif args.load_data:
    #    load_data(args.load_data)
    if args.delete_facts:
        delete_facts()
    elif args.load_concepts:
        load_concepts(config.input_dir)
    elif args.delete_concepts:
        delete_concepts()
    elif args.fact_file:
        # Check database connection before load
        demodata_connection = I2b2crcDataSource()
        demodata_connection.check_database_connection()
        load_facts(args.fact_file.name)
        args.fact_file.close()
    elif args.delete_encounters:
        delete_encounters()
    elif args.delete_encounter_mappings:
        delete_encounter_mappings()
    elif args.encounter_file:
        # Check database connection before load
        demodata_connection = I2b2crcDataSource()
        demodata_connection.check_database_connection()
        load_encounters(args.encounter_file.name)
        args.encounter_file.close()
    elif args.delete_patient_mappings:
        delete_patient_mappings()
    elif args.delete_patients:
        delete_patients()
    elif args.mrn_file:
        # Check database connection before load
        demodata_connection = I2b2crcDataSource()
        demodata_connection.check_database_connection()
        load_patient_mapping(args.mrn_file.name)
        args.mrn_file.close()
    elif args.patient_file:
        # Check database connection before load
        demodata_connection = I2b2crcDataSource()
        demodata_connection.check_database_connection()
        load_patients(args.patient_file.name)
        args.patient_file.close()
    if args.add_project_db!='-' :
        addI2b2ProjectWrapper(args)
