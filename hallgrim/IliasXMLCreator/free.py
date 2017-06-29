import xml.etree.ElementTree as et

from .xmlBuildingBlocks import *
from .abstract_question import IliasQuestion


class FreeQuestion(IliasQuestion):
    """docstring for FreeQuestion"""

    __slots__ = ('question_text', 'points', 'order',)
    external_type = 'TEXT QUESTION'
    internal_type = 'free'

    def __init__(self, question_text, author, title, points, feedback):
        self.question_text      = question_text
        self.author             = author
        self.title              = title
        self.points             = points
        self.feedback           = feedback

    def itemmetadata(self, feedback_setting=1):
        subroot = et.Element('qtimetadata')
        subroot.append(qtimetadatafield('ILIAS_VERSION', '5.1.11 2016-10-28'))
        subroot.append(qtimetadatafield('QUESTIONTYPE', self.external_type))
        subroot.append(qtimetadatafield('AUTHOR', self.author))
        subroot.append(qtimetadatafield('additional_cont_edit_mode', 'default'))
        subroot.append(qtimetadatafield('externalId', '99.99'))
        subroot.append(qtimetadatafield('textrating', 'ci'))
        subroot.append(qtimetadatafield('matchcondition', None))
        subroot.append(qtimetadatafield('termscoring', 'YTowOnt9'))
        subroot.append(qtimetadatafield('termrelation', 'non'))
        subroot.append(qtimetadatafield('specificfeedback', 'non'))
        root = et.Element('itemmetadata')
        root.append(subroot)
        return root

    ############################################################################
    def presentation(self):
        root = et.Element('presentation', attrib={'label': self.title})
        flow = et.Element('flow')

        response_str = et.Element('response_str', attrib={
            'ident': 'TEXT',
            'rcardinality': 'Ordered',
        })

        render_fib = et.Element(
            'render_fib', attrib={'fibtype': 'String', 'prompt': 'Box'})


        root.append(flow)
        flow.append(material(self.question_text))
        flow.append(response_str)
        response_str.append(render_fib)
        render_fib.append(simple_element('response_label', attrib={'ident': 'A'}))
        return root

    ############################################################################
    def resprocessing(self):
        root = et.Element('resprocessing')
        outcomes = et.Element('outcomes')
        outcomes.append(simple_element('decvar', attrib={
            'maxvalue': str(self.points),
            'minvalue': '0',
            'varname': 'WritingScore',
            'vartype': 'Integer'
        }))
        root.append(outcomes)

        respcondition = et.Element('respcondition')
        conditionvar  = et.Element('conditonvar')
        conditionvar.append(simple_element('other', 'tutor_rated'))
        respcondition.append(conditionvar)

        return root
