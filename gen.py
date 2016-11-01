try:
    import mistune
except ImportError as err:
    print("Please install mistune to make use of markdown parsing.")
    print("\t pip install mistune")

import importlib
import argparse
import os
import sys

# local import
import hallgrim.IliasXMLCreator.multi
import hallgrim.parser
from hallgrim.messages import *

def filename_to_module(name):
    return name.rstrip('.py').replace('/', '.')

def parseme():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        '--out',
        help='Output file',
        type=argparse.FileType('w'),
        metavar='FILE')
    parser.add_argument(
        '-i',
        '--input',
        help='Script to execute',
        metavar='FILE')

    args = parser.parse_args()
    return args.out, args.input


def main():
    output, script_name = parseme()
    script = importlib.import_module(filename_to_module(script_name))
    data = {
        'description': "_description",
        'question_text': mistune.markdown(script.task),
        'author': script.meta['author'],
        'title': script.meta['title'],
        'maxattempts': '0',
        'shuffle': True,
        'questions': hallgrim.parser.choice_parser(script.choices),
    }

    output = os.path.join('output', script.meta['title']) + '.xml' if not output else output
    hallgrim.IliasXMLCreator.multi.convert_and_print(data, output)
    info('Processed "{}" and wrote xml to "{}".'.format(script_name, output))

if __name__ == '__main__':
    main()