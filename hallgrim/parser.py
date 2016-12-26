import re
import collections

from .custom_markdown import get_markdown


def choice_parser(raw_choices, points):
    """ Parse the multiple choice answers and form an array that has the
    following form: (text, isCorrect, points, solution) and store them in an
    array of arbitrary size

    TODO : This is too dense. simplyfy!
    """
    markdown = get_markdown()
    if type(raw_choices) is str:
        lines = raw_choices.strip().split('\n')
    elif type(raw_choices) is list:
        lines = raw_choices
    regex = re.compile('\s*\[(([0-9]*[.])?[0-9]+|X| )\]\s+([\w\W]+)', re.MULTILINE)
    parse = [re.match(regex, line).groups() for line in lines]
    final = [(
        markdown(text),
        True if mark != ' ' else False,
        float(mark) if mark not in ' X' else points)
        for mark, _, text in parse]
    return final


def gap_parser(task):
    markdown = get_markdown()

    # '\[gap\]([\w\W]+?)\[\/gap\]'
    # '\[select\]([\w\W]+?)\[\/select\]'
    # '\[numeric\]([\w\W]+?)\[\/numeric\]'
    # We match against one big regex that consists of three smaller ones (see
    # above)
    _all = re.compile('(\[numeric\((([0-9]*[.])?[0-9]+)P\)\]([\w\W]+?)(\[\/numeric\])|(\[select\])([\w\W]+?)\[\/select\]|\[gap\((([0-9]*[.])?[0-9]+)P\)\]([\w\W]+?)(\[\/gap\]))', re.MULTILINE)
    for m in re.finditer(_all, task):
        ('[gap]' in m.groups())

    gaps = collections.deque()
    for m in re.finditer(_all, task):
        if '[select]' in m.groups():
            match = m.group(7)
            lines = match.strip().split('\n')
            regex = re.compile('\[(([0-9]*[.])?[0-9]+| )\]\s?([\w\W]+)', re.MULTILINE)
            parse = [re.search(regex, line).groups() for line in lines]
            gaps.append(([(text, float(points) if not points == ' ' else 0)
                          for points, _, text in parse], 999))

        if '[/gap]' in m.groups():
            match = m.group(10)
            gaps.append((set(m.strip() for m in match.split(',')), m.group(8)))

        if '[/numeric]' in m.groups():
            match = m.group(4)
            regex = re.compile('[-+]?\d*\.\d+|\d+')
            parse = re.findall(regex, match)
            if len(parse) == 1:
                gaps.append(((parse[0], parse[0], parse[0]), m.group(2)))
            elif len(parse) == 3:
                gaps.append((tuple(parse), m.group(2)))
            else:
                raise Exception("Numeric gap takes either exactly one value or (value, min, max).")

    source = re.sub(_all, 'AISBLAKJSD', task)
    source = markdown(source)
    texts = collections.deque(source.split('AISBLAKJSD'))

    final = collections.deque()
    for _ in range(min(len(texts), len(gaps))):
        text = texts.popleft()
        if text != "":
            final.append(text)
        final.append(gaps.popleft())

    final.extend(gaps)
    final.extend(texts)
    final.appendleft(markdown("### Aufgabenstellung"))

    return final

def order_parser(order_str):
    return [field.strip() for field in order_str.strip().split('--') if field]
