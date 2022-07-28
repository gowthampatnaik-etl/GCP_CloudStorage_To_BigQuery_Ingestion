

#### gcs_to_bq Function

-------------------------------------------------------------requirements.txt--------------------------------------------------------

# Function dependencies, for example:
# package>=version
pandas
google-cloud-bigquery
google-cloud-storage


-------------------------------------------------------------main.py-----------------------------------------------------------------


import pandas 
import datetime
from google.cloud import bigquery
from google.cloud import storage
from google.cloud.exceptions import NotFound

# Open Google cloud and navigate to IAM&ADMIN then click on Service accounts . Select your project and Navigate to keys tab.Click on Add key, Then a new key will be generated in JSON format. 
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'clever-tooling-352705-1cb0301c4bc3.json'

def gcs_to_bq(event=None, context=None):
    try:

        PROJECT_ID ='clever-tooling-352705'

        # Google storage bucket and source file details
        BUCKET_NAME = 'myfirstbucket44'
        BUCKET_FOLDER = 'Sales'
        
        # List the cloud storage bucket and get the filename
        storage_client = storage.Client()
        blobs = storage_client.list_blobs(BUCKET_NAME, prefix='Sales', delimiter='/')
        for blob in blobs:
            FILE_NAME_PATTERN = blob.name
            print(FILE_NAME_PATTERN)

        # Big Query table details
        DATASET = 'sales'
        TABLE ='sales' 

        # table_id = "your-project.your_dataset.your_table_name"
        TABLE_ID = PROJECT_ID+"."+DATASET+"."+TABLE

        # Construct a BigQuery client object.
        Client =  bigquery.Client(project=PROJECT_ID)

        schema = [
                    bigquery.SchemaField('Region', 'STRING', mode='NULLABLE'),
                    bigquery.SchemaField('Country', 'STRING', mode='NULLABLE'),
                    bigquery.SchemaField('Item_Type', 'STRING', mode='NULLABLE'),
                    bigquery.SchemaField('Sales_Channel', 'STRING', mode='NULLABLE'),
                    bigquery.SchemaField('Order_Priority', 'STRING', mode='NULLABLE'),
                    bigquery.SchemaField('Order_Date', 'STRING', mode='NULLABLE'),
                    bigquery.SchemaField('Order_ID', 'STRING', mode='NULLABLE'),
                    bigquery.SchemaField('Ship_Date', 'STRING', mode='NULLABLE'),
                    bigquery.SchemaField('Units_Sold', 'FLOAT', mode='NULLABLE'),
                    bigquery.SchemaField('Units_Price', 'FLOAT', mode='NULLABLE'),   
                    bigquery.SchemaField('Units_Cost', 'FLOAT', mode='NULLABLE'),
                    bigquery.SchemaField('Total_Revenue', 'FLOAT', mode='NULLABLE'),
                    bigquery.SchemaField('Total_Cost', 'FLOAT', mode='NULLABLE'),
                    bigquery.SchemaField('TOtal_Profit', 'FLOAT', mode='NULLABLE')
                ]


        #Load data from Google Clous Storage bucket to BQ table
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            skip_leading_rows=1,
            # The source format defaults to CSV, so the line below is optional.
            source_format=bigquery.SourceFormat.CSV,
        )
        uri = "gs://" + BUCKET_NAME  +"/" + FILE_NAME_PATTERN

        load_job = Client.load_table_from_uri(
            uri, TABLE_ID, job_config=job_config
        )  # Make an API request.

        load_job.result()  # Waits for the job to complete.

        destination_table = Client.get_table(TABLE_ID)  # Make an API request.
        print("Loaded {} rows.".format(destination_table.num_rows))

        # Move the file to archive folder once the process is completed
        bucket = storage_client.get_bucket(BUCKET_NAME)
        blob = bucket.get_blob(FILE_NAME_PATTERN)
        print(blob.name)
        bucket.rename_blob(blob, 'archive/'+FILE_NAME_PATTERN)

    except:
        print('nothing here today ',datetime)
        pass
