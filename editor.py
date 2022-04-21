import pandas as pd
import re

def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True

def isValidSite(site):
    regex2 = r'[A-Za-z0-9._%+-]+\.[A-Za-z0-9._%+-/]{2,}'
    if (re.fullmatch(regex2, site)):
        return True

def getContacts(someStr):
    data = str(someStr).split(';')
    emails = []
    sites = []
    numbers = []
    numberPrefixes = ['0', '80', '380']
    sitePrefixes = ['http://', 'https://', 'https:', 'https//', 'http:', 'http//', 'www.']
    for i in data:
        i = i.replace(' ', '')
        i = i.lower()
        # find email
        emailLine = i[:]
        if '@' in emailLine:
            email = ((emailLine.split()[-1]).lower()).replace('e-mail:', '')
            if check(email):
                emails.append(email)
                break
        # find site
        siteLine = i[:]
        if ('www.' in siteLine) or ('http' in siteLine) or ('https' in siteLine):
            for j in sitePrefixes:
                siteLine = siteLine.replace(j, '')
        if isValidSite(str(siteLine)):
            sites.append(siteLine)
            break
        # find phoneNumber
        numberLine = i[:]
        for j in '+ -()':
            numberLine = numberLine.replace(f'{j}', '')
        for k in range(3, 0, -1):
            index = numberLine.find(numberPrefixes[k - 1])
            if index != -1 and len(str(numberLine)) == 9 + k:
                number = str(numberLine)[index:index + 9 + k]
                if number.isnumeric():
                    numbers.append('380'[:3 - k] + number)
                    break
    return tuple(set(numbers)),tuple(set(emails)),tuple(set(sites))

if __name__ == '__main__':
    df = pd.read_csv('dataset.csv', sep='\t', header=None)
    phoneNumber = []
    email = []
    site = []
    for x in df.index:
        res = getContacts(df.loc[x,5])
        phoneNumber.append(''.join(res[0])) if res[0] else  phoneNumber.append('nan')
        email.append(''.join(res[1])) if res[1] else email.append('nan')
        site.append(''.join(res[2])) if res[2] else site.append('nan')
    del df[5]
    df[5] = phoneNumber
    df[5] = email
    df[5] = site
    df.drop_duplicates(keep=False, inplace=True)
    df.to_csv('newDataset.csv', encoding='utf-8', index=False, header=False)
