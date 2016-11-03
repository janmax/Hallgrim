import xml.etree.ElementTree as et

from hallgrim.IliasXMLCreator.xmlBuildingBlocks import *

class GapQuestion:
    """docstring for GapQuestion"""
    def __init__(self, type, description, question_text, author, title, questions, feedback, gapLength):
        self.type           = type
        self.description    = description
        self.question_text  = question_text
        self.author         = author
        self.title          = title
        self.questions      = questions
        self.feedback       = feedback
        self.gapLength      = gapLength
