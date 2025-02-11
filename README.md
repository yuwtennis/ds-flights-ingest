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
| java              | 1.8.0_432                                                     |
| flyway opensource | [11.3.1](https://github.com/flyway/flyway/tree/flyway-11.3.1) |
| terraform         | see [main.tf](terraform/main.tf)                              |

## Tutorial

### Prepare environment

1 Set up gcloud

Follow official guide on cloud sdk, [gcloud cli](https://cloud.google.com/sdk/docs/install) .

2 Set up cloud resource

```shell
cd terraform
terraform init
terraform plan
terraform apply
```

3 Run DDL statements on bigquery  

First setup flyway environment accordingly. Flyway required jdbc lib specific to biguqery (see [doc](https://documentation.red-gate.com/fd/google-bigquery-277579314.html)).
I used the [Command-line style of opensource version](https://documentation.red-gate.com/flyway/getting-started-with-flyway/quickstart-guides/quickstart-command-line).  

```shell
cd flyway
./flyway migration
```


### Ingest data as data-in-place style

```shell
cd script
bash ingest.sh -y YEAR -s START_MONTH -e END_MONTH
```