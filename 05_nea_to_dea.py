from collections import deque
from functools import reduce
from graphviz import Digraph
# from pprint import pprint as print


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
                next = reduce(lambda a, b: a | b, (self.delta(s, a)
                                                   for s in cur))
                table[-1].append(next)
                if next not in done:
                    new_steps.append(next)
                    done.append(next)

        return table

    def graph_output(self, file_format='svg'):
        f = Digraph('finite_state_machine', format='pdf')
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

        f.view()
        # return str(f.pipe(), encoding='utf-8')

    def generate_ilias(self):
        table = self.to_dea()

        aufgabe = ''' Aufgabentext\n\n'''


        tr = '<tr>\n{}</tr>\n'
        td = '\t<td>{}</td>\n'

        aufgabe += '<table  border-collapse: collapse; border-style: hidden;  rules=\"all\">\n'
        aufgabe += tr.format(''.join(td.format(s) for s in ["delta", "a", "b"]))
        for row in table:
            aufgabe += tr.format(''.join(td.format(','.join(sorted(s))) for s in row))
        aufgabe += '</table>'

        print(aufgabe.replace('"', r'\"'))

        print("{:>25}{:>25}{:>25}".format("delta", "a", "b"))
        for row in table:
            print("{:>25}{:>25}{:>25}".format(*map(', '.join, (sorted(s) for s in row))))



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

N = NEA(states, "ab", delta, 's0', F)
N.to_dea()
# N.graph_output()
N.generate_ilias()