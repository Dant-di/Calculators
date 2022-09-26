import json

with open('test_td.json', 'r') as td_file:
    td_db = json.load(td_file)


td_db['TD-HL4183-16'] = {"Description": "", "Lifecycle Phase": "","Height": 292.0,"Width": 301.1, "Length 3D": 100.9,"Width 3D": 229.5, "Height 3D": 37.3, "Area [cm2]": 772.35, "Cigarette Length Category": "100'S - 100", "Cigarette Length [mm]": 97, "Cigarettes per Item": 200.0, "Pack Type": "ROUND CORNER BOX - RCB", "Thickness Category": "EXTRA SLIMS - XSL", "Nesting": "", "Area": 77235.0}

print(td_db['TD-HL4183-16'])

with open('test_td.json', 'w') as td_file_write:
    json.dump(td_db, td_file_write, sort_keys=True)






# import re
# td = 'TD-HL4183-1'
#
# r = re.compile('TD-[A-Z][A-Z]+[0-9][0-9][0-9][0-9]+-+[0-9][0-9]')
#
# if r.match(td) is not None:
#     print("Yeah baby")
# else:
#     print("Something is wrong")

