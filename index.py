
import csv
import re


f = open('dataset.csv', 'r', encoding='utf-8')
w = open('new.csv', 'w', encoding='utf-8')
reader = csv.DictReader(f, delimiter=';', quotechar='"')


def getPhoneNumber(str):
    output = re.search(r'[+?]38[(]?\d{3}[)]?[0-9\-]{6,}', str)
    return output.group(0) if output else ''

def getEmail(str):
    output = re.search(r'[\w\.]+@\S+\.\S+$', str)
    return output.group(0) if output else ''

def getWebsite(str):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)\
            (?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]\
                +|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    output = re.search(regex, str)
    return output.group(0) if output else ''


output = []
for row in f.read().splitlines():
    line = [getPhoneNumber(row), getEmail(row), getWebsite(row)]
    if any(line): 
        output.append(line)


writer = csv.writer(w, delimiter=';')
writer.writerow(['phone', 'email', 'site'])
writer.writerows(output)
