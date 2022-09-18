import pandas as pd

excel_data_df = pd.read_excel('td.xlsx')

excel_data_df.set_index('Number', inplace=True)
if "Nesting" not in excel_data_df.columns:
    excel_data_df['Nesting'] = None



# process dataframe
excel_data_df.drop(['Rev', 'Type'], axis=1, inplace=True)
names = excel_data_df.columns.to_list()

new_names = ['Description', 'Lifecycle Phase',
       'Height',
       'Width',
       'Length 3D',
       'Width 3D',
       'Height 3D',
       'Area [cm2]',
       'Cigarette Length Category',
       'Cigarette Length [mm]',
       'Cigarettes per Item',
       'Pack Type',
       'Thickness Category', 'Nesting']

excel_data_df.rename(columns=dict(zip(names, new_names)), inplace=True)

excel_data_df['Area'] = excel_data_df['Area [cm2]'] * 100

json_str = excel_data_df.to_json('td.json', orient='index')

