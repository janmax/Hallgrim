import re
import mistune
import copy

try:
    from mistune import Renderer, InlineGrammar, InlineLexer, Markdown
except ImportError as err:
    print("Please install mistune to make use of markdown parsing.")
    print("\t pip install mistune")


class LaTeXRenderer(Renderer):
    def latex(self, formula):
        return '<span class="latex">{}</span>'.format(formula)

class LaTeXInlineLexer(InlineLexer):
    """ Classes are inspired by the lexer example in the mistune readme """
    def enable_latex(self):
        # add latex rules
        self.rules.latex = re.compile(
            r'\[\['                   # [[
            r'([^\]]+)'               # formula
            r'\]\](?!\])'             # ]]
        )
        self.default_rules.insert(3, 'latex')

    def output_latex(self, m):
        formula = m.group(1)
        return self.renderer.latex(formula)

def get_custom_markdown():
    renderer = LaTeXRenderer()
    inline = LaTeXInlineLexer(renderer)

    # enable the feature
    inline.enable_latex()
    return Markdown(renderer, inline=inline)


def choice_parser(raw_choices, points):
    """ Parse the multiple choice answers and form an array that has the
    following form: (text, isCorrect, points, solution) and store them in an
    array of arbitrary size """
    lines = raw_choices.strip().split('\n')
    parse = [re.match('\[(X| )\] (.*)', line).groups() for line in lines]
    final = [(markdown(text), True if mark == 'X' else False, points) for mark, text in parse]
    return final

markdown = get_custom_markdown()

