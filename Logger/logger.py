import logging
import os
import inspect


class Logger:
    __instance = None

    def __init__(self, ):

        self.logger = logging.getLogger()

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(Logger, cls).__new__(cls)
            return cls.__instance
        else:
            raise SyntaxError('This class shall not be instantiated this way. Use get_instance() method.')

    def set_logger(self, logfile):
        if not os.path.exists(os.path.dirname(logfile)):
            os.makedirs(os.path.dirname(logfile))
        self.logger.setLevel(logging.DEBUG)
        log_formatter = logging.Formatter("%(funcName)20s()[%(levelname)-5.5s]  %(message)s ")
        filehandler = logging.FileHandler(logfile)
        filehandler.setFormatter(log_formatter)
        self.logger.addHandler(filehandler)
        consolehandler = logging.StreamHandler()
        consolehandler.setFormatter(log_formatter)
        self.logger.addHandler(consolehandler)

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance


def log(message):
    print('{1}()-> {0}'.format(message, inspect.stack()[1][3]))
