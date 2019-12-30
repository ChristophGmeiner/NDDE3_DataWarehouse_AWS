import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, tables 
from sql_queries import ctabs, del_notnextsong


def load_staging_tables(cur, conn):
    '''Loads all necessary data from json files into staging tables
       INPUT:
           cur: A DB cursor object(has to be AWS Redshift based)
           conn: A connection object to an AWS Redsahift cluster
    '''
    for ctab, query in zip(ctabs, copy_table_queries):
        cur.execute(query)
        print("Copy for: {} finished!".format(ctab))
        conn.commit()


def insert_tables(cur, conn):
    '''Insert all necessary data from json files into star schema tables
       INPUT:
           cur: A DB cursor object(has to be AWS Redshift based)
           conn: A connection object to an AWS Redsahift cluster
    '''
    for tab, query in zip(tables, insert_table_queries):
        cur.execute(query)
        print("Insert for: {} finished!".format(tab))
        conn.commit()
        
def del_notnextSongs(cur, conn):
    '''
    Deletes all records in staging_events table which are not page = NextPage
    INPUT:
         cur: A DB cursor object(has to be AWS Redshift based)
         conn: A connection object to an AWS Redsahift cluster
    '''
    cur.execute(del_notnextsong)
    print("Not NextSong records succesfully deleted form staging_events")
    conn.commit()

def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    del_notnextSongs(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()