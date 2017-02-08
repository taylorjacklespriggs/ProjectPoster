

class FileLogger:
    def __init__(self, filename):
        self.filename = filename
        open(self.filename, 'w').close()
        print("Logging to file %s"%self.filename)
    def log(self, msg):
        with open(self.filename, 'a') as file:
            file.write('%s\n'%msg)


class ConsoleLogger:
    def log(self, msg):
        print(msg)


class NullLogger:
    def log(*_):
        pass


