Com funciona aquest cervell per a l'IA?
Observació en Vector: L'IA no rep un diccionari; rep una llista de 16 números. Els 5 primers són els daus, els següents 10 són el full d'anotacions i l'últim és el número de tirada.

Espai d'accions combinat:

Si l'IA tria un número de 0 a 31, el programa ho interpreta com "quins daus mantenir" (usant binari, per exemple, el 31 és 11111, tirar-ho tot).

Si tria de 32 a 41, el programa entén que vol anotar en una de les 10 caselles del full.

La Recompensa (Reward):

Li donem punts positius quan anota.

Li donem un -10 si intenta anotar en una casella que ja està plena (així aprendrà a no repetir).

Al final de la partida (10 torns), li donem tota la suma de punts com a gran premi.