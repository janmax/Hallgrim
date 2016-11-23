meta = {
    'author': 'Jan Maximilian Michal',
    'title': 'Originale Kopien? (I1-ID: 0c05by80syg0)',
    'type': 'multiple choice',
    'points': 0.5, # per correct choice
}


task = """ `a`, `b` sind Variablen vom Typ `char[]` und `c`, `d` sind Variablen
vom Typ `String`. `a`, `b`, `c` und `d` sind bereits korrekt mit Zeichenfolgen
der Länge 2 initialisiert (d.h. die jeweiligen Felder/Strings belegen
Speicherplatz und man kann auf ihre Inhalte zugreifen). Welcher Code ist
geeignet, um festzustellen, ob die in a und b bzw. in c und d gespeicherten
Zeichenfolgen gleich sind? """

# Antworten bitte aus drop-down-Menü wählen lassen:
# Auswahl jeweils geeignet/nicht geeignet

choices = """
[ ] `if (a == b) ...`
[ ] `if (a.equals(b)) ...`
[ ] `if (a[0] == b[0] || a[1] == b[1]) ...`
[X] `if (a[0] == b[0] && a[1] == b[1]) ...`
[ ] `if (c == d) ...`
[X] `if (c.equals(d)) ...`
[X] `if (c.compareTo(d) == 0) ...`
[ ] `if (c[0] == d[0] && c[1] == d[1]) ...`
"""

feedback = """

"""

