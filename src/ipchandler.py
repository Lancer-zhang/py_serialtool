import codecs
import re
import yaml
import chartranshandler

import ipcparser
import os


class ipcHandler:
    def __init__(self):
        self.ipc = ipcparser.ipc_parser()

    def parseIpcData(self, ipc_str, ipc_xml, log_description_list):
        ipcOutStr, ipcList = self.ipc.Stuff(ipc_str)
        if ipc_xml == '' or len(ipcList) is 0:
            return ipcOutStr
        else:
            pat = r'<ApplInfo  TAG0="0x%02X" TAG1 = "0x%02X" TAG2 = "0x%02X" .+\n.+\>' % (
                ipcList[0]['tag1'], ipcList[0]['tag2'], ipcList[0]['tag3'])
            patDes = r'Description = "[\w ]+"'
            patInd = r'Indication = "\w*"'
            with codecs.open(ipc_xml, "r", encoding='utf-8', errors='ignore') as fData:
                content = fData.read()
                resultStr = re.findall(pat, content)[0]
                resultDes = re.findall(patDes, resultStr)[0]
                resultInd = re.findall(patInd, resultStr)[0]
                fData.close()
            resultLog_s = ''
            for log_description in log_description_list:
                if str(log_description) in resultDes:
                    resultLog_b = ipcList[0]['appl_data']
                    resultLog_s = '\nLog decode :' + resultLog_b.decode('utf-8', 'ignore')
            return ipcOutStr + resultDes + ' ' + resultInd + resultLog_s

    def generate_tips_file(self, inputXml):
        pat = r'<ApplInfo  TAG0=.+\n.+\>'
        pat_tag = r'0x..'
        patDes = r'Description = "[\w ]+"'
        ipc_tips = os.getcwd() + "\\config\\ipc_tips.yaml"
        ipc_tip_dir = {}
        if inputXml != '':
            with codecs.open(inputXml, "r", encoding='utf-8', errors='ignore') as fData:
                content = fData.read()
                resultList = re.findall(pat, content)
                fData.close()
            for result in resultList:
                tag_str = ''
                tip_str = ''
                tags = re.findall(pat_tag, result)
                for tag in tags:
                    tag_str = tag_str + tag[2:]
                des = re.findall(patDes, result)[0]
                Description = str(des[14:]).strip('"')
                if Description.startswith('MTS '):
                    tip_str = tip_str + '---> '
                elif Description.startswith('STM '):
                    tip_str = tip_str + '<--- '
                else:
                    tip_str = tip_str + '<--> '
                tip_str = tip_str + Description
                ipc_tip_dir[str(tag_str)] = tip_str
            print(ipc_tip_dir)
            with open(ipc_tips, mode='w', encoding='utf-8') as file:
                yaml.dump(ipc_tip_dir, file)
            file.close()

    def parseIpcFile_soc(self, inputfile, outfile, inputXml, inputLog_list,
                         show_origin=True, show_detail=True, show_other=False):
        filename = str(inputfile).split('\\')[-1]
        analysed_log = os.getcwd() + "\\bin\\analysed_log.txt"
        ipc_tips = os.getcwd() + "\\config\\ipc_tips.yaml"
        cmd1 = 'cd bin & copy %s %s & LogAnalyser.exe -f %s & del %s' % (inputfile, filename, filename, filename)
        cmd2 = 'del %s' % analysed_log
        os.system(cmd1)
        if outfile == '':
            outfile = os.getcwd() + "\\data\\analysed_log_" + filename
        elif str(outfile).endswith('.txt'):
            pass
        else:
            outfile = outfile + '\\analysed_log_' + filename
        print(outfile)
        if os.path.isfile(ipc_tips):
            with open(ipc_tips, 'r') as tip_file:
                content = tip_file.read()
                tip_file.close()
            tip_dir = yaml.load(content, Loader=yaml.FullLoader)
        else:
            self.generate_tips_file(inputXml)
            with open(ipc_tips, 'r') as tip_file:
                content = tip_file.read()
                tip_file.close()
            tip_dir = yaml.load(content, Loader=yaml.FullLoader)
        print(tip_dir)
        if os.path.isfile(analysed_log):
            with open(analysed_log, 'r') as analysed_file:
                read_lines = analysed_file.readlines()
                analysed_file.close()
            with open(outfile, 'w+') as output_file:
                for line in read_lines:
                    line_msgs = line.split()
                    time_msg = line_msgs[0] + ' ' + line_msgs[1]
                    original_msg = ''
                    pack_type = line_msgs[10]
                    msg_info = line_msgs[11]
                    msg_info2 = ' '.join(line_msgs[12:])
                    data = ''
                    tip = '[]'.ljust(40, ' ')
                    msg_info_pre = ''
                    if msg_info2.strip() != '':
                        original_msg = '|Raw data: ' + line_msgs[8]
                        msg_info_pre = msg_info2[0:40] + ')'
                        tag = msg_info_pre[15:17] + msg_info_pre[23:25] + msg_info_pre[31:33]
                        tip_info = tip_dir.get(tag.upper())
                        tip = '[' + str(tip_info).ljust(40, ' ') + ']'
                        data = msg_info2[47:].strip(')')
                        for inputLog in inputLog_list:
                            if inputLog in tip_info:
                                data = chartranshandler.hex2ascii(data)
                    write_line = ' '.join([
                        time_msg, pack_type, msg_info, msg_info_pre, tip, data.ljust(100, ' '), original_msg]) + '\n'
                    output_file.write(write_line)
                output_file.close()
            os.system(cmd2)

    def parseIpcFileDir_soc(self, ipcFile):
        pass

