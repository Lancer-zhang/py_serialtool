#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author ：Kuan
# GUI         ref:http://blog.csdn.net/liuxu0703/article/details/60781107
# arithmetic  ref:https://my.oschina.net/Cw6PKk/blog/750067
# issue ：http://blog.csdn.net/sixtyfour/article/details/14109153
# function ：http://blog.csdn.net/crylearner/article/details/38521685
#            http://blog.csdn.net/robinchenyu/article/details/8989791
from tkinter import *
import ctypes
from ctypes import *
import os
import tkinter.messagebox as messagebox
import numpy as np

appl_data_t = np.dtype({
    'names': ['tag1', 'tag2', 'tag3', 'appl_len', 'appl_datalen', 'appl_data'],
    'formats': ['B', 'B', 'B', '<H', '<H', 'S300']}, align=True)


class ipc_parser:
    def __init__(self):
        ###ipc dll
        root_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
        self.__ipc_dll_path = os.path.join(root_path, 'lib\\ipc_protocol.dll')
        self.__ipc_dll = ctypes.cdll.LoadLibrary(self.__ipc_dll_path)

        ###unpack data
        self.__pt_unpack = c_ubyte(0)
        self.__cid_unpack = c_ubyte(0)
        self.__ack_sn_unpack = c_ubyte(0)
        self.__et_unpack = c_ubyte(0)
        self.__rws_unpack = c_ubyte(0)
        self.__sn_unpack = c_ubyte(0)
        self.__len_app_unpack = c_ushort(0)
        self.__appl_data_t_item_size = appl_data_t.itemsize
        self.__appl_unpack = bytes(self.__appl_data_t_item_size * 50)
        self.__appl_list = []

        self.__appl_len_unpack = c_ubyte(0)
        self.__ret_unpack = c_byte(0)

        self.__ipc_unpack_result = ''

    def createWidgets(self):
        Label(self, text="InputData").grid(row=0)
        Label(self, text="OutPutData").grid(row=1)

        self.InputData = Entry(self, width=400)
        self.InputData.grid(row=0, column=1)

        self.OutPutData = Text(self, width=400, height=10)
        self.OutPutData.grid(row=1, column=1)

        self.StuffButton = Button(self, text='anylse', command=self.Stuff)
        self.StuffButton.grid(row=2, column=0, sticky=W)

        self.ClearButton = Button(self, text='clear', command=self.clear)
        self.ClearButton.grid(row=2, column=1, sticky=W)

    def clear(self):
        self.InputData.delete(0, END)
        self.OutPutData.delete('1.0', END)
        self.InputData.focus()

    def Stuff(self):
        try:
            input_bytes = bytes.fromhex(self.InputData.get().replace(' ', ''))
            self.OutPutData.delete('1.0', END)
            self.__ipc_unpack_result = ''

            self.__ipc_unpack(input_bytes)
            tmp_str = self.__ipc_unpack_result
            self.OutPutData.insert(END, tmp_str)
            self.OutPutData.focus()
        except Exception as e:
            messagebox.showerror('Message', e)
            self.OutPutData.delete('1.0', END)
            self.InputData.focus()
        finally:
            None

    def __print_to_result(self, s):
        self.__ipc_unpack_result = self.__ipc_unpack_result + s + '\n'

    def __ipc_unpack_ack(self):
        self.__print_to_result('pt :%02X | cid:%02X | ack_sn:%02X | et:%02X | rws:%04X'
                               % (self.__pt_unpack.value, self.__cid_unpack.value, self.__ack_sn_unpack.value,
                                  self.__et_unpack.value, self.__rws_unpack.value,))

    def __ipc_unpack_data(self):
        self.__print_to_result('pt :%02X | cid:%02X | sn:%02X | len_app:%04X | app_num:%02X'
                               % (self.__pt_unpack.value, self.__cid_unpack.value, self.__sn_unpack.value,
                                  self.__len_app_unpack.value, self.__appl_len_unpack.value))

        self.__appl_list = np.frombuffer(self.__appl_unpack, dtype=appl_data_t)

        for i in range(self.__appl_len_unpack.value):
            self.__print_to_result('-------------')
            tmp = ''.join(
                ["%02X " % x for x in self.__appl_list[i]['appl_data'][:self.__appl_list[i]['appl_len']]]).strip()
            self.__print_to_result('appno :%02X| tag1:%02X | tag2:%02X | tag3:%02X | len: %02X| value: %s'
                                   % (i, self.__appl_list[i]['tag1'], self.__appl_list[i]['tag2'],
                                      self.__appl_list[i]['tag3'],
                                      self.__appl_list[i]['appl_len'], tmp))

    def __ipc_unpack(self, raw_data=[]):
        self.__ret_unpack = self.__ipc_dll.ipc_unpack(bytes(raw_data), len(raw_data),
                                                      byref(self.__pt_unpack), byref(self.__cid_unpack),
                                                      byref(self.__ack_sn_unpack), byref(self.__et_unpack),
                                                      byref(self.__rws_unpack), byref(self.__sn_unpack),
                                                      byref(self.__len_app_unpack), bytes(self.__appl_unpack),
                                                      byref(self.__appl_len_unpack))
        if (0 != self.__ret_unpack):
            self.__print_to_result('unpack error,error num is%d' % (self.__ret_unpack))
            # self.__print_to_result('-------------')
        else:
            if (2 == self.__pt_unpack.value):
                self.__ipc_unpack_ack()
            else:
                self.__ipc_unpack_data()
