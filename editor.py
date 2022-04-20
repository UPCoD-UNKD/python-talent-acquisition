import dialect as dialect
import pandas as pd
import re
import csv

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex2 = r'[A-Za-z0-9._%+-]+\.[A-Za-z0-9._%+-/]{2,}'


def check(email):
    if (re.fullmatch(regex, email)):
        return True


def isValidSite(site):
    if (re.fullmatch(regex2, site)):
        return True


def secondColumn(someStr):
    data = str(someStr).split('; ')
    if len(data) == 3:
        return data
    elif len(data) == 2:
        data.append('nan')
        return data
    else:
        return 'nan', 'nan', 'nan'


def findEmail(someStr):
    data = str(someStr).split(';')
    emails = []
    for i in data:
        i = i.replace(' ', '')
        if '@' in i:
            email = ((i.split()[-1]).lower()).replace('e-mail:', '')
            if check(email):
                emails.append(email)
    if emails:
        return list(set(emails))
    else:
        return 'nan'


def findNumbers(someStr):
    data = str(someStr).split(';')
    numbers = []
    prefixes = ['0', '80', '380']
    for i in data:
        for j in '+ -()':
            i = i.replace(f'{j}', '')
        for k in range(3, 0, -1):
            index = i.find(prefixes[k - 1])
            if index != -1 and len(str(i)) >= 9 + k:
                number = str(i)[index:index + 9 + k]
                if number.isnumeric():
                    numbers.append('380'[:3 - k] + number)
                    break
    if numbers:
        return list(set(numbers))
    else:
        return 'nan'


def findSite(someStr):
    data = str(someStr).split(';')
    sites = []
    prefixes = ['http://', 'https://', 'https:', 'https//', 'http:', 'http//', 'www.']
    for i in data:
        i = i.replace(' ', '')
        i = i.lower()
        if ('www.' in i) or ('http' in i) or ('https' in i):
            for j in prefixes:
                i = i.replace(j, '')
        if isValidSite(str(i)):
            sites.append(i)
    if sites:
        return list(set(sites))
    else:
        return 'nan'


if __name__ == '__main__':
    df = pd.read_csv('dataset.csv', sep='\t', header=None)
    df.drop_duplicates(keep=False, inplace=True)

    condition = df[0]
    someDate1 = []
    someDate2 = []
    someNumber1 = []
    someNumber2 = df[2]
    organization = df[4]
    phoneNumber = []
    email = []
    site = []

    for x in df.index:
        secondColumnData = secondColumn(df.loc[x, 1])
        someDate1.append(secondColumnData[0])
        someDate2.append(secondColumnData[1])
        someNumber1.append(secondColumnData[2])
        phoneNumber.append(findNumbers(df.loc[x, 5]))
        email.append(findEmail(df.loc[x, 5]))
        site.append(findSite(df.loc[x, 5]))

    dfDict = {'condition': condition, 'someDate1': someDate1, 'someDate2': someDate2, 'someNumber1': someNumber1,
              'someNumber2': someNumber2, 'organization': organization, 'phoneNumber': phoneNumber, 'email': email,
              'site': site}

    newDf = pd.DataFrame(dfDict)
    print(newDf)
    newDf.to_csv('newDataset.csv', encoding='utf-8', index=False, sep='|')
