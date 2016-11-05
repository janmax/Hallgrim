import xml.etree.ElementTree as et

from hallgrim.IliasXMLCreator.xmlBuildingBlocks import *


###
# Solution 1
# ['text', 'text', 'text']
# [('gap_solution', points, length), ..., (['one', 'two', 'three'], points, length)]
#
# str : str_gap
# list : choice_gap
# tuple : num_gap (x, min, max)
#
# Solution 2
# ['text', ('gap_solution', points, length), ('gap_solution', points, length), 'text', ...]
#
###

class GapQuestion:
    """docstring for GapQuestion"""
    def __init__(self, type, description, gap_list, author, title, questions, feedback, gapLength):
        self.type           = type
        self.description    = description
        self.gap_list       = gap_list
        self.author         = author
        self.title          = title
        self.questions      = questions
        self.feedback       = feedback
        self.gapLength      = gapLength

        self.itemmetadata       = self.itemmetadata(feedback_setting=1)
        self.presentation       = self.presentation()
        self.resprocessing      = self.resprocessing()
        self.xml_representation = self.create_item()

    def __call__(self):
        return self.xml_representation

    def itemmetadata(self, feedback_setting=1):
        subroot = et.Element('qtimetadata')
        subroot.append(qtimetadatafield('ILIAS_VERSION', '5.1.8 2016-08-03'))
        subroot.append(qtimetadatafield('QUESTIONTYPE', self.type))
        subroot.append(qtimetadatafield('AUTHOR',  self.author))
        subroot.append(qtimetadatafield('additional_cont_edit_mode', 'default'))
        subroot.append(qtimetadatafield('externalId', '99.99'))
        subroot.append(qtimetadatafield('textgaprating', 'ci'))
        subroot.append(qtimetadatafield('fixedTextLength', str(self.gapLength)))
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
                if type(item[0] == list):
                    f = response_choice(gap_ident, item[0])
                if type(item[0] == str):
                    f = response_str(gap_ident, self.gapLength)
                if type(item[0] == tuple):
                    f = response_num(gap_ident, self.gapLength, item[1], item[2]):
                gap_ident += 1
            flow.append(f)
        return root

    ############################################################################
    def resprocessing(self):
        root = et.Element('resprocessing')
        outcomes = et.Element('outcomes')
        outcomes.append(simple_elemet('decvar'))
        root.append(outcomes)
        for i, (_, correct, points) in enumerate(self.questions):
            root.append(respcondition(points if correct else 0, i, True))
            root.append(respcondition(points if not correct else 0, i, False))
        return root
