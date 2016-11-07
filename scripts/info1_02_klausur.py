meta = {
    'author': 'Carsten Damm',
    'title': 'Vermischtes zu elementaren Daten (I1-ID: e638zfi0qtg0)',
    'type': 'multiple choice',
    'points': 0.5, # per correct choice
}

task = """ Markieren Sie alle zutreffenden Aussagen: """

choices = """
[ ] `int x = Integer.MAX_VALUE; x++;` verursacht eine OverflowException.
[ ] Steuerzeichen werden vom Steuerwerk interpretiert.
[X] `if (b > 0 && a/b < 2)` ... ist besser als `if (a/b < 2 && b > 0)` ...
[ ] Umlaute im Quelltext verursachen Compilezeitfehler.
[X] `"h\u00F6chstens 6 Zeichen"` ist ein Literal.
[ ] `Integer.MAX_VALUE++;` verursacht einen Ganzzahlüberlauf.
[ ] UTF-8 ordnet jedem Zeichen eine Folge von 8 Bytes zu.
[X] Ganzzahl-Arithmetik ist schneller als Gleitkomma-Arithmetik.
"""

feedback = """
Die folgenden Aussagen sind korrekt:

* `if (b > 0 && a/b < 2)` ... ist besser als `if (a/b < 2 && b > 0)` ...
 * *Begründung:* `a/b < 2` ist aufwändiger zu berechnen als `b > 0`. Bei einer Prüfung des Wahrheitswerts einer Konjunktion muss der zweite Term nicht betrachtet werden, wenn der erste falsch ist.
* `"h\u00F6chstens 6 Zeichen"` ist ein Literal.
 * *Begründung:* Da der String eine konstanten Wert darstellt ist er als Literal zu bezeichnen.
* Ganzzahl-Arithmetik ist schneller als Gleitkomma-Arithmetik.
 * *Begründung:* Floating Point Arithmetik ist wesentlich aufwändiger als Integer Arithmetik (siehe zum Vergleich: Zweitkomplement und IEE-754)
"""