import codecs
import re
import ipcparser


class ipcHandler:
    def __init__(self):
        self.ipc = ipcparser.ipc_parser()

    def parseIpcData(self, ipc_str, ipc_xml):
        ipcOutStr, ipcList = self.ipc.Stuff(ipc_str)
        if ipc_xml is '' or ipcList is []:
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
            return ipcOutStr + '\n' + resultDes + ' ' + resultInd

    def parseIpcFile(self, ipcFile):
        pass
