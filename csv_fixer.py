import csv

with open('dataset.csv', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    items = list(reader)

approved_num_codes = ('031', '032', '033', '034', '035', '036',
                      '041', '043', '044', '045', '048',
                      '050', '051', '052', '053', '054', '055', '056', '057',
                      '061', '062', '063', '064', '066', '067', '073',
                      '091', '092', '093', '094', '095', '096', '097', '098', '099')

number_starts = {'80': '380', '0380': '380', '00380': '380', '3800': '380',
                 '3080': '380', '030': '380', '080': '380', '300': '380',
                 '30': '380', '00': '380', '0': '380'}


def verify_number(n):
    n = i.strip('+:;.?"')
    for sign in '-()_':
        n = n.replace(sign, '')

    for key, value in number_starts.items():
        if n.startswith(key):
            n = n.replace(key, value, 1)
            break

    if len(n) == 12:
        return n


def verify_email(address):
    address = address.strip(';"').lower()
    email_user_name, domain_name = address.split('@', 1)
    if len(email_user_name) > 1 and '.' in domain_name:
        return address


def verify_domain(domain_name):
    domain_name = domain_name.lower()

    if not domain_name.strip('.+').isnumeric() and \
            not ''.join(domain_name.split('.')).isnumeric() and '.' in domain_name.strip('.'):
        return domain_name
    else:
        return 'N/A'


mails = []
numbers = []
sites = []

for item in items:
    cur_nums = set()
    cur_mails = set()
    site = ''
    for i in list(item.values())[0].split()[7:]:

        # EMAIL
        if '@' in i:
            email = verify_email(i)
            if email:
                cur_mails.add(email)
            break

        # NUMBER
        for num in approved_num_codes:
            if num in i and len(i) in (10, 11, 12, 13, 14, 15, 16, 18, 19) and not i.startswith('10'):
                number = verify_number(i)
                if number:
                    cur_nums.add(number)
                break

    # SITE
    probable_domain_name = ''.join(list(item.values())[0].split()[-1])

    if '"' not in probable_domain_name and '@' not in probable_domain_name and not probable_domain_name.isnumeric() \
            and probable_domain_name.isascii() and '.' in probable_domain_name and len(probable_domain_name) > 1:
        site += verify_domain(probable_domain_name)
    else:
        site = 'N/A'
    if len(cur_mails) == 1:
        mails.append(cur_mails.pop())
    else:
        mails.append('N/A')

    if len(cur_nums) >= 1:
        numbers.append('; '.join(list(cur_nums)))
    else:
        numbers.append('N/A')

    sites.append(site)

with open('new_dataset.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for row in list(zip(numbers, mails, sites)):
        writer.writerow(row)
