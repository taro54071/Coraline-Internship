import requests
import json
import pandas as pd

# 
df1 = pd.DataFrame()
for i in range(20):
    response = requests.get("https://randomuser.me/api") # JSON object

    # temp = json.dumps(response) # json --> string
    # x = json.loads(temp) # string --> python object

    x = json.loads(response.text) # String --> python object


    temp = {'first_name': [x['results'][0]['name']['first']], 
        'last_name': [x['results'][0]['name']['last']],
       'gender(actual)' : [x['results'][0]['gender']]}


    df_dictionary = pd.DataFrame(temp)
    df1 = pd.concat([df1, df_dictionary], ignore_index = True)


df2 = pd.DataFrame()
for first_name, gender in zip(df1['first_name'], df1['gender(actual)']):
    response = requests.get('https://api.genderize.io/?name={fname}'.format(fname = first_name))
    # print(response.text)
    y = json.loads(response.text)
    
    if gender == y['gender']:
        checked_gender = True
    else:
        checked_gender = False
    
    temp2 = {'gender(predict)': [y['gender']],
            'probability': [y['probability']],
            'same_gender': checked_gender}
    df2_dictionary = pd.DataFrame(temp2)
    df2 = pd.concat([df2, df2_dictionary], ignore_index = True)


result_df = df1.join(df2)
print(result_df)