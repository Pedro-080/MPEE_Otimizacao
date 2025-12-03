# 1. CONFIGURAÇÃO ÚNICA ANTES DE CRIAR CONTAS
# flake8: noqa
from classes import Configurar, Circuito
import numpy as np
import pandas as pd



condutores = ['OXLIP', 'ORCHID',  'MARIGOLD']

print("=== CONFIGURANDO SISTEMA ===")
Circuito.Setup_projeto(
    Pot_aero_MW  = 6,                  # Potencia por aerogerador
    FP           = 0.95,               # Fator de potencia 
    FC           = 1,                  # Fator de capacidade considerado. 1 = 100%
    perda_maxima_percent = 2,
    condutores = ['OXLIP', 'ORCHID',  'MARIGOLD'],
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









def iniciar_circuito_01():
    comprimento = np.array([
    [    0, 1000,    0,    0,    0 ],
    [    0,    0, 3000,    0,    0],
    [    0,   0,    0, 5000,    0],
    [    0,   0,    0,    0, 1000],
    [    0,    0,    0,    0,    0]
    ])

    Circuito_01 = Circuito("SDP-01-01", comprimento)

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


    print(Circuito_01)
    print(Circuito_02)
    print("\n")

    # Circuito_02.exibir_matriz_2d("agrupamento")
    Circuito_01.exibir_comprimento()
    Circuito_02.exibir_agrupamento()
    # print(Circuito_01.comprimento)