import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries, drcrtabs


def drop_tables(cur, conn):
    for drtab, query in zip(drcrtabs, drop_table_queries):
        cur.execute(query)
        print("{} dropped!".format(drtab))
        conn.commit()


def create_tables(cur, conn):
    for crtab, query in zip(drcrtabs, create_table_queries):
        cur.execute(query)
        print("{} created!".format(crtab))
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()