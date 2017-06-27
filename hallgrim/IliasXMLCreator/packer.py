import xml.etree.ElementTree as et

from . import abstract_question
from .. import messages

__all__ = ['compile', 'print_xml']

def create_xml_tree(item_list):
    root = et.Element('questestinterop')
    tree = et.ElementTree(root)
    for item in item_list:
        root.append(item)
    return tree


def compile(data_gen, script_type):
    """ passes the intermediate representation to xml creators

    Generates the final list of descriptions for each test from a generator
    and passes each one to the XML compilers.

    Arguments:
        data_gen {generator} -- generates dictionaries that contain task description
        script_type {str} -- to specify which comiler to use

    Returns:
        ElementTree -- the final xml tree ready for print
    """
    try:
        question_class = abstract_question.IliasQuestion.available_types()[script_type]
        item_list = [question_class(**data).xml() for data in data_gen]
    except KeyError:
        messages.abort('Question type not found.')

    return create_xml_tree(item_list)


def print_xml(tree, file):
    """ Only a wrapper for the print function

    Arguments:
        tree {ElementTree} -- the final task file
        file {str} -- output destination (path has to exist)
    """
    tree.write(file, encoding="utf-8", xml_declaration=True)
