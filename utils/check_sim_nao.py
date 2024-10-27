import re

def check_sim_nao(text):
    sim_pattern = r"(?i)\bs[iíìîï]m\b"
    nao_pattern = r"(?i)\bn[aáàâãä]o\b"
    
    if re.search(sim_pattern, text):
        return True
    elif re.search(nao_pattern, text):
        return False
    
    return None
