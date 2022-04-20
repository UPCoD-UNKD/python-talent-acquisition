import csv
import re

csv_filename_old = "dataset.csv"
# New file with delimiter TAB
csv_filename_new = "dataset_new.csv"

with open(csv_filename_old, encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file, delimiter='\t')

    new_dataset = []

    # Line by line
    for row in file_reader:
        registration = row[0]
        date = row[1]
        code = row[2]
        legal_form = row[3]
        name = row[4]
        emails = str()
        urls = str()
        phones = str()
        other = str()

        split_contacts = row[5].split("; ")

        # Literally
        for part in split_contacts:
            pattern_url = r"(^[a-zA-Z0-9._%+-/]+\.[a-zA-Z0-9-.]+$)"
            part = part.strip()
            part = part.replace('https://', '')
            part = part.replace('HTTPS://', '')
            part = part.replace('HTTP://', '')
            part = part.replace('http://', '')

            # Select emails
            mail = "@" in part
            if mail is True and part[-1].isnumeric() is False:
                emails = (part.lower())
            # Select urls
            elif re.match(pattern_url, part) is not None and part[-1].isnumeric() is False:
                urls = (part.lower())
            # Select phone numbers
            elif part is not None and len(part) > 4 and part[-1].isnumeric() is True:
                part = part.replace('-', '')
                part = part.replace('(', '')
                part = part.replace(')', '')
                part = part.replace('+', '')
                part = part.replace(' ', '')
                if part[:3] == '380' and len(part) == 12:
                    phones = part + ';'
                elif part[:2] == '80' and len(part) == 11:
                    part = "3"+part
                    phones = phones + part + ';'
                elif part[:1] == '0' and len(part) == 10:
                    part = "38"+part
                    phones = phones + part + ';'
                else:
                    part_with_last_num = part

            else:
                other = part_with_last_num+part

        new_dataset.append([registration, date, code, legal_form, name, phones, emails, urls, other])

    # New file creation
    with open(csv_filename_new, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(new_dataset)
