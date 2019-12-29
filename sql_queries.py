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
                                song varchar, status int, ts varchar(50), \
                                userAgent varchar, userId int)")

staging_songs_table_create = ("CREATE TABLE staging_songs (artist_id varchar, \
                               artist_latitude varchar, \
                               artist_location varchar, \
                               artist_longtitude varchar, \
                               artist_name varchar, duration float, \
                               num_songs int, song_id varchar, title varchar, \
                               year int)")

songplay_table_create = ("CREATE TABLE songplay (songplay_id IDENTITY(0, 1), \
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

[LOG_DATA, LOG_JSONPATH, SONG_DATA] = config['S3'].values()

staging_events_copy = ("copy staging_events_table from {} \
                       credentials 'aws_iam_role={} \
                       'region 'us-west-2' json {};").format(LOG_DATA, arn, 
                       LOG_JSONPATH)

staging_songs_copy = ("COPY staging_songs FROM {} \
                        credentials 'aws_iam_role={}' \
                        gzip region 'us-west-2'").format(SONG_DATA, arn)

# FINAL TABLES

songplay_table_insert = ("INSERT INTO songplay (start_time, user_id, level, \
                          song_id, artist_id, session_id, location, \
                          user_agent) SELECT se.ts, u.user_id, u.level, \
                          s.song_id, a.artist_id, se.sessionId, a.location, \
                          se.UserAgent \
                          from staging_events se JOIN user u ON \
                          u.first_name = se.firstName AND \
                          u.last_name = se.lastName \
                          JOIN artist a ON a.name = se.artist \
                          JOIN song s ON s.artist_id = a. artist_id AND \
                          s.title = se.song")

user_table_insert = ("INSERT INTO users (user_id, first_name, last_name, \
                      gender, level) SELECT DISTINCT se.userId, se.firstName, \
                      se.lastName, se.gender, se.level from staging_events se \
                      ON CONFLICT(user_id) DO UPDATE \
                      SET LEVEL = EXCLUDED.LEVEL")

song_table_insert = ("INSERT INTO songs (song_id, title, artist_id, \
                      year, duration) SELECT DISTINCT so.song_id, so.title, \
                      so.artist_id, so.year, so.duration from \
                      staging_songs so ON CONFLICT DO NOTHING")

artist_table_insert = ("INSERT INTO artists (artist_id, name, location, \
                        latitude, longitude) SELECT DISTINCT so.artist_id, \
                        so.artist_name, so.artist_location, \
                        so.artist_latitude, so.artist_longitude FROM \
                        staging_songs so ON CONFLICT DO NOTHING")

time_table_insert = ("INSERT INTO time (start_time, hour, day, week, month, \
                      year, weekday) SELECT se.ts, EXTRACT (HOUR FROM se.ts), \
                      EXTRACT(DAY FROM se.ts), EXTRACT(WEEK FROM se.ts), \
                      EXTRACT(MONTH FROM se.ts), EXTRACT(YEAR FROM se.ts), \
                      EXTRACT(DOW FROM se.ts) FROM staging_events se")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
