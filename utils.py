import pandas as pd

def list2column(df, column):
    
    df['dict_col'] = df[column].apply(list_to_dict)


    df_new = pd.json_normalize(df['dict_col'])
    df.drop(['dict_col'], axis=1, inplace=True)
    
    return ancestry_percent(df_new)

def list_to_dict(lst):
    result_dict = {}
    for item in lst:
        key, value = item.split('=')
        result_dict[key] = int(value)
    return result_dict

def ancestry_percent(df):
    total_values = df.count().sum()

# Count non-NaN values in each column and calculate their percentage
    column_percentages = df.count() / total_values * 100

# Convert to list
    column_percentages_list = column_percentages.tolist()

    return column_percentages_list
