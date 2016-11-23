meta = {
    'author': 'Jan Maximilian Michal',
    'title': 'Originale Kopien? (I1-ID: 0c05by80syg0)',
    'type': 'gap',
    'points': 0.5, # per correct choice
}


task = """ `a`, `b` sind Variablen vom Typ `char[]` und `c`, `d` sind Variablen
vom Typ `String`. `a`, `b`, `c` und `d` sind bereits korrekt mit Zeichenfolgen
der Länge 2 initialisiert (d.h. die jeweiligen Felder/Strings belegen
Speicherplatz und man kann auf ihre Inhalte zugreifen). Welcher Code ist
geeignet, um festzustellen, ob die in a und b bzw. in c und d gespeicherten
Zeichenfolgen gleich sind?

* `if (a == b) ...` [select][ ]geeignet\n[0.5]ungeeignet[/select]
* `if (a.equals(b)) ...` [select][ ]geeignet\n[0.5]ungeeignet[/select]
* `if (a[0] == b[0] || a[1] == b[1]) ...` [select][ ]geeignet\n[0.5]ungeeignet[/select]
* `if (a[0] == b[0] && a[1] == b[1]) ...` [select][0.5]geeignet\n[ ]ungeeignet[/select]
* `if (c == d) ...` [select][ ]geeignet\n[0.5]ungeeignet[/select]
* `if (c.equals(d)) ...` [select][0.5]geeignet\n[ ]ungeeignet[/select]
* `if (c.compareTo(d) == 0) ...` [select][0.5]geeignet\n[ ]ungeeignet[/select]
* `if (c[0] == d[0] && c[1] == d[1]) ...` [select][ ]geeignet\n[0.5]ungeeignet[/select]
"""

# Antworten bitte aus drop-down-Menü wählen lassen:
# Auswahl jeweils geeignet/nicht geeignet


feedback = """

Wichtig ist darauf zu achten, dass Objekte vom Typ String spezifische Methoden
exportieren, die das vergleichen oder bearbeiten von Zeichenketten erlauben.
Einfache `char[]` Arrays erlauben das nicht.

Da der Objekte vom Typ String jedoch `char` Arrays enthalten ist es möglich
über Indizierung den Vergleich 'per Hand' durchzuführen.

"""

