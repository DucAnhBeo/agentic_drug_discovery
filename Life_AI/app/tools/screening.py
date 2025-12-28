
from typing import List, Dict, Any

def screen_molecules(molecules: List[Dict[str, Any]], filters: Dict[str, float], max_violations: int) -> tuple[List[Dict[str, Any]], Dict[str, int]]:
    """
    Screen molecules based on filters and return passed molecules with failure breakdown.

    Returns:
        tuple: (passed_molecules, failure_breakdown)
    """
    passed_molecules = []
    failure_breakdown = {
        "MW_too_high": 0,
        "LogP_too_high": 0,
        "HBD_too_high": 0,
        "HBA_too_high": 0,
        "TPSA_too_high": 0,
    }

    for mol_data in molecules:
        violations = 0
        violation_details = []

        if mol_data["properties"]["MW"] > filters.get("MW", 500):
            violations += 1
            violation_details.append("MW")
        if mol_data["properties"]["LogP"] > filters.get("LogP", 5):
            violations += 1
            violation_details.append("LogP")
        if mol_data["properties"]["HBD"] > filters.get("HBD", 5):
            violations += 1
            violation_details.append("HBD")
        if mol_data["properties"]["HBA"] > filters.get("HBA", 10):
            violations += 1
            violation_details.append("HBA")
        if mol_data["properties"]["TPSA"] > filters.get("TPSA", 140):
            violations += 1
            violation_details.append("TPSA")

        if violations <= max_violations:
            mol_data["violations"] = violations
            mol_data["violation_details"] = violation_details
            passed_molecules.append(mol_data)
        else:
            # Track failure reasons
            for detail in violation_details:
                failure_breakdown[f"{detail}_too_high"] += 1

    return passed_molecules, failure_breakdown
