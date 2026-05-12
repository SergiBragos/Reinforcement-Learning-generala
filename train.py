from stable_baselines3 import PPO
from generala_env import GeneralaEnv  # Importem la teva classe
import os

# 1. Creem l'entorn
env = GeneralaEnv()
model_path = "ppo_generala_model.zip"

# Comprovem si el fitxer existeix
if os.path.exists(model_path):
    print("Model trobat. Carregant per continuar entrenant...")
    # Carreguem el model existent i el vinculem al nou entorn
    model = PPO.load(model_path, env=env, learning_rate=0.0005, ent_coef=0.1)
else:
    print("No s'ha trobat cap model previ. Creant-ne un de nou...")
    # Creem un model des de zero
    model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0005,ent_coef=0.15)

print("Iniciant l'entrenament... Prem Ctrl+C per aturar-lo.")

# 3. Entrenem l'agent
# 100.000 timesteps és un bon inici, però per a la Generala 
# podria necessitar-ne fins a 500.000 per ser realment bo.
timesteps = 1

model.learn(total_timesteps=timesteps)

# 4. Guardem el model entrenat
model.save("ppo_generala_model")
print("Model guardat correctament!")

# 5. Prova ràpida: veure com juga una partida l'IA
obs, _ = env.reset()
done = False
while not done:
    #Fem que el model crei una resposta segons l'estat que s'ha trobat
    action, _states = model.predict(obs, deterministic=True)

    # Abans d'executar l'acció, mirem què vol fer
    if action < 32:
        # Convertim l'acció a format binari per veure quins daus selecciona
        seleccio_binaria = bin(action)[2:].zfill(5)
        print(f"🎲 Daus actuals: {env.daus} | L'IA decideix TORNAR A TIRAR (Selecció: {seleccio_binaria} Tirada: {env.tirada_actual})")
    else:
        # L'IA decideix anotar
        categories = ["1", "2", "3", "4", "5", "6", "E", "F", "P", "G"]
        categoria = categories[action % 10]
        print(f"📝 Daus actuals: {env.daus} | L'IA decideix ANOTAR a la casella: [{categoria}] Tirada: {env.tirada_actual}")

    # Executem l'acció
    obs, reward, done, truncated, info = env.step(action)
    
    # Mostrem la recompensa immediata
    if reward >= 0:
        print(f"Recompensa rebuda: +{reward}")
    elif reward < 0:
        print(f"Penalització: {reward}")

print("\n--- FINAL DE LA PARTIDA ---")
print(f"Full final de punts: {env.full}")
print(f"Puntuació total: {sum(v for v in env.full.values() if v > 0)}")