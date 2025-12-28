
from .schemas import RunConfig
from .agents.planner import PlannerAgent
from .agents.generator import GeneratorAgent
from .agents.ranker import RankerAgent
from .tools.chemistry import sanitize_smiles, compute_properties
from .tools.screening import screen_molecules

runs = {}

def execute_run(run_id: str, config: RunConfig):
    run = runs[run_id]
    run["status"] = "running"
    
    planner = PlannerAgent(config.model_dump())
    plan = planner.get_plan()
    run["trace"].append({"agent": "Planner", "action": "Created plan", "details": plan})

    generator = GeneratorAgent(plan["seeds"])
    
    all_passed_molecules = []
    total_failure_breakdown = {
        "MW_too_high": 0,
        "LogP_too_high": 0,
        "HBD_too_high": 0,
        "HBA_too_high": 0,
        "TPSA_too_high": 0,
    }

    for i in range(plan["rounds"]):
        run["trace"].append({"agent": "Generator", "action": f"Starting round {i+1}"})

        candidates = generator.propose_candidates(plan["candidates_per_round"])
        run["trace"].append({"agent": "Generator", "action": "Proposed candidates", "count": len(candidates)})

        valid_molecules = []
        seen_smiles = set()
        for smi in candidates:
            sanitized_smi = sanitize_smiles(smi)
            if sanitized_smi and sanitized_smi not in seen_smiles:
                properties = compute_properties(sanitized_smi)
                if properties:
                    valid_molecules.append({"smi": sanitized_smi, "properties": properties})
                    seen_smiles.add(sanitized_smi)

        run["trace"].append({"agent": "Chemistry Tool", "action": "Computed properties", "count": len(valid_molecules)})

        passed_molecules, failure_breakdown = screen_molecules(valid_molecules, plan["filters"], plan["max_violations"])

        for key in total_failure_breakdown:
            total_failure_breakdown[key] += failure_breakdown.get(key, 0)

        run["trace"].append({
            "agent": "Screening Tool",
            "action": "Screened molecules",
            "passed": len(passed_molecules),
            "failed": len(valid_molecules) - len(passed_molecules),
            "failure_breakdown": failure_breakdown
        })
        all_passed_molecules.extend(passed_molecules)

    ranker = RankerAgent()
    top_k = 10  
    final_results = ranker.rank_and_select(all_passed_molecules, top_k)
    run["trace"].append({"agent": "Ranker", "action": "Ranked and selected candidates", "count": len(final_results)})

    run["summary"] = {
        "total_passed": len(all_passed_molecules),
        "total_failure_breakdown": total_failure_breakdown,
        "final_selected": len(final_results)
    }

    run["results"] = final_results
    run["status"] = "completed"

