import time
from main import global_data as g_data
import re


class receiveHandler:
    def __init__(self):
        self.pre_str = ''
        self.pre_complete = False
        self.last_sequence = -1

    def rec_parser(self, data):
        pass

    def rec_str_parse(self, data):
        out_s = []
        str_list = []
        half_s = False
        data_s = str(data, encoding="utf-8")
        if re.search(r'[\r\n]', data):
            s_list = data_s.split('\r\n')
            str_list = [st for st in s_list if st != '']
        else:
            str_list.append(data_s)
            half_s = True
        print('-----start-----')
        print(str_list)
        list_len = len(str_list)
        i = 0
        while i < list_len:
            current_str = ''
            cur_s = re.sub(r'[\r\n]', '', str_list[i])
            pat = r'[EWID] \|[a-zA-Z]{2,4} '
            if re.search(pat, cur_s):
                if list_len == 1:
                    if half_s:
                        self.pre_str = cur_s
                    else:
                        current_str = cur_s
                elif list_len > 1:
                    if i == 0:
                        self.pre_complete = True
                        current_str = cur_s
                    elif i == (list_len - 1):
                        self.pre_str = cur_s
                    else:
                        current_str = cur_s
            else:
                if i == 0:
                    self.pre_str = self.pre_str + cur_s
                    self.pre_complete = True
            if self.pre_complete and self.pre_str != '':
                self.pre_complete = False
                out_s.append(self.pre_str)
                print("pre_str"+self.pre_str)
                self.pre_str = ''
            if current_str != '':
                out_s.append(current_str)
                print("current_str" + current_str)
            i = i + 1
        print(out_s)
        return self.show_and_filter_handler(out_s)

    def rec_hex_parse(self, data):
        length = len(data)
        i = 0
        while i < length:
            if data[i] == 0x55 and (i+63) < (length-1):
                pass

    def show_and_filter_handler(self, data):
        out_str = ''
        for st in data:
            print(st)
            lvl_s = st[0:2].strip().lower()
            tag_s = st[3:9].strip()
            time_s = time.strftime('%H:%M:%S')
            data_s = st[9:].strip()
            if lvl_s not in g_data.level_flag or g_data.level_flag[lvl_s] not in g_data.rec_filter['level']:
                continue
            if len(g_data.rec_filter['tag']) is not 0 and tag_s not in g_data.rec_filter['tag']:
                continue
            if len(g_data.rec_filter['content']) is not 0:
                has_content = False
                for content in g_data.rec_filter['content']:
                    rst = data_s.find(content)
                    if rst is not -1:
                        has_content = True
                if has_content is False:
                    continue
            if g_data.rec_show['level']:
                out_str = out_str + lvl_s + ' '
            if g_data.rec_show['time']:
                out_str = out_str + time_s + ' '
            if g_data.rec_show['tag']:
                out_str = out_str + tag_s + ']: '
            out_str = out_str + data_s + '\r\n'
            if g_data.plug_tool['ipc']:
                ipc_s = data_s.split(']:')[1]
                print(ipc_s)
        print('-----end-----')
        return out_str



