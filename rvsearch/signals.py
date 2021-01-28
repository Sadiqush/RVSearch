import time
from multiprocessing import Manager


class Signals:
    manager = Manager()
    terminate = manager.Value('terminate', False)
    log = ''

    @staticmethod
    def do_log(text):
        print(text)
        Signals.log = text
        time.sleep(0.15)
