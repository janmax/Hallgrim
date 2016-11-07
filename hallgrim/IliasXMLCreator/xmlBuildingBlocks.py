import xml.etree.ElementTree as et

### xmlBuildingBlocks ####################################################
#
# This file cointains all the static blocks of xml code that is needed in
# all classes. These are usually just snippets to have cleaner code in other
# files.
#
##########################################################################

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

### gap specific #########################################################
def material_raw(content):
    material = et.Element('material')
    material.append(simple_elemet(
        'mattext',
        text=content
    ))
    return material

def response_str(ident, columns):
    response_str = et.Element('response_str', attrib={'ident': indent, 'rcardinality': 'Single'})
    render_fib   = et.Element('render_fib', attrib={'columns': str(columns), 'fibtype': "String", 'prompt': "Box"})
    response_str.append(render_fib)
    return response_str

def response_choice(ident, answers):
    response_str = et.Element('response_str', attrib={'ident': indent, 'rcardinality': 'Single'})
    render_choice = et.Element('render_choice', attrib={'shuffle': 'Yes'})
    for i, answer in enumerate(answers):
        response_label = et.Element('response_label', attrib={'ident': str(i)})
        response_label.append(material_raw(answer))
    return response_str

def response_num(ident, columns, _min, _max, numtype='Decimal'):
    response_num = et.Element('response_num', attrib={'ident': ident, 'numtype': numtype, 'rcardinality': 'Single'})
    render_fib   = et.Element('render_fib', attrib={'columns': columns, 'fibtype': numtype, 'maxnumber': _min, 'minnumber': _max, 'prompt': "Box"})
    response_num.append(render_fib)
    return response_num