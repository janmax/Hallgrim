import os
import re
import runpy
import importlib

def info(message):
    print('[Info]', message)

def create_autoilias_script(type, title, author, question, solution,
                            points=9999, answer=None, gapLength=None, number=1):
    with open('templates/generic.class.php', 'r', encoding='utf-8') as script:
        script = script.read()

        if not gapLength:
            gapComment = ''
            gapLength = int(gapLength)
        else:
            gapComment = '//'
            gapLength = ''

        script = script.format(
            type=type, title=title, author=author, number=number, points=points,
            gapComment=gapComment, gapLength=gapLength, question=question,
            solution=solution,
        )

        with open('output/generator__' + title.replace(' ', '_') + '.class.php', 'w', encoding='utf-8') as output:
            print(script, file=output)


def worker():
    # runpy.run_path("src/util.py")
    for script in filter(lambda dat: re.search('\d+_\w+\.py', dat), os.listdir('./src')):
        info('excuting script ' + script)
        meta = runpy.run_module('src.' + script.replace('.py', ''))['meta']
        create_autoilias_script(**meta)

if __name__ == '__main__':
    worker()
