class Logger:
    log = ''

    @staticmethod
    def do_log(text, qtlog=[]):
        print(text)
        if qtlog:
            qtlog.append(text)
        return None
