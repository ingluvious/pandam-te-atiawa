'''
@Author: David Liu

@Description: 
Utility file supports all API files
'''

from aws_lambda_powertools import Logger #type:ignore
from dotenv import load_dotenv

import json
import os
import psycopg2 as psy
from psycopg2.extras import execute_values
import db_queries as qr

logger = Logger()

def jsonDump(payload):
    return json.dumps(payload, indent = 4, default = str)

def createConn():
    DB_HOST = "pandam-db.cl0qqegqikjy.ap-southeast-2.rds.amazonaws.com"
    DB_PORT = 5432
    DB_NAME = "pandam"
    DB_USER = "db_master"
    DB_PASSWORD = "pandamDBMaster100%"

    conn = psy.connect(
        host = DB_HOST,
        port = DB_PORT,
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD
    )
    return conn

def getColNames(cursor):
    col_names = [descrip[0] for descrip in cursor]
    return col_names

def dictionaryRows(description, data):
    dictionary = [dict(zip(getColNames(description), row)) for row in data]
    return dictionary

def getData(query):
    conn = createConn()
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
    dictionary_rows = dictionaryRows(cursor.description, rows)
    return dictionary_rows, rows

def upsertData(payload, table_name):
    
    conn = createConn()
    cursor = conn.cursor()
    
    if isinstance(payload, str):
        data = json.loads(payload)
    else:
        data = payload

    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    values = tuple(data.values())

    query = f"insert into {table_name} ({columns}) values ({placeholders})"
    
    cursor.execute(query, values)
    
    conn.commit()
    cursor.close()
    conn.close()

    response = {
        "statusCode":200,
        "status":"success",
        "message":"Data inserted successfully"
    }
    return response, 200

    
