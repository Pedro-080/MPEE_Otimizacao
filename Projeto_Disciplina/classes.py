# flake8: noqa
from abc import ABC, abstractmethod
import pandas as pd


class Configurar:
    """Classe base com configurações globais que podem ser ajustadas uma vez."""
    
    # Configurações padrão
    POT_AERO_MW   = 6
    FP           = 0.95                                       # Fator de potencia 
    FC       = 1                                              # Fator de capacidade considerado. 1 = 100%
    PERDA_MAXIMA_PERCENT = 2                                  # Pedra máxima global tolerada em porcentagem.  2 = 2%  
    CONDUTORES = []
    Q   = 1e5,         # fator de multiplicação do ganho de feromonio delta_tau
    RHO = 0.6,         # Evaporação do feromônio
    FER = 0.1,         # Feromônio inicial
    FER_MAX = 1.2, 
    ALFA = 1,          # Parâmetro de influência de feromônio, inicial
    BETA = 5,          # Parâmetro de influência de distância
    ITERACOES = 50,    # Número de iterações
    NUM_FORMIGAS = 5   # Número de formigas, duas por cidade


    @classmethod
    def Setup_projeto(cls, **kwargs):
        """Configura os parâmetros globais do sistema."""
        for chave, valor in kwargs.items():
            if hasattr(cls, chave.upper()):
                setattr(cls, chave.upper(), valor)
                print(f"Configuração '{chave}' definida como: {valor}")
            else:
                print(f"⚠️ Configuração '{chave}' não existe!")



class Circuito(Configurar):
    """Classe principal que herda as configurações."""

    # Método inicializador (construtor)
    def __init__(self, identificação, comprimento = None, agrupamento = None):
        self.identificação = identificação
        self.comprimento = comprimento     #Matriz de inicialização das distancias
        self.agrupamento = agrupamento     #Matriz de inicialização dos agrupamentos


    def __str__(self):
        return (f"Circuito {self.identificação} ")

    def exibir_comprimento(self):
        dados = self.comprimento
        if dados is None:
            print(f"Comprimento não atribuido ao circuito {self.identificação}")    

        else:
            # Criar Data  Frame
            nome_colunas = [f"{i+1}" for i in range(dados.shape[1])] \
                if len(dados.shape) > 1 else ["Valores"]

            df = pd.DataFrame(dados, columns = nome_colunas, index = range(1,len(dados)+1))
            print(f"Comprimento do {self.identificação}:")
            print(df)

    def exibir_agrupamento(self):
        dados = self.agrupamento
        if dados is None:
            print(f"Agrupamento não atribuido ao circuito {self.identificação}")     

        else:
            # Criar Data  Frame
            nome_colunas = [f"{i+1}" for i in range(dados.shape[1])] \
                if len(dados.shape) > 1 else ["Valores"]

            df = pd.DataFrame(dados, columns = nome_colunas, index = range(1,len(dados)+1))
            print(f"Agrupamento do {self.identificação}:")
            print(df)

