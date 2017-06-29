import xml.etree.ElementTree as et

from .xmlBuildingBlocks import *

from abc import ABCMeta, abstractmethod, abstractstaticmethod


def all_subclasses(cls):
    return cls.__subclasses__() \
        + [g for s in cls.__subclasses__() for g in all_subclasses(s)]


class IliasQuestion(metaclass=ABCMeta):
    """ This is the abstract class one has to implement if one wants to
    offer a question type in hallgrim. All Ilias question roughly follow
    the same structure. After you successfully implemented the methods below
    by reverse engineering the XML export of an Ilias question you prepared,
    perform the following steps:

        1. add the name of the new python module (aka. the file name) in this
        packages __init__.py to register it with the rest of hallgrim

        2. write a template for this kind of task (preferably in the
        hallgrim.templates module)

        3. write a parser that provides the intermediate representation
        your IliasXML converter can live with

        4. add a handler in the hallgrim.hallgrim module that fuses everything
        together.

    TODO: I honestly do not like this process and the whole project desperately
    needs refactoring. Also some parts need to be rewritten.
    """
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

    ### returns the final object #############################################
    def xml(self):
        """ This method stacks all the previously created structures together"""
        item = et.Element('item', attrib={
            'ident': 'undefined',
            'title': self.title,
            'maxattempts': "99"
        })

        item.append(simple_element('description', text="_description"))
        item.append(simple_element('duration', text='P0Y0M0DT0H30M0S'))
        item.append(self.itemmetadata(feedback_setting=1))
        item.append(self.presentation())
        item.append(self.resprocessing())
        item.append(itemfeedback('response_allcorrect', self.feedback))
        item.append(itemfeedback('response_onenotcorrect', self.feedback))
        return item

