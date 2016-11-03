import xml.etree.ElementTree as et

from hallgrim.IliasXMLCreator import multi, single


def create_xml_tree(item_list):
    root = et.Element('questestinterop')
    tree = et.ElementTree(root)
    for item in item_list:
        root.append(item)
    return tree


def convert_and_print(data, output, instances=1):
    if data['type'] == 'MULTIPLE CHOICE QUESTION':
        item_list = [multi.MultipleChoiceQuestion(**data)() for _ in range(instances)]
    if data['type'] == 'SINGLE CHOICE QUESTION':
        item_list = [single.SingleChoiceQuestion(**data)() for _ in range(instances)]

    tree = create_xml_tree(item_list)
    tree.write(output, encoding="utf-8", xml_declaration=True)
