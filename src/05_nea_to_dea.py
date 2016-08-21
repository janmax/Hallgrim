from collections import deque
from functools import reduce
from graphviz import Digraph

import re


def gap(content, points):
    return "[gap({points}P)]{gap}[/gap]".format(points=points, gap=content)

def p(content):
    return '<p>{}</p>\n'.format(content)

def tex(content):
    return ('<span class="latex">' + content + '</span>').replace('\\', '\\\\')


class NEA:

    """docstring for NEA"""
    __slots__ = ['states', 'sigma', 'delta', 'q0', 'F']

    def __init__(self, states, sigma, delta, q0, F):
        self.states = states
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.F = set(F)

    def to_dea(self):
        done = []
        new_steps = deque([{self.q0}])
        table = []

        while new_steps:
            cur = new_steps.popleft()
            table.append([cur])
            for a in self.sigma:
                next = reduce(lambda a, b: a | b, (self.delta(s, a) for s in cur))
                table[-1].append(next)
                if next not in done:
                    new_steps.append(next)
                    done.append(next)

        return table

    def graph_output(self, file_format='svg'):
        f = Digraph('finite_state_machine', format=file_format, engine='dot')
        f.body.extend(['rankdir=LR', 'size="8,5"'])

        f.attr('node', shape='doublecircle')
        for node in self.F:
            f.node(node)

        f.attr('node', shape='circle')
        f.node('', style='invis')
        f.edge('', self.q0)
        for state in self.states:
            for a in self.sigma:
                for next in self.delta(state, a):
                    f.edge(str(state), next, label=a)

        return str(f.pipe(), encoding='utf-8')

    def generate_form(self):
        table = self.to_dea()
        tr = '<tr>\n{}</tr>\n'
        td = '\t<td>{}</td>\n'

        aufgabe = '<table  border-collapse: collapse; border-style: hidden;  rules=\"all\">\n'
        aufgabe += tr.format(''.join(td.format(s)
                                     for s in [tex(r'\delta'), "a", "b"]))
        for row in table:
            first, second, third = map(', '.join, (sorted(s) for s in row))
            aufgabe += tr.format(td.format(first) +
                                 td.format(gap(second, 1)) +
                                 td.format(gap(third, 1)))
        aufgabe += '</table>'

        return aufgabe

    def generate_ilias(self):
        aufgabe = '''Wandeln Sie M in einen DEA M' um, indem Sie die
            Potenzmenge der Zustände aus M in M' als neue Zustände einfügen
            (Eine Anleitung befindet sich im Skript von Dr. Müller S. 25).\n\n'''

        aufgabe += p(self.graph_output())
        aufgabe += p('''Füllen Sie diese Tabelle nach dem Vorbild im Müller
            Skript aus. Achten Sie dabei darauf alle Zustände in lexikographischer
            Reihenfolge aufzulisten (Zum Beispiel: s1, s2, s4) und alle Zustände
            müssen mit Komma und Leerzeichen getrennt werden.''')
        aufgabe += p(self.generate_form())

        return aufgabe.replace('"', r'\"')

    def generate_solution(self):
        solution = "<h3>Musterloesung</h3><br>"
        solution += re.sub(r'\[gap\(\d+P\)\](.+)\[\/gap\]',
                           r'\1', self.generate_form())
        return solution.replace(r'"', r'\"')


# Define one Automaton
def delta(state, char):
    return {
        ('s0', 'a'): {'s0', 's1'},
        ('s0', 'b'): {'s0', 's2'},

        ('s1', 'a'): {'s1', 's3'},
        ('s1', 'b'): {'s1'},

        ('s2', 'a'): {'s2'},
        ('s2', 'b'): {'s2', 's3'},

        ('s3', 'a'): set(),
        ('s3', 'b'): set(),
    }[(state, char)]

states = ["s{}".format(i) for i in range(4)]
F = ["s3"]

# create
N = NEA(states, "ab", delta, 's0', F)

### END OF SCRIPT ########################################################
meta = {
    "type": "GAP",
    "title": "NEA in DEA umwandeln",
    "author": "Jan Maximilian Michal",
    "gapLength": 10,
    "question": N.generate_ilias(),
    "solution": N.generate_solution(),
}
