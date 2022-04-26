import re

class DataString:
    
    def __init__(self, full_str):
        patern = 'ГРОМАДСЬКА ОРГАНІЗАЦІЯ'

        pos_patern = full_str.find(patern)        
        if pos_patern > -1:
            self.pos_pars = pos_patern + len(patern)
        else:
            self.pos_pars = -1

        if self.pos_pars > -1:
            self.str_pars = full_str[self.pos_pars :]
        else:
            self.str_pars = ''

        
        emails_or_sites = self.findSitesEmails(self.str_pars)
        self.emails = emails_or_sites['emails']
        self.sites = emails_or_sites['sites']
        self.phones = self.findPhones(self.str_pars)
        self.first_part_str = full_str[:pos_patern] + patern + self.clearStr(self.str_pars).rstrip()
        self.norm_str = ', '.join([self.first_part_str , self.phones , self.emails ,  self.sites]) 

    def clearStr(self, str):
        patern = '(\s[:;,]\s)'
        res = re.sub(patern, '', str)        
        return res


    def findSitesEmails(self, str):
        patern = '[-a-zA-Z0-9@:%_\+.~#?&\/=]{2,256}\.[a-z]{2,4}'
        items = re.findall(patern, str)       
        
        strEmailes = ''
        strSite = ''
        for item in items:
            self.str_pars = self.str_pars.replace(item, ' ')
            if '@' in item:
                strEmailes = strEmailes + item + " "
            else:
                strSite = strSite + item + ' '

             
        strEmailes = strEmailes.strip()
        strSite = strSite.strip()
        
        
        return {'emails':strEmailes , 'sites':strSite}

    

    def findPhones(self, str):
        pattern = "(\+?\d+(\d*[\-\s\(\)\*]?\d*)*)"
        phones = re.findall(pattern, str)
        strPhones = ""
        for phone in phones:
            if len(phone[0])>5:
                self.str_pars = self.str_pars.replace(phone[0], ' ')
                strPhones = strPhones + self.normPhone(phone[0]) + " "
        strPhones = strPhones.strip()
        return strPhones

    def normPhone(self, str):
        pattern = '[\-\s\(\)\*]'
        res = ''
        str = re.sub(pattern,'',str)
        if len(str) == 13 and str[:4] == "+380": 
            return str[1:]
        elif len(str) == 11 and str[:2] == "80":        
            return "3" + str
        elif len(str) == 10 and str[:1] == "0":
            return "38" + str
        elif len(str) == 9:
            return "380" + str
        else:
            return str

        

file1 = open('dataset.csv', 'r', encoding='utf-8')
file2 = open('dataset2.csv','w', encoding='utf-8')

for line in file1:
    str_obj = DataString(line)    
    
    file2.write(str_obj.norm_str+'\n')
file1.close()
file2.close()
print('Ready')


