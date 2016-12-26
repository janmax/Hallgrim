import xml.etree.ElementTree as et

from .xmlBuildingBlocks import *

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

class GapQuestion:
    """docstring for GapQuestion"""
    def __init__(self, type, description, gap_list, author, title, shuffle, feedback, gap_length):
        self.type           = type
        self.description    = description
        self.gap_list       = gap_list
        self.author         = author
        self.title          = title
        self.shuffle        = shuffle
        self.feedback       = feedback
        self.gap_length     = gap_length

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
                    root.append(respcondition_gap(points, i, choice, j))
            if type(answer) == TEXT_GAP:
                for j, choice in enumerate(answer):
                    root.append(respcondition_gap(points, i, choice, j))
            if type(answer) == NUMERIC_GAP:
                root.append(respcondition_gap(points, i, answer[0]))
        return root

    ### returns the final object ###############################################
    def create_item(self):
        """ This method stacks all the previously created structures together"""
        item = et.Element('item', attrib={
            'ident': 'undefined',
            'title': self.title,
            'maxattempts': "99"
        })

        item.append(simple_element('description', text=self.description))
        item.append(simple_element('duration', text='P0Y0M0DT0H30M0S')) # 30 min
        item.append(self.itemmetadata)
        item.append(self.presentation)
        item.append(self.resprocessing)
        item.append(itemfeedback('response_allcorrect', self.feedback))
        item.append(itemfeedback('response_onenotcorrect', self.feedback))
        return item
