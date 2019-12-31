# ETL Process for Sparkify DB using AWS Datawarehouse(Redshift)

This is my third project for the Udacity Nanodegree of Data Engineering. It is about an etl process (AWS Redshift based) for Sparkify.

Sparkify is a simulated (not-real) online music streaming service.

This Git repository shows how to script an etl process for loading data from json raw data to a AWS Redshift Datawarehouse (DWH) and for creating fact and dimension tables there in that manner. Basically it is a little bit similar to the first NDDE project (see here: https://github.com/ChristophGmeiner/UdacityNDDE1_ETLPostgres)

This is done using Python (specifically the psycopg2 package).

## Purpose of the Database sparkifydb

The sparkifydb is an AWS Redshift datawarehouse and is about storing information about songs and listening behaviour of the users.

The analytical goal of this database to get all kinds of insights into the user beahviour (listenting preferences, highest rated artist, high volume listening times, etc.)

Please be aware that this data is for demonstration purposes only and therefore not very complete i.e. we only see some users and only data for one month, i.e. Nov. 2018.

## Description of the ETL Pipeline
All confidential information needed for connecting to AWS is stored in a local file (not part of this repo), i.e. dwh.cfg. See the scripts for details on that.

First raw data gets imported (BULK Insert) from several json files stored in a AWS S3 bucket into two staging tables, i.e. staging_events and staging_songs.

After that - based on this raw data - a star schema will be implemented showing songplay behaviour as facts and users, songs, artists and time as dimensions (see details below).

### Staging_events table
This staging table is intended for the log data stored in json files and showing data about user logs from Sparkify (i.e. what user listened to what song and when and how etc.).
This data is located in the log_data directory in the S3 bucket.
Since we're only interested here in events concerning the page "NextSong", I will delete all other records in the etl process.

### Staging_song table
This staging table is intended for the song raw data. This data is also stored in json format and shows details about specific songs.
This data is located in the song_data directory in the S3 bucket.

### Songplay table
This table is the fact table. It has an artificial primary and sort key from an identity column. Since the song dimension seems to be the biggest one, I defined the song_id here as a distkey.
Since it would not make any sense to accept NULL values for either song or artist in this table (for analytical reasons), this table is pretty small. This is due to the raw data restrictions mentioned in the purpose section above.
Details on that can also be seen in the DataChecks notebook.

### Users table
This table shows masterdata about users. I put the distribution style to ALL, since actually this seems to be a smaller dimension table. It gets sorted by the primary key, i.e. user_id.

### Song table
This table shows masterdata about songs. I defined the song_id as primary, sort and dist key (same dist as in fact table).

### Artist table
This table shows masterdata about artists. I put the distribution style to ALL, since actually this seems to be a smaller dimension table. It gets sorted by the primary key, i.e. artist_id.

### Time table
This table shows time and date based masterdata for each timestamp a songplay took place. I put the distribution style to ALL, since actually this seems to be a smaller dimension table. It gets sorted by the primary key, i.e. start_time.


### Scripts and Files

#### sql_queries.py
This Python script contains all necessary SQL scripts to extract the data from the S3-stored json files to the staging tables in AWS Redshift, delete non-necessary records from the the staging_events table and transform the staged data to fact and dimension tables.
Also all necessary tables are created in there before loading anything. The commands of this script are used in later scripts.

#### create_tables.py
Drop and (Re-)Creates all necessary tables in AWS Redshift (based on sql_queries.py)

#### etl.py
Inserts json data from a AWS S3 bucket into the newly created tables (based on sql_queries.py).

#### s3_inspect.ipynb
This notebook shows a possible way to inspect the contents of S3 buckets.

#### RunScripts.sh
Full ETL bash script, drops, (Re)Creates and inserts data. Just run this and everything gets done (the whole ETL process).

#### DataChecks.ipynb
This notebook shows some basic and analytical data checks on the new tables.