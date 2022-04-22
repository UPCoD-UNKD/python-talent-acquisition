import csv
import re


# No need to use Pandas in such a simple program. csv is times faster than pandas

ALL_CONTACTS = []


# Simple is better than complex
class GetAllData:

    def collect_data(self):
        # Open the unparsed dataset.csv file
        with open("../dataset.csv", "r") as file:
            # Putting the file object instance into a "reader" mode
            dataset = csv.reader(file)
            for row in dataset:
                # Here we got all the contact data, extracted by regex
                phones, mails, urls = self.__collect_row_data(row[0])
                if phones or mails or urls:
                    # The thing is urls are saved in such a weird format, like: [('www.telbin', '', '', '', ''), ('www.101.ua', '', '', '', '')]
                    # And besides that urls need to be parsed, also the mail addresses can get to urls list.
                    # All these problems are being solved in the function:
                    urls = self.__manage_urls(mails, urls)
                    append_data = phones, mails, urls
                    # That's all, here we save contact data to MAIN list that's going to be saved into a new .csv file
                    ALL_CONTACTS.append(append_data)

    @staticmethod
    def __collect_row_data(row):
        # ALL THE REGEX WERE GOOGLED, I've tried to choose the best ones
        # At first, we got all the possible phone numbers that are contained in a row
        _all_phones = re.findall(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", row)
        # Here we sort phones, leaving only phones that starts with "380". Slava Ukraini
        ukrainian_phones = list(filter(lambda phone: phone.startswith("380"), _all_phones))
        mails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', row)
        # This is something, I know
        urls = re.findall(
            r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))",
            row)

        return ukrainian_phones, mails, urls

    @staticmethod
    def __manage_urls(mails, urls):
        if urls:
            replace_trash_urls = [site[0] for site in urls]
            urls = list(filter(lambda site: site not in mails, replace_trash_urls))
        return urls


def write():
    headers = ["Phones", "Mails", "Sites"]
    with open("../final.csv", "w", newline="") as result_file:
        csvwriter = csv.writer(result_file)
        csvwriter.writerow(headers)
        csvwriter.writerows(ALL_CONTACTS)


if __name__ == '__main__':
    get_instance = GetAllData()
    get_instance.collect_data()
    write()
