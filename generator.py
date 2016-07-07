import os
import re


def create_autoilias_script(type, title, author, question, solution,
                            points=9999, answer=None, gapLength=None, number=1):
    with open("templates/generic.class.php", "r", encoding='utf-8') as script:
        script = script.read()

        if not gapLength:
            gapComment = ""
            gapLength = int(gapLength)
        else:
            gapComment = "//"
            gapLength = ""

        script = script.format(
            type=type, title=title, author=author, number=number, points=points,
            gapComment=gapComment, gapLength=gapLength, question=question,
            solution=solution,
        )

        with open("output/" + title.replace(' ', "_") + ".class.php", 'w', encoding='utf-8') as output:
            print(script, file=output)

for script in filter(lambda dat: re.search('\d+_\w+\.py', dat), os.listdir('./src')):
    with open('./src/' + script) as script_f:
        exec(script_f.read())
        create_autoilias_script(**meta)