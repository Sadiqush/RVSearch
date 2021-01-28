import time
from multiprocessing import Manager


class Logger:
    manager = Manager()
    terminate = manager.Value('terminate', False)
    log = ''

    @staticmethod
    def do_log(text):
        print(text)
        Logger.log = text
        time.sleep(0.15)
