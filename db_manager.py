import sqlite3
import os


db = 'db/i2pspy.db'


def createdb(path_db):
    if os.path.exists(path_db):
        print('Ok. DB True')
    else:
        try:
            sqlite_connection = sqlite3.connect('db/i2pspy.db')
            cursor = sqlite_connection.cursor()
            print("DataBase create and connect SQLite")

            sqlite_select_query = "select sqlite_version();"
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            print("SQLite version: ", record)

            with open('db/filldb.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()

            cursor.executescript(sql_script)
            print('Fill OK')
            cursor.close()

        except sqlite3.Error as error:
            print("Connection error", error)


createdb()
