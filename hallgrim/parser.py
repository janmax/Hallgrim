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
    def enable_latex(self):
        # add latex rules
        self.rules.latex = re.compile(
            r'\[\['                   # [[
            r'([^\]]+)'   # Page 2|Page 2
            r'\]\](?!\])'             # ]]
        )

        # Add latex parser to default rules
        # you can insert it some place you like
        # but place matters, maybe 3 is not good
        self.default_rules.insert(3, 'latex')

    def output_latex(self, m):
        formula = m.group(1)

        # you can create an custom render
        # you can also return the html if you like
        return self.renderer.latex(formula)

def get_custom_markdown():
    renderer = LaTeXRenderer()
    inline = LaTeXInlineLexer(renderer)

    # enable the feature
    inline.enable_latex()
    return Markdown(renderer, inline=inline)


def choice_parser(raw_choices):
    lines = raw_choices.strip().split('\n')
    parse = [re.match('\[(X| )\] (.*)', line).groups() for line in lines]
    final = [(markdown(text), True if mark == 'X' else False, 0.5) for mark, text in parse]
    return final

markdown = get_custom_markdown()

