# app/services/molecular_formula_predictor.py

import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem
from rpy2.robjects import pandas2ri, r
from rdkit.Chem import rdMolDescriptors

pandas2ri.activate()

def load_r_scripts():
    r('''
    source("app/r_scripts/user_defined_structure_model.R")
    source("app/r_scripts/ccs_model.R")
    source("app/r_scripts/retention_model.R")
    source("app/r_scripts/retention_time_structure_model.R")
    ''')

def generate_candidates(precursor_mz, tolerance=10):
    candidates = []
    for c in range(1, 30):  # Adjust ranges as needed
        for h in range(1, 60):
            for n in range(0, 10):
                for o in range(0, 10):
                    formula = f"C{c}H{h}N{n}O{o}"
                    mol = Chem.MolFromFormula(formula)
                    if mol:
                        mass = Descriptors.ExactMolWt(mol)
                        if abs(mass - precursor_mz) <= tolerance:
                            candidates.append({"formula": formula, "mass": mass})
    return candidates

def calculate_descriptors(mol):
    return {
        "ExactMolWt": Descriptors.ExactMolWt(mol),
        "MolLogP": Descriptors.MolLogP(mol),
        "TPSA": Descriptors.TPSA(mol),
        "NumHDonors": Descriptors.NumHDonors(mol),
        "NumHAcceptors": Descriptors.NumHAcceptors(mol),
        "NumRotatableBonds": Descriptors.NumRotatableBonds(mol),
    }

def score_candidates(candidates, mass_spectrum, custom_dbs, rt_model, ccs_model, rts_model, uds_model):
    scored_candidates = []
    for candidate in candidates:
        score = 0
        mol = Chem.MolFromFormula(candidate["formula"])
        
        if mol:
            # Mass accuracy score
            mass_error = abs(candidate["mass"] - mass_spectrum.precursor_mz)
            score -= mass_error
            
            # Check custom databases
            smiles = Chem.MolToSmiles(mol)
            inchikey = Chem.MolToInchiKey(mol)
            
            if any(db.inchikey == inchikey for db in custom_dbs["user_defined"]):
                score += 10
            if any(db.smiles == smiles for db in custom_dbs["retention_time_structure"]):
                score += 5
            if any(db.inchikey == inchikey for db in custom_dbs["retention_time_library"]):
                score += 5
            if any(db.inchikey == inchikey for db in custom_dbs["ccs_library"]):
                score += 5
            
            # Predict using all models
            descriptors = calculate_descriptors(mol)
            r_descriptors = pandas2ri.py2rpy(pd.DataFrame([descriptors]))
            
            predicted_rt = r("predict_retention_time")(rt_model, r_descriptors)[0]
            predicted_ccs = r("predict_ccs")(ccs_model, r_descriptors)[0]
            predicted_rts = r("predict_retention_time")(rts_model, r_descriptors)[0]
            predicted_uds = r("predict_exact_mass")(uds_model, r_descriptors)[0]
            
            rt_error = abs(predicted_rt - mass_spectrum.retention_time)
            ccs_error = abs(predicted_ccs - mass_spectrum.ccs)
            rts_error = abs(predicted_rts - mass_spectrum.retention_time)
            uds_error = abs(predicted_uds - candidate["mass"])
            
            score -= (rt_error + ccs_error + rts_error + uds_error) / 4
            
            # Isotopic pattern score
            isotope_score = calculate_isotope_score(mol, mass_spectrum)
            score += isotope_score
            
            # MS/MS fragmentation score
            msms_score = calculate_msms_score(mol, mass_spectrum)
            score += msms_score
        
        scored_candidates.append({
            "formula": candidate["formula"],
            "mass": candidate["mass"],
            "score": score,
            "predicted_rt": predicted_rt,
            "predicted_ccs": predicted_ccs,
            "predicted_rts": predicted_rts,
            "predicted_uds": predicted_uds
        })
    
    return sorted(scored_candidates, key=lambda x: x["score"], reverse=True)

def calculate_isotope_score(mol, mass_spectrum):
    # Generate theoretical isotope pattern
    theoretical_pattern = rdMolDescriptors.GetMassDistribution(mol)
    
    # Compare with observed pattern in mass_spectrum
    # This is a simplified example - you'd need to implement the comparison logic
    score = compare_patterns(theoretical_pattern, mass_spectrum.isotope_pattern)
    
    return score

def calculate_msms_score(mol, mass_spectrum):
    # Generate theoretical fragments
    theoretical_fragments = generate_theoretical_fragments(mol)
    
    # Compare with observed fragments in mass_spectrum
    # This is a simplified example - you'd need to implement the comparison logic
    score = compare_fragments(theoretical_fragments, mass_spectrum.msms_spectrum)
    
    return score


async def predict_molecular_formula(mass_spectrum, custom_dbs, db):
    load_r_scripts()
    
    # Generate candidates
    candidates = generate_candidates(mass_spectrum.precursor_mz)
    
    # Prepare data for R models
    retention_time_data = pd.DataFrame([
        {"retention_time": rts.retentionTime, **calculate_descriptors(Chem.MolFromSmiles(rts.smiles))}
        for rts in custom_dbs["retention_time_structure"]
    ])
    
    ccs_data = pd.DataFrame([
        {"ccs": ccs.ccs, **calculate_descriptors(Chem.MolFromSmiles(ccs.smiles))}
        for ccs in custom_dbs["ccs_library"]
    ])
    
    user_defined_data = pd.DataFrame([
        {"Exact mass": uds.exactMass, "Formula": uds.formula, "SMILES": uds.smiles}
        for uds in custom_dbs["user_defined"]
    ])
    
    # Train models
    r_rt_data = pandas2ri.py2rpy(retention_time_data)
    r_ccs_data = pandas2ri.py2rpy(ccs_data)
    r_uds_data = pandas2ri.py2rpy(user_defined_data)
    
    rt_model = r("train_retention_model")(r_rt_data)
    ccs_model = r("train_ccs_model")(r_ccs_data)
    rts_model = r("train_retention_time_structure_model")(r_rt_data)
    uds_model = r("train_user_defined_structure_model")(r_uds_data)
    
    # Score candidates
    final_candidates = score_candidates(candidates, mass_spectrum, custom_dbs, rt_model, ccs_model, rts_model, uds_model)
    
    return final_candidates  # Return all candidates
