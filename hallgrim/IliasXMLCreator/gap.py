import xml.etree.ElementTree as et

from .xmlBuildingBlocks import *
from .abstract_question import IliasQuestion


###
#
# Type of first item in gap tuple determines the gap type. gap might be changed
# to set
# str : str_gap
# list : choice_gap
# tuple : num_gap (x, min, max)
#
# Format of gap_list
# ['text', ('gap_solution', points), ('gap_solution', points), 'text', ...]
#
###

TEXT_GAP = set
NUMERIC_GAP = tuple
SELECT_GAP = list

class GapQuestion(IliasQuestion):
    """docstring for GapQuestion"""

    __slots__ = ('gap_list', 'shuffle', 'gap_length',)
    external_type = 'CLOZE QUESTION'
    internal_type = 'gap'

    def __init__(self, gap_list, author, title, shuffle, feedback, gap_length):
        self.gap_list       = gap_list
        self.author         = author
        self.title          = title
        self.shuffle        = shuffle
        self.feedback       = feedback
        self.gap_length     = gap_length

    def itemmetadata(self, feedback_setting=1):
        subroot = et.Element('qtimetadata')
        subroot.append(qtimetadatafield('ILIAS_VERSION', '5.1.8 2016-08-03'))
        subroot.append(qtimetadatafield('QUESTIONTYPE', self.external_type))
        subroot.append(qtimetadatafield('AUTHOR',  self.author))
        subroot.append(qtimetadatafield('additional_cont_edit_mode', 'default'))
        subroot.append(qtimetadatafield('externalId', '99.99'))
        subroot.append(qtimetadatafield('textgaprating', 'ci'))
        subroot.append(qtimetadatafield('fixedTextLength', str(self.gap_length)))
        subroot.append(qtimetadatafield('identicalScoring', '1'))
        subroot.append(qtimetadatafield('combinations', 'W10='))
        root = et.Element('itemmetadata')
        root.append(subroot)
        return root

    ############################################################################
    def presentation(self):
        root = et.Element('presentation', attrib={'label': self.title})
        flow = et.Element('flow')
        root.append(flow)
        gap_ident = 0
        for item in self.gap_list:
            if type(item) == str:
                f = material(item)
            if type(item) == tuple:
                if type(item[0]) == SELECT_GAP:
                    f = response_choice("gap_{}".format(gap_ident), item[0])
                if type(item[0]) == TEXT_GAP:
                    f = response_str("gap_{}".format(gap_ident), self.gap_length)
                if type(item[0]) == NUMERIC_GAP:
                    f = response_num("gap_{}".format(gap_ident), self.gap_length, item[0][1], item[0][2])
                gap_ident += 1
            flow.append(f)
        return root

    ############################################################################
    def resprocessing(self):
        root = et.Element('resprocessing')
        outcomes = et.Element('outcomes')
        outcomes.append(simple_element('decvar'))
        root.append(outcomes)
        is_gap = lambda t: type(t) == tuple
        for i, (answer, points) in enumerate(filter(is_gap, self.gap_list)):
            if type(answer) == SELECT_GAP:
                for j, (choice, points) in enumerate(answer): # answer is hidden
                    root.append(self.respcondition(points, i, choice, j))
            if type(answer) == TEXT_GAP:
                for j, choice in enumerate(answer):
                    root.append(self.respcondition(points, i, choice, j))
            if type(answer) == NUMERIC_GAP:
                root.append(self.respcondition(points, i, answer[0]))
        return root

    ############################################################################
    @staticmethod
    def respcondition(points, resp_count, answer, count=0):
        root = et.Element('respcondition', attrib={'continue': 'Yes'})
        conditionvar = et.Element('conditionvar')
        varequal = simple_element(
            'varequal',
            text=answer,
            attrib={'respident': 'gap_{}'.format(resp_count)}
        )

        conditionvar.append(varequal)
        setvar = simple_element(
            'setvar',
            text=str(points),
            attrib={'action': 'Add'}
        )

        displayfeedback = et.Element(
            'displayfeedback',
            attrib={'feedbacktype': 'Response',
                    'linkrefid': '{}_Response_{}'.format(resp_count, count)})

        root.append(conditionvar)
        root.append(setvar)
        root.append(displayfeedback)
        return root
