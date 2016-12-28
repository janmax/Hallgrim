gap = r'''meta = {{
    'author': '{}',
    'title': '{}',
    'type': 'gap',
}}

task = """ description

[gap(1.0P)]Answer A, Answer B, Answer C[/gap]

[numeric(1.0P)]<value>,<min>,<max>[/numeric]

[select]
[ ] Answer A
[ ] Answer B
[X] Answer C
[/select]

"""

feedback = """ feedback """
'''

order = r'''meta = {{
    'author': '{}',
    'title': '{}',
    'type': 'order',
    'points': {}, # total number of points
}}

task = """ decription """

order = """ Answer A -- Answer B -- Answer C """

feedback = """ feedback """
'''

choice = r'''meta = {{
    'author': '{}',
    'title': '{}',
    'type': '{} choice',
    'points': {}, # points per correct question
}}

task = """ decription """

choices = """
    [ ] Answer A
    [ ] Answer B
    [X] Answer C
"""

feedback = """ feedback """
'''

config_sample = """[META]
author = <your name>

[UPLAODER]
user = root
pass = homer
host = http://localhost:8000/
rtoken = c13456ec3d71dc657e19fb826750f676
"""
