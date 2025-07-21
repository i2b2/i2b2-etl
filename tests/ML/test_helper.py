import uuid,sys
sys.path.append('/home/kwig/code/i2b2-etl/')
import datetime, time
from pathlib import Path
from i2b2_cdi.config.config import Config
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from loguru import logger
from i2b2_cdi.config.config import Config
import i2b2_cdi.fact.runner as fact_runner
import i2b2_cdi.concept.runner as concept_runner

config = Config().new_config(argv=[
    "concept", "load",
    "--input-dir", ''
])

def create_patient_set(project_id, user_id, query_name, sql_patient_query, max_patients=None):
    """
    Creates a patient set in i2b2 from a SQL query.
    """
    import datetime
    timestamp = datetime.datetime.now()

    # Request XML so the query appears in the webclient
    request_xml = """
        <query_definition>
            <query_name>{query_name}</query_name>
            <query_timing>SAME</query_timing>
            <panel>
                <panel_number>1</panel_number>
                <invert>0</invert>
                <panel_timing>SAME</panel_timing>
                <total_item_occurrences>1</total_item_occurrences>
                <item>
                    <item_key>\\i2b2\\Diagnoses\\ICD10\\E11\\</item_key>
                    <item_name>Type 2 Diabetes Mellitus</item_name>
                    <tooltip>Type 2 Diabetes Mellitus</tooltip>
                    <class>ENC</class>
                    <hlevel>4</hlevel>
                    <operator>EQ</operator>
                </item>
            </panel>
        </query_definition>
    """.format(query_name=query_name)

    with I2b2crcDataSource(config) as cursor:
        logger.info("Creating patient set...")

        # Insert into QT_QUERY_MASTER
        cursor.execute("""
            INSERT INTO QT_QUERY_MASTER (
                name,
                user_id,
                group_id,
                create_date,
                delete_flag,
                request_xml
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING query_master_id
        """, (query_name, user_id, project_id, timestamp, 'N', request_xml))
        query_master_id = cursor.fetchone()[0]
        logger.info(f"Created QT_QUERY_MASTER with ID {query_master_id}")

        # Insert into QT_QUERY_INSTANCE
        cursor.execute("""
            INSERT INTO QT_QUERY_INSTANCE (
                query_master_id,
                user_id,
                group_id,
                start_date,
                end_date,
                status_type_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING query_instance_id
        """, (query_master_id, user_id, project_id, timestamp, timestamp, 3))  # status_type_id=3: Finished
        query_instance_id = cursor.fetchone()[0]
        logger.info(f"Created QT_QUERY_INSTANCE with ID {query_instance_id}")

        # Fetch patients
        fetch_sql = f"""
            SELECT DISTINCT patient_num
            FROM ({sql_patient_query}) AS subquery
        """
        if max_patients:
            fetch_sql += f" LIMIT {int(max_patients)}"

        logger.info("Fetching patient numbers...")
        cursor.execute(fetch_sql)
        rows = cursor.fetchall()
        num_patients = len(rows)

        # Insert into QT_QUERY_RESULT_INSTANCE
        cursor.execute("""
            INSERT INTO QT_QUERY_RESULT_INSTANCE (
                query_instance_id,
                result_type_id,
                set_size,
                start_date,
                end_date,
                status_type_id,
                description
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING result_instance_id
        """, (
            query_instance_id,
            1,              # result_type_id=1: patient set
            num_patients,   # set_size
            timestamp,
            timestamp,
            3,              # status_type_id=3: Finished
            'Patient Set for "{}"'.format(query_name)
        ))
        result_instance_id = cursor.fetchone()[0]
        logger.info(f"Created QT_QUERY_RESULT_INSTANCE with ID {result_instance_id}")

        if not rows:
            logger.warning("No patients found for the query.")
        else:
            # Insert patients
            insert_sql = """
                INSERT INTO QT_PATIENT_SET_COLLECTION (
                    result_instance_id,
                    patient_num
                )
                VALUES (%s, %s)
            """
            for row in rows:
                patient_num = row[0]
                cursor.execute(insert_sql, (result_instance_id, patient_num))
            logger.info(f"Inserted {num_patients} patients into QT_PATIENT_SET_COLLECTION.")

        # Commit everything
        cursor.connection.commit()

        logger.info(f"✅ Created patient set with {num_patients} patients.")
        return result_instance_id
