# flake8: noqa
import numpy as np
import matplotlib.pyplot as plt
import random


def criar_roleta(elemento, porcentagem):
    # Criar uma lista com todos os elementos (permite duplicatas)
    elementos_completos = list(zip(elemento, porcentagem))
    
    # Ordenar por porcentagem
    elementos_ordenados = sorted(elementos_completos, key=lambda x: x[1])
    
    # Criar intervalos
    intervalos = []
    inicio = 0
    indice = 0

    # print("\nIntervalos da roleta (com duplicatas):")
    for chave, valor in elementos_ordenados:
        fim = inicio + valor
        # Usar índice para garantir unicidade mesmo com chaves duplicadas
        intervalos.append((inicio, fim, chave, indice))
        print(f"Elemento {indice} (valor {chave}): [{inicio:.2f} - {fim:.2f}] ({valor:.2f}%)")
        inicio = fim
        indice += 1

    # print(f"Soma total dos intervalos: {inicio:.2f}%")
    return intervalos


def girar_roleta(intervalos):

    valor_aleatorio = random.uniform(0, 100)
    print(f"Valor roletado: {valor_aleatorio}")
    for inicio, fim, chave, indice in intervalos:
        if inicio <= valor_aleatorio < fim:
            return chave

    # Caso esteja exatamente no limite superior
    return intervalos[-1][2]



def _invert_matriz(matriz_2d):
    # Cria array de zeros com o mesmo shape e dtype float
    invertida = np.zeros_like(matriz_2d, dtype=float)
    
    # Aplica a inversão apenas onde não é zero
    mask = matriz_2d != 0
    invertida[mask] = 1.0 / matriz_2d[mask]
    
    return invertida

    ...


def _calc_nij(matriz_2d):
    n_ij = _invert_matriz(matriz_2d)
    return n_ij


def _calc_percent(matriz_2d):
    soma_linhas = np.sum(matriz_2d, axis=1)
    diag_soma_linhas = np.diag(soma_linhas)
    S = _invert_matriz(diag_soma_linhas) 

    percent = np.dot(S, matriz_2d) * 100

    return percent


# DADOS DE ENTRADA
comprimento = np.array([
[ 0.0, 1.0, 2.2, 2.0, 4.1],
[ 1.0, 0.0, 1.4, 2.2, 4.0],
[ 2.2, 1.4, 0.0, 2.2, 3.2],
[ 2.0, 2.2, 2.2, 0.0, 2.2],
[ 4.1, 4.0, 3.2, 2.2, 0.0]
])

n_ij = _calc_nij(comprimento)

# print(n_ij)

S = _calc_percent(n_ij)

print(S)

for i in S:
    coluna = []
    for n_j in range(len(i)):
        coluna.append(n_j+1)
    
    # print(coluna)
    # print( i)


    intervalos = criar_roleta(coluna, i)
    print(girar_roleta(intervalos))
    
    # print (i)
    


# print(S)

