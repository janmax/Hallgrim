# -*- coding: utf-8 -*-

from random import shuffle, sample

meta = {
    'author': 'Jan Maximilian Michal',
    'title': 'Feldarbeit (I1-ID: p0kaixs0lyg0)',
    'type': 'single choice',
    'points': 1,  # per correct choice
}


def list_to_str(lst):
    return str(lst).strip('[]')


N = 8
a = sample(range(20), N)
o = list(a)
for i in range(N):
    a[i] = a[(i + 1) % N]

c = a[:-1] + [o[0]]

task = """
Welche Ausgabe erzeugt folgender Code:

```java
public class Feldarbeit {
    public static void main(String[] args) {
        int[] a = { %s };
        int N = a.length;
        for (int i = 0; i < N; i++) {
            a[i] = a[(i+1) %% N];
        }
        for (int i = 0; i < N; i++)
            System.out.print(a[i] + " ");
        System.out.println();
    }
}
```
""" % list_to_str(o)

choices = """
[4] `%s`
[2] `%s`
[ ] `1 1 1 1 1 1 1 1`
[ ] `%s`
""" % (list_to_str(a), list_to_str(c), list_to_str(shuffle(o)))

feedback = """

Betrachten Sie die folgenden Zeilen:
```java
for (int i = 0; i < N; i++) {
    a[i] = a[(i+1) %% N];
}
```

Der Inhalt jeder Zelle des Arrays jeweils durch den linken Nachbarn ersetzt,
wobei an den Rändern zyklisch verfahren wird. Dadurch, dass *in-place* verfahren
wird, also keine Kopie erstellt wird, wird der neue Inhalt der 0. Zelle in die
letzte geschrieben, daher enthält das neue Array keine %d mehr.""" % o[0]
