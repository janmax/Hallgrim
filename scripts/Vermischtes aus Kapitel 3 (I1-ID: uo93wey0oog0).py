meta = {
    'author': 'Jan Maximilian Michal',
    'title': 'Vermischtes aus Kapitel 3 (I1-ID: uo93wey0oog0)',
    'type': 'multiple choice',
    'points': 0.5,
}

task = """ Kreuzen Sie alles an, was im weitesten Sinne wahr ist (wahre Aussagen, korrekte Formulierungen, Ausdrücke mit Wert true): """

choices = """
[X] Formalparameter sind lokale Variablen.
[X] Die JVM interpretiert Java-Bytecode.
[X] (false ? true : false) == (true ? false : true)
[ ] Das rekursive Grundschema lautet: Rekurriere - Finalisiere (falls trivial)
[ ] Die Java-Laufzeitumgebung beinhaltet Compiler, Klassenbibliotheken und die (JVM) Java Virtual Machine.
[ ] An Ausdrücke dürfen keine Zuweisungen erfolgen.
[ ] Methoden mit Signatur int (int) werden mit call-by-reference aufgerufen.
[ ] (false ? false : true) == (false ? true : false)
"""

feedback = """
| Aussage                                                                                                 |  Wert   |   Begründung                                                                                                                                                                                                                                                                                                         |
|---------------------------------------------------------------------------------------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Formalparameter sind lokale Variablen.                                                                  | TRUE    |  Die im Methodenkopf definierten Parameter heißen auch Formalparameter und werden innerhalb der Methode als Variable gebraucht. TatsÃ¤chliche Parameter sind die im Programmablauf übergebenen Werte oder Referenzen.                                                                                                |
| Die JVM interpretiert Java-Bytecode.                                                                    | TRUE    |  Java-Bytecode ist das Instruction-Set der Java-Virtual-Machine                                                                                                                                                                                                                                                      |
| (false ? true : false) == (true ? false : true)                                                         | TRUE    |  (false ? true : false) == (true ? false : true) -> false == false -> true                                                                                                                                                                                                                                           |
| Das rekursive Grundschema lautet: Rekurriere - Finalisiere (falls trivial)                              | FALSE   |  Das rekursive Grundschema lautet: Finalisiere (falls trivial) - Rekurriere                                                                                                                                                                                                                                          |
| Die Java-Laufzeitumgebung beinhaltet Compiler, Klassenbibliotheken und die (JVM) Java Virtual Machine.  | FALSE   |  Wikipedia: "Allgemein besteht die Laufzeitumgebung aus der Java Virtual Machine (Java VM), die für die Ausführung der Java-Anwendungen verantwortlich ist, einer Programmierschnittstelle (API, für Application and Programming Interface) und weiteren Programmbibliotheken." Ein Compiler gehört nicht dazu.      |
| An Ausdrücke dürfen keine Zuweisungen erfolgen.                                                         | FALSE   |  Da zum Beispiel x[0] = 1                                                                                                                                                                                                                                                                                            |
| Methoden mit Signatur int (int) werden mit call-by-reference aufgerufen.                                | FALSE   |  SÃ¤mtliche Java Methoden werden mit call-by-value aufgerufen. Eine gute ErklÃ¤rung zu den Unterschieden finden Sie hier.                                                                                                                                                                                            |
| (false ? false : true) == (false ? true : false)                                                        | FALSE   |  (false ? false : true) == (false ? true : false) -> true == false -> false                                                                                                                                                                                                                                          |
"""
