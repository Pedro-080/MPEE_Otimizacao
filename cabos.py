# flake8: noqa
import math 
import numpy as np

class Cabo():
    def __init__(self, condutor, peso_kgkm, RCA, XL,ampacidade):
        self.condutor  = condutor
        self.peso_kgkm = peso_kgkm
        self.RCA       = RCA
        self.XL        = XL
        self.ampacidade= ampacidade
    
    def __str__(self) :
        return self.condutor

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
    # def analisar_cenario_array(self, comprimentos_array, potencias_array, potencia_total_MW, FP=0.95, FC=1):
    #     """
    #     Análise completa para arrays de comprimentos e potências.
        
    #     Returns:
    #         dict: Resultados completos incluindo percentuais
    #     """
    #     resultados = self.calcular_perdas_array(comprimentos_array, potencias_array, FP, FC)
        
    #     # Calcular percentuais (requer potencia_total_MW como array compatível)
    #     potencia_total_array = np.full_like(resultados['potencias'], potencia_total_MW)
    #     resultados['perdas_percent'] = self._perdas_percent(
    #         resultados['comprimentos'], 
    #         resultados['potencias'], 
    #         potencia_total_array, 
    #         FP, 
    #         FC
    #     )
        
    #     return resultados







# OXLIP = Cabo('CA Oxlip 4/0 AWG', 295.7, 0.3281, 0.4025, 430)
# OXLIP._resitencia_ohm(1000)

# # print(OXLIP._corrente_A(6,0.95,0.6))

# # print(OXLIP._perdas_W(1000,6,0.95))
# # print(OXLIP._perdas_MWh_ano(1000,6,0.95))




# CABOS CADASTRADOS (INICIALIZADOS)
OXLIP      = Cabo('CA Oxlip 4/0 AWG'     ,  295.7, 0.3281, 0.4025,  430)
GOLDENTUFT = Cabo('CA Goldentuft 450 MCM',  628.7, 0.1549, 0.3700,  692)
COSMOS     = Cabo('CA Cosmos 477 MCM'    ,  665.9, 0.1460, 0.3678,  718)
ORCHID     = Cabo('CA Orchid 636 MCM'    ,  888.4, 0.1100, 0.3557,  859)
ARBUTUS    = Cabo('CA Arbutus 795 MCM'   , 1111.1, 0.0882, 0.3472,  988)
ANEMONE    = Cabo('CA Anemone 874,5 MCM' , 1221.7, 0.0808, 0.3437, 1045)
MAGNOLIA   = Cabo('CA Magnolia 954 MCM'  , 1333.0, 0.0746, 0.3404, 1100)
MARIGOLD   = Cabo('CA Marigold 1113 MCM' , 1555.8, 0.0640, 0.3340, 1212)


