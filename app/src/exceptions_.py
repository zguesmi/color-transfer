import sys


class BaseException(Exception):

    def messages(self, key, param=None):
        return {
            # Warning
            # Error
            'InputConfigNotFound': 'can not load input config file - {}',
            'CantTransferColor': 'can not transfer color between images',
            'CantRenameInputFiles': 'can not rename input files to avoid removing them by the sdk',
            'CantCreateConsensusFile': 'can not create consensus file - {}',
            # Fatal
            'IllegalInputConfigFormat': 'can not parse input config file',
        }[key].format(param)

    def __init__(self, category, key=None, param=None):
        message = self.messages(key, param) if key is not None else ''
        print('[{}] {}'.format(category, message))
        return


class Warning(BaseException):

    def __init__(self, err=None, key=None, param=None):
        super().__init__('WARNING', key=key, param=param)
        if err is not None: print(err)


class Error(BaseException):

    def __init__(self, err=None, key=None, param=None):
        super().__init__('ERROR', key=key, param=param)
        if err is not None: print(err)


class Fatal(BaseException):

    def __init__(self, err=None, key=None, param=None):
        super().__init__('FATAL', key=key, param=param)
        if err is not None: print(err)
        sys.exit()