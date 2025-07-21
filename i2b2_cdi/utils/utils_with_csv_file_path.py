from datetime import datetime
from pathlib import Path
import shutil
import pandas as pd
from loguru import logger
from i2b2_cdi.config.config import Config
import i2b2_cdi.fact.runner as fact_runner
import i2b2_cdi.concept.runner as concept_runner

def load_concepts(csv_file_path, rm_tmp_dir=False):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    outDir = '/usr/src/app/tmp/{}/output'.format(timestamp)
    Path(outDir).mkdir(parents=True, exist_ok=True)

    # Destination path
    fpath = outDir + '/concepts.csv'

    # Copy the CSV file
    shutil.copy(csv_file_path, fpath)

    # Count rows
    df = pd.read_csv(fpath)
    num_concepts = len(df)

    conceptLoad = ['concept', 'load', '-i', outDir]
    logger.debug(f"conceptLoad command: {conceptLoad}")

    config = Config().new_config(argv=conceptLoad)
    conceptsErrorsList = concept_runner.mod_run(config)

    if rm_tmp_dir:
        shutil.rmtree(Path(outDir).parent)

    # Build report dictionary
    report = {
        "timestamp": timestamp,
        "csv_file": csv_file_path,
        "uploaded": num_concepts,
        "errors": conceptsErrorsList
    }

    return report

def load_facts(csv_file_path, rm_tmp_dir=False, args=[]):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    outDir = '/usr/src/app/tmp/{}/output'.format(timestamp)
    Path(outDir).mkdir(parents=True, exist_ok=True)

    # Destination path
    fpath = outDir + '/facts.csv'

    # Copy the CSV file
    shutil.copy(csv_file_path, fpath)

    # Count rows
    df = pd.read_csv(fpath)
    num_facts = len(df)

    factLoad = ['fact', 'load', '-i', outDir]+args
    logger.info(f"factLoad command: {factLoad}")

    config = Config().new_config(argv=factLoad)
    factsErrorsList = fact_runner.mod_run(config)

    if rm_tmp_dir:
        shutil.rmtree(Path(outDir).parent)

    # Build report dictionary
    report = {
        "timestamp": timestamp,
        "csv_file": csv_file_path,
        "uploaded": num_facts,
        "errors": factsErrorsList
    }

    return report
