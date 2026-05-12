Com funciona aquest cervell per a l'IA?
Observació en Vector: L'IA no rep un diccionari; rep una llista de 16 números. Els 5 primers són els daus, els següents 10 són el full d'anotacions i l'últim és el número de tirada.

Espai d'accions combinat:

Si l'IA tria un número de 0 a 31, el programa ho interpreta com "quins daus mantenir" (usant binari, per exemple, el 31 és 11111, tirar-ho tot).

Si tria de 32 a 41, el programa entén que vol anotar en una de les 10 caselles del full.

La Recompensa (Reward):

Li donem punts positius quan anota.

Li donem un -10 si intenta anotar en una casella que ja està plena (així aprendrà a no repetir).

Al final de la partida (10 torns), li donem tota la suma de punts com a gran premi.


RUTINA D'ENTRENAMENT

1. Secció rollout/ (El rendiment del joc)
Això ens diu com li va a l'IA mentre juga les partides de pràctica.

ep_len_mean: És la durada mitjana d'una partida (episodi). Com que la Generala té 10 torns i cada torn té fins a 3 tirades, un valor de 23 és molt normal (indica que fa servir unes 2-3 tirades per torn abans d'anotar).

ep_rew_mean: Aquest és el valor clau. És la puntuació mitjana que treu per partida.

Si és negatiu, vol dir que l'IA encara està cometent molts errors "tontos", es menja els càstigs de punts negatius.

L'objectiu: Veure com aquest número puja i es torna positiu i cada cop més alt a mesura que avança l'entrenament.

2. Secció train/ (La part matemàtica)
Això ens diu com s'està ajustant el "cervell" de l'IA.

entropy_loss: Mesura la curiositat o desordre.

Si és un número "gran" (en valor absolut), l'IA està explorant moltes accions diferents (està provant coses).

A mesura que aprengui, aquest número anirà baixant perquè l'IA estarà més segura de què ha de fer i deixarà d'actuar a l'atzar.

explained_variance: Diu si l'IA entén per què rep recompenses.

A prop de 0: No té ni idea de per què guanya o perd punts (està confosa).

A prop de 1: Entén perfectament el valor de cada jugada. Ara mateix està al principi de tot.

loss: L'error total de la xarxa neuronal. Normalment baixarà i després s'estabilitzarà.

3. Secció time/ (La velocitat)
fps: "Frames per second". La teva IA està jugant i aprenent a una velocitat de 610 accions per segon. És una velocitat molt bona per a un ordinador domèstic.

total_timesteps: Quantes interaccions totals ha fet amb el joc des que has començat.