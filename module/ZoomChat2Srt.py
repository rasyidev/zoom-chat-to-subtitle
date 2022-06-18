import codecs
import re
from datetime import datetime, date, time, timedelta

class ZoomChat2Txt:
    def __init__(self, file_path):
        self.text = ''
        self.start_hour = None
        self.ts0 = [] # timestamp start
        self.ts1 = [] # timestamp end
        self.delays = [] # t1 - t2 in ms
        self.users = []
        self.messages = []
        self.load_file(file_path)
        
    def set_start_hour(self):
        self.start_hour = self.ts0[0].hour
    
    def extract_ts0(self):
        temp = re.findall("(\d{2}:\d{2}:\d{2}) From", self.text)
        for t in temp:
            self.ts0.append(self.txt_to_time(t))
         
    def extract_messages(self):
        messages = re.split("\d{2}:\d{2}:\d{2} From [ \S]+to [ \S]+:", self.text)
        messages.pop(0) # remove the first empty element
        self.messages = [m.strip() for m in messages]
        
    def extract_users(self):
        users = re.findall("\d{2}:\d{2}:\d{2} From ([ \S]+)to [ \S]+:", self.text)
        self.users = [user.strip() for user in users]
    
    def load_file(self, file_path):
        f = codecs.open(file_path, 'r', 'utf-8')
        text = f.readlines()
        self.text = ''.join(text)
        self.extract_messages()
        self.extract_ts0()
        self.extract_users()
        self.set_start_hour()
        self.reset_hour()
        self.generate_delays()
        self.generate_ts1()
    
    
    # input: datetime obj
    # return: resetted datetime object
    def reset_hour(self):
        for i in range(len(self.ts0)):
            self.ts0[i] -= timedelta(hours=self.start_hour)
    
    # input: text
    # return: datetime object
    def txt_to_time(self, text):
        h, m, s = (int(part) for part in text.split(":"))
        t = time(h,m,s)
        return datetime.combine(date.today(), t)
    
    # input: datetime: ts0
    # return: datetime object: ts0 + ms
    def generate_ts1(self):
        for i, t in enumerate(self.ts0):
            self.ts1.append(t + timedelta(milliseconds=self.delays[i]))
        
    
    # input single message
    # return delay time in ms
    def generate_delays(self):
        for i in range(len(self.messages)):
            text_list = re.split("\s", self.messages[i])
            result = len(text_list) * 750
            if result > 3000:
                result = 3000
            self.delays.append(result)
            
    def display_result(self, elements=5):
        for i in range(elements):
            ts1ms = f"{int([self.ts1[0].microsecond/1000 if self.ts1[0].microsecond >= 100000 else self.ts1[0].microsecond][0]):03d}"
            print(i+1)
            print(f"{self.ts0[i].hour:02d}:{self.ts0[i].minute:02d}:{self.ts0[i].second:02d},000  -->  {self.ts1[i].hour:02d}:{self.ts1[i].minute:02d}:{self.ts1[i].second:02d},{ts1ms}")
            print(f"<b>{self.users[i]}</b>: {self.messages[i]}", end="\n\n")
            
            
    def save_srt(self, file_path):
        with codecs.open(file_path, 'w+', 'utf-8') as f:
            for i in range(len(self.users)):
                ts1ms = f"{int([self.ts1[0].microsecond/1000 if self.ts1[0].microsecond >= 100000 else self.ts1[0].microsecond][0]):03d}"
                f.write(str(i+1))
                f.write("\n")
                f.write(f"{self.ts0[i].hour:02d}:{self.ts0[i].minute:02d}:{self.ts0[i].second:02d},000  -->  {self.ts1[i].hour:02d}:{self.ts1[i].minute:02d}:{self.ts1[i].second:02d},{ts1ms}")
                f.write("\n")
                f.write(f"<b>{self.users[i]}</b>: {self.messages[i]}")
                f.write("\n")
                f.write("\n")
            f.close()
        print(f"Success exporting srt files: {file_path}")