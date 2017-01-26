import xml.etree.ElementTree as et

from .multi import MultipleChoiceQuestion
from .xmlBuildingBlocks import *

class SingleChoiceQuestion(MultipleChoiceQuestion):
    """ is just a subclass of multi with the exception of this method.
    Some other minor differences exists but they are handled in the
    parent since they only concert irrelevant fields. """

    __slots__ = ()
    external_type = 'SINGLE CHOICE QUESTION'
    internal_type = 'single choice'

    def resprocessing(self):
        root = et.Element('resprocessing')
        outcomes = et.Element('outcomes')
        outcomes.append(simple_element('decvar'))
        root.append(outcomes)
        for i, (_, correct, points) in enumerate(self.questions):
            root.append(self.respcondition(points if correct else 0, 'MCSR', i, True))
        return root
