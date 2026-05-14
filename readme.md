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
_________________

PARÀMETRES DE L'ENTRENAMENT

1. Rollout (Rendiment en el joc)
ep_len_mean (27.1): Indica quants steps (accions) fa l'IA per acabar una partida de 10 torns.

Com que el màxim teòric són 30 (3 accions per torn) i el mínim són 10 (anotar directament), un 27.1 vol dir que l'IA està aprofitant gairebé totes les tirades. No s'està rendint ràpidament, sinó que busca millorar la mà.

ep_rew_mean (65.7): És la mitjana de recompensa per partida.

Encara és baixa. Tenint en compte que una sola Generala ja pot donar més de 200 punts, aquest 65.7 indica que l'IA encara crema moltes caselles o rep moltes penalitzacions de -50 per triar caselles ocupades. Està en la fase de "deixar de castigar-se a si mateixa".

2. Train (Salut de l'aprenentatge)
entropy_loss (-2.71): Mesura el grau de "caos" o curiositat.

Si aquest número és alt (com ara), vol dir que l'IA encara està experimentant amb accions aleatòries. A mesura que aprengui, aquest número anirà pujant cap a 0 (es tornarà més determinista).

explained_variance (0.036): Aquest és el punt més crític ara mateix.

Mesura si l'IA entén per què rep els punts. Un valor proper a 0 (com el teu) vol dir que l'IA encara no sap predir si la seva jugada serà bona o dolenta. És normal en aquesta fase, però hauria de pujar cap a 0.5 - 0.9 a mesura que avanci l'entrenament.

value_loss (6.96e+03): És una pèrdua molt alta.

Això passa perquè has posat recompenses molt grans (els bonus de +50 i el sumatori final). La xarxa neuronal està rebent "impactes" molt forts de reward i està intentant ajustar-se. No t'espantis, anirà baixant.

3. Time (Eficiència)
fps (417): L'entorn és molt ràpid! Està processant 417 accions per segon. Això és genial, vol dir que pots deixar-la entrenant un milió de passos i ho farà en un temps raonable.