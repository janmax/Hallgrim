import xml.etree.ElementTree as et

from .xmlBuildingBlocks import *


class MultipleChoiceQuestion:
    """docstring for MultipleChoiceQuestion"""
    def __init__(self, type, description, question_text, author, title, maxattempts, questions, feedback, shuffle=True):
        self.type               = type
        self.description        = description
        self.question_text      = question_text
        self.author             = author
        self.title              = title
        self.maxattempts        = maxattempts
        self.shuffle            = shuffle
        self.questions          = questions
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
            'rcardinality': 'Multiple' if not self.is_single() else 'Single'
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
            root.append(respcondition(points if correct else 0, 'MCMR', i, True))
            root.append(respcondition(points if not correct else 0, 'MCMR', i, False))
        return root

    ### returns the final object ###############################################
    def create_item(self):
        """ This method stacks all the previously created structures together"""
        item = et.Element('item', attrib={
            'ident': 'undefined',
            'title': self.title,
            'maxattempts': self.maxattempts
        })

        item.append(simple_element('description', text=self.description))
        item.append(simple_element('duration', text='P0Y0M0DT0H30M0S')) # 30 min
        item.append(self.itemmetadata)
        item.append(self.presentation)
        item.append(self.resprocessing)
        item.append(itemfeedback('response_allcorrect', self.feedback))
        item.append(itemfeedback('response_onenotcorrect', self.feedback))
        return item
