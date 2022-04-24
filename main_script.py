import re
import pandas as pd

REGEX_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
REGEX_NUMBER = r'^(?:\+)?(?:38)(?:\[0-9]\{3}[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|[0-9]{3}[ .-]?[0-9]{3}[ .-]?' \
               r'[0-9]{2}[ .-]?[0-9]{2}|[0-9]{3}[0-9]{7})(?:;)?$'
REGEX_SITE = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]' \
                r'[a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.' \
             r'[a-zA-Z0-9]+\.[^\s]{2,})'

def check_data(row):
    if re.search(REGEX_EMAIL, str(row)) or re.search(REGEX_NUMBER, str(row)) or re.search(REGEX_SITE, str(row)):
        return True
    return False

def split_data(row):
    emails = re.findall(REGEX_EMAIL, row)
    phone_numbers = re.findall(REGEX_NUMBER, row)
    websites = re.findall(REGEX_SITE, row)
    return emails, phone_numbers, websites

def main(data):
    print('process started...')
    result = pd.DataFrame(
        columns=["компанія", "номер телефону", "імейл", "сайт"]
    )
    for index, row in data.iterrows():
        if check_data(row[data.columns[-1]]):
            email, phone_number, website = split_data(row[data.columns[-1]])
            new_row = {
                "компанія": row[data.columns[4]],
                "номер телефону": phone_number,
                "імейл": email,
                "сайт": website
            }
            result.loc[len(result.index)] = new_row
    result.to_csv('result.csv', index=False, encoding='utf_8_sig', sep=';')
    print('process finished!')

if __name__ == "__main__":
    data = pd.read_csv("dataset.csv", sep='\t', error_bad_lines=False)
    main(data)