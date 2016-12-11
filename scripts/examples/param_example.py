from random import randint, sample

meta = {
    'author': 'Jan Maximilian Michal',
    'title': 'Parameter example',
    'type': 'single choice',
    'points': 4,  # for correct answer
}

a = randint(-50, 49)
b = randint(-50, 49)


def get_answers(right, count=4):
    possible = sample(range(-100, a+b), count//2) + \
        sample(range(a+b+1, 100), count//2-1) + [a+b]
    return [('X' if answer == right else ' ', answer) for answer in possible]


task = """ What is the answer to the question {} + {}?""".format(a, b)

choices = '\n'.join('[%s] a + b = %d' % c for c in get_answers(a+b))

feedback = "[[a + b = {}]]".format(a + b)
