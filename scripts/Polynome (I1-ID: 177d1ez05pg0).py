meta = {
    'author': 'Jan Maximilian Michal',
    'title': 'Polynome (I1-ID: 177d1ez05pg0)',
    'type': 'gap',
    'points': 0.0,
}

task = """
Vervollständigen Sie die folgende Klasse:

```java
public class Polynom {
    // diese Klasse dient dazu, Polynome (also Funktionen der Gestalt
    // a(x) = a0 + a1*x + a2*x^2 + ... + ad*x^d) als statische
    // Java-Funktionen bereitzustellen

    /* Argumente: double-Feld (fuer Koeffizienten a0, a1, .., ad) und Zahl x
       Ergebniswert: Wert des Polynoms an der Stelle x (Typ double)*/
    public static double p([gap(0.5P)]double[] a[/gap], double x) {
        // Sonderfall: das Nullpolynom
        int d = [gap(0.5P)]a.length - 1[/gap]; // Polynomgrad
        if ( d == -1)
            return 0;
        // ansonsten: berechne gesuchten Wert nach dem Horner-Schema:
        double v = 0;
        for (int i = d; i [gap(0.5P)]>=[/gap] 0; i--) {
            v [gap(0.5P)]*=[/gap] x;
            v += a[i];
        }
        return v;
    }

    public static void main(String[] args) {     /* Unit-Test */
        [gap(0.5P)]double[][/gap] a = {2,1,-1,3};
        System.out.println(p([gap(0.5P)]a[/gap], 10));
    }
}
```

Welcher Wert wird bei dem Unit-Test ausgegeben? [gap(1P)]2912[/gap]
"""

feedback = """
Der vollständige Quelltext

```java
public class Polynom {
    // diese Klasse dient dazu, Polynome (also Funktionen der Gestalt
    // a(x) = a0 + a1*x + a2*x^2 + ... + ad*x^d) als statische
    // Java-Funktionen bereitzustellen

    /* Argumente: double-Feld (fuer Koeffizienten a0, a1, .., ad) und Zahl x
       Ergebniswert: Wert des Polynoms an der Stelle x (Typ double)*/
    public static double p(double[] a, double x) {
        // Sonderfall: das Nullpolynom
        int d = a.length - 1; // Polynomgrad
        if ( d == -1)
            return 0;
        // ansonsten: berechne gesuchten Wert nach dem Horner-Schema:
        double v = 0;
        for (int i = d; i >= 0; i--) {
            v *= x;
            v += a[i];
        }
        return v;
    }

    public static void main(String[] args) {     /* Unit-Test */
        double[] a = {2,1,-1,3};
        System.out.println(p(a, 10));
    }
}
```

 """
