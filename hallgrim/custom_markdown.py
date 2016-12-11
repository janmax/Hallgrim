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

style = """
<style id="ilias-table" type="text/css" scoped>
.mytable {
  margin: 1cm;
  padding: 10px;
  border: 1px solid black;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
  border-collapse: collapse;
  border-spacing: 3px;
}

tr.mytable:nth-child(even) {
    background-color: #f2f2f2
}

tr.mytable:hover {
    background-color: #f5f5f5
}

th.mytable {
    background-color: #557196;
    color: white;
}
</style>
<script>

// Writing this code was a huge fuckup. For some reason (I'm not a web
// developer) ILIAS encodes all occurrences of curly braces and the backlash
// escape character. In order to get my custom style working I had to write
// JavaScript without these characters. Goodbye functions and goodbye loops.
// Here is the ugly result:

x = document.getElementById("ilias-table");
x.innerHTML = x.innerHTML.replace("&#123;", String.fromCharCode(0x7B))
x.innerHTML = x.innerHTML.replace("&#123;", String.fromCharCode(0x7B))
x.innerHTML = x.innerHTML.replace("&#123;", String.fromCharCode(0x7B))
x.innerHTML = x.innerHTML.replace("&#123;", String.fromCharCode(0x7B))
x.innerHTML = x.innerHTML.replace("&#125;", String.fromCharCode(0x7D))
x.innerHTML = x.innerHTML.replace("&#125;", String.fromCharCode(0x7D))
x.innerHTML = x.innerHTML.replace("&#125;", String.fromCharCode(0x7D))
x.innerHTML = x.innerHTML.replace("&#125;", String.fromCharCode(0x7D))
</script>
"""


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

    def table(self, header, body):
        """Rendering table element. Wrap header and body in it.
        :param header: header part of the table.
        :param body: body part of the table.
        """
        return (
            '<div id="scoped-content"> %s'
            '<table class="mytable">\n<thead>%s</thead>\n'
            '<tbody>\n%s</tbody>\n</table>\n'
            '</div>'
        ) % (style, header, body)

    def table_row(self, content):
        """Rendering a table row. Like ``<tr>``.
        :param content: content of current table row.
        """
        return '<tr class="mytable">\n%s</tr>\n' % content

    def table_cell(self, content, **flags):
        """Rendering a table cell. Like ``<th>`` ``<td>``.
        :param content: content of current table cell.
        :param header: whether this is header or not.
        :param align: align of current table cell.
        """
        if flags['header']:
            tag = 'th'
        else:
            tag = 'td'
        align = flags['align']
        if not align:
            return '<%s class="mytable">%s</%s>\n' % (tag, content, tag)
        return '<%s class="mytable" style="text-align:%s">%s</%s>\n' % (
            tag, align, content, tag
        )

    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % escape(code)
        if lang.endswith('_copy'):
            lang = lang.rsplit('_')[0]
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter(noclasses=True)
        else:
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


def get_markdown():
    renderer = LaTeXRenderer()
    inline = LaTeXInlineLexer(renderer)

    # enable the feature
    inline.enable_latex()
    return Markdown(renderer, inline=inline)
