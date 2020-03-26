import time
from main import global_data as g_data
import re


class receiveHandler:
    def __init__(self):
        self.pre_L_T = ''
        self.pre_str = ''
        self.rest_str = ''
        self.pre_complete = False

    def rec_parse(self, data):
        #to string
        if data[0] != '\r' or data[0] != '\n':
            str_list = str(data, encoding="utf-8").split('\r\n')
            list_len = len(str_list)
            i = 0
            out_s = []
            print(list_len)
            while i < list_len:
                current_L_T = ''
                current_str = ''
                pat = r'[EWID] \|[a-zA-Z]{2,4}'
                if re.search(pat, str_list[i]):
                    if i == (list_len - 1):
                        self.pre_str = str_list[i]
                    elif i == 0:
                        self.pre_complete = True
                        current_str = str_list[i]
                    else:
                        current_str = str_list[i]
                else:
                    if i == 0:
                        self.pre_str = self.pre_str + str_list[i]
                        self.pre_complete = True
                if self.pre_complete:
                    self.pre_complete = False
                    out_s.append(self.pre_str)
                if current_str != '':
                    out_s.append(current_str)
                i = i + 1
            print(out_s)

    def find_head(self):
        pass

    def show_parse(self, data):
        out_s = ''
        str_list = str(data).split('\n')
        # tag = str(data[2:6]).strip()
        print(str_list)
        return out_s

    def filter_parse(self, data):
        pass


