import time
from main import global_data as g_data
import re


class receiveHandler:
    def __init__(self):
        self.pre_str = ''
        self.pre_complete = False
        self.last_sequence = -1

    def rec_str_parse(self, data):
        out_s = []
        s_list = str(data, encoding="utf-8").split('\r\n')
        str_list = [st for st in s_list if st != '']
        print("111")
        print(str_list)
        print("111")
        list_len = len(str_list)
        i = 0
        while i < list_len:
            current_str = ''
            cur_s = re.sub(r'[\r\n]', '', str_list[i])
            pat = r'[EWID] \|[a-zA-Z]{2,4}'
            if re.search(pat, cur_s):
                if i == (list_len - 1):
                    self.pre_str = cur_s
                elif i == 0:
                    self.pre_complete = True
                    current_str = cur_s
                else:
                    current_str = cur_s
                print('212'+current_str)
            else:
                if i == 0:
                    self.pre_str = self.pre_str + cur_s
                    self.pre_complete = True
            if self.pre_complete and self.pre_str != '':
                self.pre_complete = False
                out_s.append(self.pre_str)
                self.pre_str = ''
            if current_str != '':
                out_s.append(current_str)
            i = i + 1
            print("222")
            print(out_s)
            print("222")
        return self.show_handler(out_s)

    def rec_hex_parse(self, data):
        length = len(data)
        i = 0

    def show_handler(self, data):
        out_str = ''
        for st in data:
            lvl_s = st[0:2].strip()
            tag_s = st[3:9].strip()
            time_s = time.strftime('%H:%M:%S')
            data_s = st[9:].strip()
            out_str = out_str + '['
            if g_data.rec_show['level']:
                out_str = out_str + lvl_s + ' '
            if g_data.rec_show['time']:
                out_str = out_str + time_s + ' '
            if g_data.rec_show['tag']:
                out_str = out_str + tag_s + ']: '
            out_str = out_str + data_s + '\r\n'
        print(out_str)
        return out_str

    def filter_parse(self, data):
        pass


