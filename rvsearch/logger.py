class Logger:
    def do_log(self, text, qtlog=[]):
        print(text)
        if qtlog:
            qtlog.append(text)
        return None
