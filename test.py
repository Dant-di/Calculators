import json

with open('resource/td.json') as td:
    td_db = json.load(td)

print(td_db.get('TD-HL4073-11').keys())




# import re
# td = 'TD-HL4183-1'
#
# r = re.compile('TD-[A-Z][A-Z]+[0-9][0-9][0-9][0-9]+-+[0-9][0-9]')
#
# if r.match(td) is not None:
#     print("Yeah baby")
# else:
#     print("Something is wrong")