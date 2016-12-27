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

import importlib.util
import argparse
import os
import configparser

# local import
from .IliasXMLCreator import packer
from .custom_markdown import get_markdown
from .messages import warn, info, error, abort
from .parser import choice_parser, gap_parser, order_parser
from .uploader import send_script
from .templates import scaffolding

__all__ = ['parseme']

# set markdown
markdown = get_markdown()

def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if not config.sections():
        warn('Could not find config file.')
        warn('Please edit config.sample.ini and move it to config.ini')
        info('Continue with default values. Script might fail.')
        config['META'] = {'author': '__default__'}
    return config


def look_for_output():
    if not os.path.exists('output'):
        info('Created directory "output/"')
        os.makedirs('output')


def type_selector(type):
    if 'multi' in type:
        return 'MULTIPLE CHOICE QUESTION'
    if 'single' in type:
        return 'SINGLE CHOICE QUESTION'
    if 'gap' in type:
        return 'CLOZE QUESTION'
    if 'order' in type:
        return 'ORDERING QUESTION'


def file_exists(path):
    if not os.path.exists(path):
        msg = 'The script "{}" does not exist.'.format(path)
        raise argparse.ArgumentTypeError(msg)
    return path


def load_script(script_name):
    module_name = os.path.basename(script_name)
    spec = importlib.util.spec_from_file_location(module_name, script_name)
    script = importlib.util.module_from_spec(spec)
    return script, spec


def script_is_valid(script, required):
    for field in required:
        if not hasattr(script, field):
            error("script does not export '{}' field.".format(field))
    if any(not hasattr(script, field) for field in required):
        abort("Script is invalid (see above)")


def parseme():
    config = get_config()
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
        default=config['META']['author'],
        metavar='AUTHOR'
    )
    parser_new.add_argument(
        "-p",
        "--points",
        help='Points given for correct answer (different behaviour for different questions)',
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
        '-p',
        '--parametrized',
        help='Print the number of parametrized instances specified in question.',
        action='store_true')

    parser_gen = subparsers.add_parser(
        "upload", help="Subcommand to upload created xml instances.")
    parser_gen.add_argument(
        'script_list',
        help='The scripts that should be uploaded',
        nargs='+',
        type=file_exists,
        metavar='FILE')

    args = parser.parse_args()

    if args.command == 'gen':
        look_for_output()
        delegator(args.out, args.input, args.parametrized)
    if args.command == 'upload':
        handle_upload(args.script_list, config)
    if args.command == 'new':
        handle_new_script(args.name, args.type, args.author, args.points)
    if args.command == None:
        parser.print_help()


def delegator(output, script_list, parametrized):
    """
    It gets a list of filenames and delegates them to the correct handler.
    Every file that does not end with ``.py`` will be ignored. Each script
    is imported and then passed as module to the handler:

    Args:
        output (str): where to write the finished XML document
        script_list (list): a list of filenames that contain scripts
        parametrized (bool): output all instances (no test mode)
    """
    for script_name in filter(lambda a: a.endswith('.py'), script_list):
        script, spec = load_script(script_name)
        spec.loader.exec_module(script)
        handler = {
            'gap': handle_gap_questions,
            'single': handle_choice_questions,
            'single choice': handle_choice_questions,
            'multi': handle_choice_questions,
            'multiple choice': handle_choice_questions,
            'order': handle_order_questions,
        }[script.meta['type']]

        if not output:
            output = os.path.join('output', script.meta['title']) + '.xml'

        if 'instances' in script.meta and parametrized:
            instances = script.meta['instances']
        else:
            instances = 1

        final = packer.compile(
            handler(script, spec, instances),
            type_selector(script.meta['type'])
        )

        packer.print_xml(final, output)
        info('Processed "{}" and'.format(script.__name__))
        info('wrote xml "{}"'.format(output), notag=True)


def handle_gap_questions(script, spec, instances):
    """ a generator for all kinds of gap questions

    A script can contain any mixture of gap, numeric gap and choice gap
    questions. The data object that is needed by the XML creating scripts
    is generated and the task itself is handled by the parser. The parser
    returns the intermediate representation of the task.

    Arguments:
        script (module): the loaded module
        spec (object):   the specification of the module
        instances (int): number of instances that should be generated
    """
    script_is_valid(script, required=['meta', 'task', 'feedback'])
    for _ in range(instances):
        spec.loader.exec_module(script) # reload the script to get new instance
        yield {
            'type': type_selector(script.meta['type']),
            'description': "_description",
            'gap_list': gap_parser(script.task),
            'author': script.meta['author'],
            'title': script.meta['title'],
            'shuffle': script.meta['shuffle'] if 'shuffle' in script.meta else True,
            'feedback': markdown(script.feedback),
            'gap_length': script.meta['gap_length'] if 'gap_length' in script.meta else 20,
        }


def handle_choice_questions(script, spec, instances):
    """ a generator for choice questions

    Handles multiple and single choice questions. The relevant parts of the
    script are fed into a parser that return the correct intermediate
    representation for the task. In this case a list of answers.

    Arguments:
        script (module): the loaded module
        spec (object):   the specification of the module
        instances (int): number of instances that should be generated

    """
    script_is_valid(script, required=['meta', 'task', 'choices', 'feedback'])
    for _ in range(instances):
        spec.loader.exec_module(script) # reload the script to get new instance
        yield {
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


def handle_order_questions(script, spec, instances):
    """ a generator for order questions

    Currently handles only vertical ordering questions. The order field of
    the script is fed to the parser, which just retuns a splited list of
    the string where '--' is split character.

    Arguments:
        script (module): the loaded module
        spec (object): the specification of the module
        instances (int): number of instances that should be generated
    """
    script_is_valid(script, required=['meta', 'task', 'order', 'feedback'])
    for _ in range(instances):
        spec.loader.exec_module(script) # reload the script to get new instance
        yield {
            'type': type_selector(script.meta['type']),
            'description': "_description",
            'question_text': markdown(script.task),
            'author': script.meta['author'],
            'title': script.meta['title'],
            'order': order_parser(script.order),
            'points': script.meta['points'],
            'feedback': markdown(script.feedback),
        }


def handle_new_script(name, qtype, author, points):
    """ Creates a new script file.

    Takes in some meta information from the command line of if not present takes
    it from the config.ini or uses default values.

    Arguments:
        name (str):     name of the script, will also become filename
        qtype (str):    question type (choice, gap, alignment)
        author (str):   the author of the script
        points (float): number of points for the task
    """
    head, tail = os.path.split(name)
    if not os.path.exists(head):
        os.makedirs(head)
    if not tail.endswith('.py'):
        base = tail
    else:
        base = tail.rstrip('.py')
    with open(os.path.join(head, base + '.py'), 'x') as new_script:
        choice = ''
        if qtype in ['multiple choice', 'single choice']:
            choice = '\nchoices = """\n[X] A\n[ ] B\n[ ] C\n[X] D\n"""\n'

        print(scaffolding.format(author, base, qtype, points, choice).strip(), file=new_script)
        info('Generated new script "%s."' % new_script.name)


def handle_upload(script_list, config):
    """ Passes data to the upload script.

    The status code should be 500, since ILIAS always replies with that error
    code after an upload is confirmed. If anything else the script will say
    the status code was bad.

    Arguments:
        script_path (str): path to the file that should be uploaded
        config (config object): the loaded configuration
    """
    for script in script_list:
        r = send_script(
            script,
            config['UPLAODER']['host'],
            config['UPLAODER']['user'],
            config['UPLAODER']['pass'],
            config['UPLAODER']['rtoken'],
        )
        info("Uploaded %s. Status code looks %s." %
            (script, "good" if r else "bad"))
