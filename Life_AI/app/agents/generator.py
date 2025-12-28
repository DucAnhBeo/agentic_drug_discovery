
import random
from typing import List

def mutate_smiles(smi: str) -> str:
    
    mutations = [
        lambda s: s.replace('F', 'Cl', 1) if 'F' in s else s,
        lambda s: s.replace('Cl', 'F', 1) if 'Cl' in s else s,
        lambda s: s.replace('Br', 'Cl', 1) if 'Br' in s else s,

        lambda s: s + 'C',
        lambda s: s.replace('C', '', 1) if len(s) > 3 else s,

        lambda s: s + 'O',
        lambda s: s + 'N',
        lambda s: s + 'CC',
        lambda s: s + 'C(C)C',  

        lambda s: s.replace('C', 'N', 1),
        lambda s: s.replace('C', 'O', 1),
        lambda s: s.replace('c', 'C', 1),
        lambda s: s.replace('C', 'c', 1),

        lambda s: s + 'O' if random.random() > 0.5 else s + 'N',

        lambda s: s.replace('c1ccccc1', 'C1CCCCC1', 1),  
        lambda s: s.replace('C1CCCCC1', 'c1ccccc1', 1),  
    ]
    
    mutation = random.choice(mutations)
    try:
        return mutation(smi)
    except:
        return smi

class GeneratorAgent:
    def __init__(self, seeds: List[str]):
        self.seeds = seeds
        self.generated_history = set()

    def propose_candidates(self, num_candidates: int) -> List[str]:
        candidates = []
        attempts = 0
        max_attempts = num_candidates * 10  

        while len(candidates) < num_candidates and attempts < max_attempts:
            seed = random.choice(self.seeds)
            mutated = mutate_smiles(seed)

            if mutated not in candidates and mutated not in self.generated_history:
                candidates.append(mutated)
                self.generated_history.add(mutated)

            attempts += 1

        return candidates

