import pandas as pd
import psycopg2


def connect():
    conn = None
    try:
        print('Connecting...')
        conn = psycopg2.connect(
                        host='10.10.248.108',
                        database='postgres',
                        user='eatin',
                        password='eatin')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    print('Connection Successful')

    return conn


def execute_select(conn, query, column_names):
    cursor = conn.cursor()
    data = pd.DataFrame()
    try:
        cursor.execute(query)
        data = cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    cursor.close()

    return data
