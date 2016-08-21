import re

from itertools import product
from graphviz import Digraph

# relative imports

def gap(content, points):
    return "[gap({points}P)]{gap}[/gap]".format(points=points, gap=content)

def tex(content):
    return ('<span class="latex">' + content + '</span>').replace('\\', '\\\\')


class Automaton:

    """docstring for Automaton"""
    __slots__ = ['states', 'sigma', 'delta', 'q0', 'F']

    def __init__(self, states, sigma, delta, q0, F):
        self.states = states
        self.sigma = set(sigma)
        self.delta = delta
        self.q0 = q0
        self.F = set(F)

    def state_pairs(self):
        return filter(lambda p: p[0] != p[1], product(self.states[:-1], self.states[1:]))

    def bisimilar(self, k, z1, z2):
        if k == 0:
            return (z1 in self.F) == (z2 in self.F)

        return self.bisimilar(k-1, z1, z2) and \
            all(self.bisimilar(k-1, self.delta(z1, a), self.delta(z2, a))
                for a in self.sigma)

    def minimize(self):
        # Initialize
        k = 0
        change = True
        marker = {
            pair: 0 for pair in self.state_pairs() if not self.bisimilar(0, *pair)}

        # Iterate
        while change:
            change = False
            for z1, z2 in (pair for pair in self.state_pairs() if pair not in marker):
                if any(not self.bisimilar(k, self.delta(z1, a), self.delta(z2, a)) for a in self.sigma):
                    marker[(z1, z2)] = k+1
                    change = True
            k += 1

        # Finalize TODO
        return marker

    def generate_form(self):
        marker = self.minimize()

        form = '\n\n<p><table  border-collapse: collapse; border-style: hidden;  rules=\"all\">\n'
        form += '<tr>\n\t<td> </td>\n\t<td>' + \
            '</td>\n\t<td>'.join(self.states[1:]) + '</td></tr>\n'
        for i, z1 in enumerate(self.states[:-1]):
            form += '<tr>\n\t<td>{}</td>\n'.format(z1)
            for j, z2 in enumerate(self.states[1:]):
                content = '\t<td>{}</td>\n'
                if j < i:
                    content = content.format(' ')
                elif (z1, z2) not in marker:
                    content = content.format(gap('X', 1))
                else:
                    content = content.format(gap(marker[(z1, z2)], 1))
                form += content
            form += '</tr>\n'
        form += '</table></p>'

        return form

    def generate_task(self):

        aufgabe = '''Minimieren Sie den folgenden deterministischen Automaten
{[tex]M = \\{\\{%s\\},\\{%s\\},\\\\delta,\\{%s\\},\\{%s\\}\\}[/tex]} oder zeigen Sie, dass der Automat
bereits minimal ist. Geben Sie die Tabelle mit den Zustandspaaren an, sowie den
minimierten Graphen.<br>\n\n''' % (', '.join(self.states), ', '.join(self.sigma),
                                   str(self.q0), ', '.join(self.F))

        aufgabe += '<p>' + self.graph_output() + '</p>'

        aufgabe += self.generate_form()

        return aufgabe.replace(r'"', r'\"')

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
                f.edge(state, self.delta(state, a), label=a)

        return str(f.pipe(), encoding='utf-8')

    def generate_solution(self):
        solution = "<h3>Musterloesung</h3><br>"
        solution += re.sub(r'\[gap\(\d+P\)\](.+)\[\/gap\]',
                           r'\1', self.generate_form())
        return solution.replace(r'"', r'\"')


def delta(state, char):
    return {
        ('s0', 'a'): 's3',
        ('s0', 'b'): 's1',
        ('s1', 'a'): 's2',
        ('s1', 'b'): 's4',
        ('s2', 'a'): 's2',
        ('s2', 'b'): 's4',
        ('s3', 'a'): 's3',
        ('s3', 'b'): 's1',
        ('s4', 'a'): 's4',
        ('s4', 'b'): 's4'
    }[(state, char)]


def delta2(state, char):
    return {
        ('s0', 'a'): 's2',
        ('s0', 'b'): 's2',

        ('s1', 'a'): 's0',
        ('s1', 'b'): 's3',

        ('s2', 'a'): 's1',
        ('s2', 'b'): 's4',

        ('s3', 'a'): 's4',
        ('s3', 'b'): 's3',

        ('s4', 'a'): 's5',
        ('s4', 'b'): 's4',

        ('s5', 'a'): 's3',
        ('s5', 'b'): 's6',

        ('s6', 'a'): 's6',
        ('s6', 'b'): 's6',
    }[(state, char)]

states = ["s{}".format(i) for i in range(5)]
states2 = ["s{}".format(i) for i in range(7)]

F = ["s2"]
F2 = ["s0", "s3", "s4", "s6"]

A = Automaton(states, "ab", delta, "s0", F)


### END OF SCRIPT ########################################################
meta = {
    "type": "GAP",
    "title": "Minimieren eines deterministischen Automaten small",
    "author": "Jan Maximilian Michal",
    "gapLength": 10,
    "question": A.generate_task(),
    "solution": A.generate_solution(),
}
