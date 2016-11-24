#!/usr/local/bin/python3

################################################################################
#
# This script contains the main part of hallgrim and ist the only script that
# needs to ne invoked. The steps it takes to generate a task are as follows:
#
# * parse the commandline arguments with argparse
# * for each script determine the type and validate correct syntax
# * delegate the script to a handler for the specific type
# * the handler parses the script into the intermediate represenatation (mostly
#   arrays)
# * the handler passes the needed information to the script generator, which
#   will ptint the final xml file.
# * a finisher compresses data if needed (needs to be implemented, maybe as s
#   eperate subparser).
#
################################################################################

import importlib
import argparse
import os
import sys

# local import
from hallgrim.IliasXMLCreator import packer
from hallgrim.messages import *
from hallgrim.parser import *

scaffolding = r'''
meta = {{
    'author': '{}',
    'title': '{}',
    'type': '{}',
    'points': {},
}}

task = """ decription """
{}
feedback = """ decription """
'''


def file_to_module(name):
    return name.rstrip('.py').replace('/', '.')


def type_selector(type):
    if 'multiple' in type:
        return 'MULTIPLE CHOICE QUESTION'
    if 'single' in type:
        return 'SINGLE CHOICE QUESTION'
    if 'gap' in type:
        return 'CLOZE QUESTION'


def file_exists(path):
    if not os.path.exists(path):
        msg = 'The script "{}" does not exist.'.format(path)
        raise argparse.ArgumentTypeError(msg)
    return path


def script_is_valid(script, required):
    for field in required:
        if not hasattr(script, field):
            error("script does not export '{}' field.".format(field))
    if any(not hasattr(script, field) for field in required):
        abort("Script is invalid (see above)")


def parseme():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    parser_new = subparsers.add_parser(
        "new", help="The utility the generate new scripts.")
    parser_new.add_argument(
        "name",
        help="The name of the new script",
        metavar='NAME'
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
        default=0.0,
        metavar='POINTS',
    )

    parser_gen = subparsers.add_parser(
        "gen", help="Subcommand to convert from script to xml.")
    parser_gen.add_argument(
        '-o',
        '--out',
        help='''Specify different output file. If no argument is given the Name
        of the script is used.''',
        metavar='FILE')
    parser_gen.add_argument(
        'input',
        help='Script to execute',
        nargs='+',
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
        delegator(args.out, args.input, args.instances)
    if args.command == 'new':
        handle_new_script(args.name, args.type, args.author, args.points)
    if args.command == None:
        parser.print_help()


def delegator(output, script_list, instances):
    for script_name in filter(lambda a: a.endswith('.py'), script_list):
        script = importlib.import_module(file_to_module(script_name))
        handler = {
            'gap': handle_gap_questions,
            'single choice': handle_choice_questions,
            'multiple choice': handle_choice_questions
        }[script.meta['type']]

        handler(output, script, instances)


def handle_gap_questions(output, script, instances):
    script_is_valid(script, required=['meta', 'task', 'feedback'])
    data = {
        'type': type_selector(script.meta['type']),
        'description': "_description",
        'gap_list': gap_parser(script.task),
        'author': script.meta['author'],
        'title': script.meta['title'],
        'shuffle': script.meta['shuffle'] if 'shuffle' in script.meta else True,
        'feedback': markdown(script.feedback),
        'gap_length': script.meta['gap_length'] if 'gap_length' in script.meta else 20,
    }

    output = os.path.join(
        'output', script.meta['title']) + '.xml' if not output else output
    packer.convert_and_print(data, output, instances)
    info('Processed "{}" and wrote xml to "{}".'.format(
        script.__name__, output))


def handle_choice_questions(output, script, instances):
    script_is_valid(script, required=['meta', 'task', 'choices', 'feedback'])
    data = {
        'type': type_selector(script.meta['type']),
        'description': "_description",
        'question_text': markdown(script.task),
        'author': script.meta['author'],
        'title': script.meta['title'],
        'maxattempts': '0',
        'shuffle': script.meta['shuffle'] if 'shuffle' in script.meta else True,
        'questions': choice_parser(script.choices, script.meta['points']),
        'feedback': markdown(script.feedback),
    }

    output = os.path.join(
        'output', script.meta['title']) + '.xml' if not output else output
    packer.convert_and_print(data, output, instances)
    info('Processed "{}" and'.format(script.__name__))
    info('wrote xml "{}"'.format(output), notag=True)


def handle_new_script(name, qtype, author, points):
    with open('scripts/' + name + '.py', 'w') as new_script:
        choice = ''
        if qtype in ['multi', 'single']:
            choice = '\nchoices = """\n[X] A\n[ ] B\n[ ] C\n[X] D\n"""\n'

        print(scaffolding.format(
            author, name, qtype, points, choice).strip(), file=new_script)
        info('Generated new script "{}."'.format(new_script.name))

if __name__ == '__main__':
    parseme()
