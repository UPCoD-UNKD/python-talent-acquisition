import csv
from operator import delitem
import re

with open('dataset.csv', encoding='utf-8') as file:
    ds_reader = csv.reader(file, delimiter='\t')
    
    new_ds = list()
    
    for row in ds_reader:
        registration = row[0]
        date = row[1]
        code = row[2]
        form = row[3]
        name = row[4]
        contacts = row[5].split('; ')
        phone, email, url, other = str(), str(), str(), str()
        
        for contact in contacts:
            pattern_url = r"(^[a-zA-Z0-9._%+-/]+\.[a-zA-Z0-9-.]+$)"
            contact = contact.strip()
            if 'http://' in contact.lower() or 'https://' in contact.lower():
                contact = contact.lower().replace('https://', '').replace('http://', '')
            
            if '@' in contact and contact[-1].isalpha():
                email = contact.lower()
            elif re.match(pattern_url, contact) and contact[-1].isalpha():
                url = contact.lower()
            elif len(contact) > 4 and contact[-1].isnumeric():
                contact = contact.replace('-', '').\
                    replace('(', '').\
                    replace(')', '').\
                    replace('+', '').\
                    replace(' ', '')
                if contact.startswith('380') and len(contact) == 12:
                    phone = contact + ';'
                elif contact.startswith('80') and len(contact) == 11:
                    phone = f'3{contact};'
                elif contact.startswith('0') and len(contact) == 10:
                    phone = f'38{contact};'
                else:
                    other = contact
            else:
                other += contact
        
        new_ds.append([registration, date, code, form, name, phone, email, url, other])

with open('new_dataset.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerows(new_ds)