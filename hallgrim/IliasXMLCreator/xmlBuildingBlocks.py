import xml.etree.ElementTree as et

### xmlBuildingBlocks ####################################################
#
# This file cointains all the static blocks of xml code that is needed in
# all classes. These are usually just snippets to have cleaner code in other
# files.
#
##########################################################################


def simple_elemet(name, text=None, attrib={}):
    if not text:
        return et.Element(name, attrib=attrib)
    node = et.Element(name, attrib=attrib)
    node.text = text
    return node


def qtimetadatafield(label, entry):
    root = et.Element('qtimetadatafield')
    root.append(simple_elemet('fieldlabel', text=label))
    root.append(simple_elemet('fieldentry', text=entry))
    return root


def material(content):
    material = et.Element('material')
    material.append(simple_elemet(
        'mattext',
        text=content,
        attrib={'texttype': 'text/xhtml'}
    ))
    return material


def response_label(content, count):
    response_label = et.Element('response_label', attrib={'ident': str(count)})
    response_label.append(material(content))
    return response_label


def respcondition(points, count, correct=True):
    root = et.Element('respcondition', attrib={'continue': 'Yes'})
    conditionvar = et.Element('conditionvar')
    varequal = simple_elemet(
        'varequal',
        text=str(count),
        attrib={'respident': 'MCMR'}
    )

    if correct:
        conditionvar.append(varequal)
    else:
        _not = et.Element('not')
        _not.append(varequal)
        conditionvar.append(_not)

    root.append(conditionvar)

    setvar = simple_elemet(
        'setvar',
        text=str(points),
        attrib={'action': 'Add'}
    )
    root.append(setvar)

    if correct:
        displayfeedback = et.Element(
            'displayfeedback',
            attrib={'feedbacktype': 'Response',
                    'linkrefid': 'response_{}'.format(count)})
        root.append(displayfeedback)
    return root

def itemfeedback(ident, content='NONE'):
    root = et.Element(
        'itemfeedback',
        attrib={'ident': ident, 'view': 'All'}
    )
    flow_mat = et.Element('flow_mat')
    flow_mat.append(material(content))
    root.append(flow_mat)
    return root