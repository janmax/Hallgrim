meta = {
    'author': 'Jan Maximilian Michal',
    'title': 'Nur Sterne sehen (I1-ID: cgu8rno0kyg0)',
    'type': 'single choice',
    'points': 1, # per correct choice
}

task = """

Das folgende Programm (nach [Sedgewick/Wayne]) erzeugt als Ausgaben mehrere
Zeilen mit Ziffern (hier genau vier):

```java
public class Ruler {
    public static void main(String[] args) {
        String ruler1 = "1";                   System.out.println(ruler1);
        String ruler2 = ruler1 + "2" + ruler1; System.out.println(ruler2);
        String ruler3 = ruler2 + "3" + ruler2;or System.out.println(ruler3);
        String ruler4 = ruler3 + "4" + ruler3; System.out.println(ruler4);
        // usw.
    }
}```

Wäre `main` auf genügend Codezeilen nach dem gleichen Schema ergänzt, wieviele
Zahlen würde bei Ausführung die n-te Ausgabezeile enthalten? """

choices = """
[ ] [[n]]
[4] [[2^n−1]]
[ ] [[2^n]]
[ ] [[2n+1]]"""

feedback = r""" Die erste Zeile ergibt genau die Ausgabe `1`. In jeder folgenden
Zeile wird die Anzahl der Zahlen verdoppelt und um eine weitere Zahl ergänzt.
Die Anzahl der Zahlen [[a_n]] im Schritt [[n]] ist daher: [[a_n = 2a_{n-1} +
1]].
Als natürlche Folge ergibt sich:

* [[S_n = a_0 + 2a_0 + 4a_0 + \dots + 2^{n-1}a_0 = a_0 (2^n - 1)]]

Weil [[a_0 = 1]] ist [[2^n−1]] die korrekte Antwort.
"""