#!/usr/local/bin/python3

##########################################################################
#
# This script contains the main part of hallgrim and is the only script that
# needs to be invoked. The steps it takes to generate a task are as follows:
#
# * parse the commandline arguments with argparse
# * for each script determine the type and validate correct syntax
# * delegate the script to a handler for the specific type
# * the handler parses the script into the intermediate representation (mostly
#   arrays)
# * the handler passes the needed information to the script generator, which
#   will print the final xml file.
# * a finisher compresses data if needed (needs to be implemented, maybe as
#   separate subparser).
#
##########################################################################

import importlib
import argparse
import os
import sys
import configparser

# local import
from hallgrim.IliasXMLCreator import packer
from hallgrim.custom_markdown import get_markdown
from hallgrim.messages import *
from hallgrim.parser import *
from hallgrim.uploader import send_script


def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def file_to_module(name):
    return name.rstrip('.py').replace('/', '.')


def type_selector(type):
    if 'multi' in type:
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

    parser_gen = subparsers.add_parser(
        "upload", help="Subcommand to upload created xml instances.")
    parser_gen.add_argument(
        'script',
        help='The script that should be uploaded',
        type=file_exists,
        metavar='FILE')

    args = parser.parse_args()

    if args.command == 'gen':
        delegator(args.out, args.input, args.instances)
    if args.command == 'upload':
        handle_upload(args.script, args.host)
    if args.command == 'new':
        handle_new_script(args.name, args.type, args.author, args.points)
    if args.command == None:
        parser.print_help()


def delegator(output, script_list, instances):
    """
    It gets a list of filenames and delegates them to the correct handler.
    Every file that does not end with .py will be ignored. Each script
    is imported and then passed as module to the handler.

    Arguments:
        output {filename}  -- where to write the finished XML document
        script_list {list} -- a list of filenames that contain scripts
        instances {int}    -- number of instances that should be generated
    """
    for script_name in filter(lambda a: a.endswith('.py'), script_list):
        script = importlib.import_module(file_to_module(script_name))
        handler = {
            'gap': handle_gap_questions,
            'single': handle_choice_questions,
            'single choice': handle_choice_questions,
            'multi': handle_choice_questions,
            'multiple choice': handle_choice_questions
        }[script.meta['type']]

        handler(output, script, instances)


def handle_gap_questions(output, script, instances):
    """ Handles gap questions of all kinds

    A script can contain any mixture of gap, numeric gap and choice gap
    questions. The data object that is needed by the XML creating scripts
    is generated and the task itself is handled by the parser. The parser
    returns the intermediate representation of the task.

    Arguments:
        output {str}    -- where to write the final file
        script {module} -- the loaded module that describes the task
        instances {int} -- number of instances that should be generated
    """
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
    info('Processed "{}" and'.format(script.__name__))
    info('wrote xml "{}"'.format(output), notag=True)


def handle_choice_questions(output, script, instances):
    """
    Handles multiple and single choice questions. The relevant parts of the
    script are fed into a parser that return the correct intermediate
    representation for the task. In this case a list of answers.

    Arguments:
        output {str}    -- where to write the finished XML document
        script {module} -- the loaded module that describes the task
        instances {int} -- number of instances that should be generated
    """
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
        'feedback': markdown(script.feedback)
    }

    output = os.path.join(
        'output', script.meta['title']) + '.xml' if not output else output
    packer.convert_and_print(data, output, instances)
    info('Processed "{}" and'.format(script.__name__))
    info('wrote xml "{}"'.format(output), notag=True)


def handle_new_script(name, qtype, author, points):
    """ Creates a new script file.

    Takes in some meta information from the command line of if not present takes
    it from the config.ini or uses default values.

    TODO: put the configuration before the parser and use as default values

    Arguments:
        name {str}     -- name of the script, will also become filename
        qtype {str}    -- question type (choice, gap, alignment)
        author {str}   -- the author of the script
        points {float} -- number of points for the task
    """
    from hallgrim.templates import scaffolding
    config = get_config()

    if not author:
        author = config['META']['author']

    with open('scripts/' + name + '.py', 'w') as new_script:
        choice = ''
        if qtype in ['multiple choice', 'single choice']:
            choice = '\nchoices = """\n[X] A\n[ ] B\n[ ] C\n[X] D\n"""\n'

        print(scaffolding.format(
            author, name, qtype, points, choice).strip(), file=new_script)
        info('Generated new script "{}."'.format(new_script.name))


def handle_upload(script_path):
    """ Passes data to the upload script.

    The status code should be 500, since ILIAS always replies with that error
    code after an upload is confirmed. If anything else the script will say
    the status code was bad.

    Arguments:
        script_path {str} -- path to the file that should be uploaded
    """
    config = get_config()
    r = send_script(
        script_path,
        config['UPLAODER']['host'],
        config['UPLAODER']['user'],
        config['UPLAODER']['pass'],
        config['UPLAODER']['rtoken'],
    )
    info("Uploaded %s. Status code looks %s." %
         (script_path, "good" if r else "bad"))

if __name__ == '__main__':
    markdown = get_markdown()
    parseme()
