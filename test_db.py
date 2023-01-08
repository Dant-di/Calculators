import sqlite3
import json
from datetime import datetime

with open('resource/td.json', 'r') as td:
    td_db = json.load(td)

td_list = list(td_db.keys())


td_id = td_list[0]
values = td_db.get(td_id).values()
now = datetime.now()





try:
    db_connect = sqlite3.connect('database/main.db')
    cursor = db_connect.cursor()


    insert_values = """INSERT INTO technical_drawings values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

    data_tuple = (td_id,) + tuple(values) + (now,)
    cursor.execute(insert_values, data_tuple)
    db_connect.commit()
    cursor.close()

except sqlite3.Error as error:
    print('Error occured - ', error)

finally:
    if db_connect:
        db_connect.close()
        print('Connection closed')


