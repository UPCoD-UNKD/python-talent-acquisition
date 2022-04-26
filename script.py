import csv
import re

email = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" # regular exspresion to get email address
#telephone = r'^\s?(?:\+38)?(?:\([0-9]{3}\)[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|\s?380[ .-]?[0-9]{2}[ .-]?[0-9]{3}[ .-]?[0-9]{4}|\s?\+?380[0-9]{9})$' # regular exspresion to get phone number
website = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))" # regular exspresion to get website
telephone = r'\+?380[0-9]{9}|0[0-9]{9}'

with open('dataset.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter='\t')

    zero = 0
    with open("myfile.txt", "w") as file1:
        for i in csv_reader:
            zero += 1
            file1.write(str(zero) + ' -------------- >' + i[-2] + '\n')
            #print(zero, '--------------')

            #print(i[-2])

            em = re.findall(email, i[-1])
            tel_result = []
            web = re.findall(website, i[-1])
            web_result = [x[0] for x in web]

            for item in i[-1].split(';'):
                remove = ['-', ' ', '(', ')', '+']
                for i in item:
                    if i in remove:
                        item = item.replace(i, '')
                tel = re.findall(telephone, item)
                if tel:
                    if len(tel[0]) == 10:
                        tel[0] = '38' + tel[0]
                    tel_result.append(tel)
            
            if tel_result:
                file1.write('phone: ' + str(tel_result) + '\n')
                #print('phone: ', tel_result)

            if em:
                file1.write('email: ' + str(em) + '\n')
                #print('email: ', em)

            if web_result:
                file1.write('website: ' + str(web_result) + '\n')
                #print('website: ', web_result)