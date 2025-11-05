# flake8: noqa
import numpy as np
import random

# ================================
# PARÂMETROS DO ALGORITMO
# ================================
q = 10      # Constante de atualização do feromônio
s = 0.01    # Evaporação do feromônio
fer = 0.1   # Feromônio inicial
alfa = 1      # Parâmetro de influência de feromônio, inicial
beta = 2       # Parâmetro de influência de distância
err = 10**(-4)


# Matriz de distâncias
d = np.array([
        [0, 2, 9, 10, 7],
        [1, 0, 6, 4, 3],
        [15, 7, 0, 8, 3],
        [6, 3, 12, 0, 11],
        [9, 7, 5, 6, 0]
])

CIDADES = ['A', 'B', 'C', 'D', 'E']

NCidades = d.shape[0]

# ================================
# INICIALIZAÇÃO
# ================================
num_formigas = 5                                            # Número de formigas, duas por cidade
tau = np.ones((NCidades, NCidades)) * 0.001  # Deposição inicial de feromonio
Matriz_Infor = np.zeros((num_formigas, NCidades))            # Caminho das formigas
Matriz_Infor_Temp = Matriz_Infor.copy()            # Informativo das cidades
iteracoes = 3                                  # Número de iterações
prob = np.zeros((num_formigas, NCidades))                    # Matriz probabilidade

K = d + np.eye(NCidades, NCidades)                 # Matriz auxiliar para somar zeros

m1 = K**(-1)                                # Invertendo termos da matriz auxiliar
n1 = m1 - np.eye(NCidades, NCidades)        # Matriz de termos inversos a distância


# print(f"d: \n {d}")
# print(f"Feromonio: \n {Feromonio}")
# print(f"n: \n {n1}")


# print(Matriz_Infor) 
for iteracao in range(iteracoes):
    '''Matriz que armazena o percurso de cada formiga'''
    Matriz_Infor = np.zeros((num_formigas, NCidades), dtype=int)

    Cidades_disponiveis = np.tile(np.arange(1,NCidades+1),(num_formigas,1))

    # for cidade in Cidades_disponiveis:
    #     print(f"type cidade: {type(cidade)}")

    for formiga in range(num_formigas):

        '''Inicia todas as formigas saindo da cidade 0'''
        Matriz_Infor[formiga, 0] = 1 +  int(abs( NCidades* random.random()))
        # Matriz_Infor[formiga, 0] =  0

        '''Define a cidade atual'''
        Cidade_atual = Matriz_Infor[formiga, 0]

        # print(f"Cidade_atual: {Cidade_atual}") 
        # print(f"type Cidade_atual: {type(Cidade_atual)}")
        
        '''Verifica as cidades disponiveis'''
        # print(f"usadas: {set(Matriz_Infor[formiga, :])}")
        Cidades_percorridas = np.unique(Matriz_Infor[formiga][Matriz_Infor[formiga] != 0])

        # Cidades_disponiveis.remove(int(3))
        # Cidades_disponiveis.remove(3)

        '''Remove a cidade atual da lista de cidades disponíveis'''
        # print(f"Cidades_disponíveis: {Cidades_disponiveis}")

        # print(f"Cidades_percorridas: {Cidades_percorridas[0]}")
        # print(f"Cidades_percorridas: {type(Cidades_percorridas[0])}")
        # Cidades_disponiveis.remove(1)



        # Cidades_disponiveis.remove(Cidade_atual)

        n_cidade_beta = n1[Cidade_atual-1,:] ** beta
        tau_cidade_alfa = tau[Cidade_atual-1,:] ** alfa



        # print(n_cidade_beta)    
        # print(f"formiga: {formiga}")

    # print(f"Cidades_disponíveis: {Cidades_disponíveis}")
    print(Matriz_Infor) 
    print(iteracao) 