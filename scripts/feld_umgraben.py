# -*- coding: utf-8 -*-

meta = {
    'author': 'Jan Maximilian Michal',
    'title': 'Feld umgraben (I1-ID: xu71ubs0lyg0)',
    'type': 'single choice',
    'shuffle' : False,
    'points': 1, # per correct choice
}

task = """Die Reihenfolge der Elemente im Feld `a` der Länge **N** soll umgekehrt werden. Wählen
Sie den Code aus, der diese Aufgabe am besten löst:"""

choices = [
"""[4]
```
for (int i = 0; i < N/2; i++) {
    int tmp = a[i];
    a[i] = a[N-i-1];
    a[N-i-1] = tmp;
}
```
""",

"""[ ]
```
int[] b = new int[N];
for (int i = 0; i < N; i++)
    b[i] = a[N-i-1];
a = b;
```
""",

"""[ ]
```
for (int i = 0; i < N; i++) {
    int tmp = a[i];
    a[i] = a[N-i-1];
    a[N-i-1] = tmp;
}```
""",

"""[ ]
```
for (int i = 0; i < N/2; i++) {
    int tmp = a[i];
    a[i] = a[N-i];
    a[N-i] = tmp;
}```
"""


]

feedback = """
1. löst die Aufgabe, indem alle Elemente "um die Mitte herum rotiert" werden. Das sind maximal n/2 Operationen.
2. löst die Aufgabe NICHT, denn nach n/2 Tauschoperationen wird nochmal zurückgetauscht und alles steht am alten Platz.
3. löst die Aufgabe, verbraucht aber doppelt soviel Speicher wie nötig.
4. löst die Aufgabe NICHT: bei der ersten Iteration wird auf das nicht existente Element a[N] zugegriffen.
"""