***************************
Bemessung von Holzbauteilen
***************************

Begriffe
########

* Einwirkung **F** 

    * als Einwirkung werden Kräfte (auch Lasten genannt) und aufgezwungene Verformung (durch Temperatur, Setzung, etc...) bezeichnet
    * Kräfte werden auch als direkte Einwirkung und aufgezwungene Verformung (Temperatur, Setzung ...) als indirekte Einwirkung bezeichnet

* Auswirkung der Einwirkung **E**

    * logischerweise induziert die Einwirkung eine Auswirkung, die mit **E** bezeichnet wird.
    * Die Auswirkungen können als 

        * Beanspruchungen von Bauteilen in Form von Schnittkräften, Momenten und Spannungen auftreten
        * Reaktion des Gesamttragwerks (Durchbiegung) auftreten

Charakteristische Werte und Bemessungwerte
##########################################

Charakteristische Werte :math:`F_k` und Bemessungswerte :math:`F_d` für Einwirkungen
************************************************************************************

* Charakteristische Werte :math:`F_k`

    * werden in Lastnormen festgelegt

        * bei ständiger Einwirkung wird das Symbol :math:`G_k` verwendet. 
  
            * Ständige Einwirkungen sind in der Regel Eigenlasten (Gewichtskraft), daher macht es Sinn, :math:`G` zu verwenden
            * in manchen Fällen werden obere und untere Grenzen der ständigen Einwirkung durch :math:`G_{k,inf}` und :math:`G_{k,sup}` bezeichnet
  
        * bei veränderlichen Einwirkungen wird das Symbol :math:`Q_k` verwendet

            * Bsp: charakteristische Schnee, Wind und Nutzlasten
            * da die Einwirkungen veränderlich sind, muss die Einwirkungsdauer berücksichtigt werden.
            * auch hier kann es untere und obere Grenzwerte geben, die mit :math:`G_{k,sup}` und :math:`G_{k,inf}$` berücksichtigt werden.

        * außergewöhnliche Einwirkungen :math:`A_k`

* Aus den charakteristischen Werten der **veränderlichen** Einwirkungen (:math:`Q_k`) ergeben sich die **repräsentativen Werte von veränderlichen Einwirkungen** :math:`Q_{rep}`, indem die einzelnen :math:`Q_{k}` mit entsprchenden Koeffizienten :math:`\psi` gewichtet werden.

    * Die Koeffizienten :math:`\psi_i` hängen von dem Kombinationsfall ab
    * :math:`\psi_0 * Q_k`  --> Kombinationswert
    * :math:`\psi_1 * Q_k`  --> Häufiger Wert
    * :math:`\psi_2 * Q_k`  --> Quasi-ständiger Wert

* Nicht-veränderliche Lasten erhalten einen Faktor :math:`\psi_G`, der häufig 1.0 ist.

.. todo::
    It is not really clear, what "Kombinationswert", "Häufiger Wert" and "Quasi-ständiger Wert" means
    An example would be great


* Bemessungswerte der Einwirkung :math:`F_d`

    * Für den Bemessungswert :math:`F_d` wird zum representativen Wert :math:`F_{rep}` noch ein Teilsicherheitsbeiwert :math:`\gamma_F` verwendet.

    .. math::

        F_d = \gamma_F \cdot F_{rep} = \gamma_F \cdot \psi F_k


Charakteristische Werte :math:`X_k` und Bemessungswerte :math:`X_d` für Baustoffeigenschaften
*********************************************************************************************

Auch hier wird wieder mit Beiwerten gearbeitet:

* :math:`X_d = \frac{\eta}{\gamma_M} X_k`

* :math:`\gamma_M` steht für Teilsicherheitsbeiwert für das **M** aterial
* :math:`\eta` modeliert die Umrechnung von Probeneigenschaften und maßgebenden Eigenscahften im Bauteil
* Es stellt sich noch die Frage, welcher Wert für :math:`X_k` angenommen wird

    * in den meisten Fällen wird der das 5% Quantil der Verteilung der jeweiligen Größe angesetzt, also der Wert, der über die inneren 95% der Verteilungen gemittelt wurde.

    .. math::

        X_d = \frac{\eta}{\gamma_M} X_{0.05 }
  
.. todo::
    Meaning of :math:`\eta` is not really clear yet


Referenzen
**********

* Schneider, Bautabellen für Ingenieure


