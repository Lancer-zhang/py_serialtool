import os
import configparser


class configParser:
    def __init__(self):
        self.config = configparser.ConfigParser()
        if not os.path.isfile('config.ini'):
            self.config['showCfg'] = {'show_format': 'asc',
                                      'show_time': '1',
                                      'show_level': '1',
                                      'show_tag': '1'}
            self.config['sendCfg'] = {'send_format': 'asc'}
            self.config['level color'] = {'debug': 'green',
                                          'info': 'yellow',
                                          'warning': 'orange',
                                          'error': 'red'}
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)

        self.config.read('config.ini')
        print(self.config.sections())

    def is_show_time(self):
        return self.config.getboolean('showCfg', 'show_time')

    def is_show_level(self):
        return self.config.getboolean('showCfg', 'show_level')

    def is_show_tag(self):
        return self.config.getboolean('showCfg', 'show_tag')

    def get_show_format(self):
        return self.config.get('showCfg', 'show_format')

    def get_send_format(self):
        return self.config.get('send config', 'send_format')

    def get_serial_config_list(self):
        ser_list = []
        for section in self.config.sections():
            if str(section).startswith('serialCfg'):
                ser_dict = {'name': self.config.get(section, 'name'), 'port': self.config.get(section, 'port'),
                            'baud': self.config.get(section, 'baud'), 'data': self.config.get(section, 'data'),
                            'stop': self.config.get(section, 'stop'), 'parity': self.config.get(section, 'parity'),
                            '_id': self.config.get(section, '_id')}
                ser_list.append(ser_dict)
        return ser_list

    def set_show_format(self, args):
        self.config.set('showCfg', 'show_format', args)

    def set_send_format(self, args):
        self.config.set('sendCfg', 'send_format', args)

    def add_serial_config(self, dic):
        num = self.get_port_count()
        section_str = 'serialCfg' + str(num)
        self.config.add_section(section_str)
        self.config.set(section_str, 'name', dic['name'])
        self.config.set(section_str, 'port', dic['port'])
        self.config.set(section_str, 'baud', str(dic['baud']))
        self.config.set(section_str, 'data', str(dic['data']))
        self.config.set(section_str, 'stop', str(dic['stop']))
        self.config.set(section_str, 'parity', dic['parity'])
        self.config.set(section_str, '_id', str(dic['_id']))

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
