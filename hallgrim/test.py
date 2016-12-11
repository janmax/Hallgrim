# -*- coding: utf-8 -*-

from custom_markdown import get_markdown
from collections import deque
from pprint import pprint


task = """[gap]LALAL2[/gap] KJAakjsfdaskdjfnalksdf


```java
[select]
    [3] `int n_ze = m.length;`
    [ ] `int n_ze = m[0].length;`
    [ ] `int n_ze = m.length();`
    [ ] `int n_ze = m[0].length();`
[/select]

[gap]LALAL1[/gap][gap]LALAL2[/gap]

public static void main {
    System.out.println("TATAT");
}
[numeric]3.4,-1, 34.7[/numeric][numeric]4,+5,6[/numeric][numeric]4[/numeric]
```


HALLO WO BIN ICH

[select]
    [4] `int n_ze = m.length;`
    [ ] `asdlkjasld;`
[/select]

END"""

import re

markdown = get_markdown()


# '\[gap\]([\w\W]+?)\[\/gap\]'
# '\[select\]([\w\W]+?)\[\/select\]'
# '\[numeric\]([\w\W]+?)\[\/numeric\]'
# We match against one big regex that consists of three smaller ones (see above)
_all = re.compile('(\[numeric\]([\w\W]+?)(\[\/numeric\])|(\[select\])([\w\W]+?)\[\/select\]|\[gap\]([\w\W]+?)(\[\/gap\]))', re.MULTILINE)
for m in re.finditer(_all, task):
    ('[gap]' in m.groups())

gaps = deque()
for m in re.finditer(_all, task):
    if '[select]' in m.groups():
        match = m.group(5)
        lines = match.strip().split('\n')
        regex = re.compile('\[(([0-9]*[.])?[0-9]+| )\]\s?([\w\W]+)', re.MULTILINE)
        parse = [re.search(regex, line).groups() for line in lines]
        gaps.append([(text, float(points) if not points == ' ' else 0) for points, _, text in parse])

    if '[/gap]' in m.groups():
        match = m.group(6).strip('\n\t ')
        gaps.append((match, 4)) ## ADD POINTS !!

    if '[/numeric]' in m.groups():
        match = m.group(2)
        regex = re.compile('[-+]?\d*\.\d+|\d+')
        parse = re.findall(regex, match)
        if len(parse) == 1:
            gaps.append(((parse[0], parse[0], parse[0]), 4))
        elif len(parse) == 3:
            gaps.append((tuple(parse), 4))
        else:
            raise Exception("Numeric gap takes either exactly one value or (value, min, max).")

n = re.sub(_all, 'GAPGAP', task)
n = markdown(n)
t = deque(n.split('GAPGAP'))

final = deque()
while text or gaps:
    if text[0] != "":
        final.append(text.popleft())
    final.append(gap.popleft())

return final