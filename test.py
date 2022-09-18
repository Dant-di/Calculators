import json

with open('resource/td.json') as td:
    td_db = json.load(td)

print(td_db.get('TD-HL4073-11').keys())

