import codecs
import os
import re

import openpyxl
from xml.dom.minidom import parse
import xml.dom.minidom


def generate_ipc_info_excel(self, inputXml):
    pat = r'<ApplInfo  TAG0=.+\n.+\>'
    pat_tag = r'0x..'
    pat_len = r'Len = ".{1,3}"'
    pat_mna = r'"MND?A"'
    patDes = r'Description = "[\w ]+"'
    ipc_tips = os.getcwd() + "\\data\\ipc_info.xlsx"

    if inputXml != '':
        with codecs.open(inputXml, "r", encoding='utf-8', errors='ignore') as fData:
            content = fData.read()
            resultList = re.findall(pat, content)
            fData.close()
        i = 2
        wb = openpyxl.load_workbook(ipc_tips)
        for result in resultList:
            column_E = ("E%d" % i)
            column_F = ("F%d" % i)
            column_G = ("G%d" % i)
            column_D = ("D%d" % i)
            column_H = ("H%d" % i)
            column_I = ("I%d" % i)
            column_J = ("J%d" % i)
            i = i + 1
            sheet = wb.get_sheet_by_name("Sheet1")

            tags = re.findall(pat_tag, result)
            sheet[column_E].value = tags[0][2:]
            sheet[column_F].value = tags[1][2:]
            sheet[column_G].value = tags[2][2:]
            print(tags)
            lens = re.findall(pat_len, result)[0]
            len_str = str(lens[6:]).strip('"')
            sheet[column_H].value = len_str
            print(lens)
            mna = re.findall(pat_mna, result)[0]
            mna_str = str(mna).strip('"')
            sheet[column_I].value = mna_str
            print(mna)
            des = re.findall(patDes, result)[0]
            Description = str(des[14:]).strip('"')
            sheet[column_D].value = Description
            if Description.startswith('MTS '):
                sheet[column_J].value = 'send'
            elif Description.startswith('STM '):
                sheet[column_J].value = 'receive'
            else:
                sheet[column_J].value = 'send or receive'
        wb.save(ipc_tips)


def transfer_xml(inject, cfg):
    inject_parse = xml.dom.minidom.parse(inject)
    collection = inject_parse.documentElement
    appInfos = collection.getElementsByTagName("ApplInfo")

    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'ipc_cfg', None)
    root = dom.documentElement
    inc_files = dom.createElement('inc_files')
    root.appendChild(inc_files)

    parameters = dom.createElement('parameters')
    parameters.setAttribute('tx_buffer_size', '4')
    parameters.setAttribute('payload_buffer_size', '256')
    root.appendChild(parameters)

    phy_channel = dom.createElement('phy_channel')
    channel = dom.createElement('channel')
    channel.setAttribute('phy_cid', '0')
    channel.setAttribute('timeout', '200')
    channel.setAttribute('retransmission', '3')
    channel.setAttribute('drv_init', 'ipc_drv_uart_init')
    channel.setAttribute('drv_deinit', 'ipc_drv_uart_deinit')
    channel.setAttribute('drv_send', 'ipc_drv_uart_send')
    channel.setAttribute('drv_mainfunction', 'ipc_drv_uart_mainfunction')
    phy_channel.appendChild(channel)
    root.appendChild(phy_channel)

    channel_map = dom.createElement('channel_map')
    channel2 = dom.createElement('channel')
    channel2.setAttribute('logic_cid', '4')
    channel2.setAttribute('phy_cid', '0')
    channel_map.appendChild(channel2)
    root.appendChild(channel_map)

    message_list = dom.createElement("message_list")
    root.appendChild(message_list)
    for appInfo in appInfos:
        tag0 = appInfo.getAttribute("TAG0")
        tag1 = appInfo.getAttribute("TAG1")
        tag2 = appInfo.getAttribute("TAG2")
        lens = appInfo.getAttribute("Len")
        MnaFlag = appInfo.getAttribute("MnaFlag")
        ApplLogicHandle = appInfo.getAttribute("ApplLogicHandle")
        Name = appInfo.getAttribute("Description")
        Cryptos = appInfo.getAttribute("Cryptos")
        Indication = appInfo.getAttribute("Indication")
        print(tag0, tag1, tag2, lens, MnaFlag, ApplLogicHandle, Name, Cryptos, Indication)
        message = dom.createElement("message")
        message.setAttribute("TAG0", tag0)
        message.setAttribute("TAG1", tag1)
        message.setAttribute("TAG2", tag2)
        message.setAttribute("Len", lens)
        message.setAttribute("MnaFlag", MnaFlag)
        message.setAttribute("ApplLogicHandle", ApplLogicHandle)
        message.setAttribute("Name", str(Name).upper().replace(' ', '_'))
        message.setAttribute("Cryptos", Cryptos)
        message.setAttribute("Indication", Indication)
        message_list.appendChild(message)

    with open(cfg, 'w') as f:
        # 缩进 - 换行 - 编码
        dom.writexml(f, indent="", addindent='\t', newl="\n", encoding='utf-8')
        f.close()


transfer_xml("D:/00_personal/py_lesson/myCmdParser/ipc_par_inject.xml",
             "D:/00_personal/py_lesson/myCmdParser/serialtool/py_serialtool/data/ipc_cfg5.xml")
