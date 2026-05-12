import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random

class GeneralaEnv(gym.Env):
    def __init__(self):
        super(GeneralaEnv, self).__init__()

        # --- DEFINICIÓ DE L'ESPAI D'ACCIONS ---
        # Accions: 32 combinacions de mantenir/tirar daus (2^5) 
        # + 10 accions per triar on anotar al final del torn.
        # Per simplificar, farem un espai discret.
        self.action_space = spaces.Discrete(32 + 10)

        # --- DEFINICIÓ DE L'ESPAI D'OBSERVACIÓ (ESTAT) ---
        # 5 daus (1-6) + 10 caselles del full (-1 si buit, o punts) + tirada actual (1-3)
        self.observation_space = spaces.Box(
            low=-1, high=211, shape=(16,), dtype=np.int32
        )

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.daus = [0, 0, 0, 0, 0]
        self.full = {k: -1 for k in ["1", "2", "3", "4", "5", "6", "E", "F", "P", "G"]}
        self.tirada_actual = 0
        self.torn_actual = 1
        self.es_servit = False
        
        # Primera tirada obligatòria
        self._executar_tirada([True, True, True, True, True])
        
        return self._get_obs(), {}

    def _get_obs(self):
        # Convertim el diccionari i llistes en un vector numèric per a l'IA
        full_vector = [val for val in self.full.values()]
        return np.array(self.daus + full_vector + [self.tirada_actual], dtype=np.int32)

    def _executar_tirada(self, tirs):
        self.es_servit = all(tirs)
        for i in range(5):
            if tirs[i]:
                self.daus[i] = random.randint(1, 6)
        self.tirada_actual += 1

    def step(self, action):
        reward = 0
        terminated = False
        truncated = False

        punts_tot = self.calcular_punts_lògica(self.daus, self.es_servit)
        max_punts_abans = max(punts_tot.values())

        # --- CAS 1: L'agent vol tirar els daus i encara pot ---
        if action < 32 and self.tirada_actual < 3:
            tirs = [bool(int(x)) for x in bin(action)[2:].zfill(5)]
            self._executar_tirada(tirs)
            
            punts_despres = self.calcular_punts_lògica(self.daus, self.es_servit)
            max_punts_despres = max(punts_despres.values())
            
            # Recompensa per millorar la jugada o càstig per empitjorar-la
            reward = (max_punts_despres - max_punts_abans) - 0.1

            return self._get_obs(), reward, terminated, truncated, {}

        # --- CAS 2: L'agent vol tirar però JA HA TIRAT 3 COPS (ERROR D'ESTRATEGIA) ---
        elif action < 32 and self.tirada_actual >= 3:
            reward = -100  # Càstig sever

            # NO avancem el torn, NO tirem daus. 
            # L'IA es queda en el mateix estat fins que triï una acció d'anotar.
            return self._get_obs(), reward, terminated, truncated, {}

        # --- CAS 3: L'agent decideix anotar (action >= 32) ---
        else:
            idx_anotar = (action % 32)
            idx_anotar = min(idx_anotar, 9) 
            
            claus = list(self.full.keys())
            casella_triada = claus[idx_anotar]

            if self.full[casella_triada] == -1: # Casella lliure
                punts = punts_tot[casella_triada]
                self.full[casella_triada] = punts
                
                if casella_triada in ["E", "F", "P", "G"]:
                    reward = punts if punts > 0 else -100 # Millor càstig fix que -punts (que seria 0)
                else:
                    reward = max(-0.1, punts - 2 * int(casella_triada))
            
            else: # CASELLA OCUPADA: L'IA ha fallat
                reward = -100 
                # Busquem la primera casella lliure per "cremar-la" amb un 0 i avançar el joc
                for c in claus:
                    if self.full[c] == -1:
                        self.full[c] = 0
                        break # Només en cremem una

            # --- LÒGICA D'AVANÇAR EL TORN (COMÚ PER A TOTA ANOTACIÓ) ---
            self.torn_actual += 1
            if self.torn_actual > 10:
                terminated = True
                reward += sum(v for v in self.full.values() if v > 0)
            else:
                self.tirada_actual = 0
                self._executar_tirada([True, True, True, True, True])
            
            
            return self._get_obs(), reward, terminated, truncated, {}

    def calcular_punts_lògica(self, resultats, servit):
        valors = [0] * 6
        for r in resultats: valors[r-1] += 1
        p = {str(i+1): (i+1)*v for i, v in enumerate(valors)}
        p.update({"E": 0, "F": 0, "P": 0, "G": 0})
        
        hi_ha_trio = 3 in valors
        hi_ha_parella = 2 in valors
        
        if 5 in valors: p["G"] = 100 + (valors.index(5)+1) + (100 * servit)
        elif 4 in valors: p["P"] = 80 + (valors.index(4)+1) + (10 * servit)
        
        if hi_ha_trio and hi_ha_parella: p["F"] = 70 + (5 * servit)
        if valors in ([1,1,1,1,1,0], [0,1,1,1,1,1], [1,0,1,1,1,1]): p["E"] = 60 + (5 * servit)
        
        return p