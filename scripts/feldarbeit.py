meta = {
    'author': 'Jan Maximilian Michal',
    'title': 'Feldarbeit (I1-ID: p0kaixs0lyg0)',
    'type': 'single choice',
    'points': 1, # per correct choice
}

task = """
Welche Ausgabe erzeugt folgender Code:

```java
public class Feldarbeit {
    public static void main(String[] args) {
        int[] a = { 0, 1, 2, 3, 4, 5, 6, 7};
        int N = a.length;
        for (int i = 0; i < N; i++) {
            a[i] = a[(i+1) % N];
        }
        for (int i = 0; i < N; i++)
            System.out.print(a[i] + " ");
        System.out.println();
    }
}
```
"""

choices = """
[4] `1 2 3 4 5 6 7 1`
[2] `1 2 3 4 5 6 7 0`
[ ] `1 1 1 1 1 1 1 1`
[ ] `7 0 1 2 3 4 5 6`
"""

feedback = """
Betrachten Sie die folgenden Zeilen:
```java
for (int i = 0; i < N; i++) {
    a[i] = a[(i+1) % N];
}
```

Der Inhalt jeder Zelle des Arrays jeweils durch den linken Nachbarn ersetzt,
wobei an den Rändern zyklisch verfahren wird. Dadurch, dass *in-place* verfahren
wird, also keine Kopie erstellt wird, wird der neue Inhalt der 0. Zelle in die
letzte geschrieben, daher enthält das neue Array keine 0 mehr. """


