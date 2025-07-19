import re


def validar_cpf(cpf: str) -> bool:
    """Valida se o CPF possui formato básico correto"""
    return bool(re.fullmatch(r'\d{11}', cpf))

def validar_rg(rg: str) -> bool:
    """Valida se o RG possui números"""
    return bool(re.fullmatch(r'\d{5,12}', rg))

def validar_nome(nome: str) -> bool:
    """Valida se o nome completo possui pelo menos nome e sobrenome"""
    partes = nome.strip().split()
    return len(partes) >= 2
