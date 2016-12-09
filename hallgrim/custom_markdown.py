import re

try:
    from mistune import Renderer, InlineLexer, Markdown, escape
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
except ImportError as err:
    print("Please install mistune to make use of markdown parsing.")
    print("\t pip install mistune")


no_copy = "-webkit-touch-callout: none; \
           -webkit-user-select: none; \
           -khtml-user- select: none; \
           -moz-user-select: none;\
           -ms-user-select: none;\
           user-select: none;"


def box(content, color):
    return '<div style="background-color: #ffedc9; border: 1px solid {}; \
    padding: 10px; font-size: smaller;">{}</div>'.format(color, content)


def yellow_box(content):
    return box(content, '#FFB12E')


def blue_box(content):
    return box(content, '#9999ff')


def markdown(value):
    renderer = HighlightRenderer()
    markdown = Markdown(renderer=renderer)
    return markdown(value)


class LaTeXRenderer(Renderer):

    def latex(self, formula):
        return r'\({}\)'.format(formula)
        # alternative return '<span class="latex">{}</span>'.format(formula)

    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(noclasses=True, cssstyles=no_copy)
        return highlight(code, lexer, formatter)


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
        formula = m.group(1).replace('\n', ' ')
        return self.renderer.latex(formula)


def get_custom_markdown():
    renderer = LaTeXRenderer()
    inline = LaTeXInlineLexer(renderer)

    # enable the feature
    inline.enable_latex()
    return Markdown(renderer, inline=inline)

markdown = get_custom_markdown()
