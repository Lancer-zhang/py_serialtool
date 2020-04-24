import time
from main import global_data as g_data
import re
import ipcparser


class receiveHandler:
    def __init__(self):
        self.pre_str = ''
        self.pre_complete = False
        self.last_sequence = -1
        self.ipc = ipcparser.ipc_parser()

    def rec_parser(self, data):
        pass

    def rec_str_parse(self, data):
        out_str = ""
        out_list = []
        str_list = []
        half_s = False
        data_s = str(data, encoding="utf-8")#转化为字符串
        #检查是否为有[\r\n]，如果有进行分割，如果没有则判定为半句话柄
        if re.search(r'[\r\n]', data_s):
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
            cur_s = re.sub(r'[\r\n]', '', str_list[i])#如果有单个\r或\n则替换为‘’
            pat = r'[EWID] \|[a-zA-Z]{2,4} '#查找log的开头 level |tag
            if re.search(pat, cur_s):#如果找到了head
                if list_len == 1:#当list长度为1
                    if half_s:#如果一开始就没有\r或\n，且能找到head，则认定该句为上半句
                        self.pre_str = cur_s
                    else:#如果存在\r或\n，且能找到head，认为是一个完整的句柄
                        current_str = cur_s
                elif list_len > 1:#当list长度大于1时
                    if i == 0:#当为第一句时，能找到head，则pre str已经完整
                        self.pre_complete = True
                        current_str = cur_s
                    elif i == (list_len - 1):#当为最后一句时，不论完整与否，赋值给pre str
                        self.pre_str = cur_s
                    else:#中间的句子都是完整的
                        current_str = cur_s
            else:#如果没有找到head
                if list_len == 1:#当list长度为1
                    if half_s:#没有head，且没有\r\n，则为中间句子
                        self.pre_str = self.pre_str + cur_s
                    else:#没有head,但是有\r\n
                        self.pre_str = self.pre_str + cur_s
                        self.pre_complete = True
                elif list_len > 1:#当list长度大于1时
                    if i == 0:#当为第一句时，且没有找到head，则pre str完整
                        self.pre_str = self.pre_str + cur_s
                        self.pre_complete = True
                    elif i == (list_len - 1):#当为最后一句时，且没有找到head，赋值给pre str
                        self.pre_str = cur_s
            if self.pre_complete and self.pre_str != '':
                self.pre_complete = False
                out_list.append(self.pre_str)
                print("pre_str: "+self.pre_str)
                self.pre_str = ''
            if current_str != '':
                out_list.append(current_str)
                print("current_str: " + current_str)
            i = i + 1
        print(out_list)
        out_str = self.show_and_filter_handler(out_list)
        print('-----end-----')
        return out_str

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
            has_content = True
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
            else:
                has_content = True
            if has_content is False:
                continue
            if g_data.rec_show['level']:
                out_str = out_str + lvl_s + ' '
            if g_data.rec_show['time']:
                out_str = out_str + time_s + ' '
            if g_data.rec_show['tag']:
                out_str = out_str + tag_s
            out_str = '[' + out_str + ']: ' + data_s + '\r\n'
            if g_data.plug_tool['ipc']:
                ipc_s = data_s.split(']:')[1]
                out_str = out_str + self.ipc.Stuff(ipc_s)
        return out_str



