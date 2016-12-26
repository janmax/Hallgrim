import xml.etree.ElementTree as et

from . import multi, single, gap, order
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
    if script_type == 'MULTIPLE CHOICE QUESTION':
        item_list = [multi.MultipleChoiceQuestion(**data)() for data in data_gen]
    elif script_type == 'SINGLE CHOICE QUESTION':
        item_list = [single.SingleChoiceQuestion(**data)() for data in data_gen]
    elif script_type == 'CLOZE QUESTION':
        item_list = [gap.GapQuestion(**data)() for data in data_gen]
    elif script_type == 'ORDERING QUESTION':
        item_list = [order.OrderQuestion(**data)() for data in data_gen]
    else:
        messages.abort('Question type not found.')

    return create_xml_tree(item_list)


def print_xml(tree, file):
    """ Only a wrapper for the print function

    Arguments:
        tree {ElementTree} -- the final task file
        file {str} -- output destination (path has to exist)
    """
    tree.write(file, encoding="utf-8", xml_declaration=True)
