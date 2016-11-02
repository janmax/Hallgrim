import xml.etree.ElementTree as et


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


def itemmetadata(type, author, feedback_setting=1):
    subroot = et.Element('qtimetadata')
    subroot.append(qtimetadatafield('ILIAS_VERSION', '5.1.8 2016-08-03'))
    subroot.append(qtimetadatafield('QUESTIONTYPE', type))
    subroot.append(qtimetadatafield('AUTHOR', author))
    subroot.append(qtimetadatafield('additional_cont_edit_mode', 'default'))
    subroot.append(qtimetadatafield('externalId', '99.99'))
    subroot.append(qtimetadatafield('thumb_size', None))
    subroot.append(qtimetadatafield('feedback_setting', str(feedback_setting)))
    root = et.Element('itemmetadata')
    root.append(subroot)
    return root

##########################################################################
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


def presentation(title, question_text, questions, shuffle=True):
    root = et.Element('presentation', attrib={'label': title})
    flow = et.Element('flow')
    response_lid = et.Element(
        'response_lid', attrib={'ident': 'MCMR', 'rcardinality': 'Multiple'})
    render_choice = et.Element(
        'render_choice', attrib={'shuffle': 'Yes' if shuffle else 'No'})
    for i, (answer, _, _) in enumerate(questions):
        render_choice.append(response_label(answer, i))

    root.append(flow)
    flow.append(material(question_text))
    flow.append(response_lid)
    response_lid.append(render_choice)
    return root

##########################################################################
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


def resprocessing(questions):
    root = et.Element('resprocessing')
    outcomes = et.Element('outcomes')
    outcomes.append(simple_elemet('decvar'))
    root.append(outcomes)
    for i, (_, correct, points) in enumerate(questions):
        root.append(respcondition(points if correct else 0, i, True))
        root.append(respcondition(points if not correct else 0, i, False))
    return root


##########################################################################
def itemfeedback(count):
    root = et.Element(
        'itemfeedback',
        attrib={'ident': 'response_{}'.format(count), 'view': 'All'}
    )
    flow_mat = et.Element('flow_mat')
    flow_mat.append(material('NONE'))
    root.append(flow_mat)
    return root
##########################################################################


def create_xml_tree(type, description, question_text, author, title, maxattempts, shuffle, questions):
    root = et.Element('questestinterop')
    tree = et.ElementTree(root)
    item = et.Element('item', attrib={
        'ident': 'undefined',
        'title': title,
        'maxattempts': maxattempts
    })

    item.append(simple_elemet('description', text=description))
    item.append(simple_elemet('duration', text='P0Y0M0DT0H30M0S'))
    item.append(itemmetadata(type, author))
    item.append(presentation(title, question_text, questions, shuffle))
    item.append(resprocessing(questions))
    for i, _ in enumerate(questions):
        item.append(itemfeedback(i))
    root.append(item)

    return tree


def convert_and_print(data, output):
    tree = create_xml_tree('MULTIPLE CHOICE QUESTION', **data)
    tree.write(output, encoding="utf-8", xml_declaration=True)
