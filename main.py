import re
import os

class Parser:
    def __init__(self, path):
        self.path = path
        self.check_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        self.check_phone_number = r"\+?3?8?\(?\d{3}\)?\s?-?\d{3}\s?-?\d{2}\s?-?\d{2}\n?$"
        self.domain_pattern = r"(www|http:|https:)+[^\s]+[\w]"
        self.data = ''

    def start(self):
        lambda_add = lambda some_list: "".join([i.ljust(50) for i in some_list]) + "\n"
        table = lambda_add(["phone number", "email address", "website"])
        with open(self.path, 'r') as file:
            self.data = file.readlines()
            for row in self.data:
                row_to_add = {"phones": "none", "email": "none", "website": "none"}
                row = re.split(";|,| ", "".join(row.split("\t")[-1:]))
                phones = []
                for phone in row:
                    if re.search(self.check_phone_number, phone.strip()):
                        fix_phone = re.search(self.check_phone_number, phone.strip())[0]
                        fix_phone = f"38{fix_phone}" if fix_phone[0] == '0' else (
                            f"3{fix_phone}" if fix_phone[0] == '8' else (
                                f"{phone.replace('+','')}" if fix_phone[0] == '+' else fix_phone
                            )
                        )
                        fix_phone = ''.join(filter(str.isalnum, fix_phone))
                        phones.append(fix_phone)
                row_to_add["phones"] = ",".join(phones) if phones else "none"

                for email in row:
                    if re.search(self.check_email, email):
                        row_to_add["email"] = email.strip()

                for site in row:
                    if re.search(self.domain_pattern, site):
                        row_to_add["website"] = site.strip()

                if any(row_to_add.values()):
                    table += lambda_add([row_to_add['phones'], row_to_add['email'], row_to_add['website']])
            with open("final.csv", "w") as wf:
                wf.write(table)


if __name__ == '__main__':
    prog = Parser('dataset.csv').start()
