# 1. CONFIGURAÇÃO ÚNICA ANTES DE CRIAR CONTAS
# flake8: noqa
from classes import Configurar, Circuito, Cabo
import numpy as np
import pandas as pd



# CABOS CADASTRADOS (INICIALIZADOS)
OXLIP      = Cabo('OXLIP','CA Oxlip 4/0 AWG'          ,  295.7, 0.3281, 0.4025,  430)
GOLDENTUFT = Cabo('GOLDENTUFT','CA Goldentuft 450 MCM',  628.7, 0.1549, 0.3700,  692)
COSMOS     = Cabo('COSMOS','CA Cosmos 477 MCM'        ,  665.9, 0.1460, 0.3678,  718)
ORCHID     = Cabo('ORCHID','CA Orchid 636 MCM'        ,  888.4, 0.1100, 0.3557,  859)
ARBUTUS    = Cabo('ARBUTUS','CA Arbutus 795 MCM'      , 1111.1, 0.0882, 0.3472,  988)
ANEMONE    = Cabo('ANEMONE','CA Anemone 874,5 MCM'    , 1221.7, 0.0808, 0.3437, 1045)
MAGNOLIA   = Cabo('MAGNOLIA','CA Magnolia 954 MCM'    , 1333.0, 0.0746, 0.3404, 1100)
MARIGOLD   = Cabo('MARIGOLD','CA Marigold 1113 MCM'   , 1555.8, 0.0640, 0.3340, 1212)


condutores = [OXLIP, ORCHID,  MARIGOLD]

print("=== CONFIGURANDO SISTEMA ===")
Circuito.Setup_projeto(
    Pot_aero_MW  = 6,                  # Potencia por aerogerador
    FP           = 0.95,               # Fator de potencia 
    FC           = 1,                  # Fator de capacidade considerado. 1 = 100%
    perda_maxima_percent = 2,
    condutores = condutores,
    q   = 1e5,         # fator de multiplicação do ganho de feromonio delta_tau
    rho = 0.6,         # Evaporação do feromônio
    fer = 0.1,         # Feromônio inicial
    fer_max = 1.2, 
    alfa = 1,          # Parâmetro de influência de feromônio, inicial
    beta = 5,          # Parâmetro de influência de distância
    iteracoes = 50,    # Número de iterações
    num_formigas = 5   # Número de formigas, duas por cidade
)


print("\n=== CRIANDO CIRCUITOS ===")
# 2. AGORA CRIAMOS OS CIRCUITOS




def print_matrix3d(matrix_3d,condutores=[]):
    # num_linhas =  matrix_3d.shape[0]
    # num_colunas =  matrix_3d.shape[1]
    num_layers = matrix_3d.shape[2]

    # print(f"num_layers: {num_layers}")
    # print(f"num_linhas: {num_linhas}")
    # print(f"num_colunas: {num_colunas}")

    for layer in range(num_layers):
        if condutores != []:
            print(f'Condutor: {condutores[layer]}')
        else:
            print(f'index {layer}')
        np.set_printoptions(precision=4, floatmode='fixed')
        print(matrix_3d[:,:,layer])




def iniciar_circuito_01():
    comprimento = np.array([
    [    0, 1000,    0,    0,    0 ],
    [    0,    0, 3000,    0,    0],
    [    0,   0,    0, 5000,    0],
    [    0,   0,    0,    0, 1000],
    [    0,    0,    0,    0,    0]
    ])

    agrupamento = np.array([
        [    0,    1,    0,    0,    0],
        [    0,    0,    2,    0,    0],
        [    0,    0,    0,    3,    0],
        [    0,    0,    0,    0,    3],
        [    0,    0,    0,    0,    0]
    ])

    Circuito_01 = Circuito("SDP-01-01", comprimento,agrupamento)

    return Circuito_01

def iniciar_circuito_02():
    comprimento = np.array([
    [    0, 1000,    0,    0,    0 ],
    [    0,    0, 3000,    0,    0],
    [    0,   0,    0, 5000,    0],
    [    0,   0,    0,    0, 1000],
    [    0,    0,    0,    0,    0]
    ])

    agrupamento = np.array([
        [    0,    1,    0,    0,    0],
        [    0,    0,    2,    0,    0],
        [    0,    0,    0,    3,    0],
        [    0,    0,    0,    0,    3],
        [    0,    0,    0,    0,    0]
    ])


    Circuito_02 = Circuito("SDP-01-02", comprimento, agrupamento)

    return Circuito_02

# ============ EXECUÇÃO ============
if __name__ == "__main__":
    Circuito_01 = iniciar_circuito_01()
    Circuito_02 = iniciar_circuito_02()


    # print(Circuito_01)
    # print(Circuito_02)
    # print("\n")

    # Circuito_02.exibir_matriz_2d("agrupamento")
    Circuito_01.exibir_comprimento()
    Circuito_02.exibir_agrupamento()


    perdas_test = Circuito_01.perdas
    # Circuito_01.exibir_matriz3d(perdas_test)
    print_matrix3d(perdas_test)

    # print(Circuito_01.CONDUTORES[0])

    # print(Circuito_02.calcular_pesos())

    # print(Circuito_01.comprimento)