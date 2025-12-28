
import random
from typing import List

def mutate_smiles(smi: str) -> str:
    """
    Apply random mutations to SMILES string.
    Supports: swap F↔Cl, add/remove methyl, add/remove atoms, ring modifications
    """
    mutations = [
        # Swap halogens
        lambda s: s.replace('F', 'Cl', 1) if 'F' in s else s,
        lambda s: s.replace('Cl', 'F', 1) if 'Cl' in s else s,
        lambda s: s.replace('Br', 'Cl', 1) if 'Br' in s else s,

        # Add/remove methyl groups
        lambda s: s + 'C',
        lambda s: s.replace('C', '', 1) if len(s) > 3 else s,

        # Add functional groups
        lambda s: s + 'O',
        lambda s: s + 'N',
        lambda s: s + 'CC',  # ethyl
        lambda s: s + 'C(C)C',  # isopropyl

        # Atom substitutions
        lambda s: s.replace('C', 'N', 1),
        lambda s: s.replace('C', 'O', 1),
        lambda s: s.replace('c', 'C', 1),
        lambda s: s.replace('C', 'c', 1),

        # Add hydroxyl or amino groups
        lambda s: s + 'O' if random.random() > 0.5 else s + 'N',

        # Ring modifications
        lambda s: s.replace('c1ccccc1', 'C1CCCCC1', 1),  # aromatic to aliphatic
        lambda s: s.replace('C1CCCCC1', 'c1ccccc1', 1),  # aliphatic to aromatic
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
        """
        Generate candidate molecules by mutating seed SMILES.
        Ensures uniqueness within a single call.
        """
        candidates = []
        attempts = 0
        max_attempts = num_candidates * 10  # Prevent infinite loop

        while len(candidates) < num_candidates and attempts < max_attempts:
            seed = random.choice(self.seeds)
            mutated = mutate_smiles(seed)

            # Ensure uniqueness
            if mutated not in candidates and mutated not in self.generated_history:
                candidates.append(mutated)
                self.generated_history.add(mutated)

            attempts += 1

        return candidates
