# ETL Process for Sparkify DB using AWS Datawarehouse(Redshift)

This is my third project for the Udacity Nanodegree of Data Engineering. It is about an etl process (AWS Redshift based) for Sparkify.

Sparkify is a simulated (not-real) online music streaming service.

This Git repository shows how to script an etl process for loading data from json raw data to a AWS Redshift Datawarehouse (DWH) and for creating fact and dimension tables there in that manner. Basically it is a little bit similar to the first NDDE project (see here: https://github.com/ChristophGmeiner/UdacityNDDE1_ETLPostgres)

This is done using Python.

## Purpose of the Database sparkifydb

The sparkifydb database is postgre SQL based and is about storing information about songs and listening behaviour of the users.

The analytical goal of this database to get all kings of insight into the user beahviour.

## Description of the ETL Pipeline
All confidential information needed for connecting to AWS is stored in a local file (not part of this repo), i.e. dwh.cfg. See the scripts for details on that.

### Description of the raw Datasets

Raw data comes in json formats and is stored in several subdirectories in a AWS S3 bucket.

#### log data
This directory contains jsons which show basically user activity per day on Sparkify.

#### song data
This directory contains jsons which show basically available songs and artists on Sparkify.

### Scripts and Files

#### sql_queries.py
This Python script contains all necessary SQL scripts to extract the data from the S3-stored json files to staging tables in AWS Redshift, transform it to fact and dimension tables and load these into the final tables.
Also all necessary tables are created in there. This commands of this script are used in later scripts.

#### create_tables.py
Creates all necessary tables in AWS Redshift (based on sql_queries.py)

#### etl.py

#### s3_inspect.ipynb
This notebook shows a possible way to inspect the contents of S3 buckets.