#!/bin/python3 

import csv, re

# Input data
dataset_file = open('dataset.csv')
dataset_reader = csv.reader(dataset_file, delimiter='\t')
dataset_data = list(dataset_reader)

# Output
output_file = open('output.csv', 'w', newline='')
output_writer = csv.writer(output_file)

regex_phone = re.compile(r'''(
    (\+)?       # + for international format
    (38)?       # 38 - country code
    (\s|-)?     # optional separator
    (0\d{2,4})  # are code 0xx or 0xxx
    (\s|-)?     # optional separator
    (\d{1,3})   # first group of digits
    (\s|-)?     # optional separator
    (\d{2})     # second group of digits
    (\s|-)?     # optional separator
    (\d{2})     # third group of digits
    )''', re.VERBOSE)

regex_email = re.compile(r'''(
    [a-zA-Z0-9._%+-]+      # username
    @                      # @ symbol
    [a-zA-Z0-9.-]+         # domain name
    (\.[a-zA-Z]{2,4})       # dot-something
    )''', re.VERBOSE)

regex_web = re.compile(r'''(
        [a-zA-Z0-9\.@-]+
        (\.[a-zA-Z]{2,4})
        )''', re.VERBOSE)

max_phones = 0
max_emails = 0
max_web = 0
output_writer.writerow(['Назва', 'Телефони', 'Єлектронна пошта', 'Сайт'])

for row in range(len(dataset_data)):
    phone = []
    email = []
    websites= []
    count = 0
    # 0 - status, 1 - dates and reg numbers, 2 - reg number, 3 - legal entity type,
    # 4 - legal entity name, 5 - contact information
    line=[dataset_data[row][4]]
    for phones in regex_phone.findall(dataset_data[row][5]):
        phone_num = ''.join(["38",phones[4],phones[6],phones[8],phones[10]])
        phone.append(phone_num)
        count +=1
    if count > max_phones:
        max_phones = count
    count = 0
    for emails in regex_email.findall(dataset_data[row][5]):
        email.append(emails[0].lower())
        count += 1
    if count > max_emails:
        max_emails = count
    count = 0
    for web in regex_web.findall(dataset_data[row][5]):
        websites.append(web[0].lower())
        count += 1
    if count > max_web:
        max_web = count
    line.append(';'.join(phone))
    line.append(';'.join(email))
    line.append(';'.join(websites))
    output_writer.writerow(line)
   
dataset_file.close()   
output_file.close()
