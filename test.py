import mysql.connector
import sshtunnel
import pandas as pd
import pymysql
from sshtunnel import SSHTunnelForwarder
from mysql.connector import Error
import logging

MySQL_hostname = 'localhost'
sql_username = 'dant'
sql_password = '!CS05tirepc'
sql_main_database = 'pd'
sql_port = 3306
ssh_host = '192.168.1.121'
ssh_user = 'dant'
ssh_password = '!CS05tirepc'
ssh_port = 22



def open_ssh_tunnel(verbose=False):

    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG

    global tunnel
    tunnel = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_user,
        ssh_password=ssh_password,
        remote_bind_address=('127.0.0.1', 3306)
    )

    tunnel.start()


def mysql_connect():

    global connection

    connection = pymysql.connect(
        host='127.0.0.1',
        user=sql_username,
        passwd=sql_password,
        db=sql_main_database,
        port=tunnel.local_bind_port
    )


def fetch_data(sql):
    """Runs a given SQL query via the global database connection.

    :param sql: MySQL query
    :return: Pandas dataframe containing results
    """

    return pd.read_sql_query(sql, connection)


def mysql_disconnect():
    """Closes the MySQL database connection.
    """

    connection.close()


def close_ssh_tunnel():
    """Closes the SSH tunnel connection.
    """

    tunnel.close


open_ssh_tunnel()
mysql_connect()
df = fetch_data("SELECT * FROM boards")
print(df.tail())

insert_boards_query = """
INSERT INTO boards (name, grammage, width, supplier_id)
VALUES ('New Name', '666', '820', '16')
"""

with connection.cursor() as cursor:

    cursor.execute(insert_boards_query)
    connection.commit()

df = fetch_data("SELECT * FROM boards")
print(df.tail())

mysql_disconnect()
close_ssh_tunnel()