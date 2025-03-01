
from __future__ import annotations
import time
import json
import io
from datetime import datetime
from airflow.models import Variable
from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.python import PythonOperator
from google.cloud import storage
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import pandas as pd

# Dag name
DAG_ID = "Station_lyon"
blob_name = 'lyon_data'
var_bucket = Variable.get('BUCKET_NAME')
var_project = Variable.get('PROJECT_ID')

current_timestamp = time.time()
current_time_struct = time.localtime(current_timestamp)
current_date_str = time.strftime("%Y%m%d", current_time_struct)
current_timestamp_for_bq = time.strftime("%Y-%m-%d %H:%M:%S", current_time_struct)
current_timestamp_str = time.strftime("%Y%m%d_%H%M%S", current_time_struct)

# DAG definitions with all required params
dag = DAG(
    DAG_ID,
    default_args={"retries": 1},
    tags=["lyon"],
    start_date=datetime(2023, 4, 26),
    catchup=False,
    schedule_interval = '20 * * * *'
)

def transform_data(ti):
    """
    Extract needed fields from JSON response for Lyon stations.
    Returns a dictionary.
    """
    data = ti.xcom_pull(task_ids='extract_data_task')
    if not data:
        raise ValueError("No data found from extract_data_task")

    station_dic = {
        'address': [],
        "address_jcd": [],
        "availability": [],
        "availabilitycode": [],
        "available_bike_stands": [],
        "available_bikes": [],
        "banking": [],
        "bike_stands": [],
        "bonus": [],
        "code_insee": [],
        "commune": [],
        "gid": [],
        "last_update": [],
        "last_update_fme": [],
        "last_update_gl": [],
        "lat": [],
        "lng": [],
        "bikes": [],
        "electricalBikes": [],
        "electricalInternalBatteryBikes": [],
        "electricalRemovableBatteryBikes": [],
        "mechanicalBikes": [],
        "stands": []
    }

    dic_keys = list(station_dic.keys())

    print(f'🛠️ extracting Lyon JSON data...')
    stations = data['values']
    for station in stations:
        for key in dic_keys:
            if key in station:
                station_dic[key].append(station.get(key))
            else:
                sub_json = station.get('main_stands', {})
                if key not in sub_json:
                    sub_json = sub_json.get('availabilities', {})
                station_dic[key].append(sub_json.get(key))

    print(f'✅ Lyon stations JSON data extracted')
    return station_dic

def load_data_to_dataframe_to_csv_to_bucket(ti):
    """
    Load extracted data into a pandas DataFrame to csv.
    """
     # get current time to add it in blob name
    blob_full_name = f'{blob_name}/{blob_name}_{current_date_str}/{blob_name}_{current_timestamp_str}.csv'
    # Initialize a GCS client
    client = storage.Client()
    # Get the bucket

    bucket = client.bucket(Variable.get('BUCKET_NAME'))
    # Create a new blob (object) in the bucket
    blob = bucket.blob(blob_full_name)
    
    
    station_dic = ti.xcom_pull(task_ids='transform_data_task')
    # df = ti.xcom_pull(task_ids='load_data_to_dataframe')
    if not station_dic:
        raise ValueError("No data found from transform_data_task task")

    df = pd.DataFrame(station_dic)
    df['GCS_loaded_at'] = current_timestamp_for_bq
    print(f'✅ Data loaded into DataFrame')
    # Convert the DataFrame to a CSV string
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    # Upload the CSV string to the blob
    blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')
    print(f"✅ DataFrame uploaded to {blob_full_name} in bucket {Variable.get('BUCKET_NAME')}")

def load_data_gs_bigquery():
    """
    function to load the csv from a bucket folder to big query
    here the GCS bucket folder take the same name of the Big Query Dataset
    """
    blob_full_name = f'{blob_name}/{blob_name}_{current_date_str}/{blob_name}_{current_timestamp_str}.csv'
    gcs_uri = f'gs://{var_bucket}/{blob_full_name}'
    
    # Initialize a BigQuery client
    client = bigquery.Client(Variable.get('PROJECT_ID'))
    # dataset id in Big Query will have the same name of data folder in GCS
    dataset_ref = client.dataset(blob_name)
    # test if the dataset exists in BQ, create it if not
    try:      
        client.get_dataset(dataset_ref)
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "EU"  # Vous pouvez spécifier une autre région si nécessaire
        dataset = client.create_dataset(dataset)

    table_id = f'{blob_name}_{current_date_str}'
    print(f'🛠️ Loading data into BigQuery...')

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip header row if present
        autodetect=True,  # Automatically detect schema
    )
    # Load data into BigQuery
    load_job = client.load_table_from_uri(
        source_uris = gcs_uri,
        destination = f'{var_project}.{blob_name}.{table_id}',
        job_config=job_config
    )

    # Wait for the job to complete
    load_job.result()

    print(f'✅ Loaded {load_job.output_rows} rows into {var_project}:{blob_name}.{table_id}.') 

# Task to get data from given HTTP end point
extract_data_task = HttpOperator(
    task_id="extract_data_task",
    http_conn_id="http_conn_id_velo_lyon",
    method="GET",
    endpoint="/fr/datapusher/ws/rdata/jcd_jcdecaux.jcdvelov/all.json?maxfeatures=-1&filename=stations-velo-v-metropole-lyon-disponibilites-temps-reel",
    response_filter = lambda response : json.loads(response.text),
    dag=dag
)

transform_data_task = PythonOperator(
    task_id='transform_data_task',
    python_callable=transform_data
)

load_data_bucket_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data_to_dataframe_to_csv_to_bucket,
    dag=dag
)

load_data_to_bq = PythonOperator(
    task_id='load_data_to_bq',
    python_callable=load_data_gs_bigquery,
    dag=dag
)


# Task dependency set
extract_data_task >> transform_data_task >> load_data_bucket_task >> load_data_to_bq

