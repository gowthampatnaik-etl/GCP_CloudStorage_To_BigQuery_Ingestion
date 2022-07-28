# GCP_CloudStorage_To_BigQuery_Ingestion


Agenda is to ingest the files from Google cloud storage to Big Query using a Cloud function.

## Prerequisite 
Create a Google cloud account and create a project.

## GCP Services Used :
1. Google Cloud Function
2. Google Cloud Storage
3. Big Query
4. Pub/Sub 
5. Cloud Scheduler 


## Steps 

### Create a bucket and place the file in Google Cloud Storage

1. Login to your project and open "Cloud Storage" service and Create a Bucket.
2. Upload the Source/input file in the bucket.(Please find in Github repository)

    <img src="https://user-images.githubusercontent.com/102896115/181431544-ec0f2697-b142-437f-8ada-275bee16230d.png" width="800" height="300">

###  Create a table in Big Query.
1. Run the DDL. (Please find in Github repository)

###  Create a Pub sub topic
1. Topic Name - Cloud scheduler will send a message to cloud function though topic and triggers cloud function.

    <img src="https://user-images.githubusercontent.com/102896115/181421836-457ff5aa-c91b-4ae1-bd51-0e02bc72a219.png" width="800" height="300">


###  Create a Cloud function
Cloud function will gets triggered once the message from topic is received and ingests the data from Cloud storage to Big Query.

Steps to create cloud functionn :
1. Create a Cloud function from the GCP service as shown below -

    <img src="https://user-images.githubusercontent.com/102896115/181422314-67aabe72-3d40-45d2-a351-6f68e780a69f.png" width="800" height="300">
2. Select the trigger type as Pub/Sub and Select the topic that was created.
    
    <img src="https://user-images.githubusercontent.com/102896115/181431132-6ff5da82-aa70-441d-880a-0847b1c3b4a4.png" width="800" height="400">
3. Click on next and chnage the runtime to Python 3.7 and type the entry point (gcs_to_bq). Copy the requirement.txt and main.py code then click on deplot to deploy      the code.
    
    <img src="https://user-images.githubusercontent.com/102896115/181422755-e5c6a8fc-e5a5-4c7d-bf71-b7f518fa124a.png" width="800" height="500">

requirements.txt 
```
pandas
google-cloud-bigquery
google-cloud-storage
```

main.py 
```
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
```

###  Create a Cloud Scheduler

    <img src="https://user-images.githubusercontent.com/102896115/181432424-0eff779c-c9ba-4a06-9c33-ba38cc695cfe.png" width="800" height="300">
    
    <img src="https://user-images.githubusercontent.com/102896115/181432478-fb6fcd99-dc1f-445d-90a2-95cc1284c01a.png" width="800" height="400">
    


