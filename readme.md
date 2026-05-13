Agent de Reinforcement Learning enfocat a la presa de decisions en el joc de la generala.

Entrenat de moment amb 2.000.000 d'iteracions.


___________

Lògica del Sistema de Recompenses (Reward Function)

1. Exploració i Tirada de Daus
Millora de la mà: Cada vegada que l'IA tira els daus i aconsegueix una combinació millor que la que tenia (en potència), rep una petita recompensa calculada com la meitat de la millora dels punts potencials.
Cost de decisió: Cada tirada té un cost de -0.1. Això evita que l'agent es quedi tirant indefinidament i l'obliga a valorar si realment val la pena arriscar per buscar una jugada millor.
(pts_act - pts_ant)/2 - 0.1


2. Càstig per tirada il·legal: Si l'IA intenta tirar els daus quan ja ha esgotat els 3 intents permesos, rep un càstig sever de -100.


3. Gestió d'Errors i Caselles
Error d'ocupació: Intentar anotar en una casella que ja té punts es penalitza amb -50. Aquesta és la penalització més alta en el joc normal per garantir que l'IA aprengui ràpidament les regles bàsiques de la llibreta de punts.

Cremar jocs grans: Si l'agent decideix anotar un 0 en una casella de joc (Escala, Full, Pòquer o Generala), rep un reward de -20. Això li ensenya que "perdre" una d'aquestes caselles és un error estratègic greu.

4. Puntuació de Números (1 al 6)
Per a les caselles de números, utilitzem una fórmula de normalització: 6 * (N - 2) - V.

On:
N és el nombre de daus iguals.
V és el valor del dau (de l'1 al 6).

Aquesta fórmula és la clau de l'estratègia:
-Tenir 3 daus o més dóna un reward positiu.
-Tenir 2 daus dóna un reward lleugerament negatiu (cost d'oportunitat).
-Tenir 0 o 1 dau castiga l'agent, però el càstig és més lleuger en els números baixos (com l'1) que en els alts (com el 6). Això ensenya a l'IA a fer servir els "1" com a paperera quan la jugada és dolenta.


4. Puntuació de Jocs (E, F, P, G)
Quan l'IA anota correctament un joc, la recompensa és el valor total dels punts obtinguts més un Bonus de Coherència:

Generala: Punts (fins a 206) + Bonus de 50.

Pòquer: Punts (fins a 96) + Bonus de 40.

Full: Punts (70 o 75) + Bonus de 30.

Escala: Punts (60 o 65) + Bonus de 20.

L'objectiu d'aquests bonus és que l'IA senti una "satisfacció" immediata molt forta en completar les jugades grans, accelerant l'aprenentatge d'aquestes combinacions complexes.


5. Objectiu Final (Long-term Reward)
Al final del torn 10 (quan s'acaba la partida), l'IA rep un reward final equivalent a la suma total de tots els punts del seu full. Això serveix per connectar totes les decisions individuals amb l'objectiu definitiu: guanyar la partida amb la màxima puntuació possible.