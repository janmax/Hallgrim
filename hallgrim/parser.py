import re

from hallgrim.custom_markdown import markdown

def choice_parser(raw_choices, points):
    """ Parse the multiple choice answers and form an array that has the
    following form: (text, isCorrect, points, solution) and store them in an
    array of arbitrary size

    TODO : This is too dense. simplyfy!
    """
    if type(raw_choices) is str:
        lines = raw_choices.strip().split('\n')
    elif type(raw_choices) is list:
        lines = raw_choices
    regex = re.compile('\[(([0-9]*[.])?[0-9]+|X| )\]\s+([\w\W]+)', re.MULTILINE)
    parse = [re.match(regex, line).groups() for line in lines]
    final = [(
        markdown(text),
        True if mark != ' ' else False,
        float(mark) if mark not in ' X' else points)
    for mark, _, text in parse]
    return final

def gap_parser(task):
    r = re.compile('\[select\]([\w\W]+?)\[\/select\]', re.MULTILINE)
    m = re.findall(r, task)

    final = []
    for s in m:
        lines = s.strip().split('\n')
        regex = re.compile('\[(([0-9]*[.])?[0-9]+| )\]\s?([\w\W]+)', re.MULTILINE)
        parse = [re.search(regex, line).groups() for line in lines]
        final.append([(text.strip(), float(points) if not points == ' ' else 0) for points, _, text in parse])

    sep = '  !"§$%&/(XCVBNM;  '
    no_gaps   = re.sub(r, sep, task)
    text_only = [markdown(text) for text in no_gaps.split(sep)]

    for i, s in enumerate(final):
        text_only.insert(2*i+1, (s, -1))

    return text_only
