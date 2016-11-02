import xml.etree.ElementTree as et

from hallgrim.IliasXMLCreator import multi, single


def create_xml_tree(item_list):
    root = et.Element('questestinterop')
    tree = et.ElementTree(root)
    for item in item_list:
        root.append(item)
    return tree


def convert_and_print(data, output):
    if data['type'] == 'MULTIPLE CHOICE QUESTION':
        item = multi.MultipleChoiceQuestion(**data)()
    if data['type'] == 'SINGLE CHOICE QUESTION':
        item = single.SingleChoiceQuestion(**data)()

    tree = create_xml_tree([item])
    tree.write(output, encoding="utf-8", xml_declaration=True)
