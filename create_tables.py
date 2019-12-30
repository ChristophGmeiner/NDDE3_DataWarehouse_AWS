import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries, drcrtabs


def drop_tables(cur, conn):
    '''Drops all tables in DWH
       INPUT:
           cur: A DB cursor object(has to be AWS Redshift based)
           conn: A connection object to an AWS Redsahift cluster
    '''
    for drtab, query in zip(drcrtabs, drop_table_queries):
        cur.execute(query)
        print("{} dropped!".format(drtab))
        conn.commit()


def create_tables(cur, conn):
    '''Creates all necessary tables in DWH
       INPUT:
           cur: A DB cursor object(has to be AWS Redshift based)
           conn: A connection object to an AWS Redsahift cluster
    '''
    for crtab, query in zip(drcrtabs, create_table_queries):
        cur.execute(query)
        print("{} created!".format(crtab))
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} \
                            port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()