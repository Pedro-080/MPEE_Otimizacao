# flake8: noqa
from cabos import OXLIP, GOLDENTUFT, COSMOS, ORCHID, ARBUTUS , ANEMONE, MAGNOLIA, MARIGOLD
import numpy as np
import random


def calcular_mascara_cidades_disponiveis(Cidades_disponiveis,cidade_atual, num_cabos):

    # Cidades_disponiveis_index = np.subtract(Cidades_disponiveis, 1)
    Cidades_disponiveis_index = np.unique(Cidades_disponiveis)
    Cidades_disponiveis_index = np.insert(Cidades_disponiveis_index, 0, 0)

    # print(f"Cidades_disponiveis_index:{Cidades_disponiveis_index}")

    NCidades = len(Cidades_disponiveis_index)
    
    Cidades_disponiveis_list = (Cidades_disponiveis_index != 0).astype(int)
    print(f"Cidades_disponiveis_index:{Cidades_disponiveis_index}")
    print(f"Cidades_disponiveis_lis:  {Cidades_disponiveis_list}")

    # #Cria a base que será usada 
    base = np.zeros((NCidades,NCidades),dtype=int)
    base[cidade_atual-1] = Cidades_disponiveis_list 
    
    matriz = np.stack([base]*num_cabos,axis=2)
    # print(f"Cidades_disponiveis_list:{Cidades_disponiveis_list}")
    print_matrix3d(matriz)
    # print(matriz)
    print('='*50)
    return matriz

def matrix3d_fatiar_linha(linha, matrix3d):
    # Criar cópia zerada
    matriz_resultado = np.zeros_like(matrix3d)

    # Manter apenas a linha 0 (índice 0) de todos os layers
    matriz_resultado[linha-1, :, :] = matrix3d[linha-1, :, :]
    return matriz_resultado


def Remover_cidade(lista_cidades,cidade):
    """
    Remove uma cidade (substitui por 0) em um array NumPy
    """
    array_modificado = lista_cidades.copy()
    
    if cidade in array_modificado:
        # Encontrar o primeiro índice onde a cidade aparece
        indices = np.where(array_modificado == cidade)[0]
        if len(indices) > 0:
            array_modificado[indices[0]] = 0
    else:
        print("Cidade não disponível")
    
    return array_modificado




def print_matrix3d(matrix_3d,condutores=[]):
    num_linhas =  matrix_3d.shape[0]
    num_colunas =  matrix_3d.shape[1]
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

def calcular_n(matriz):
    """
    Calcula o inverso da matriz de entrada.
    
    Args:
        input: matriz de entrada
        
    Returns:
        massa: array com massa de cada trecho
    """   

    mascara = (matriz == 0).astype(int)

    K = matriz + mascara
    m1 = K**(-1)
    n = m1 - mascara

    return n



# ================================
# DADOS DO CIRCUITO
# ================================
Pot_aero_MW = 6
Pot_circ_MW = 18
FP          = 0.95
FC_100      = 1 


# DADOS DE ENTRADA
comprimento = np.array([
    [    0, 100,    0,    0,    0 ],
    [    0,    0, 300,    0,    0],
    [    0,   0,    0, 500,    0],
    [    0,   1e-6,    0,    0, 1000],
    [    0,    0,    0,    0,    0]
])

agrupamento = np.array([
    [    0,    1,    0,    0,    0],
    [    0,    0,    2,    0,    0],
    [    0,    0,    0,    3,    0],
    [    0,    0,    0,    0,    3],
    [    0,    0,    0,    0,    0]
])

condutores = ['OXLIP', 'GOLDENTUFT', 'COSMOS', 'ORCHID', 'ARBUTUS' , 'ANEMONE', 'MAGNOLIA', 'MARIGOLD']

Pot_acumulado_MW = agrupamento * Pot_aero_MW

perdas_OXLIP      = OXLIP.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_GOLDENTUFT = GOLDENTUFT.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_COSMOS     = COSMOS.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_ORCHID     = ORCHID.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_ARBUTUS    = ARBUTUS.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_ANEMONE    = ANEMONE.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_MAGNOLIA   = MAGNOLIA.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_MARIGOLD   = MARIGOLD.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)

peso_OXLIP        = OXLIP.array_calcular_massa_ton(comprimento)
peso_GOLDENTUFT   = GOLDENTUFT.array_calcular_massa_ton(comprimento)
peso_COSMOS       = COSMOS.array_calcular_massa_ton(comprimento)
peso_ORCHID       = ORCHID.array_calcular_massa_ton(comprimento)
peso_ARBUTUS      = ARBUTUS.array_calcular_massa_ton(comprimento)
peso_ANEMONE      = ANEMONE.array_calcular_massa_ton(comprimento)
peso_MAGNOLIA     = MAGNOLIA .array_calcular_massa_ton(comprimento)
peso_MARIGOLD     = MARIGOLD  .array_calcular_massa_ton(comprimento)




# ================================
# PARÂMETROS DO ALGORITMO
# ================================
rho = 0.01    # Evaporação do feromônio
fer = 0.1   # Feromônio inicial
alfa = 1      # Parâmetro de influência de feromônio, inicial
beta = 2       # Parâmetro de influência de distância



pesos = np.stack([
    peso_OXLIP,
    peso_GOLDENTUFT,
    peso_COSMOS,
    peso_ORCHID,
    peso_ARBUTUS,
    peso_ANEMONE,
    peso_MAGNOLIA,
    peso_MARIGOLD
], axis=2)

perdas = np.stack([
    perdas_OXLIP,
    perdas_GOLDENTUFT,
    perdas_COSMOS,
    perdas_ORCHID,
    perdas_ARBUTUS,
    perdas_ANEMONE,
    perdas_MAGNOLIA,
    perdas_MARIGOLD
], axis=2)


NCidades = comprimento.shape[0]
NCabos   = pesos.shape[2]


# ================================
# INICIALIZAÇÃO
# ================================
num_formigas = 10                                            # Número de formigas, duas por cidade
tau = np.ones((NCidades, NCidades,NCabos)) * 0.001         # Deposição inicial de feromonio
n = calcular_n(pesos)                                        # Matriz de termos inversos a distância

lista_tau = [tau] * NCabos
lista_n   = [n] * NCabos

Matriz_Infor = np.zeros((num_formigas, NCabos))              # Caminho das formigas pelos layers
iteracoes = 3                                                # Número de iterações



# print(lista_tau)

# K = pesos + np.eye(NCidades, NCidades,NCabos)              # Matriz auxiliar para somar zeros



# print(f"NCidades: {NCidades}")
# print(f"NCabos: {NCabos}")








# print(np.eye((NCidades, NCidades,NCabos)))
# print_matrix3d(pesos,condutores)



Layers_disponiveis = np.tile(np.arange(1,NCabos+1),(num_formigas,1))  

# print(f"Matriz_Infor: \n{Matriz_Infor}")
# print(f"Layers_disponiveis: \n{Layers_disponiveis}")


#Criando lista de cidades disponiveis
# Encontrar índices das colunas onde há valores não-zero
linhas, colunas = np.where(comprimento != 0)
colunas = np.add(colunas,1)
# Ordenar pelas colunas (já vem ordenado por padrão)
# lista_resultado = sorted(colunas.tolist())

Cidades_disponiveis = np.tile(sorted(colunas.tolist()),(num_formigas,1))  


'''Versão correta - Descomentar apos testes'''
num_passos = np.count_nonzero(comprimento)
num_passos = 1

# print(f"Cidades_disponiveis: \n{Cidades_disponiveis}")

# print(f"num_passos:{num_passos}")


for passo in range(1, num_passos+1):
    print(f"passo atual:{passo}")


    for formiga in range(num_formigas):
        # linha_limpa = [0 if x == cidade_atual else x for x in Cidades_disponiveis[formiga]]
        # Cidades_disponiveis[formiga] = linha_limpa

        if passo == 1:
            cidade_atual = 1
            # '''Inicia todas as formigas em cidades aleatorias'''
            Matriz_Infor[formiga, 0] = random.choice(Layers_disponiveis[formiga])

            # '''Define a cidade atual como a cidade aleatoria sorteada'''
            layer_atual = int(Matriz_Infor[formiga, 0])

            # print(f"tau {layer_atual}: \n{lista_tau[layer_atual-1]}")

        

        # '''Executa a partir da segunda cidade'''   
        else:
            cidade_atual = 2
            # layer_atual = int(Matriz_Infor[formiga, passo])    
            ...    

        print(f"cidade_atual: {cidade_atual}")
        # Cidades_disponiveis[formiga] = Remover_cidade(Cidades_disponiveis[formiga],2)

        Layers_disponiveis_list = (Layers_disponiveis[formiga] != 0).astype(int)

        # print(f"Layers_disponiveis_list\n{Layers_disponiveis_list}")

        # n_cidade_beta    = lista_n[layer_atual] ** beta
        # tau_cidade_alfa  = lista_tau[layer_atual] ** alfa
        
        matriz = lista_tau[layer_atual-1] ** alfa * lista_n[layer_atual-1] ** beta

        

        mascara_cidades_disponiveis = calcular_mascara_cidades_disponiveis(Cidades_disponiveis[formiga],cidade_atual, NCabos)

        numerador = matriz * mascara_cidades_disponiveis

        denominador = np.sum(numerador)

        # '''Calcula a probabilidade das proximas cidades'''
        probabilidade = matriz * 1/denominador  * mascara_cidades_disponiveis
        

    # print(f"Cidade atual: \n{cidade}")

        # Cidades_disponiveis_list = (Cidades_disponiveis[formiga] != 0).astype(int)
        # calcular_mascara_cidades_disponiveis(cidade_atual,Cidades_disponiveis[formiga])
        # print(f"Cidades_disponiveis_list atual: \n{Cidades_disponiveis_list}")



# print(f"Cidades_disponiveis: \n{Cidades_disponiveis}")
# # print(f"matriz {matriz.shape}")
print_matrix3d(matriz)
print('\n' + '='*50)
print_matrix3d(numerador)
print(f"denominador: { denominador}")
print_matrix3d(probabilidade)
print(f"probabilidade total: {np.sum(probabilidade)}")
# print(f"Matriz_Infor: \n{Matriz_Infor}")