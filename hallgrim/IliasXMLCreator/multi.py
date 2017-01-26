import xml.etree.ElementTree as et

from .xmlBuildingBlocks import *
from .abstract_question import IliasQuestion

class MultipleChoiceQuestion(IliasQuestion):
    """docstring for MultipleChoiceQuestion"""

    __slots__ = ('question_text', 'shuffle', 'questions',)
    external_type = 'MULTIPLE CHOICE QUESTION'
    internal_type = 'multiple choice'

    def __init__(self, question_text, author, title, questions, feedback, shuffle=True, single=False):
        self.question_text      = question_text
        self.author             = author
        self.title              = title
        self.shuffle            = shuffle
        self.questions          = questions
        self.feedback           = feedback

    def itemmetadata(self, feedback_setting=1):
        subroot = et.Element('qtimetadata')
        subroot.append(qtimetadatafield('ILIAS_VERSION', '5.1.11 2016-10-28'))
        subroot.append(qtimetadatafield('QUESTIONTYPE', self.external_type))
        subroot.append(qtimetadatafield('AUTHOR', self.author))
        subroot.append(qtimetadatafield('additional_cont_edit_mode', 'default'))
        subroot.append(qtimetadatafield('externalId', '99.99'))
        subroot.append(qtimetadatafield('thumb_size', None))
        subroot.append(qtimetadatafield('feedback_setting', str(feedback_setting)))
        root = et.Element('itemmetadata')
        root.append(subroot)
        return root

    ############################################################################
    def presentation(self):
        root = et.Element('presentation', attrib={'label': self.title})
        flow = et.Element('flow')
        response_lid = et.Element('response_lid', attrib={
            'ident': 'MCMR',
            'rcardinality':
                'Multiple' if not self.internal_type == 'single choice' else 'Single'
        })
        render_choice = et.Element(
            'render_choice', attrib={'shuffle': 'Yes' if self.shuffle else 'No'})
        for i, (answer, _, _) in enumerate(self.questions):
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
        for i, (_, correct, points) in enumerate(self.questions):
            root.append(self.respcondition(points if correct else 0, 'MCMR', i, True))
            root.append(self.respcondition(points if not correct else 0, 'MCMR', i, False))
        return root

    ############################################################################
    @staticmethod
    def respcondition(points, respident, count, correct=True):
        root = et.Element('respcondition', attrib={'continue': 'Yes'})
        conditionvar = et.Element('conditionvar')
        varequal = simple_element(
            'varequal',
            text=str(count),
            attrib={'respident': respident}
        )

        if correct:
            conditionvar.append(varequal)
        else:
            _not = et.Element('not')
            _not.append(varequal)
            conditionvar.append(_not)

        setvar = simple_element(
            'setvar',
            text=str(points),
            attrib={'action': 'Add'}
        )

        root.append(conditionvar)
        root.append(setvar)
        if correct:
            displayfeedback = et.Element(
                'displayfeedback',
                attrib={'feedbacktype': 'Response',
                        'linkrefid': 'response_{}'.format(count)})
            root.append(displayfeedback)
        return root
