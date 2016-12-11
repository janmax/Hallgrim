meta = {
    'author': 'ILIAS Author',
    'title': 'Eine Methode (I1-ID: 75li4j91gdg0)',
    'type': 'gap',
    'points': 5.0,
}

gap1 = "[select][0.0]final\n [0.5]static\n [0]void\n [0]private\n [/select]"
gap2 = "[select][0]string\n [0]int\n [0.5]boolean\n [0]class\n [/select]"
gap3 = "[select][1]return\n [0]system.out.println\n [0]=\n [0]set\n [/select]"
gap4 = "[select][0]j % 4\n [0]j : 4\n [0.5]j % 4 == 0\n [0]j : 4 == 0\n [/select]"
gap5 = "[select][0.5]&&\n [0.5]||\n [0.5]&\n [0]^\n [/select]"
gap6 = "[select][0]j : 100 != 0 || j : 400 == 0\n [0]j % 100 != 0 || j % 400 = 0\n [0]j : 100 != 0 || j : 400 = 0\n [1]j % 100 != 0 || j % 400 == 0\n [/select]"

task = """

Ein Jahr ist ein Schaltjahr, wenn es durch 4 aber nicht durch 100 teilbar ist
oder aber, wenn es durch 400 teilbar ist. Ergänzen Sie den folgenden Quelltext
so, dass die Methode genau dann den Wert true liefert, wenn Jahr j ein
Schaltjahr ist.

```java
class Schaltjahr {
    public static void main(String[] args) {
        int jahr = Integer.parseInt(args[0]);
        System.out.println(schaltjahr(jahr));
    }
    public %s %s schaltjahr (int j) {
        %s (%s %s %s);
    }
}
```

""" % (gap1, gap2, gap3, gap4, gap5, gap6)


feedback = """
Der vollständige Code:

```java_copy
class Schaltjahr {
    public static void main(String[] args) {
        int jahr = Integer.parseInt(args[0]);
        System.out.println(schaltjahr(jahr));
    }
    public static boolean schaltjahr (int j) {
        return (j % 4 == 0 && j % 100 != 0 || j % 400 == 0);
    }
}
```
"""
