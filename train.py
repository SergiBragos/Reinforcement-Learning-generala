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
    model = PPO.load(model_path, env=env)
else:
    print("No s'ha trobat cap model previ. Creant un de nou...")
    # Creem un model des de zero
    model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0003)

print("Iniciant l'entrenament... Prem Ctrl+C per aturar-lo.")

# 3. Entrenem l'agent
# 100.000 timesteps és un bon inici, però per a la Generala 
# podria necessitar-ne fins a 500.000 per ser realment bo.
timesteps = 100000

model.learn(total_timesteps=timesteps)

# 4. Guardem el model entrenat
model.save("ppo_generala_model")
print("Model guardat correctament!")

# 5. Prova ràpida: veure com juga una partida l'IA
obs, _ = env.reset()
done = False
while not done:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    print(env.daus)
    # Aquí podries afegir un print(env.daus) per "veure'l" jugar
print(reward)