from dotenv import load_dotenv
import os
from os.path import join, dirname
from mysql.connector import pooling

envpath = join(dirname(__file__), "../.env")

load_dotenv(envpath)

connection_pool = pooling.MySQLConnectionPool(
    pool_name="Poe_stash_tab_pool",
    pool_size=5,
    host=os.getenv('db_host'),
    user=os.getenv('db_user'),
    password=os.getenv('db_password'),
    database=os.getenv('db_database'),
    port=os.getenv('db_port'),
    autocommit=True
)

def get_connection():
    return connection_pool.get_connection()

def release_connection(connection):
    connection.close()

