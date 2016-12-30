import sys

def warn(message):
    print('[WARN]', message)

def debug(message):
    print('[DEBUG]', message)

def info(message, notag=False):
    print('[INFO]' if not notag else '      ', message)

def error(message):
    print('[ERROR]', message)

def abort(message):
    print('[FATAL]', message)
    sys.exit('exiting...')

def exit(message='exiting...'):
    sys.exit(message)