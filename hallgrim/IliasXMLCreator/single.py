from .multi import *

def resprocessing(questions):
    root = et.Element('resprocessing')
    outcomes = et.Element('outcomes')
    outcomes.append(simple_elemet('decvar'))
    root.append(outcomes)
    for i, (_, correct, points) in enumerate(questions):
        root.append(respcondition(points if correct else 0, i, True))
    return root

def convert_and_print(data, output):
    tree = create_xml_tree('SINGLE CHOICE QUESTION', **data)
    tree.write(output, encoding="utf-8", xml_declaration=True)