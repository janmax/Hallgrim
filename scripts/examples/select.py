meta = {
    'author': 'Jan Maximilian Michal',
    'title': 'Zeilen sind anders, Spalten auch (I1-ID: lhu27691fzg0)',
    'type': 'gap',
}


gap_1 = """[select]
[1] int n_ze = m.length;
[ ] int n_ze = m[0].length;
[ ] int n_ze = m.length();
[ ] int n_ze = m[0].length();
[/select]"""

gap_2 = """[select]
[ ] int n_sp = m.length();
[ ] int n_sp = m[0].length();
[ ] int n_sp = m.length;
[1] int n_sp = m[0].length;
[/select]"""

gap_3 = """[select]
[ ] for (int i = 1; i <= n_ze; i++)
[1] for (int i = 0; i < n_ze; i++)
[ ] for (int i = 1; i <= n_sp; i++)
[ ] for (int i = 0; i < n_sp; i++)
[/select]"""

gap_4 = """[select]
[ ] ms[i] = ms[i] + m[j][i]*s[i];
[ ] ms[i] = ms[i] + m[i][j]*s[i];
[ ] ms[i] = ms[i] + m[j][i]*s[j];
[1] ms[i] = ms[i] + m[i][j]*s[j];
[/select]"""


task = """ Folgendes Codefragment soll die Multiplikation eines Zeilenvektors mit einer Matrix sowie einer Matrix mit einem Spaltenvektor realisieren. Wählen Sie die fehlenden Zeilen unten entsprechend aus:

```java
01: int[][] m = {{ 0, 1, 2, 3},   // Matrix
02:              { 4, 5, 6, 7},
03:              {8, 9, 10, 11}};
04: int[] z = { 12, 13, 14};      // Zeile
05: int[] s = {15, 16, 17, 18};   // Spalte
06:
07: %s     // Zeilenanzahl der Matrix
08: %s     // Spaltenanzahl der Matrix
09:
10: /* 1: Zeile mal Matrix */
11: int[] zm = new int[n_sp];
12: for (int j = 0; j < n_sp; j++) {
13:     zm[j] = 0;
14:     %s
15:         zm[j] = zm[j] + z[i]*m[i][j];
16: }
17: /* 2: Matrix mal Spalte */
18: int[] ms = new int[n_ze];
19: for (int i = 0; i < n_ze; i++) {
20:     ms[i] = 0;
21:     for (int j = 0; j < n_sp; j++)
22:         %s
23:
```
""" % (gap_1, gap_2, gap_3, gap_4)

feedback = """

Der vollständige Code:

```java
int[][] m = {{ 0, 1, 2, 3},   // Matrix
             { 4, 5, 6, 7},
             {8, 9, 10, 11}};
int[] z = { 12, 13, 14};      // Zeile
int[] s = {15, 16, 17, 18};   // Spalte

int n_ze = m.length;        // Zeilenanzahl der Matrix
int n_sp = m[0].length;     // Spaltenanzahl der Matrix

/* 1: Zeile mal Matrix */011: int[] zm = new int[n_sp];
for (int j = 0; j < n_sp; j++) {
    zm[j] = 0;
    for (int i = 0; i < n_ze; i++)
        zm[j] = zm[j] + z[i]*m[i][j];
}
/* 2: Matrix mal Spalte */
int[] ms = new int[n_ze];
for (int i = 0; i < n_ze; i++) {
    ms[i] = 0;
    for (int j = 0; j < n_sp; j++)
        ms[i] = ms[i] + m[i][j]*s[j];

```
"""