import pymysql.connections

MYSQL_HOST = 'localhost'
MYSQL_DB = 'orders'
MYSQL_USER = 'educative'
MYSQL_PASS = 'educative'

orders_conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    port=3306,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)