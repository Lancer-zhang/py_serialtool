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
                        self.rest_str = str_list[i]
                    elif i == 0:
                        if self.rest_str != '':#上一个while的最后一条为完整的句子，这一个while中的第一个也为完整的句子，则遗漏上一个的最后一条
                            self.pre_str = self.rest_str
                            self.pre_complete = True
                        current_str = str_list[i]
                        self.rest_str = ''
                    else:
                        current_str = str_list[i]
                else:
                    if i == 0:
                        self.pre_str = self.rest_str + str_list[i]
                        self.pre_complete = True
                    elif i == (list_len - 1):
                        self.rest_str = str_list[i]
                if self.pre_complete:
                    out_s.append(self.pre_str)
                    self.pre_complete = False
                    self.pre_str = ''
                out_s.append(current_str)
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

    s = 'D |ipc   [drv send appl data  ]:00 02 05 06 04 01 2A 10 02 01 02 38 00
D |ipc   [drv send appl data  ]:00 02 09 0D 05 01 40 18 06 20 03 11 03 34 08 5E 00
D |ipc   [ipc drv recv raw data]:06 FF 0F 04 41 B5
D |ipc   [ipc drv recv raw data]:06 FF 0F 05 41 B4
D |ipc   [drv send appl data  ]:00 02 05 06 06 01 2A 10 02 01 02 3A 00
D |ipc   [drv send appl data  ]:00 02 09 0D 07 01 40 18 06 20 03 11 03 34 09 5D 00
D |ipc   [ipc drv recv raw data]:06 FF 0F 06 41 B7
D |ipc   [ipc drv recv raw data]:06 FF 0F 07 41 B6
D |ipc   [ipc drv recv raw data]:02 03 04 21 01 01 01 02 22
D |ipc   [drv send ack nack   ]:00 02 06 04 21 41 66 00
D |ipc   [drv send appl data  ]:00 02 09 0D 08 01 40 18 06 20 03 11 03 34 10 4B 00
D |ipc   [drv send appl data  ]:00 02 05 06 09 01 2A 10 02 01 02 35 00
D |ipc   [ipc drv recv raw data]:06 FF 0F 08 41 B9
D |ipc   [ipc drv recv raw data]:06 FF 0F 09 41 B8
D |ipc   [drv send appl data  ]:00 02 09 0D 0A 01 40 18 06 20 03 11 03 34 11 48 00
D |ipc   [ipc drv recv raw data]:06 FF 0F 0A 41 BB
D |ipc   [drv send appl data  ]:00 02 05 06 0B 01 2A 10 02 01 02 37 00
D |ipc   [ipc drv recv raw data]:06 FF 0F 0B 41 BA
D |ipc   [ipc drv recv raw data]:02 03 04 22 01 01 01 02 21
D |ipc   [drv send ack nack   ]:00 02 06 04 22 41 65 00
D |ipc   [drv send appl data  ]:00 02 09 0D 0C 01 40 18 06 20 03 11 03 34 12 4D 00
D |ipc   [ipc drv recv raw data]:06 FF 0F 0C 41 BD '

