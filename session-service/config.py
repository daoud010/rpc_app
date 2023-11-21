import os
import pymysql.connections

MYSQL_HOST = '0.0.0.0'
MYSQL_DB = 'sessions'
MYSQL_USER = 'educative'
MYSQL_PASS = 'educative'


session_conn = pymsql.connect (
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    port=3306,
    charset='utff8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
