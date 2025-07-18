# models/research.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Research:
    filtro: int
    cpf: Optional[str] = None
    rg: Optional[str] = None
    nome: Optional[str] = None
    cod_pesquisa: Optional[int] = 123  # Temporário: depois vamos buscar do banco
    cod_cliente: int = 1
    cod_servico: int = 1

    def get_documento(self) -> str:
        if self.filtro == 0 and self.cpf:
            return self.cpf
        elif self.filtro in [1, 3] and self.rg:
            return self.rg
        elif self.filtro == 2 and self.nome:
            return self.nome
        raise ValueError("Documento inválido para o filtro selecionado.")
