import gymnasium as gym
from stable_baselines3 import PPO
from generala_env import GeneralaEnv  # Assegura't que el fitxer es diu així
import numpy as np
import random

def traduir_accio_daus(action):
    """Converteix l'acció 0-31 en un text llegible de quins daus es guarden."""
    tirs = [bool(int(x)) for x in bin(action)[2:].zfill(5)]
    daus_text = ["TIRAR" if t else "GUARDAR" for t in tirs]
    return daus_text

def simular_torn(model_path, daus_inicials=None):
    # 1. Carregar l'entorn i el model
    env = GeneralaEnv()
    model = PPO.load(model_path)
    
    obs, _ = env.reset()
    
    # 2. Forçar una situació inicial (si es vol provar quelcom específic)
    if daus_inicials:
        env.daus = daus_inicials
        env._actualitzar_estat_daus()
        obs = env._get_obs()

    print("--- INICI DEL SIMULADOR DE DECISIONS ---")
    print(f"Daus inicials: {env.daus}")
    print(f"Estat del full: {env.full}")
    print("-" * 40)

    finalitzat = False
    
    while not finalitzat:
        # L'agent prediu l'acció (deterministic=True per evitar aleatorietat)
        action, _states = model.predict(obs, deterministic=True)
        
        # --- LÒGICA DE TIRAR (Acció 0-31) ---
        if action < 32:
            instruccio = traduir_accio_daus(action)
            print(f"➤ L'agent decideix TIRAR (Torn {env.tirada_actual}/3)")
            print(f"   Acció {action}: {instruccio}")
            
            obs, reward, terminated, truncated, info = env.step(action)
            print(f"   Nous daus: {env.daus} (Recompensa: {reward:.2f})")

        # --- LÒGICA D'ANOTAR (Acció 32-41) ---
        else:
            claus = list(env.full.keys())
            casella = claus[action - 32]
            print(f"🏁 L'agent decideix ANOTAR a la casella: '{casella}'")
            
            obs, reward, terminated, truncated, info = env.step(action)
            print(f"   Punts obtinguts: {env.full[casella]}")
            print(f"   Recompensa de l'acció: {reward:.2f}")
            finalitzat = True

        print("-" * 20)

    print("--- FI DEL TORN ---")

if __name__ == "__main__":
    # Posa aquí el camí al teu fitxer .zip del model entrenat
    PATH_MODEL = "ppo_generala_model.zip" 
    
    #situacio_especifica = [1,1,1,1,1]
    
    try:
        #simular_torn(PATH_MODEL, daus_inicials=situacio_especifica)
        simular_torn(PATH_MODEL)
    except FileNotFoundError:
        print(f"Error: No s'ha trobat el model a {PATH_MODEL}. Entrena l'agent primer!")