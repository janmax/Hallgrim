import xml.etree.ElementTree as et

from .xmlBuildingBlocks import *

from abc import ABCMeta, abstractmethod, abstractstaticmethod


def all_subclasses(cls):
    return cls.__subclasses__() \
        + [g for s in cls.__subclasses__() for g in all_subclasses(s)]


class IliasQuestion(metaclass=ABCMeta):
    """docstring for IliasQuestion"""

    @classmethod
    def available_types(cls):
        return {sub.internal_type : sub for sub in all_subclasses(cls)}

    def __new__(cls, *args, **kwargs):
        assert hasattr(cls, 'internal_type'), "internaltype not defined"
        assert hasattr(cls, 'external_type'), "externaltype not defined"
        return super().__new__(cls)

    @abstractmethod
    def itemmetadata(self, feedback_setting):
        return NotImplemented

    @abstractmethod
    def presentation(self):
        return NotImplemented

    @abstractmethod
    def resprocessing(self):
        return NotImplemented

    @abstractstaticmethod
    def respcondition(points, resp_count, answer, count):
        return NotImplemented

    ### returns the final object #############################################
    def xml(self):
        """ This method stacks all the previously created structures together"""
        item = et.Element('item', attrib={
            'ident': 'undefined',
            'title': self.title,
            'maxattempts': "99"
        })

        item.append(simple_element('description', text="_description"))
        # 30 min
        item.append(simple_element('duration', text='P0Y0M0DT0H30M0S'))
        item.append(self.itemmetadata(feedback_setting=1))
        item.append(self.presentation())
        item.append(self.resprocessing())
        item.append(itemfeedback('response_allcorrect', self.feedback))
        item.append(itemfeedback('response_onenotcorrect', self.feedback))
        return item

