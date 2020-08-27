import os
import configparser


class configParser:
    def __init__(self):
        self.config = configparser.ConfigParser()
        if not os.path.isfile('config.ini'):
            self.config['showCfg'] = {'show_format': 'asc',
                                      'show_time': '1'}
            self.config['sendCfg'] = {'send_format': 'asc', 'auto_send_cnt': '0', 'auto_send_time': '0',
                                      'porting_send_cnt': '0', 'porting_send_time': '0'}
            self.config['windowHide'] = {'right': '0', 'send_button': '0', 'send_line': '0'}
            self.config['ipcCfg'] = {'document': 'D:/00_personal/py_lesson/myCmdParser/ipc_par_inject.xml'}
            self.config['sendRecord'] = {'send1': '', 'send2': '', 'send3': '', 'send4': '', 'send5': '',
                                         'send6': '', 'send7': '', 'send8': '', 'send9': '', 'send10': '',
                                         'autoSend': '',
                                         'portingSend1': '', 'portingSend2': '', 'portingSend3': '',
                                         'portingSend4': '', 'portingSend5': '', 'portingSend6': '',
                                         'portingSend7': '', 'portingSend8': '', 'portingSend9': '', 'portingSend10': ''
                                         }
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)

        self.config.read('config.ini')
        print(self.config.sections())

    def is_show_time(self):
        return self.config.getboolean('showCfg', 'show_time')

    def get_ipc_document(self):
        return self.config.get('ipcCfg', 'document')

    def get_show_format(self):
        return self.config.get('showCfg', 'show_format')

    def get_send_format(self):
        return self.config.get('sendCfg', 'send_format')

    def get_right_hide(self):
        return self.config.get('windowHide', 'right')

    def get_send_button_hide(self):
        return self.config.get('windowHide', 'send_button')

    def get_send_line_hide(self):
        return self.config.get('windowHide', 'send_line')

    def get_send_record(self):
        send_list = []
        for option in self.config.options('sendRecord'):
            if str(option).startswith('send'):
                send_list.append(self.config.get('sendRecord', option))
        return send_list

    def get_porting_send_record(self):
        send_list = []
        for option in self.config.options('sendRecord'):
            if str(option).startswith('portingsend'):
                send_list.append(self.config.get('sendRecord', option))
        return send_list

    def get_porting_send_cnt(self):
        return self.config.get('sendCfg', 'porting_send_cnt')

    def get_porting_send_time(self):
        return self.config.get('sendCfg', 'porting_send_time')

    def get_auto_send_record(self):
        return self.config.get('sendRecord', 'autoSend')

    def get_auto_send_cnt(self):
        return int(self.config.get('sendCfg', 'auto_send_cnt'))

    def get_auto_send_time(self):
        return int(self.config.get('sendCfg', 'auto_send_time'))

    def get_serial_config_list(self):
        ser_list = []
        for section in self.config.sections():
            if str(section).startswith('serialCfg'):
                ser_dict = {'name': self.config.get(section, 'name'), 'port': self.config.get(section, 'port'),
                            'baud': self.config.get(section, 'baud'), 'data': self.config.get(section, 'data'),
                            'stop': self.config.get(section, 'stop'), 'parity': self.config.get(section, 'parity')}
                ser_list.append(ser_dict)
        return ser_list

    def set_show_format(self, args):
        self.config.set('showCfg', 'show_format', args)

    def set_send_format(self, args):
        self.config.set('sendCfg', 'send_format', args)

    def add_serial_config(self, dic):
        i = 0
        while 1:
            section_str = 'serialCfg' + str(i)
            if self.config.has_section(section_str) is False:
                self.config.add_section(section_str)
                self.config.set(section_str, 'name', dic['name'])
                self.config.set(section_str, 'port', dic['port'])
                self.config.set(section_str, 'baud', str(dic['baud']))
                self.config.set(section_str, 'data', str(dic['data']))
                self.config.set(section_str, 'stop', str(dic['stop']))
                self.config.set(section_str, 'parity', dic['parity'])
                break
            i = i + 1

    def delete_serial_config(self, dic):
        for section in self.config.sections():
            if str(section).startswith('serialCfg'):
                cur_name = self.config.get(section, 'name')
                if cur_name == dic['name']:
                    delete_section = section
                    print(delete_section)
                    break
        try:
            self.config.remove_section(delete_section)
        except:
            pass

    def set_auto_send(self, text, cnt, time):
        self.config.set('sendRecord', 'autosend', text)
        self.config.set('sendCfg', 'auto_send_cnt', cnt)
        self.config.set('sendCfg', 'auto_send_time', time)

    def set_polling_send_message(self, num, text):
        option = 'portingsend' + num
        self.config.set('sendRecord', option, text)

    def set_polling_send_cnt_time(self, cnt, time):
        self.config.set('sendCfg', 'porting_send_cnt', cnt)
        self.config.set('sendCfg', 'porting_send_time', time)

    def write_to_config(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
            configfile.close()

    def get_port_count(self):
        num = 0
        for section in self.config.sections():
            if str(section).startswith('serialCfg'):
                num = num + 1
        return num

    def set_config(self, section, option, value):
        if section in self.config.sections():
            if option in self.config.options(section):
                self.config.set(section, option, value)
