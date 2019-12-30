import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

arn = config.get("IAM_ROLE", "ARN")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
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
                                song varchar, status int, ts varchar(50), \
                                userAgent varchar, userId int)")

staging_songs_table_create = ("CREATE TABLE staging_songs (artist_id varchar, \
                               artist_latitude varchar, \
                               artist_location varchar, \
                               artist_longtitude varchar, \
                               artist_name varchar, duration float, \
                               num_songs int, song_id varchar, title varchar, \
                               year int)")

songplay_table_create = ("CREATE TABLE songplay \
                         (songplay_id int IDENTITY(0, 1) PRIMARY KEY SORTKEY, \
                         start_time timestamp not null, user_id int not null, \
                         level varchar, song_id varchar DISTKEY, \
                         artist_id varchar, session_id int, location varchar, \
                         user_agent varchar)")

user_table_create = ("CREATE TABLE users \
                     (user_id int not null PRIMARY KEY SORTKEY, \
                     first_name varchar, last_name varchar, gender varchar, \
                     level varchar) DISTSTYLE ALL")

song_table_create = ("CREATE TABLE song \
                     (song_id varchar not null PRIMARY KEY SORTKEY DISTKEY, \
                     title varchar, artist_id varchar not null, year int, \
                     duration float)")

artist_table_create = ("CREATE TABLE artist (artist_id varchar not null \
                       PRIMARY KEY SORTKEY DISTKEY, name varchar, \
                       location varchar, latitude varchar, longitude varchar)")

time_table_create = ("CREATE TABLE time (start_time timestamp NOT NULL \
                     PRIMARY KEY SORTKEY DISTKEY, \
                     hour int, day int, week int, month int, year int, \
                     weekday int)")

# STAGING TABLES

[LOG_DATA, LOG_JSONPATH, SONG_DATA] = config['S3'].values()

staging_events_copy = ("copy staging_events from {} \
                       credentials 'aws_iam_role={}' \
                       region 'us-west-2' json {};").format(LOG_DATA, arn, 
                       LOG_JSONPATH)

staging_songs_copy = ("COPY staging_songs FROM {} \
                        credentials 'aws_iam_role={}' \
                        region 'us-west-2' \
                        json 'auto' truncatecolumns").format(SONG_DATA, arn)

# FINAL TABLES

tsvar = "TIMESTAMP 'epoch' + se.ts/1000 * interval '1 second'"

songplay_table_insert = ("INSERT INTO songplay (start_time, user_id, level, \
                          song_id, artist_id, session_id, location, \
                          user_agent) SELECT {}, u.user_id, \
                          u.level, s.song_id, a.artist_id, se.sessionId, \
                          a.location, se.UserAgent \
                          from staging_events se JOIN users u ON \
                          u.first_name = se.firstName AND \
                          u.last_name = se.lastName \
                          JOIN artist a ON a.name = se.artist \
                          JOIN song s ON s.artist_id = a. artist_id AND \
                          s.title = se.song").format(tsvar)

user_table_insert = ("INSERT INTO users (user_id, first_name, last_name, \
                      gender, level) SELECT DISTINCT se.userId, se.firstName, \
                      se.lastName, se.gender, se.level from staging_events se \
                      WHERE se.userId IS NOT NULL")

song_table_insert = ("INSERT INTO song (song_id, title, artist_id, \
                      year, duration) SELECT DISTINCT so.song_id, so.title, \
                      so.artist_id, so.year, so.duration from \
                      staging_songs so WHERE so.song_id IS NOT NULL")

artist_table_insert = ("INSERT INTO artist (artist_id, name, location, \
                        latitude, longitude) SELECT DISTINCT so.artist_id, \
                        so.artist_name, so.artist_location, \
                        so.artist_latitude, so.artist_longtitude FROM \
                        staging_songs so WHERE so.artist_id IS NOT NULL")

time_table_insert = ("INSERT INTO time (start_time, hour, day, week, month, \
                      year, weekday) SELECT {}, \
                      EXTRACT (HOUR FROM {}), \
                      EXTRACT(DAY FROM {}), EXTRACT(WEEK FROM {}), \
                      EXTRACT(MONTH FROM {}), EXTRACT(YEAR FROM {}), \
                      EXTRACT(DOW FROM {}) \
                      FROM staging_events se").format(tsvar, tsvar, tsvar, 
                      tsvar, tsvar, tsvar, tsvar)

# QUERY LISTS

create_table_queries = [staging_events_table_create, 
                        staging_songs_table_create, songplay_table_create, 
                        user_table_create, song_table_create, 
                        artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, 
                      songplay_table_drop, user_table_drop, song_table_drop, 
                      artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
ctabs = ["staging_events", "staging_songs"]
insert_table_queries = [songplay_table_insert, user_table_insert, 
                        song_table_insert, artist_table_insert, 
                        time_table_insert]
tables = ["songplay", "user", "song", "artist", "time"]
drcrtabs = ctabs + tables