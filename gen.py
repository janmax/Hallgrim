#!/usr/local/bin/python3

import importlib
import argparse
import os
import sys

# local import
from hallgrim.IliasXMLCreator import multi, single
from hallgrim.messages import *
from hallgrim.parser import *


def filename_to_module(name):
    return name.rstrip('.py').replace('/', '.')


def type_selector(type):
    if 'multiple' in type:
        return multi
    if 'single' in type:
        return single


def parseme():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        '--out',
        help='''Specifiy different output file. If no argument is given the Name
        of the script is used.''',
        type=argparse.FileType('w'),
        metavar='FILE')
    parser.add_argument(
        'input',
        help='Script to execute',
        metavar='FILE')

    args = parser.parse_args()
    return args.out, args.input


def main():
    output, script_name = parseme()
    script = importlib.import_module(filename_to_module(script_name))
    data = {
        'description': "_description",
        'question_text': markdown(script.task),
        'author': script.meta['author'],
        'title': script.meta['title'],
        'maxattempts': '0',
        'shuffle': True,
        'questions': choice_parser(script.choices),
    }

    output = os.path.join(
        'output', script.meta['title']) + '.xml' if not output else output
    type_selector(script.meta['type']).convert_and_print(data, output)
    info('Processed "{}" and wrote xml to "{}".'.format(script_name, output))

if __name__ == '__main__':
    main()
