# STATES OF THE WORLD (A:21)

Se va crea un crawler ce va intra pe pagina de Wikipedia cu tarile lumii si va retine intr-o
baza de date informatii precum: nume, nume capitala, populatie, densitate, suprafata,
vecini, limba vorbita, fusul orar, tip de regim politic (democratic, monarhie, etc).

De asemenea, se va construi un API peste baza de date, care va avea multiple rute,
apelate cu metoda GET. Aceste apeluri vor returna topul primelor 10 tari cu: cea mai
mare populatie, cea mai mare densitate.

### Exemplu
Vreau topul primelor 10 tari dupa populatie - apelez GET pe ruta
/top-10-tari-populatie si voi primi un raspuns, pe care il voi afisa pe ecran.
De asemenea, ar trebui sa se poata cere si alte informatii (de genul - toate tarile de pe
GMT+2, sau toate tarile în care se vorbeste ENGLEZA, sau toate tarile care se bazeaza
pe un anumit tip de regim politic), la fel sub forma de rute.