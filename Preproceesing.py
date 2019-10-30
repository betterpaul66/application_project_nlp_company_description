import os, json
import csv
import pandas as pd
import re

# path_to_json = '/Users/weiding/Google Drive/Application Project/100_files'
path_to_json = 'C:/Users/kwokp/OneDrive/Desktop/Study/zzz_application project/vc/sum_all'
# read all json files from the folder
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

# enumerate each file
count_empty_file = 0
count_file = 0 #paul
accurate_tab = 0
company_tab_list = []
for index, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        json_text = json.load(json_file)
        #print(js) #paul
        count_file += +1 #paul
        if len(json_text) == 0:  # find and ignore empty files
            count_empty_file += 1
        else:
            js = js.split('_20', 1)[0]  # only keep the website name or company name
            for key in json_text.keys():
                x = re.search("^[0-9]{8}\_.*\.html$", key)

                if (x):
                    accurate_tab += 1
                key = key.split('_', 1)[-1]  # remove the date
                key = key.split('.html', 1)[0]  # remove the .html
                values = key.split('_')
                for value in values:
                    if len(value) != 0:
                        value = value.encode("utf-8") #paul
                        company_tab_list.append([js, value])

#x = re.search("^[0-9]{8}\..*\.html$", "20180903.dsafdsfsd.html")
#if (x):
#    accurate_tab += 1
print("Number of empty file: " + str(count_empty_file))
print("Number of file: " + str(count_file)) #paul
print("Number of accurate tab: " + str(accurate_tab)) #paul
with open('tabs1.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    for row in company_tab_list:
        writer.writerow(row)

writeFile.close()

# analyse the tabs and list the unique tabs with their occurences
df = pd.read_csv("tabs1.csv")
df.columns = ['Company', 'Tab']
pivoted = pd.pivot_table(df, index=['Company','Tab'], aggfunc='size')
df_aggregation = pivoted.to_frame().reset_index()
df_aggregation.rename(columns={0: 'Occurrences'}, inplace=True)
print(df_aggregation['Tab'].value_counts())