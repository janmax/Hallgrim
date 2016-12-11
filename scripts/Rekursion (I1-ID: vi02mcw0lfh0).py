meta = {
    'author': 'ILIAS Author',
    'title': 'Rekursion (I1-ID: vi02mcw0lfh0)',
    'type': 'gap',
    'points': 4,
}

task = """
Welchen String liefert der Aufruf exB(5)?

```java_copy
public static String exB(int n) {
    if (n <= 0)
        return "";
    return exB(n-2) + (n+1) + exB(n-1);
}
```

Geben Sie die Ziffern hintereinander an, d.h. ohne Leerzeichen o.ä.: [gap(4P)]243263252432[/gap]
"""

feedback = """

Der Rekursionsbaum stellt die Aufrufe durch Knoten dar, die jeweils mit dem
Aufrufargument markiert sind. Die äußeren Knoten (ganz unten) entsprechen
Basisfällen, sie tragen nicht zum Ergebnisstring bei (denn sie liefern nur das
leere Wort). Die anderen (inneren) Knoten tragen bei, und zwar in unserem Fall
je eine Ziffer.

glw4u2g0xfg0.png

Traversiert man den Baum in Inorder-Reihenfolge, so ist die Reihenfolge der
Aufrufargumente genau `1, 3, 2, 1, 5, 2, 1, 4, 1, 3, 2, 1`. Die entsprechenden
Ziffern sind immer um 1 höher, also lautet der Ergebnisstring: 243263252432
"""
