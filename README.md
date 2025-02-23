# About this repository

My personal implementation for the book, [Data Science on Google Cloud Platform, 2nd edition](https://www.amazon.com/Data-Science-Google-Cloud-Platform/dp/1098118952).  
For the official repository, see [GoogleCloudPlatform/data-science-on-gcp](https://github.com/GoogleCloudPlatform/data-science-on-gcp).

It will be a great pleasure if the code base can help viewers in some way.

My previous archived repos is [yuwtennis/google-data-engineer](https://github.com/yuwtennis/google-data-engineer)
Please feel free to send any comments to me.
@yuwtennis

## Pre-requisite

Below tool will be required when running on local pc.  
_Tested version_ in the table represents the version which I have used for testing.

| Tool name         | Tested version                                                |
|-------------------|---------------------------------------------------------------|
| gcloud            | 486.0.0                                                       |
| bq                | 2.1.7                                                         |
| gsutil            | 5.30                                                          | 

## Tutorial

### Prepare environment

1 Set up gcloud

Follow official guide on cloud sdk, [gcloud cli](https://cloud.google.com/sdk/docs/install) .

2 Set up cloud resource

See README in [data-science-with-flights-iac](https://github.com/yuwtennis/data-science-with-flights-iac)

3 Run DDL statements on bigquery  

See README in [data-science-with-flights-ddl](https://github.com/yuwtennis/data-science-with-flights-ddl)

### Ingest data as data-in-place style

#### Shell script

```shell
cd script
bash ingest.sh -y YEAR -s START_MONTH -e END_MONTH
```

#### Python

Set environment variables in advance.

| Key              | Description                                 |
|------------------|---------------------------------------------|
| GC_PROJECT_ID    | YOUR Google Cloud project ID                |
| GCS_BUCKET       | Google Storage Bucket Name to upload csv to |
| BQ_DEST_TBL_FQDN | Bigquery Table FQDN to upload csv data to   |
| YEAR             | Year of the csv to download                 |
| MONTH            | 2 digit month of the csv to download        |

Run the script

```shell
poetry run python3.11 __main__.py \
  --bucket YOURBUCKET \
  --year YEAR \
  --month MONTH \
  --project GOOGLE_CLOUD_PROJECT_ID \
  --bq_dest_tbl_fqdn BQ_TBL_FQDN
```