import time


class Logger:
    log = ''
    terminate = False

    @staticmethod
    def do_log(text):
        print(text)
        Logger.log = text
        time.sleep(0.15)
