import xml.etree.ElementTree as et

from .xmlBuildingBlocks import *


class OrderQuestion:
    """docstring for OrderQuestion"""
    def __init__(self, type, description, question_text, author, title, order, points, feedback):
        self.type               = type
        self.description        = description
        self.question_text      = question_text
        self.author             = author
        self.title              = title
        self.order              = order
        self.points             = points
        self.feedback           = feedback

        self.itemmetadata       = self.itemmetadata(feedback_setting=1)
        self.presentation       = self.presentation()
        self.resprocessing      = self.resprocessing()
        self.xml_representation = self.create_item()

    def __call__(self):
        return self.xml_representation

    def is_single(self):
        return self.type == 'SINGLE CHOICE QUESTION'

    def itemmetadata(self, feedback_setting=1):
        subroot = et.Element('qtimetadata')
        subroot.append(qtimetadatafield('ILIAS_VERSION', '5.1.11 2016-10-28'))
        subroot.append(qtimetadatafield('QUESTIONTYPE', self.type))
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
            root.append(respcondition_order(i, self.points / len(self.order)))
        return root

    ### returns the final object ###############################################
    def create_item(self):
        """ This method stacks all the previously created structures together"""
        item = et.Element('item', attrib={
            'ident': 'undefined',
            'title': self.title,
            'maxattempts': "0",
        })

        item.append(simple_element('description', text=self.description))
        item.append(simple_element('duration', text='P0Y0M0DT0H30M0S')) # 30 min
        item.append(self.itemmetadata)
        item.append(self.presentation)
        item.append(self.resprocessing)
        item.append(itemfeedback('response_allcorrect', self.feedback))
        item.append(itemfeedback('response_onenotcorrect', self.feedback))
        return item
