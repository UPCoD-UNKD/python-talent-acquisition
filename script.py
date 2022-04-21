# You can see my CV at google drive
# https://docs.google.com/document/d/1pF6fw9RJI5_-wb1XJ683halO2LIfi1h1l4E90eqXS5c/edit?usp=sharing
# 
# My Bitbucket repository
# https://bitbucket.org/olegsuyarkov/


import re
import pandas as pd


phone_pattern = r'^[0-9 ()+-]+$'
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
site_email_pattern = r'[a-zA-Z0-9]+\.[a-zA-Z]+$'


# convert phones from +380.., +38(0..) +380(..) etc. to 380 and checking for a valid number of digits
# check for valid email and site
# clear bad data
def clear_data(x):
    x = str(x)
    x = x.strip()
    if re.fullmatch(phone_pattern, x):
        x = re.sub('\D', '', x)
        if len(x) < 12: # 12 - a valid number of digits
            return None
        else:
            return x
    elif re.search(site_email_pattern, x):
        return x
    else:
        return None


def normalized_csv():
    # create dataframe
    # csv is uneven, so we use an arbitrary range of column names to grab all the data
    col_names = [i for i in range(1, 20)]
    df = pd.read_csv('dataset.csv', sep='[\t|;]', names=col_names, engine='python')

    # remove empty columns
    df.dropna(axis='columns',how='all', inplace=True)

    # get uneven part with contacts
    uneven_df = df.iloc[:,[i for i in range(7, df.shape[1])]]

    # get first clear part df
    df = df.iloc[:,[j for j in range(df.shape[1] - uneven_df.shape[1])]]

    # convert phones and clear data
    uneven_df = uneven_df.applymap(clear_data, na_action='ignore')

    # remove all rows where is no any contacts
    uneven_df.dropna(axis='index', how='all', inplace=True)

    # remove duplicates values in all rows
    mask = uneven_df.apply(pd.Series.duplicated, 1) & uneven_df.astype(bool)
    uneven_df = uneven_df.mask(mask, other=None)

    # reindex
    uneven_df = uneven_df.reset_index()

    # create a new clear dataframe with the contacts
    clear_df = pd.DataFrame(columns=[i for i in range(9)])

    for index, row in uneven_df.iterrows():
        phone_from = 0
        email_from = 3
        site_from = 6
        row_data = [None for i in range(9)]
        for value in row[1:]:
            value = str(value)
            if re.search(phone_pattern, value) and len(value) == 12:
                row_data[phone_from] = value
                phone_from += 1
            elif re.search(email_pattern, value):
                row_data[email_from] = value
                email_from += 1
            elif re.search(site_email_pattern, value):
                row_data[site_from] = value
                site_from += 1                
        print(index) # see process in the console
        clear_df.loc[row['index']] = row_data

    # drop the contact columns where is no value
    clear_df.dropna(axis='columns', how='all', inplace=True)

    # rebuild for nice view
    clear_df = clear_df.replace(pd.NA, '<----->')

    # get valid rows from df
    df = df[df.index.isin(uneven_df['index'].to_list())]

    # concat two dataframes
    final_df = pd.concat([df, clear_df], axis=1)

    # rename columns to human readble view
    final_df.columns = ['STATUS', 'FIRST DATE', 'SECOND DATE', 'FIRST NUMBERS', 'SECOND NUMBERS', 'ORGANIZATION TYPE', 'NAME', 'PHONE_1', 'PHONE_2', 'PHONE_3', 'EMAIL_1', 'EMAIL_2', 'SITE_1', 'SITE_2', 'SITE_3']

    # reindex
    final_df = final_df.reset_index()
    final_df.pop('index')

    print(final_df) # see result in console
    # '~' - SEPARATOR OF COLUMNS!!!!!
    final_df.to_csv('output_COLUMNS_SEPARATOR_~.csv', sep='~', index=False)


def main():
    normalized_csv()

if __name__ == '__main__':
   main()
