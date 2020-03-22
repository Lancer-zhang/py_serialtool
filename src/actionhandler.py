import time
import configutil


class actionHandler:
    action_cmd = [{'show'}]

    def __init__(self):
        self.showHandler = self.showActionHandler()
        self.filterHandler = self.filterActionHandler()

    class showActionHandler:
        def show_time(self):
            str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            return str_time

        def show_level(self):
            pass

        def show_tag(self):
            pass

    class filterActionHandler:
        filter_list = []

        def filter_level(self):
            pass

        def filter_tag(self):
            pass

        def filter_customize(self):
            pass

        def filter_clear(self):
            pass

