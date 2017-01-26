import xml.etree.ElementTree as et

from .xmlBuildingBlocks import *
from .abstract_question import IliasQuestion


class OrderQuestion(IliasQuestion):
    """docstring for OrderQuestion"""

    __slots__ = ('question_text', 'points', 'order',)
    external_type = 'ORDERING QUESTION'
    internal_type = 'order'

    def __init__(self, question_text, author, title, order, points, feedback):
        self.question_text      = question_text
        self.author             = author
        self.title              = title
        self.order              = order
        self.points             = points
        self.feedback           = feedback

    def itemmetadata(self, feedback_setting=1):
        subroot = et.Element('qtimetadata')
        subroot.append(qtimetadatafield('ILIAS_VERSION', '5.1.11 2016-10-28'))
        subroot.append(qtimetadatafield('QUESTIONTYPE', self.external_type))
        subroot.append(qtimetadatafield('AUTHOR', self.author))
        subroot.append(qtimetadatafield('additional_cont_edit_mode', 'default'))
        subroot.append(qtimetadatafield('externalId', '99.99'))
        subroot.append(qtimetadatafield('thumb_geometry', '100'))
        subroot.append(qtimetadatafield('element_height', '99'))
        subroot.append(qtimetadatafield('points', str(self.points)))
        root = et.Element('itemmetadata')
        root.append(subroot)
        return root

    ############################################################################
    def presentation(self):
        root = et.Element('presentation', attrib={'label': self.title})
        flow = et.Element('flow')
        response_lid = et.Element('response_lid', attrib={
            'ident': 'OQT',
            'output': 'javascript',
            'rcardinality': 'Ordered',
        })

        render_choice = et.Element(
            'render_choice', attrib={'shuffle': 'Yes'})
        for i, answer in enumerate(self.order):
            render_choice.append(response_label(answer, i))

        root.append(flow)
        flow.append(material(self.question_text))
        flow.append(response_lid)
        response_lid.append(render_choice)
        return root

    ############################################################################
    def resprocessing(self):
        root = et.Element('resprocessing')
        outcomes = et.Element('outcomes')
        outcomes.append(simple_element('decvar'))
        root.append(outcomes)
        for i, _ in enumerate(self.order):
            root.append(self.respcondition(i, self.points / len(self.order)))
        return root

    ############################################################################
    @staticmethod
    def respcondition(index, points):
        root = et.Element('respcondition', attrib={'continue': 'Yes'})
        conditionvar = et.Element('conditionvar')
        varequal = simple_element(
            'varequal',
            text=str(index),
            attrib={'respident': "OQT", 'index': str(index)}
        )

        setvar = simple_element(
            'setvar',
            text=str(points),
            attrib={'action': 'Add'}
        )

        displayfeedback = et.Element(
            'displayfeedback',
            attrib={'feedbacktype': 'Response', 'linkrefid': 'link_%d' % index}
        )

        conditionvar.append(varequal)
        root.append(conditionvar)
        root.append(setvar)
        root.append(displayfeedback)
        return root
