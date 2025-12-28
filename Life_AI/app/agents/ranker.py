
from typing import List, Dict, Any

class RankerAgent:
    def rank_and_select(self, molecules: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
        for mol in molecules:
            mol["score"] = mol["properties"]["QED"] - 0.1 * mol["violations"]
            
        ranked_molecules = sorted(molecules, key=lambda x: x["score"], reverse=True)
        
        return ranked_molecules[:top_k]

