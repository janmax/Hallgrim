import re
import mistune

def choice_parser(raw_choices):
    lines = raw_choices.strip().split('\n')
    parse = [re.match('\[(X| )\] (.*)', line).groups() for line in lines]
    final = [(mistune.markdown(text), True if mark == 'X' else False, 0.5) for mark, text in parse]
    return final
