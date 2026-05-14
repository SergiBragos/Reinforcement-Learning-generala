import gymnasium as gym
from stable_baselines3 import PPO
from generala_env import GeneralaEnv
import os

def formatar_full(full):
    """Retorna una cadena visual de l'estat del full d'anotacions."""
    items = []
    for k, v in full.items():
        val = v if v != -1 else "-"
        items.append(f"{k}:{val}")
    return " | ".join(items)

def jugar_partida(model_path):
    if not os.path.exists(model_path):
        print(f"❌ Error: No s'ha trobat el model a {model_path}")
        return

    # 1. Carregar entorn i model una sola vegada
    env = GeneralaEnv()
    model = PPO.load(model_path)
    
    obs, _ = env.reset()
    terminated = False
    truncated = False
    
    print("="*60)
    print("🎲 INICI DE LA PARTIDA DE GENERALA 🎲")
    print("="*60)

    num_torn = 1
    
    while not (terminated or truncated):
        print(f"\n🔹 TORN {num_torn}/10")
        final_del_torn = False
        
        while not final_del_torn:
            # Predicció de l'agent
            action, _states = model.predict(obs, deterministic=True)
            
            # --- DECISIÓ: TIRAR ---
            if action < 32:
                # Traduïm quins daus es queden
                # Si el bit és 1, es tira. Si és 0, es guarda.
                bits = [int(x) for x in bin(action)[2:].zfill(5)]
                decisio_text = []
                for i in range(5):
                    status = "🔄" if bits[i] == 1 else "✅"
                    decisio_text.append(f"D{i+1}:{env.daus[i]}{status}")
                
                print(f"  Tirada {env.tirada_actual}/3 | Daus: {env.daus}")
                print(f"  ↳ Decisió: {' '.join(decisio_text)} (Tirar els 🔄)")
                
                obs, reward, terminated, truncated, info = env.step(action)

            # --- DECISIÓ: ANOTAR ---
            else:
                claus = list(env.full.keys())
                casella = claus[action - 32]
                
                # Guardem els daus abans de l'anotació per al log
                daus_finals = env.daus.copy()
                
                obs, reward, terminated, truncated, info = env.step(action)
                
                punts = env.full[casella]
                print(f"  Tirada FINAL | Daus: {daus_finals}")
                print(f"  🎯 ANOTACIÓ: L'agent posa {punts} punts a la casella [{casella}]")
                print(f"  📋 Full actual: {formatar_full(env.full)}")
                print("-" * 40)
                
                final_del_torn = True
                num_torn += 1

    # --- FINAL DE PARTIDA ---
    print("\n" + "="*60)
    print("🏁 FINAL DE LA PARTIDA")
    puntuacio_total = sum(v for v in env.full.values() if v > 0)
    print(f"📊 PUNTUACIÓ FINAL: {puntuacio_total} PUNTS")
    print(f"📋 Full final: {formatar_full(env.full)}")
    print("="*60)

if __name__ == "__main__":
    PATH_MODEL = "ppo_generala_model.zip" 
    jugar_partida(PATH_MODEL)