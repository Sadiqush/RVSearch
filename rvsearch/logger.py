import time


class Logger:
    log = ''

    def do_log(self, text):
        self.log = text
        time.sleep(0.15)
