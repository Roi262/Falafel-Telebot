"""
A helper file to handle the fast food order data base
"""

import sqlite3 as lite
import sys
 
ORDERS_DB = "orders.db"

con = lite.connect(ORDERS_DB)

def create_table(table, columns):
    with con:
        cur = con.cursor()    
        cur.execute("CREATE TABLE " + table + "(" + columns + ")")


def insert_value(value, table, columns):
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE " + table + "(" + columns + ")")
        cur.execute("INSERT INTO Users VALUES(1,'Michelle')")