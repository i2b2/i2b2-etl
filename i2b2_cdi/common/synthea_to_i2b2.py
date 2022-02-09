#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`synthea_to_i2b2` -- transforms synthea dataset to i2b2 format dataset
===========================================================================

.. module:: synthea_to_i2b2
    :platform: Linux/Windows
    :synopsis: module contains methods for transforming synthea dataset to i2b2 format dataset



"""
# __since__ = "2020-06-11"

import csv
from collections import OrderedDict
import os
from pathlib import Path
from alive_progress import alive_bar, config_handler
import subprocess

config_handler.set_global(length=50, spinner='triangles2')


def csv_rw_fact(synthetic_file, delimiter):
    """method for transforming synthetic observations to i2b2 format facts

    Args:
        synthetic_file (str): synthetic observations file path
        delimiter (str): delimiter needs to be added for csv operations

    """
    header = ['EncounterID', 'PatientID', 'ConceptCD', 'ProviderID',
              'StartDate', 'ModifierCD', 'InstanceNum', 'value', 'UnitCD']
    if os.path.exists(synthetic_file):
        fact_file_path = os.path.join(
            Path(synthetic_file).parent, "i2b2", 'facts.csv')

        delete_file_if_exists(fact_file_path)
        mkParentDir(fact_file_path)
    else:
        raise Exception

    with open(synthetic_file, mode='r') as csv_file:
        max_line = file_len(synthetic_file)-1
        write_file_header(fact_file_path, header, delimiter)
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        count = 1
        time = " 00:00:00"
        batch_size = 100
        batch = []
        with alive_bar(max_line, bar='smooth') as bar:
            for row in csv_reader:
                i2b2_row = OrderedDict()
                i2b2_row['EncounterID'] = row['ENCOUNTER']
                i2b2_row['PatientID'] = row['PATIENT']
                i2b2_row['ConceptCD'] = "LOINC:"+row['CODE']
                i2b2_row['ProviderID'] = "SYNTHEA"
                i2b2_row['StartDate'] = row['DATE'] + time
                i2b2_row['ModifierCD'] = "@"
                i2b2_row['InstanceNum'] = ""
                i2b2_row['value'] = row['VALUE']
                i2b2_row['UnitCD'] = row['UNITS']
                batch.append(i2b2_row)
                if(len(batch) == batch_size):
                    write_to_file(batch, fact_file_path, delimiter, header)
                    batch = []

                bar()

        write_to_file(batch, fact_file_path, delimiter, header)


def csv_rw_allergies(synthetic_file, delimiter):
    """method for transforming synthetic observations to i2b2 format facts

    Args:
        synthetic_file (str): synthetic observations file path
        delimiter (str): delimiter needs to be added for csv operations

    """
    header = ['EncounterID', 'PatientID', 'ConceptCD', 'ProviderID',
              'StartDate', 'ModifierCD', 'InstanceNum', 'value', 'UnitCD']
    if os.path.exists(synthetic_file):
        fact_file_path = os.path.join(
            Path(synthetic_file).parent, "i2b2", 'allergies_facts.csv')

        delete_file_if_exists(fact_file_path)
        mkParentDir(fact_file_path)
    else:
        raise Exception

    with open(synthetic_file, mode='r') as csv_file:
        max_line = file_len(synthetic_file)-1
        write_file_header(fact_file_path, header, delimiter)
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        count = 1
        time = " 00:00:00"
        batch_size = 100
        batch = []
        with alive_bar(max_line, bar='smooth') as bar:
            for row in csv_reader:
                i2b2_row = OrderedDict()
                i2b2_row['EncounterID'] = row['ENCOUNTER']
                i2b2_row['PatientID'] = row['PATIENT']
                i2b2_row['ConceptCD'] = "SNOMED-CT:"+row['CODE']
                i2b2_row['ProviderID'] = "SYNTHEA"
                i2b2_row['StartDate'] = row['START'] + time
                i2b2_row['ModifierCD'] = "@"
                i2b2_row['InstanceNum'] = ""
                i2b2_row['value'] = ""
                i2b2_row['UnitCD'] = ""
                batch.append(i2b2_row)
                if(len(batch) == batch_size):
                    write_to_file(batch, fact_file_path, delimiter, header)
                    batch = []

                bar()

        write_to_file(batch, fact_file_path, delimiter, header)


def csv_rw_careplans(synthetic_file, delimiter):
    """method for transforming synthetic observations to i2b2 format facts

    Args:
        synthetic_file (str): synthetic observations file path
        delimiter (str): delimiter needs to be added for csv operations

    """
    header = ['EncounterID', 'PatientID', 'ConceptCD', 'ProviderID',
              'StartDate', 'ModifierCD', 'InstanceNum', 'value', 'UnitCD']
    if os.path.exists(synthetic_file):
        fact_file_path = os.path.join(
            Path(synthetic_file).parent, "i2b2", 'careplans_facts.csv')

        delete_file_if_exists(fact_file_path)
        mkParentDir(fact_file_path)
    else:
        raise Exception

    with open(synthetic_file, mode='r') as csv_file:
        max_line = file_len(synthetic_file)-1
        write_file_header(fact_file_path, header, delimiter)
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        count = 1
        time = " 00:00:00"
        batch_size = 100
        batch = []
        with alive_bar(max_line, bar='smooth') as bar:
            for row in csv_reader:
                i2b2_row = OrderedDict()
                i2b2_row['EncounterID'] = row['ENCOUNTER']
                i2b2_row['PatientID'] = row['PATIENT']
                i2b2_row['ConceptCD'] = "SNOMED-CT:"+row['CODE']
                i2b2_row['ProviderID'] = "SYNTHEA"
                i2b2_row['StartDate'] = row['START'] + time
                i2b2_row['ModifierCD'] = "@"
                i2b2_row['InstanceNum'] = ""
                i2b2_row['value'] = ""
                i2b2_row['UnitCD'] = ""
                batch.append(i2b2_row)
                if(len(batch) == batch_size):
                    write_to_file(batch, fact_file_path, delimiter, header)
                    batch = []

                bar()

        write_to_file(batch, fact_file_path, delimiter, header)


def csv_rw_devices(synthetic_file, delimiter):
    """method for transforming synthetic observations to i2b2 format facts

    Args:
        synthetic_file (str): synthetic observations file path
        delimiter (str): delimiter needs to be added for csv operations

    """
    header = ['EncounterID', 'PatientID', 'ConceptCD', 'ProviderID',
              'StartDate', 'ModifierCD', 'InstanceNum', 'value', 'UnitCD']
    if os.path.exists(synthetic_file):
        fact_file_path = os.path.join(
            Path(synthetic_file).parent, "i2b2", 'devices_facts.csv')

        delete_file_if_exists(fact_file_path)
        mkParentDir(fact_file_path)
    else:
        raise Exception

    with open(synthetic_file, mode='r') as csv_file:
        max_line = file_len(synthetic_file)-1
        write_file_header(fact_file_path, header, delimiter)
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        count = 1
        time = " 00:00:00"
        batch_size = 100
        batch = []
        with alive_bar(max_line, bar='smooth') as bar:
            for row in csv_reader:
                i2b2_row = OrderedDict()
                i2b2_row['EncounterID'] = row['ENCOUNTER']
                i2b2_row['PatientID'] = row['PATIENT']
                i2b2_row['ConceptCD'] = "SNOMED-CT:"+row['CODE']
                i2b2_row['ProviderID'] = "SYNTHEA"
                i2b2_row['StartDate'] = row['START'] + time
                i2b2_row['ModifierCD'] = "@"
                i2b2_row['InstanceNum'] = ""
                i2b2_row['value'] = ""
                i2b2_row['UnitCD'] = ""
                batch.append(i2b2_row)
                if(len(batch) == batch_size):
                    write_to_file(batch, fact_file_path, delimiter, header)
                    batch = []

                bar()

        write_to_file(batch, fact_file_path, delimiter, header)


def csv_rw_imaging_studies(synthetic_file, delimiter):
    """method for transforming synthetic observations to i2b2 format facts

    Args:
        synthetic_file (str): synthetic observations file path
        delimiter (str): delimiter needs to be added for csv operations

    """
    header = ['EncounterID', 'PatientID', 'ConceptCD', 'ProviderID',
              'StartDate', 'ModifierCD', 'InstanceNum', 'value', 'UnitCD']
    if os.path.exists(synthetic_file):
        fact_file_path = os.path.join(
            Path(synthetic_file).parent, "i2b2", 'imaging_studies_facts.csv')

        delete_file_if_exists(fact_file_path)
        mkParentDir(fact_file_path)
    else:
        raise Exception

    with open(synthetic_file, mode='r') as csv_file:
        max_line = file_len(synthetic_file)-1
        write_file_header(fact_file_path, header, delimiter)
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        count = 1
        time = " 00:00:00"
        batch_size = 100
        batch = []
        with alive_bar(max_line, bar='smooth') as bar:
            for row in csv_reader:
                i2b2_row = OrderedDict()
                i2b2_row['EncounterID'] = row['ENCOUNTER']
                i2b2_row['PatientID'] = row['PATIENT']
                i2b2_row['ConceptCD'] = "SNOMED-CT:"+row['BODYSITE_CODE']
                i2b2_row['ProviderID'] = "SYNTHEA"
                i2b2_row['StartDate'] = row['DATE'] + time
                i2b2_row['ModifierCD'] = "@"
                i2b2_row['InstanceNum'] = ""
                i2b2_row['value'] = ""
                i2b2_row['UnitCD'] = ""
                batch.append(i2b2_row)
                if(len(batch) == batch_size):
                    write_to_file(batch, fact_file_path, delimiter, header)
                    batch = []

                bar()

        write_to_file(batch, fact_file_path, delimiter, header)


def csv_rw_medications(synthetic_file, delimiter):
    """method for transforming synthetic observations to i2b2 format facts

    Args:
        synthetic_file (str): synthetic observations file path
        delimiter (str): delimiter needs to be added for csv operations

    """
    header = ['EncounterID', 'PatientID', 'ConceptCD', 'ProviderID',
              'StartDate', 'ModifierCD', 'InstanceNum', 'value', 'UnitCD']
    if os.path.exists(synthetic_file):
        fact_file_path = os.path.join(
            Path(synthetic_file).parent, "i2b2", 'medications_facts.csv')

        delete_file_if_exists(fact_file_path)
        mkParentDir(fact_file_path)
    else:
        raise Exception

    with open(synthetic_file, mode='r') as csv_file:
        max_line = file_len(synthetic_file)-1
        write_file_header(fact_file_path, header, delimiter)
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        count = 1
        time = " 00:00:00"
        batch_size = 100
        batch = []
        with alive_bar(max_line, bar='smooth') as bar:
            for row in csv_reader:
                i2b2_row = OrderedDict()
                i2b2_row['EncounterID'] = row['ENCOUNTER']
                i2b2_row['PatientID'] = row['PATIENT']
                i2b2_row['ConceptCD'] = "RXNORM:"+row['CODE']
                i2b2_row['ProviderID'] = "SYNTHEA"
                i2b2_row['StartDate'] = row['START'] + time
                i2b2_row['ModifierCD'] = "@"
                i2b2_row['InstanceNum'] = ""
                i2b2_row['value'] = ""
                i2b2_row['UnitCD'] = ""
                batch.append(i2b2_row)
                if(len(batch) == batch_size):
                    write_to_file(batch, fact_file_path, delimiter, header)
                    batch = []

                bar()

        write_to_file(batch, fact_file_path, delimiter, header)


def csv_rw_supplies(synthetic_file, delimiter):
    """method for transforming synthetic observations to i2b2 format facts

    Args:
        synthetic_file (str): synthetic observations file path
        delimiter (str): delimiter needs to be added for csv operations

    """
    header = ['EncounterID', 'PatientID', 'ConceptCD', 'ProviderID',
              'StartDate', 'ModifierCD', 'InstanceNum', 'value', 'UnitCD']
    if os.path.exists(synthetic_file):
        fact_file_path = os.path.join(
            Path(synthetic_file).parent, "i2b2", 'supplies_facts.csv')

        delete_file_if_exists(fact_file_path)
        mkParentDir(fact_file_path)
    else:
        raise Exception

    with open(synthetic_file, mode='r') as csv_file:
        max_line = file_len(synthetic_file)-1
        write_file_header(fact_file_path, header, delimiter)
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        count = 1
        time = " 00:00:00"
        batch_size = 100
        batch = []
        with alive_bar(max_line, bar='smooth') as bar:
            for row in csv_reader:
                i2b2_row = OrderedDict()
                i2b2_row['EncounterID'] = row['ENCOUNTER']
                i2b2_row['PatientID'] = row['PATIENT']
                i2b2_row['ConceptCD'] = "SNOMED-CT:"+row['CODE']
                i2b2_row['ProviderID'] = "SYNTHEA"
                i2b2_row['StartDate'] = row['DATE'] + time
                i2b2_row['ModifierCD'] = "@"
                i2b2_row['InstanceNum'] = ""
                i2b2_row['value'] = ""
                i2b2_row['UnitCD'] = ""
                batch.append(i2b2_row)
                if(len(batch) == batch_size):
                    write_to_file(batch, fact_file_path, delimiter, header)
                    batch = []

                bar()

        write_to_file(batch, fact_file_path, delimiter, header)


def csv_rw_conditions(synthetic_file, delimiter):
    """method for transforming synthetic conditions to i2b2 format facts

    Args:
        synthetic_file (str): synthetic observations file path
        delimiter (str): delimiter needs to be added for csv operations

    """
    header = ['EncounterID', 'PatientID', 'ConceptCD', 'ProviderID',
              'StartDate', 'ModifierCD', 'InstanceNum', 'value', 'UnitCD']
    if os.path.exists(synthetic_file):
        fact_file_path = os.path.join(
            Path(synthetic_file).parent, "i2b2", 'conditions_facts.csv')

        delete_file_if_exists(fact_file_path)
        mkParentDir(fact_file_path)
    else:
        raise Exception

    with open(synthetic_file, mode='r') as csv_file:
        max_line = file_len(synthetic_file)-1
        write_file_header(fact_file_path, header, delimiter)
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        count = 1
        time = " 00:00:00"
        batch_size = 100
        batch = []
        with alive_bar(max_line, bar='smooth') as bar:
            for row in csv_reader:

                # START,STOP,PATIENT,ENCOUNTER,CODE,DESCRIPTION
                i2b2_row = OrderedDict()
                i2b2_row['EncounterID'] = row['ENCOUNTER']
                i2b2_row['PatientID'] = row['PATIENT']
                i2b2_row['ConceptCD'] = "SNOMED-CT:"+row['CODE']
                i2b2_row['ProviderID'] = "SYNTHEA"
                i2b2_row['StartDate'] = row['START'] + time
                i2b2_row['ModifierCD'] = "@"
                i2b2_row['InstanceNum'] = ""
                i2b2_row['value'] = ""
                i2b2_row['UnitCD'] = ""
                batch.append(i2b2_row)
                if(len(batch) == batch_size):
                    write_to_file(batch, fact_file_path, delimiter, header)
                    batch = []

                bar()

        write_to_file(batch, fact_file_path, delimiter, header)


def csv_rw_encounter(synthetic_file, delimiter):
    """method for transforming synthetic encounters to i2b2 format encounters

    Args:
        synthetic_file (str): synthetic encounters file path
        delimiter (str): delimiter needs to be added for csv operations

    """
    header = ['EncounterID', 'PatientID', 'StartDate', 'EndDate',
              'ActivityTypeCD', 'ActivityStatusCD', 'ProgramCD']
    if os.path.exists(synthetic_file):
        fact_file_path = os.path.join(
            Path(synthetic_file).parent, "i2b2", 'encounters.csv')

        delete_file_if_exists(fact_file_path)
        mkParentDir(fact_file_path)
    else:
        raise Exception

    with open(synthetic_file, mode='r') as csv_file:
        max_line = file_len(synthetic_file)-1
        write_file_header(fact_file_path, header, delimiter)
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        count = 1
        batch_size = 100
        batch = []
        with alive_bar(max_line, bar='smooth') as bar:
            for row in csv_reader:
                i2b2_row = OrderedDict()
                i2b2_row['EncounterID'] = row['Id']
                i2b2_row['PatientID'] = row['PATIENT']
                start_date = row['START']
                i2b2_row['StartDate'] = start_date.replace(
                    "T", " ").replace("Z", "")
                end_date = row['STOP']
                i2b2_row['EndDate'] = end_date.replace(
                    "T", " ").replace("Z", "")
                i2b2_row['ActivityTypeCD'] = row['ENCOUNTERCLASS']
                i2b2_row['ActivityStatusCD'] = row['DESCRIPTION']
                i2b2_row['ProgramCD'] = row['CODE']
                batch.append(i2b2_row)
                if(len(batch) == batch_size):
                    write_to_file(batch, fact_file_path, delimiter, header)
                    batch = []

                bar()

        write_to_file(batch, fact_file_path, delimiter, header)


def csv_rw_mrn(synthetic_file, delimiter):
    """method for transforming synthetic patients to i2b2 format patients

    Args:
        synthetic_file (str): synthetic patients file path
        delimiter (str): delimiter needs to be added for csv operations

    """
    header = ['SYNTHEA']
    if os.path.exists(synthetic_file):
        fact_file_path = os.path.join(
            Path(synthetic_file).parent, "i2b2", 'mrn.csv')

        delete_file_if_exists(fact_file_path)
        mkParentDir(fact_file_path)
    else:
        raise Exception

    with open(synthetic_file, mode='r') as csv_file:
        max_line = file_len(synthetic_file)-1
        write_file_header(fact_file_path, header, delimiter)
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        count = 1
        batch_size = 100
        batch = []
        with alive_bar(max_line, bar='smooth') as bar:
            for row in csv_reader:
                i2b2_row = OrderedDict()
                i2b2_row['SYNTHEA'] = row['Id']
                batch.append(i2b2_row)
                if(len(batch) == batch_size):
                    write_to_file(batch, fact_file_path, delimiter, header)
                    batch = []

                bar()

        write_to_file(batch, fact_file_path, delimiter, header)


def write_file_header(file_path, header, delimiter):
    """This method writes the header to the file using csv writer

    Args:
        file_path (:obj:`str`, mandatory): Path to the file.
        header (:obj:`str`, mandatory): headers to be written to the files.
        delimiter (:obj:`str`, mandatory): delimiter needs to be added to csv file

    """
    try:
        with open(file_path, 'a+') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=header, delimiter=delimiter)
            writer.writeheader()
    except Exception as e:
        raise e


def write_to_file(batch, file_path, delimiter, header):
    """This method writes the list of rows to the file using csv writer

    Args:
        batch (:obj:`str`, mandatory): List of records to be written to the file.
        file_path (:obj:`str`, mandatory): Path to the output file.
        delimiter (:obj:`str`, mandatory): Delimeter to be used in csv file.
        header (:obj:`str`, mandatory): headers to which the records to be written.

    """
    try:
        with open(file_path, 'a+') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=header, delimiter=delimiter, lineterminator='\n')
            writer.writerows(batch)
    except Exception as e:
        raise e


def mkParentDir(file_path):
    """This method create the paranet directory for the provided file path

    Args:
        file_path (:obj:`str`, mandatory): Path to the file.

    """
    if not os.path.exists(file_path):
        return Path(Path(file_path).parent).mkdir(parents=True, exist_ok=True)


def delete_file_if_exists(file_path):
    """This method deletes the provided file

    Args:
        file_path (:obj:`str`, mandatory): Path to the file to be deleted.

    """
    if os.path.exists(file_path):
        os.remove(file_path)


def file_len(fname):
    """Provide the total number of line counts for the specified file

    Args:
       fname (str): name or path of the file for which, the lines to be calculated

    Returns:
        int: count of total number of lines from the provided file

    """
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])


def procedures_to_obsfacts(synthetic_file, delimiter):
    """method for transforming synthetic observations to i2b2 format facts

    Args:
        synthetic_file (str): synthetic observations file path
        delimiter (str): delimiter needs to be added for csv operations

    """
    # Procedures Headers = [DATE,PATIENT,ENCOUNTER,CODE,DESCRIPTION,BASE_COST,REASONCODE,REASONDESCRIPTION]
    header = ['EncounterID', 'PatientID', 'ConceptCD', 'ProviderID',
              'StartDate', 'ModifierCD', 'InstanceNum', 'value', 'UnitCD']
    if os.path.exists(synthetic_file):
        fact_file_path = os.path.join(
            Path(synthetic_file).parent, "i2b2", 'procedures_facts.csv')

        delete_file_if_exists(fact_file_path)
        mkParentDir(fact_file_path)
    else:
        raise Exception

    with open(synthetic_file, mode='r') as csv_file:
        max_line = file_len(synthetic_file)-1
        write_file_header(fact_file_path, header, delimiter)
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        count = 1
        time = " 00:00:00"
        batch_size = 100
        batch = []
        with alive_bar(max_line, bar='smooth') as bar:
            for row in csv_reader:
                i2b2_row = OrderedDict()
                i2b2_row['EncounterID'] = row['ENCOUNTER']
                i2b2_row['PatientID'] = row['PATIENT']
                i2b2_row['ConceptCD'] = 'SNOMED-CT:' + row['CODE']
                i2b2_row['ProviderID'] = "SYNTHEA"
                i2b2_row['StartDate'] = row['DATE'] + time
                i2b2_row['ModifierCD'] = "@"
                i2b2_row['InstanceNum'] = ""
                i2b2_row['value'] = ""
                i2b2_row['UnitCD'] = ''
                batch.append(i2b2_row)
                if(len(batch) == batch_size):
                    write_to_file(batch, fact_file_path, delimiter, header)
                    batch = []

                bar()

        write_to_file(batch, fact_file_path, delimiter, header)


if __name__ == '__main__':
    print("Transforming synthetic observations to i2b2 observations...")
    csv_rw_fact('data/synthea/observations.csv', ',')

    print("Transforming synthetic encounters to i2b2 encounters...")
    csv_rw_encounter('data/synthea/encounters.csv', ',')

    print("Transforming synthetic patients to i2b2 mrn...")
    csv_rw_mrn('data/synthea/patients.csv', ',')

    print("Transforming synthetic conditions to i2b2 observations...")
    csv_rw_conditions('data/synthea/conditions.csv', ',')

    print("Transforming synthetic procedures to i2b2 observation facts...")
    procedures_to_obsfacts('data/synthea/procedures.csv', ',')

    print("Transforming synthetic allergies to i2b2 observation facts...")
    csv_rw_allergies('data/synthea/allergies.csv', ',')

    print("Transforming synthetic careplans to i2b2 observation facts...")
    csv_rw_careplans('data/synthea/careplans.csv', ',')

    print("Transforming synthetic devices to i2b2 observation facts...")
    csv_rw_devices('data/synthea/devices.csv', ',')

    print("Transforming synthetic imaging_studies to i2b2 observation facts...")
    csv_rw_imaging_studies('data/synthea/imaging_studies.csv', ',')

    print("Transforming synthetic medications to i2b2 observation facts...")
    csv_rw_medications('data/synthea/medications.csv', ',')

    print("Transforming synthetic supplies to i2b2 observation facts...")
    csv_rw_supplies('data/synthea/supplies.csv', ',')
