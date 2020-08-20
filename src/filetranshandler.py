import codecs
import os
import re
from struct import *


# def crc24(crc, firstbyte, secondbyte):
#    crcpoly = 0x80001B
#    #print(type(firstbyte),type(secondbyte))
#    data_word = (secondbyte << 8) | firstbyte
#    result = ((crc << 1) ^ data_word)

#    if result & 0x1000000:
#        result ^= crcpoly

#    return result

def binToHex(src, obj, src_start):
    from intelhex import bin2hex
    if str(src).endswith('.bin') and str(obj).endswith('.hex'):
        if src_start is '':
            offset = 0
        else:
            offset = int(src_start, 16)
        bin2hex(src, obj, offset)


def hexToBin(src, src_start, src_end, obj, obj_start, obj_end, pad):
    from intelhex import hex2bin
    if str(src).endswith('.hex') and str(obj).endswith('.bin'):
        size = None
        s_start = int(src_start, 16)
        s_end = int(src_end, 16)
        padding = int(pad, 16)
        if obj_start is not '' and obj_end is not '':
            start = int(obj_start, 16)
            end = int(obj_end, 16)
            size = end - start
        hex2bin(src, obj, s_start, s_end, size, padding)


def txtToBin(src, obj):
    if str(src).endswith('.txt') and str(obj).endswith('.bin'):

        with codecs.open(src, "r", encoding='utf-8', errors='ignore') as fData:
            content = fData.read()
            fData.close()
        data_list = re.findall(r'0x.{1,2},', content)
        print(data_list)
        fOut = open(obj, 'wb')
        for data in data_list:
            print(data)
            data_num = str(data[2:]).strip(',')
            b = int(data_num, 16)
            fOut.write(pack('B', b))
        fOut.close()
        return


def binToTxt(src, obj):
    if str(src).endswith('.bin') and str(obj).endswith('.txt'):
        file = open(src, 'rb')
        fsize = os.path.getsize(src)
        val = file.read()
        file.close()

        with open(obj, 'w') as nfile:
            # write head info
            nfile.write("const uint8_t buf[]={" + "\n")
            w_cnt = 0
            # crc = 0
            # b_cnt = 0
            nfile.write("\t\t")
            while w_cnt < fsize:
                nfile.write(str(hex(val[w_cnt])) + ",")
                # b_cnt += 1
                # if b_cnt == 2:
                #     b_cnt = 0
                #     crc = crc24(crc, val[w_cnt - 1], val[w_cnt])
                w_cnt += 1
                if (w_cnt % 16) == 0:
                    nfile.write("\n")
                    nfile.write("\t\t")
                #        nfile.write(str(hex(crc)) + "};" + "\n")
            # if b_cnt == 1:
            #     crc = crc24(crc, val[w_cnt - 1], 0)
            # nfile.write(str(hex((crc >> 16) & 0xff)) + "," + str(hex((crc >> 8) & 0xff)) + "," + str(
            #     hex((crc >> 0) & 0xff)) + "};" + "\n")
            nfile.write("};" + "\n")
    return
