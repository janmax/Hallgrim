from itertools import product

delta = """
    S := AB | ABA
    A := aA | a
    B := Bb | eps
"""

class rule:
    __slots__ = ['left', 'right']
    def __init__(self, left, right, sep=""):
        self.left = left
        self.right = [c for c in right] if right != "eps" else []

    def __str__(self):
        return self.left + " := " + ''.join(self.right)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right


def parse(grammer):
    grammer = grammer.strip()
    terminals = set()
    non_terms = set()
    rules     = set()

    for line in grammer.split("\n"):
        N, rule_list = line.split(":=")
        rules |= {rule(N.strip(), right.strip()) for right in rule_list.split("|")}
        non_terms |= {N}

    for r in rules:
        if r.right != 'eps':
            terminals |= {T for T in r.right if T.islower()}

    return rules, terminals, non_terms

P, T, N = parse(delta)

print(('\n'.join(map(str, P))))
print()

letters_to_kill = {p.left for p in P if not p.right}
new_P = set() | P
for p in P:
    for l in letters_to_kill:
        n = p.right.count(l)
        r = ''.join(p.right).replace(l, "{}")

        # 0 is a placeholder for empty string
        for prod in product(l + "0", repeat=n):
            new_P |= {rule(p.left, r.format(*prod).replace("0", ""))}

P = {p for p in new_P if p.right}
print(('\n'.join(map(str, P))))
print()

for t in T:
    P |= {rule("T_" + t, t)}

print(T)

new_P = set() | P
for p in P:
    p.right = ["T_" + p if p in T else p for p in p.right]

P = new_P
print(('\n'.join(map(str, P))))
print()

new_P = set() | P
for p in P:
    if len(p.right) > 2:
        pass
