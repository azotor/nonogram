# Nonogram
Nonogram w Pythonie. Program używa biblioteki `Tkinter`.

## Pliki z noogramami
Pliki z nonogramamy znajdują się w katalogu `nonograms`. Posiadają rozszerzenie `*.nono`.\
W pliku z nonogramem znajdują się w kolejnych wierszach liczby całkowite oddzielone znakami pojedynczych spacji.\
W pierwszym wierszu znajdują się zwsze 2 liczby całkowite $N$ i $M$ określające kolejno ilość kolumn oraz ilość wierszy w nonogramie.\
W kolejnych $N$ wierszach znajdują się grupy liczb całkowitych dla kolejnych kolumn nonogramu, a kolejne $M$ wierszy określa grupy liczb całkowitych dla kolejnych wierszy nonogramu.

![Reprezentacja pliku](images/nonofile.png)

Grupy liczb w każdtym $N$-tym wierszu czytane od lewej do prawej umieszczane są nad diagramem od góry do dołu, a liczby w każdym $M$-tym wierszu umieszczane są po lewej stronie diagramu od lewej storny.

![Reprezentacja pliku](images/nonofile2.png)
