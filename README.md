# ETL Process for Sparkify DB using AWS Datawarehouse(Redshift)

This is my third project for the Udacity Nanodegree of Data Engineering. It is about an etl process (AWS Redshift based) for Sparkify.

Sparkify is a simulated (not-real) online music streaming service.

This Git repository shows how to script an etl process for loading data from json raw data to a AWS Redshift Sataewarehouse (DWH) and for creating fact and dimension tables there in that manner. Basically itz is a littöe bit similar to the first NDDE project (see here: https://github.com/ChristophGmeiner/UdacityNDDE1_ETLPostgres)

This is done using Python.

## Purpose of the Database sparkifydb

The sparkifydb database is postgre SQL based and is about storing information about songs and listening behaviour of the users.

The analytical goal of this database to get all kings of insight into the user beahviour.

## Description of the ETL Pipeline

### Description of the raw Datasets

Raw data comes in json formats and is stored in several subdirectories in AWS S3 buckets.

#### log data
This directory contains jsons which show basically user activity per day on Sparkify.

#### song data
This directory contains jsons which show basically available songs and artists on Sparkify.

### Scripts and Files
