import re


def gap(content, points):
    return "[gap({points}P)]{gap}[/gap]".format(points=points, gap=content)

def p(content):
    return '<p>{}</p>\n'.format(content)

def li(content):
    return '<li>{}</li>\n'.format(content)

def tex(content):
    return ('<span class="latex">' + content + '</span>').replace('\\', '\\\\')

def generate_ilias():
    aufgabe = p('Berechnen Sie:')

    aufgabe += li(tex(r'\{a,b\} \cdot \{\varepsilon, cd\} = \{') + gap('a, acd, b, bcd', 0.5) + tex('\}'))
    aufgabe += li(tex(r'\{\varepsilon, cd\} \cdot \{a, b\} = \{') + gap('a, b, cda, cdb', 0.5) + tex('\}'))
    aufgabe += li(tex(r'\{\varepsilon, a, ab\}^2 = \{') + gap('eps, a, aa, aab, aba, abab', 0.5) + tex('\}'))
    aufgabe += li(tex(r'\{\varepsilon\} \cdot \{\varepsilon\} = \{') + gap('eps', 0.5) + tex('\}'))
    aufgabe += li(tex(r'\{\varepsilon\} \cdot \emptyset = ') + gap('{}', 0.5))
    aufgabe += li(tex(r'\{\varepsilon\} \cdot \emptyset = ') + gap('{}', 0.5))
    aufgabe += li(tex(r'\emptyset^2 = ') + gap('{}', 0.5))
    aufgabe += li(tex(r'\emptyset^* = \{') + gap('eps', 0.5) + tex('\}'))
    aufgabe += li(tex(r'\{\varepsilon\}^* = \{') + gap('eps', 0.5) + tex('\}'))
    aufgabe += li(tex(r'\{\varepsilon, a\}^+ = \{') + gap('a*', 0.5) + tex('\}'))

    aufgabe += ''' Verwenden Sie <code>eps</code> für {eps} und
    <code>{{}}</code> für {empty}. Geben Sie alle Elemente der neuen Menge in
    lexikographischer Reihenfolge an und verwenden Sie Leerzeichen nach einem
    Komma. (Z.B. eps, a, ab, acd, ba)'''.format(eps=tex(r'\varepsilon'), empty=tex(r'\emptyset'))


    return aufgabe.replace(r'"', r'\"')

def generate_solution():
        solution = "<h3>Musterloesung</h3><br>"
        solution += re.sub(r'\[gap\(\d+P\)\](.+)\[\/gap\]',
                           r'\1', generate_ilias())
        return solution


### END OF SCRIPT ########################################################
meta = {
    "type": "GAP",
    "title": "Grundlagen",
    "author": "Jan Maximilian Michal",
    "gapLength": 10,
    "question": generate_ilias(),
    "solution": generate_solution(),
}
