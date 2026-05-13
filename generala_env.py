#generala_env.py

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random

class GeneralaEnv(gym.Env):
    def __init__(self):
        super(GeneralaEnv, self).__init__()

        # --- DEFINICIÓ DE L'ESPAI D'ACCIONS ---
        # 32 (daus) + 10 (caselles) = 42
        self.action_space = spaces.Discrete(42)

        # --- DEFINICIÓ DE L'ESPAI D'OBSERVACIÓ (ESTAT) ---
        # 5 (daus) + 10 (full) + 6 (jocs bool) + 1 (tirada) = 22 variables
        self.observation_space = spaces.Box(
            low=-1, high=500, shape=(22,), dtype=np.int32
        )

        self.reset()

    def _actualitzar_estat_daus(self):
        """Calcula quantes vegades surt cada número i actualitza els jocs possibles."""
        self.valors = [0] * 6
        for r in self.daus:
            if r > 0:  # Evitem els zeros de la inicialització prèvia a la tirada
                self.valors[r-1] += 1
        
        # Booleans per a la xarxa neuronal (si es compleix la condició)
        self.hi_ha_trio = 3 in self.valors or 4 in self.valors or 5 in self.valors
        self.hi_ha_parella = 2 in self.valors or 4 in self.valors
        self.hi_ha_full = (3 in self.valors and 2 in self.valors)
        self.hi_ha_poker = 4 in self.valors or 5 in self.valors
        self.hi_ha_generala = 5 in self.valors
        self.hi_ha_escala = self.valors in ([1,1,1,1,1,0], [0,1,1,1,1,1], [1,0,1,1,1,1])

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.daus = [0, 0, 0, 0, 0]
        self.full = {k: -1 for k in ["1", "2", "3", "4", "5", "6", "E", "F", "P", "G"]}
        self.tirada_actual = 0
        self.torn_actual = 1
        self.es_servit = False
        
        # Generem la primera tirada de la partida
        self._executar_tirada([True, True, True, True, True])
        
        return self._get_obs(), {}

    def _get_obs(self):
        # 1. Valors del full
        full_vector = list(self.full.values())
        
        # 2. Convertim els booleans a 1 o 0 perquè l'IA ho entengui bé com a Box
        jocs_bools = [
            int(self.hi_ha_parella), int(self.hi_ha_trio), 
            int(self.hi_ha_poker), int(self.hi_ha_generala), 
            int(self.hi_ha_escala), int(self.hi_ha_full)
        ]
        
        # 3. Concatenem-ho tot en un sol vector de longitud 22
        estat = self.daus + full_vector + jocs_bools + [self.tirada_actual]
        return np.array(estat, dtype=np.int32)

    def _executar_tirada(self, tirs):
        # Només es considera "servit" si és la primera tirada i es tiren tots
        if all(tirs):
            self.es_servit = True
        elif any(tirs):
            self.es_servit = False # Si retira daus més tard, ja no és servit

        for i in range(5):
            if tirs[i]:
                self.daus[i] = random.randint(1, 6)
                
        self.tirada_actual += 1
        self._actualitzar_estat_daus() # Vital: Actualitza l'estat just després de tirar

    def calcular_punts_lògica(self):
        """Avalua els punts de la mà actual sobre TOTA la taula."""
        # 1. Creem el diccionari per als números (1-6) de forma neta (Dictionary Comprehension)
        p = {str(i+1): (i+1) * self.valors[i] for i in range(6)}
        
        # 2. Inicialitzem els jocs a 0
        p.update({"E": 0, "F": 0, "P": 0, "G": 0})
        
        # 3. ESCALA (60 punts + 5 si és servida)
        if self.hi_ha_escala and self.full["E"] == -1: 
            p["E"] = 60 + (5 if self.es_servit else 0)
        
        # 4. FULL (70 punts + 5 si és servit)
        if self.hi_ha_full and self.full["F"] == -1: 
            p["F"] = 70 + (5 if self.es_servit else 0)
            
        # 5. PÒQUER (80 punts + valor del dau + 10 si és servit)
        if self.hi_ha_poker and self.full["P"] == -1:
            # Busquem quin dau té 4 (o 5) repeticions
            dau_poker = 0
            if 4 in self.valors:
                dau_poker = self.valors.index(4) + 1
            
            p["P"] = 80 + dau_poker + (10 if self.es_servit else 0)
            
        # 6. GENERALA (100 punts + valor del dau + 100 si és servida)
        if self.hi_ha_generala and self.full["G"] == -1:
            dau_generala = self.valors.index(5) + 1
            p["G"] = 100 + dau_generala + (100 if self.es_servit else 0)
            
        return p

    def step(self, action):
        reward = 0
        terminated = False
        truncated = False

        punts_tot = self.calcular_punts_lògica()
        max_punts_abans = max(punts_tot.values())

        # --- CAS 1: L'agent vol tirar els daus i encara pot ---
        if action < 32 and self.tirada_actual < 3:
            tirs = [bool(int(x)) for x in bin(action)[2:].zfill(5)]
            self._executar_tirada(tirs)
            
            punts_despres = self.calcular_punts_lògica()
            max_punts_despres = max(punts_despres.values())
            
            # Recompensa suau per millorar la mà
            reward = (max_punts_despres - max_punts_abans) / 2.0 - 0.1
            return self._get_obs(), reward, terminated, truncated, {}

        # --- CAS 2: L'agent vol tirar però JA HA TIRAT 3 COPS ---
        elif action < 32 and self.tirada_actual >= 3:
            reward = -100  # Càstig sever
            return self._get_obs(), reward, terminated, truncated, {}

        # --- CAS 3: L'agent decideix anotar (action >= 32) ---
        else:
            # En lloc del mòdul % 32, restem 32 per treure exactament l'índex (0 a 9)
            idx_anotar = action - 32
            idx_anotar = min(idx_anotar, 9) 
            
            claus = list(self.full.keys())
            casella_triada = claus[idx_anotar]

            if self.full[casella_triada] == -1: # Casella lliure (Èxit)
                punts = punts_tot[casella_triada]
                self.full[casella_triada] = punts
                
                # Càlcul del reward
                if casella_triada in ["E", "F", "P", "G"]:
                    if punts > 0:
                        reward = punts 
                    else:
                        reward = -50 #és -50 perquè anotar un 0 a una casella gran és molt pitjor que cremar números (cremar arribaria fins a -18).
                    
                    # BONUS DE COHERÈNCIA: Força l'aprenentatge si utilitza la casella correcta
                    if casella_triada == "G" and self.hi_ha_generala: reward += 50
                    if casella_triada == "P" and self.hi_ha_poker: reward += 40
                    if casella_triada == "F" and self.hi_ha_full: reward += 30
                    if casella_triada == "E" and self.hi_ha_escala: reward += 20
                else:
                    reward = 6*(punts/int(casella_triada) - 2) - int(casella_triada)
            
            else: # CASELLA OCUPADA (Error d'agent)
                reward = -50 #és -50 perquè el pitjor valor de no equivocar-se podria ser -18. Equivocar-se ha de ser clarament pitjor.
                # Busquem la primera lliure i la cremem
                for c in claus:
                    if self.full[c] == -1:
                        self.full[c] = 0
                        break 

            # --- AVANCEM EL TORN ---
            self.torn_actual += 1
            if self.torn_actual > 10:
                terminated = True
                # Bonus final de la partida
                reward += sum(v for v in self.full.values() if v > 0)
            else:
                self.tirada_actual = 0
                self._executar_tirada([True, True, True, True, True])
            
            return self._get_obs(), reward, terminated, truncated, {}