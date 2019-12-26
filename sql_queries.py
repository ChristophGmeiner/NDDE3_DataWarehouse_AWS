import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

arn = config.get("IAM_ROLE", "ARN")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS user"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("CREATE TABLE staging_events (artist varchar, \
                                auth varchar, firstName varchar, \
                                gender varchar, ItemInSession int, \
                                lastName varchar, length float, \
                                level varchar, location varchar, \
                                method varchar, page varchar, \
                                registration float, sessionId int, \
                                song varchar, status int, ts timestamp, \
                                userAgent varchar, userId int)")

staging_songs_table_create = ("CREATE TABLE staging_songs (num_songs int, \
                               artist_id varchar, artist_latitude varchar, \
                               artist_longtitude varchar, \
                               artist_location varchar, artist_name varchar, \
                               song_id varchar, title varchar, duration float \
                               year int)")

songplay_table_create = ("CREATE TABLE songplay (songplay_id serial not null, \
                         start_time timestamp not null, user_id int not null, \
                         level varchar, song_id varchar, artist_id varchar, \
                         session_id int, location varchar, user_agent \
                         varchar)")

user_table_create = ("CREATE TABLE user (user_id int not null, \
                     first_name varchar, last_name varchar, gender varchar, \
                     level varchar)")

song_table_create = ("CREATE TABLE song song_id varchar not null, \
                     title varchar, artist_id varchar not null, year int, \
                     duration float)")

artist_table_create = ("CREATE TABLE artist (artist_id varchar not null \
                       primary key, name varchar, location varchar, \
                       latitude float, longitude float)")

time_table_create = ("CREATE TABLE time (start_time timestamp not null, \
                     hour int, day int, week int, month int, year int, \
                     weekday int)")

# STAGING TABLES

staging_events_copy = ("COPY staging_events FROM 's3://udacity-dend/log_data' \
                        credentials 'aws_iam_role={}' \
                        gzip region 'us-west_2'").format(arn)

staging_songs_copy = ("COPY staging_songs FROM 's3://udacity-dend/song_data' \
                        credentials 'aws_iam_role={}' \
                        gzip region 'us-west_2'").format(arn)

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
