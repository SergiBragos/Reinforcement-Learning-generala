#train.py
from stable_baselines3 import PPO
from generala_env import GeneralaEnv  # Importem la teva classe
import os

# 1. Creem l'entorn
env = GeneralaEnv()
model_path = "ppo_generala_model.zip"


# Comprovem si el fitxer existeix
if os.path.exists(model_path):
    print("Model trobat. Carregant per continuar entrenant...")
    # Utilitzem custom_objects per sobreescriure l'entropia i el n_steps del fitxer guardat
    custom_params = {
        "ent_coef": 0.1,
        "n_steps": 8192,
        "learning_rate": 0.0005,
        "batch_size": 512
    }
    model = PPO.load(model_path, env=env, custom_objects=custom_params)

else:
    print("No s'ha trobat cap model previ. Creant-ne un de nou...")
    # Creem un model des de zero
    model = PPO(
        "MlpPolicy", 
        env, 
        verbose=1, 
        learning_rate=0.001, 
        batch_size=512,
        n_steps=8192,
        ent_coef=0.1,
        policy_kwargs=dict(net_arch=[256, 256, 256]) # Xarxa més profunda
    )

print("Iniciant l'entrenament... Prem Ctrl+C per aturar-lo.")

# 3. Entrenem l'agent
timesteps = 1000000
model.learn(total_timesteps=timesteps, tb_log_name="PPO_run")

# 4. Guardem el model entrenat
model.save("ppo_generala_model")
print("Model guardat correctament!")

# 5. Prova ràpida: veure com juga una partida l'IA
obs, _ = env.reset()

# Actualització a la nova nomenclatura de Gymnasium
terminated = False
truncated = False

print("\n--- INICI DE LA PARTIDA DE PROVA ---")
while not (terminated or truncated):
    # Fem que el model crei una resposta segons l'estat que s'ha trobat
    action, _states = model.predict(obs, deterministic=True)

    # Abans d'executar l'acció, mirem què vol fer
    if action < 32:
        # Convertim l'acció a format binari per veure quins daus selecciona
        seleccio_binaria = bin(action)[2:].zfill(5)
        print(f"🎲 Daus actuals: {env.daus} | L'IA decideix TORNAR A TIRAR (Selecció: {seleccio_binaria} Tirada: {env.tirada_actual})")
    else:
        # L'IA decideix anotar
        categories = ["1", "2", "3", "4", "5", "6", "E", "F", "P", "G"]
        # RETOC CLAU: Ara utilitzem la mateixa lògica que a l'entorn
        idx_categoria = min(action - 32, 9) 
        categoria = categories[idx_categoria]
        print(f"📝 Daus actuals: {env.daus} | L'IA decideix ANOTAR a la casella: [{categoria}] Tirada: {env.tirada_actual}")

    # Executem l'acció
    obs, reward, terminated, truncated, info = env.step(action)
    
    # Mostrem la recompensa immediata
    if reward >= 0:
        print(f"   --> Recompensa rebuda: +{reward}")
    elif reward < 0:
        print(f"   --> Penalització: {reward}")

print("\n--- FINAL DE LA PARTIDA ---")
print(f"Full final de punts: {env.full}")
print(f"Puntuació total: {sum(v for v in env.full.values() if v > 0)}")