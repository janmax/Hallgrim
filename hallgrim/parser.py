import re

try:
    from mistune import Renderer, InlineLexer, Markdown, escape
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
except ImportError as err:
    print("Please install mistune to make use of markdown parsing.")
    print("\t pip install mistune")

## TODO get lexer elsewhere


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
        return '<span class="latex">{}</span>'.format(formula)

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
    regex = re.compile('\[(\d|X| )\]\s+([\w\W]+)', re.MULTILINE)
    parse = [re.match(regex, line).groups() for line in lines]
    final = [(
        markdown(text),
        True if mark != ' ' else False,
        float(mark) if mark not in ' X' else points)
    for mark, text in parse]
    return final

def gap_parser(task):
    r = re.compile('\[select\]([\w\W]+?)\[\/select\]', re.MULTILINE)
    m = re.findall(r, task)

    final = []
    for s in m:
        lines = s.strip().split('\n')
        regex = re.compile('\[(\d|X| )\]\s+([\w\W]+)', re.MULTILINE)
        parse = [re.search(regex, line).groups() for line in lines]
        final.append([(text.strip(), float(points) if not points == ' ' else 0) for points, text in parse])

    sep = '  !"§$%&/(XCVBNM;  '
    no_gaps   = re.sub(r, sep, task)
    text_only = [markdown(text) for text in no_gaps.split(sep)]

    for i, s in enumerate(final):
        text_only.insert(2*i+1, (s, -1))

    return text_only
