# GCP_CloudStorage_To_BigQuery_Ingestion


Agenda is to ingest the files from Google cloud storage to Big Query using a Cloud function.

## GCP Services Used :
1. Google Cloud Function
2. Google Cloud Storage
3. Big Query
4. Pub/Sub 
5. Cloud Scheduler 

## Prerequisite 
Create a Google cloud account and create a project.

## Steps 

### Create a bucket and place the file in Google Cloud Storage

1. Login to your project and open "Cloud Storage" service and Create a Bucket.
2. Upload the Source/input file in the bucket.(Please find in Github repository)


###  Create a table in Big Query.
1. Run the DDL. (Please find in Github repository)

###  Create a Pub sub topic
1. Topic Name 

###  Create a Cloud function

requirements.txt 
pandas
google-cloud-bigquery
google-cloud-storage

main.py 
def gcs_to_bq(event=None, context=None):
    try:

        PROJECT_ID ='clever-tooling-352705'

        # Google storage bucket and source file details
        BUCKET_NAME = 'myfirstbucket44'
        BUCKET_FOLDER = 'Sales'
        FILE_NAME_PATTERN = 'Sales Data 2022-07-15.csv'

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
        uri = "gs://" + BUCKET_NAME +"/"+ BUCKET_FOLDER +"/" + FILE_NAME_PATTERN

        load_job = Client.load_table_from_uri(
            uri, TABLE_ID, job_config=job_config
        )  # Make an API request.

        load_job.result()  # Waits for the job to complete.

        destination_table = Client.get_table(TABLE_ID)  # Make an API request.
        print("Loaded {} rows.".format(destination_table.num_rows))

    except:
        print('nothing here today ',datetime)
        pass

