import xml.etree.ElementTree as et

from .xmlBuildingBlocks import *

available_types = {}

def _register_class(target_class):
    available_types[target_class.__dict__['internal_type']] = target_class

class ValidateScriptModule(type):
    """docstring for ValidateScriptModule"""
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if name != 'IliasQuestion':
            if 'internal_type' not in class_dict \
            or 'external_type' not in class_dict:
                raise ValueError('Must define internal_type and external_type')
            _register_class(cls)
        return cls


class IliasQuestion(object, metaclass=ValidateScriptModule):
    """docstring for IliasQuestion"""

    __slots__ = ('author', 'title', 'feedback',)

    ### returns the final object #############################################
    @property
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
