#!/usr/local/bin/python3

import importlib
import argparse
import os
import sys

# local import
from hallgrim.IliasXMLCreator import packer
from hallgrim.messages import *
from hallgrim.parser import *


def file_to_module(name):
    return name.rstrip('.py').replace('/', '.')


def type_selector(type):
    if 'multiple' in type:
        return 'MULTIPLE CHOICE QUESTION'
    if 'single' in type:
        return 'SINGLE CHOICE QUESTION'

def file_exists(path):
    if not os.path.exists(path):
        msg = 'The script "{}" does not exist.'.format(path)
        raise argparse.ArgumentTypeError(msg)
    return path

def parseme():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    parser_new = subparsers.add_parser("new", help="The utility the generate new scripts.")
    parser_new.add_argument(
        "name",
        help="The name of the new script"
    )
    parser_new.add_argument(
        "-t",
        "--type",
        choices=['multi', 'single', 'gap', 'alignment'],
        default='multi',
        metavar='TYPE'
    )
    parser_new.add_argument(
        "-a",
        "--author",
        help="Name of the scripts author",
        default='ILIAS Author',
        metavar='AUTHOR'
    )
    parser_new.add_argument(
        "-p",
        "--points",
        help='Points given for correct answer (different behavior for different questions)',
        type=float,
        metavar='POINTS',
    )

    parser_gen = subparsers.add_parser("gen", help="Subcommand to convert from script to xml.")
    parser_gen.add_argument(
        '-o',
        '--out',
        help='''Specify different output file. If no argument is given the Name
        of the script is used.''',
        metavar='FILE')
    parser_gen.add_argument(
        'input',
        help='Script to execute',
        type=file_exists,
        metavar='FILE')
    parser_gen.add_argument(
        '-i',
        '--instances',
        help='How many instances should be produced (Only for parametrized questions).',
        type=int,
        default=1,
        metavar='COUNT')

    args = parser.parse_args()

    if args.command == 'gen':
        handle_choice_questions(args.out, args.input, args.instances)
    if args.command == 'new':
        handle_new_script(args.name, args.type, args.author, args.points)
    if args.command == None:
        parser.print_help()


def handle_choice_questions(output, script_name, instances):
    script = importlib.import_module(file_to_module(script_name))
    data = {
        'type': type_selector(script.meta['type']),
        'description': "_description",
        'question_text': markdown(script.task),
        'author': script.meta['author'],
        'title': script.meta['title'],
        'maxattempts': '0',
        'shuffle': True,
        'questions': choice_parser(script.choices, script.meta['points']),
        'feedback': markdown(script.feedback),
    }

    output = os.path.join(
        'output', script.meta['title']) + '.xml' if not output else output
    packer.convert_and_print(data, output, instances)
    info('Processed "{}" and wrote xml to "{}".'.format(script_name, output))

def handle_new_script(name, type, author, points):
    raise NotImplementedError()

if __name__ == '__main__':
    parseme()
