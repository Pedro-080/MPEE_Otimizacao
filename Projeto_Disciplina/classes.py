# flake8: noqa
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import math 
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
    def __init__(self, identificação, comprimento , agrupamento ):
        self.identificação = identificação
        self.comprimento = comprimento     #Matriz de inicialização das distancias
        self.agrupamento = agrupamento     #Matriz de inicialização dos agrupamentos
        self.perdas = self.calcular_perdas()


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
            print(f"\nAgrupamento não atribuido ao circuito {self.identificação}")     

        else:
            # Criar Data  Frame
            nome_colunas = [f"{i+1}" for i in range(dados.shape[1])] \
                if len(dados.shape) > 1 else ["Valores"]

            df = pd.DataFrame(dados, columns = nome_colunas, index = range(1,len(dados)+1))
            print(f"\nAgrupamento do {self.identificação}:")
            print(df)

    def exibir_matriz3d(self,dados):
        condutores = self.CONDUTORES
        n_condutores, n_linhas, n_colunas = dados.shape
        nomes_colunas = [f'col_{i}' for i in range(n_colunas)]

        # Achatar o array
        dados_flat = dados.reshape(-1, n_colunas)

        # Criar nomes de condutores repetidos
        condutores_repetidos = np.repeat(condutores, n_linhas)

        # Criar DataFrame
        df = pd.DataFrame(dados_flat, columns=nomes_colunas)
        df.insert(0, 'condutor', condutores_repetidos)
        
        return df
        ...

    def calcular_perdas(self):
        print(f"tipo self.agrupamento:\n{self.agrupamento}")

        Pot_acumulado_MW_3d = self.agrupamento * self.POT_AERO_MW
        Pot_circ_MW  = np.max(self.agrupamento) * self.POT_AERO_MW
        FP  = self.FP
        FC = self.FC

        perdas_por_condutor = []

        for condutor in self.CONDUTORES:
            perda = condutor.array_calcular_perdas_percent(self.comprimento, Pot_acumulado_MW_3d, Pot_circ_MW, FP, FC)
            perdas_por_condutor.append(perda)

        perdas = np.stack(perdas_por_condutor, axis=2)
        return perdas

class Cabo():
    def __init__(self, ID,condutor, peso_kgkm, RCA, XL,ampacidade):
        self.id        = ID
        self.condutor  = condutor
        self.peso_kgkm = peso_kgkm
        self.RCA       = RCA
        self.XL        = XL
        self.ampacidade= ampacidade
    
    def __str__(self) :
        return self.id
    
    def _resitencia_ohm(self, comprimento_m):
        RCA_ohm = comprimento_m * self.RCA /1000
        # print(f"RCA_ohm: {RCA_ohm}")
        return RCA_ohm
        ...

    def _corrente_A(self, potencia_MW, FP, FC=1):
        return ((potencia_MW * 1000) / (34.5 * math.sqrt(3) * FP)) * FC
        
    def _perdas_W(self, comprimento, potencia_MW, FP, FC=1):
        corrente = self._corrente_A(potencia_MW, FP, FC)
        RCA_ohm  = self._resitencia_ohm(comprimento)
    
        return 3 * RCA_ohm * corrente**2

    def _perdas_MWh_ano(self, comprimento, potencia_MW, FP, FC=1):
        perdas_W = self._perdas_W(comprimento, potencia_MW, FP, FC)
        return (perdas_W * 24 * 365)/1000000
        ...

    def _perdas_percent (self, comprimento, potencia_MW, potencia_total_MW, FP, FC=1 ):
        Potencia_total_MWh_ano = potencia_total_MW * 24 * 365
        perdas_MWh_ano = self._perdas_MWh_ano(comprimento, potencia_MW, FP, FC=1)
        resultado = perdas_MWh_ano / Potencia_total_MWh_ano * 100
        return np.round(resultado,4)
        ...

# NOVOS MÉTODOS VECTORIZADOS
    def array_calcular_perdas_percent(self, comprimentos_array, potencias_array, potencia_total_MW, FP, FC=1):
        """
        Calcula perdas para arrays de comprimentos e potências.
        
        Args:
            comprimentos_array: np.array de comprimentos em metros
            potencias_array: np.array de potências em MW
            FP: Fator de potência (scalar)
            FC: Fator de carga (scalar)
            
        Returns:
            dict: Dicionário com arrays de resultados
        """
        # Garantir que são arrays numpy
        comprimentos = np.asarray(comprimentos_array)
        potencias = np.asarray(potencias_array)
        
        # Verificar dimensões compatíveis para broadcasting
        if comprimentos.ndim == 1 and potencias.ndim == 1:
            # Criar meshgrid para todas as combinações
            comprimentos_grid, potencias_grid = np.meshgrid(comprimentos, potencias, indexing='ij')
        else:
            comprimentos_grid = comprimentos
            potencias_grid = potencias
        
        # Calcular todos os resultados de uma vez
        # correntes = self._corrente_A(potencias_grid, FP, FC)
        # perdas_W = self._perdas_W(comprimentos_grid, potencias_grid, FP, FC)
        # perdas_MWh_ano = self._perdas_MWh_ano(comprimentos_grid, potencias_grid, FP, FC)
        perdas_percent = self._perdas_percent(comprimentos_grid, potencias_grid, potencia_total_MW, FP,FC )

        # def _perdas_percent (self, comprimento, potencia_MW, potencia_total_MW, FP, FC=1 ):


        return perdas_percent

    def array_calcular_massa_ton(self,comprimentos_array):
        """
        Calcula a massa equivalente em toneladas para o trecho específico.
        
        Args:
            comprimentos_array: np.array de comprimentos em metros
            
        Returns:
            massa: array com massa de cada trecho
        """
        peso_kg_km = self.peso_kgkm
        peso_ton_m = peso_kg_km * 1e-6   #Conversão de kg/km para ton/m

        array_peso = comprimentos_array * peso_ton_m

        return array_peso