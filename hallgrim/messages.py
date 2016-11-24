import sys

def warn(msg):
    print('[WARN]', msg)

def debug(msg):
    print('[DEBUG]', msg)

def info(msg, notag=False):
    print('[INFO]' if not notag else '      ', msg)

def error(msg):
    print('[ERROR]', msg)

def abort(msg):
    print('[FATAL]', msg)
    sys.exit('exiting...')
