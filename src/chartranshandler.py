import binascii


def hex2ascii(inputS):
    strList = str(inputS).split(' ')
    outStr = ''
    for iStr in strList:
        try:
            int_num = int(iStr, 16)
        except ValueError:
            return 'Error source, Please check it!'
        outStr = outStr + chr(int_num)
    return outStr


def ascii2hex(inputS):
    str_bin = inputS.encode('utf-8')
    str_hex = binascii.hexlify(str_bin).decode('utf-8')
    output_s = ''
    while str_hex != '':
        try:
            num = int(str_hex[0:2], 16)
            num = hex(num)
        except ValueError:
            return 'Error source, Please check it!'
        str_hex = str_hex[2:].strip()
        output_s = output_s + ' ' + str(num)
    return output_s
