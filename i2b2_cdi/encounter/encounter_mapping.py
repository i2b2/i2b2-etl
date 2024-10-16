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

"""
:mod:`encounter_mapping` -- Create/Get encounter mapping
========================================================

.. module:: encounter_mapping
    :platform: Linux/Windows
    :synopsis: module contains method for creating, retriving encounter mapping from i2b2 instance

"""

from loguru import logger
from alive_progress import alive_bar, config_handler
from Mozilla.mozilla_encounter_mapping import MozillaEncounterMapping
config_handler.set_global(length=50, spinner='triangles')


class EncounterMapping(MozillaEncounterMapping):
    """The class provides the interface for de-identifying i.e. (mapping src encounter id to i2b2 generated encounter num) encounter file"""

    def __init__(self): 
        super().__init__()

    def create_encounter_mapping(self, csv_file_path, encounter_mapping_file_path,config):  
        super().create_encounter_mapping(self, csv_file_path, encounter_mapping_file_path,config)

    def prepare_encounter_mapping(self, encounter_num, encounter_id, encounter_src, patient_id): 
        """This method writes encounter mapping to the database table using pyodbc connection cursor

        Args:
            encounter_num (:obj:`str`, mandatory): I2b2 mapped encounter id.
            encounter_id (:obj:`str`, mandatory): Src encounter id.
            encounter_src (:obj:`str`, mandatory): Encounter source.
            patient_id (:obj:`str`, mandatory): Src petient id.
        """
        try:
            self.new_encounter_map.update(
                {encounter_id: [encounter_num, encounter_src, patient_id]})
        except Exception as e:
            raise e

    def check_if_encounter_exists(self, encounter_id, encounter_map): 
        super().check_if_encounter_exists(self, encounter_id, encounter_map)

    def get_max_encounter_num(self,config): 
        super().get_max_encounter_num(self,config)


    def write_encounter_mapping(self, encounter_mapping_file_path, bcp_file_delimiter, source_system_cd, upload_id): 
        """This method writes encounter mappings in a csv file

        Args:
            encounter_mapping_file_path (:obj:`str`, mandatory): Path to the output csv file.
            bcp_file_delimiter (:obj:`str`, mandatory): Delimiter of the bcp file.
        """
        try:
            batch = []
            if len(self.new_encounter_map) != 0:
                logger.debug("Writing encounter_mapping bcp file \n")
                max_records = len(self.new_encounter_map)
                with alive_bar(max_records, bar='smooth') as bar:
                    for mapping in self.new_encounter_map:
                        value = self.new_encounter_map.get(mapping)
                        _row = [mapping, value[1], 'DEMO', str(
                            value[0]), value[2], 'DEMO', '', '', '', '', self.import_time, source_system_cd, str(upload_id)]
                        batch.append(_row)
                        if(len(batch) == self.write_batch_size):
                            self.write_to_bcp_file(
                                batch, encounter_mapping_file_path, bcp_file_delimiter)
                            batch = []
                        bar()
                # Write remaining records in map
                self.write_to_bcp_file(
                    batch, encounter_mapping_file_path, bcp_file_delimiter)
                print('\n')
        except Exception:
            raise

    def write_to_bcp_file(self, _valid_rows_arr, bcp_file_path, bcp_delimiter):
        """This method writes the list of rows to the bcp file using csv writer

        Args:
            _valid_rows_arr (:obj:`str`, mandatory): List of valid patients to be written into bcp file.
            bcp_file_path (:obj:`str`, mandatory): Path to the output bcp file.
            bcp_delimiter (:obj:`str`, mandatory): Delimeter to be used in bcp file.

        """
        try:
            with open(bcp_file_path, 'a+') as csvfile:
                for _arr in _valid_rows_arr:
                    csvfile.write(bcp_delimiter.join(_arr) + "\n")
        except Exception as e:
            raise e


def create_encounter_mapping(csv_file_path,config): 
    from Mozilla.mozilla_encounter_mapping import create_encounter_mapping as mozilla_create_encounter_mapping
    return (mozilla_create_encounter_mapping(csv_file_path,config))

def get_encounter_mapping(config): 
    from Mozilla.mozilla_encounter_mapping import get_encounter_mapping as mozilla_get_encounter_mapping
    mozilla_get_encounter_mapping(config)   
