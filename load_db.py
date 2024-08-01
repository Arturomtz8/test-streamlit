# Tables in the database:
# supplier
# medicine
# order
# buyer

import sqlite3

import pandas as pd


def get_table(table_name):
    conn = sqlite3.connect("database.db")
    if table_name == "order":
        query = f"SELECT * FROM `order`"
    else:
        query = f"SELECT * FROM {table_name}"

    df = pd.read_sql_query(query, conn)

    conn.close()
    return df
