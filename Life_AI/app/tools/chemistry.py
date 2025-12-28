
from rdkit import Chem
from rdkit.Chem import Descriptors, QED

def sanitize_smiles(smi):
    try:
        mol = Chem.MolFromSmiles(smi)
        if mol:
            return Chem.MolToSmiles(mol, isomericSmiles=True)
    except:
        return None

def compute_properties(smi):
    mol = Chem.MolFromSmiles(smi)
    if not mol:
        return None

    return {
        "MW": Descriptors.MolWt(mol),
        "LogP": Descriptors.MolLogP(mol),
        "HBD": Descriptors.NumHDonors(mol),
        "HBA": Descriptors.NumHAcceptors(mol),
        "TPSA": Descriptors.TPSA(mol),
        "RotB": Descriptors.NumRotatableBonds(mol),
        "QED": QED.qed(mol),
    }
