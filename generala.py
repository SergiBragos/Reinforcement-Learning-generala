import random
import time

def tirada(resultats, tirs):
    servit = all(tirs)
    for i in range(len(tirs)):
        if tirs[i]:
            resultats[i] = random.randint(1, 6)
    return resultats, servit

def calcular_punts(resultats, servit):
    valors = [0] * 6
    for r in resultats:
        valors[r-1] += 1
    
    posibilitats = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "E": 0, "F": 0, "P": 0, "G": 0}
    hi_ha_parella, hi_ha_trio = False, False

    for i, quantitat in enumerate(valors):
        cara = i + 1
        posibilitats[str(cara)] = cara * quantitat
        if quantitat == 5:
            posibilitats["G"] = 100 + cara + (100 * servit)
        elif quantitat == 4:
            posibilitats["P"] = 80 + cara + (10 * servit)
        elif quantitat == 3:
            hi_ha_trio = True
        elif quantitat == 2:
            hi_ha_parella = True

    if hi_ha_trio and hi_ha_parella:
        posibilitats["F"] = 70 + (5 * servit)
    if valors in ([1,1,1,1,1,0], [0,1,1,1,1,1], [1,0,1,1,1,1]):
        posibilitats["E"] = 60 + (5 * servit)

    return posibilitats

# --- INICIALITZACIÓ DEL JOC ---

# El "Full d'anotacions" comença buit (None indica casella lliure)
taula_punts = {k: None for k in ["1", "2", "3", "4", "5", "6", "E", "F", "P", "G"]}

# El joc de la Generala dura exactament 10 torns (un per cada casella)
torns_totals = 10

for torn in range(1, torns_totals + 1):
    print(f"\n" + "█"*45)
    print(f" TORN {torn} de {torns_totals}")
    print("█"*45)
    
    # Mostrar el full d'anotacions actual
    print("\n--- EL TEU FULL D'ANOTACIONS ---")
    for cat, pts in taula_punts.items():
        estat = pts if pts is not None else "lliure"
        print(f"[{cat}]: {estat}", end="  |  ")
    print("\n" + "-"*45)

    daus = [0, 0, 0, 0, 0]
    es_servit = False
    
    # Fase de tirades (fins a 3)
    for tir in range(1, 4):
        if tir == 1:
            daus, es_servit = tirada(daus, [True]*5)
        else:
            print(f"\nDaus: {daus} (Tirada {tir}/3)")
            entrada = input("Quines posicions tires de nou? (ex: 1 2 5, o buit per parar): ").strip()
            if not entrada: break
            
            nous_tirs = [False] * 5
            try:
                seleccio = [int(x) - 1 for x in entrada.split() if 1 <= int(x) <= 5]
                for idx in seleccio: nous_tirs[idx] = True
                daus, es_servit = tirada(daus, nous_tirs)
            except ValueError:
                print("⚠️ Entrada no vàlida."); continue

    # Fase d'anotació
    possibles = calcular_punts(daus, es_servit)
    print(f"\n✅ FINAL DEL TORN. Daus: {daus}")
    print("Jugades possibles per aquests daus:")
    for k, v in possibles.items():
        if taula_punts[k] is None: # Només mostrem les que encara estan lliures
            print(f" - {k}: {v} punts")

    while True:
        triat = input("\nA quina casella vols apuntar el resultat? ").upper().strip()
        
        if triat in taula_punts:
            if taula_punts[triat] is None:
                taula_punts[triat] = possibles[triat]
                print(f"✔️ Apuntat {possibles[triat]} a la casella {triat}.")
                break
            else:
                print("❌ Aquesta casella ja està ocupada. Tria'n una altra.")
        else:
            print("⚠️ Casella no vàlida (usa 1-6, E, F, P o G).")

# --- FINAL DEL JOC ---
total = sum(v for v in taula_punts.values() if v is not None)
print("\n" + "═"*45)
print("🏆 JOC FINALITZAT!")
print(f"PUNTUACIÓ TOTAL: {total}")
print("Full final:", taula_punts)
print("═"*45)