meta = {
    'author': 'Jan Maximilian Michal',
    'title': 'Sortieren nach Punkten (I1-ID: nipe84411eh0)',
    'type': 'multiple choice',
    'points': 0.5, # per correct choice
}

task = """
Hier der Anfang der Datei `punkte.csv`, die Komma-getrennte Angaben
zu erreichten Übungspunkten enthält [[Example Formula \\sum_{i=0}^n i]]:

```
21600001,Herr,Bollman,Fritze-Peter,15
21600002,Frau,Bollwoman,Franzi,19
21600003,Herr,Lindemann,Erwin,17
21600004,Frau,Lindefrau,Edelgard Martha,12
21600005,Herr,Machtnix,Mike,2
.....
```

Welches Shell-Kommando ist geeignet, die Zeilen nach fallender Punktzahl
sortiert auszugeben (also erst große, dann kleinere Punktzahlen)? """

choices = """
[ ] `sort --reverse --k 5 --numeric-sort punkte.csv`
[X] `sort --r --field-separator=, -k 5 --n punkte.csv`
[ ] `sort -r -t="," -k 5 --n punkte.csv`
[X] `sort --reverse -t "," -k 5 -n punkte.csv`
[ ] `sort -r --field-separator "," -k 4 -numeric punkte.csv`
[ ] `sort -r --field-separator "," -k 4 punkte.csv`
"""

explanations = """
[ ] sort --reverse --k 5 --numeric-sort punkte.csv falsch (u.a.: ungültiges Argument --k)
[ ] sort --r --field-separator=, -k 5 --n punkte.csv falsch (u.a.: bei kurzem Argument -k darf kein = stehen)
[ ] sort -r -t="," -k 5 --n punkte.csv falsch (siehe oben)
[X] sort --reverse -t "," -k 5 -n punkte.csv richtig
[ ] sort -r --field-separator "," -k 4 -numeric punkte.csv falsch (u.a.: Punkte stehen in Spalte 5)
[ ] sort -r --field-separator "," -k 4 punkte.csv falsch (u.a.: keine numerische Sortierung)
"""