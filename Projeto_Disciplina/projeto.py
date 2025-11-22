# flake8: noqa
from cabos import OXLIP, GOLDENTUFT, COSMOS, ORCHID, ARBUTUS , ANEMONE, MAGNOLIA, MARIGOLD
import numpy as np
import random


def calcular_mascara_cidades_disponiveis(Cidades_disponiveis,num_cidades, Layers_disponiveis_list):

    # print(f"Num cidades: {num_cidades}")
    # '''Esta função não está funcionando crretamente, corrigir!!!'''
    # Layers_disponiveis_list

    Cidades_disponiveis_index = np.unique(Cidades_disponiveis)
    Cidades_disponiveis_index = Cidades_disponiveis_index[Cidades_disponiveis_index != 0]
    Cidades_disponiveis_index = np.subtract(Cidades_disponiveis_index, 1)

    # print(f"Cidades_disponiveis_index pre: {Cidades_disponiveis_index}")
    # Cidades_disponiveis_index = np.insert(Cidades_disponiveis_index, 0, 0)

    range_cidades = [x for x in range(0,num_cidades)]
    Cidades_disponiveis_index = Cidades_disponiveis_index.tolist()


    # print(f"Cidades_disponiveis_index: {Cidades_disponiveis_index}")
    # print(f"range_cidades: {range_cidades}")
    lista_cidades = []

    for cidade in range_cidades:
        if cidade in Cidades_disponiveis_index:
            lista_cidades.append(1)
        else:
            lista_cidades.append(0)




    # print(f"Cidades_disponiveis_index:{Cidades_disponiveis_index}")

    # NCidades = len(Cidades_disponiveis_index)
    
    # Cidades_disponiveis_list = (Cidades_disponiveis_index != 0).astype(int)
    # print(f"Cidades_disponiveis_index:{Cidades_disponiveis_index}")
    # print(f"Cidades_disponiveis_lis:  {Cidades_disponiveis_list}")

    # #Cria a base que será usada 
    base = np.zeros((NCidades,NCidades),dtype=int)
    base[cidade_atual-1] = lista_cidades
    
    matriz = np.stack([base]*7,axis=2)

    # Modificação: criar matriz 3D com cada camada multiplicada pelo respectivo valor
    matriz = base[:, :, np.newaxis] * Layers_disponiveis_list[np.newaxis, np.newaxis, :]

    # matriz = base[np.newaxis, :, :] * Layers_disponiveis_list[:, np.newaxis, np.newaxis]

    # print(f"Cidades_disponiveis_list:{Cidades_disponiveis_list}")
    # print_matrix3d(matriz)
    # # print(matriz)
    # print('*'*50)
    return matriz

def matrix3d_fatiar_linha(linha, matrix3d):
    # Criar cópia zerada
    matriz_resultado = np.zeros_like(matrix3d)

    # Manter apenas a linha 0 (índice 0) de todos os layers
    matriz_resultado[linha-1, :, :] = matrix3d[linha-1, :, :]
    return matriz_resultado

def Remover_elemento(lista_cidades,cidade):
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

def criar_roleta_3d(probabilidade):
    """
    Cria uma roleta para uma matriz 3D de probabilidades
    Retorna uma lista de intervalos onde cada elemento tem sua faixa proporcional à probabilidade
    
    Args:
        matriz_3d: array numpy 3D onde a soma de todos os elementos é 1
    
    Returns:
        Lista de tuplas (inicio, fim, coordenadas, indice_original)
    """
    # Achatar a matriz para 1D mantendo as coordenadas originais
    probabilidades_flat = probabilidade.flatten()
    
    # Gerar coordenadas para cada elemento
    coordenadas = []
    shape = probabilidade.shape
    for idx in np.ndindex(shape):
        coordenadas.append(idx)
    
    # Converter para porcentagem
    probabilidades_porcentagem = probabilidades_flat * 100
    
    # Combinar coordenadas com probabilidades
    elementos_completos = list(zip(coordenadas, probabilidades_porcentagem))
    
    # Ordenar por probabilidade (do menor para o maior)
    elementos_ordenados = sorted(elementos_completos, key=lambda x: x[1])
    
    # Criar intervalos
    intervalos = []
    inicio = 0
    indice = 0
    
    # print(f"Matriz 3D shape: {shape}")
    # print(f"Total de elementos: {len(elementos_ordenados)}")
    # print("\nIntervalos da roleta:")
    
    for coordenada, probabilidade in elementos_ordenados:
        if probabilidade > 0:  # Ignorar elementos com probabilidade zero
            fim = inicio + probabilidade
            intervalos.append((inicio, fim, coordenada, indice))
            coordenada_print = tuple(x + 1 for x in coordenada)
            print(f"Elemento {indice+1} (coord {coordenada_print}): [{inicio:.4f} - {fim:.4f}] ({probabilidade:.4f}%)")
            inicio = fim
            indice += 1
    
    # print(f"Soma total dos intervalos: {inicio:.4f}%")
    return intervalos

def girar_roleta(intervalos):
    """
    Gira a roleta e retorna as coordenadas do elemento sorteado
    
    Args:
        intervalos: lista de intervalos retornada por criar_roleta_3d
    
    Returns:
        Tupla com coordenadas (i, j, k) do elemento sorteado
    """
    if not intervalos:
        raise ValueError("Lista de intervalos vazia")
    
    valor_aleatorio = random.uniform(0, 100)
    print(f"Valor sorteado: {valor_aleatorio:.4f}")
    
    for inicio, fim, coordenada, indice in intervalos:
        if inicio <= valor_aleatorio < fim:
            cidade_escolhida = coordenada[1]
            layer_escolhida = coordenada[2]
            return cidade_escolhida,layer_escolhida
    
    # Caso raro: valor exatamente no limite superior
    return intervalos[-1][2]

def matriz_caminho_3d(caminho, layers, Nlayers):
    layers = np.subtract(layers, 1)
    
    NCidades = caminho.shape[0]
    matriz_3d = np.zeros((NCidades, NCidades, Nlayers), dtype=int)
    
    pares_com_layers = []
    for i in range(len(caminho)-1):
        cidade_origem = int(caminho[i])
        cidade_destino = int(caminho[i+1])
        layer = int(layers[i])
        pares_com_layers.append((cidade_origem, cidade_destino, layer))
    
    for origem, destino, layer in pares_com_layers:
        matriz_3d[origem-1, destino-1, layer] = 1
    
    return matriz_3d

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

# condutores = ['OXLIP', 'GOLDENTUFT', 'COSMOS', 'ORCHID', 'ARBUTUS' , 'ANEMONE', 'MAGNOLIA', 'MARIGOLD']
condutores = ['OXLIP', 'ORCHID',  'MARIGOLD']

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
rho = 0.5   # Evaporação do feromônio
fer = 0.001   # Feromônio inicial
alfa = 1      # Parâmetro de influência de feromônio, inicial
beta = 5       # Parâmetro de influência de distância

iteracoes = 100                                                # Número de iterações
num_formigas = 20                                            # Número de formigas, duas por cidade

# pesos = np.stack([
#     peso_OXLIP,
#     peso_GOLDENTUFT,
#     peso_COSMOS,
#     peso_ORCHID,
#     peso_ARBUTUS,
#     peso_ANEMONE,
#     peso_MAGNOLIA,
#     peso_MARIGOLD
# ], axis=2)


pesos = np.stack([
    peso_OXLIP,
    peso_ORCHID,
    peso_MARIGOLD
], axis=2)



# print(f"matriz pesos: \n{pesos}")

# perdas = np.stack([
#     perdas_OXLIP,
#     perdas_GOLDENTUFT,
#     perdas_COSMOS,
#     perdas_ORCHID,
#     perdas_ARBUTUS,
#     perdas_ANEMONE,
#     perdas_MAGNOLIA,
#     perdas_MARIGOLD
# ], axis=2)

perdas = np.stack([
    perdas_OXLIP,
    perdas_ORCHID,
    perdas_MARIGOLD
], axis=2)




# print("perdas")
# print_matrix3d(perdas,condutores)

# print("pesos")
# print_matrix3d(pesos,condutores)
# teste = (0,1,7)
# print(pesos[teste])

NCidades = comprimento.shape[0]
NCabos   = pesos.shape[2]


# ================================
# INICIALIZAÇÃO
# ================================

tau = np.ones((NCidades, NCidades,NCabos)) * fer         # Deposição inicial de feromonio
n = calcular_n(pesos)                                        # Matriz de termos inversos a distância

# lista_tau = [tau] * NCabos
# lista_n   = [n] * NCabos

# print("Matriz n")
# print_matrix3d(n,condutores)



# print(lista_tau)

# K = pesos + np.eye(NCidades, NCidades,NCabos)              # Matriz auxiliar para somar zeros



# print(f"NCidades: {NCidades}")
# print(f"NCabos: {NCabos}")








# print(np.eye((NCidades, NCidades,NCabos)))
# print_matrix3d(pesos,condutores)





# print(f"Matriz_layer: \n{Matriz_layer}")
# print(f"Layers_disponiveis: \n{Layers_disponiveis}")


#Criando lista de cidades disponiveis
# Encontrar índices das colunas onde há valores não-zero

linhas, colunas = np.where(comprimento != 0)               #Extrai as cidades, duplicando a que possuem multiplos caminhos
colunas = np.add(colunas,1)                                #Adiciona 1 ao índice de todas as cidades, evitando começar em 0
colunas = np.insert(colunas,0,1)                           #Adiciona a primeira cidade como 1


# Ordenar pelas colunas (já vem ordenado por padrão)
# lista_resultado = sorted(colunas.tolist())

# print(f"colunas: {colunas}")





N_cidades_totais = len(colunas.tolist())                                           #Conta o numero de cidades mesmo que duplicadas
Layers_disponiveis = np.tile(np.arange(1,NCabos+1),(num_formigas,1))  






# Cidades_disponiveis = np.tile(np.arange(1,NCidades+1),(num_formigas,1))  

'''Versão correta - Descomentar apos testes'''
num_passos = np.count_nonzero(comprimento)
num_passos = 4

# print(f"Cidades_disponiveis no começo do codigo: \n{Cidades_disponiveis}")
# print(f"Num cidades totais: {N_cidades_totais}")
# print(f"Matriz_cidades: \n{Matriz_cidades}")

# print(f"num_passos:{num_passos}")

melhor_resultado = [ np.inf , [] ]


for iteracao in range(1,iteracoes+1):
    print('='*40 +"Iteração: "+ str(iteracao) + '='*40)
    Matriz_layer = np.zeros((num_formigas, N_cidades_totais),dtype = int)                     # Caminho das formigas pelos layers
    Matriz_cidades = np.zeros((num_formigas, len(colunas.tolist())),dtype = int)              # Caminho das formigas pelos layers
    FuncObj = np.zeros((num_formigas,1))
    Layers_disponiveis = np.tile(np.arange(1,NCabos+1),(num_formigas,1))
    Cidades_disponiveis = np.tile(sorted(colunas.tolist()),(num_formigas,1)) 

    for passo in range(1, num_passos+1):
        # print(f"passo atual:{passo}")


        for formiga in range(num_formigas):
            print('='*20 +"formiga: ["+ str(formiga) + "] - passo [" + str(passo) +"]" +'='*20)
            # print(f"Cidades_disponiveis no começo da formiga: \n{Cidades_disponiveis}")
            # linha_limpa = [0 if x == cidade_atual else x for x in Cidades_disponiveis[formiga]]
            # Cidades_disponiveis[formiga] = linha_limpa

            if passo == 1:
                cidade_atual = 1
                # '''Inicia todas as formigas em cidades aleatorias'''
                Matriz_layer[formiga, 0] = random.choice(Layers_disponiveis[formiga])
                Matriz_cidades[formiga, passo-1] = cidade_atual

                # '''Define a cidade atual como a cidade aleatoria sorteada'''
                cabo_atual = int(Matriz_layer[formiga, 0])

                # print(f"tau {cabo_atual}: \n{lista_tau[cabo_atual-1]}")

            

            # '''Executa a partir da segunda cidade'''   
            else:
                cidade_atual =  Matriz_cidades[formiga, passo-1]
        

            # print(f"cidade_atual: {cidade_atual}")

            Cidades_disponiveis[formiga] = Remover_elemento(Cidades_disponiveis[formiga],cidade_atual)
            # print(f"Cidades_disponiveis na formiga [{formiga}]: {Cidades_disponiveis[formiga]}")
            # print(f"Cabos usados na formiga [{formiga}]: {Matriz_layer[formiga]}")
                
            '''Remove os cabos inferiores aos já escolhidos '''
            # Layers_disponiveis[formiga] = np.where(Layers_disponiveis[formiga] < cabo_atual, 0, Layers_disponiveis[formiga])



            Layers_disponiveis_list = (Layers_disponiveis[formiga] != 0).astype(int)
            

            # 
            # print(f"Layers_disponiveis_list: {Layers_disponiveis_list}")
            # print(f"cabo_atual: {cabo_atual}")
            # print(f"resultado: {resultado}")
            # matriz = lista_tau[cabo_atual-1] ** alfa * lista_n[cabo_atual-1] ** beta
            matriz = tau ** alfa * n ** beta
            
            

            mascara_cidades_disponiveis = calcular_mascara_cidades_disponiveis(Cidades_disponiveis[formiga],NCidades, Layers_disponiveis_list)

            


            numerador = matriz * mascara_cidades_disponiveis

            

            denominador = np.sum(numerador)

            '''Calcula a probabilidade das proximas cidades'''
            probabilidade = matriz * 1/denominador  * mascara_cidades_disponiveis
            
            # print('='*50)
            # print_matrix3d(probabilidade)
            # print('='*50)

            # print(f"Layers_disponiveis[{formiga}]: {Layers_disponiveis[formiga]}")
            # print(f"Cidade atual: {cidade_atual}")
            # print(f"cabo_atual: {cabo_atual}")

            # print('============ ROLETA ============')

            intervalos = criar_roleta_3d(probabilidade)
            proxima_cidade, proximo_cabo = girar_roleta(intervalos)
            proxima_cidade = proxima_cidade + 1                                     #corrige o indice        
            proximo_cabo = proximo_cabo + 1                                         #corrige o indice   

            # print('='*50)

            
            # print(f"proxima_cidade: {proxima_cidade}")
            # print(f"proximo_cabo: {proximo_cabo}")
            

            # print_matrix3d(mascara_cidades_disponiveis)

            Matriz_layer[formiga, passo] = proximo_cabo
            Matriz_cidades[formiga, passo] = proxima_cidade

            FuncObj[formiga] = FuncObj[formiga] + pesos[cidade_atual-1 , proxima_cidade-1 ,cabo_atual -1] 

            # Cidades_disponiveis[formiga] = Remover_elemento(Cidades_disponiveis[formiga],cidade_atual)
            # print(f"Cidades_disponiveis aqui: \n{Cidades_disponiveis[formiga]}")


            cabo_atual = proximo_cabo
            # print(f'============ FIM DA FORMIGA ============')
        # print(f"Cidade atual: \n{cidade}")

            # Cidades_disponiveis_list = (Cidades_disponiveis[formiga] != 0).astype(int)
            # calcular_mascara_cidades_disponiveis(cidade_atual,Cidades_disponiveis[formiga])
            # print(f"Cidades_disponiveis_list atual: \n{Cidades_disponiveis_list}")

    indice_menor_valor = np.argmin(FuncObj)

    novo_melhor_resultado = [ FuncObj[indice_menor_valor].tolist()[0] , Matriz_layer[indice_menor_valor].tolist() ]

    if novo_melhor_resultado[0] < melhor_resultado[0]:
        melhor_resultado = novo_melhor_resultado

    delta_tau = np.zeros((NCidades, NCidades, NCabos))
    # lista_delta_tau = [delta_tau] * NCabos


    Matriz_layer = Matriz_layer[:, :-1]
    # print_matrix3d(delta_tau)


    for formiga in range(num_formigas):
        # print(f"=== Matriz_layer[formiga] ===\n{Matriz_layer[formiga]}")

        caminhos = Matriz_cidades[formiga]
        layers   = Matriz_layer[formiga]
        
        # caminho_3d = matriz_caminho_3d(caminhos, layers,NCabos)
        # print(f"shape matriz_caminho_3d: {caminho_3d.shape}")
        # print("matriz_caminho_3d")
        # print_matrix3d(caminho_3d)

        delta_tau = delta_tau + matriz_caminho_3d(caminhos, layers,NCabos) * 1/FuncObj[formiga]

        # print(caminho_3d)


        # for index, cabo_atual in enumerate(Matriz_layer[formiga]):
        #     de_cidade    = Matriz_cidades[formiga][index]
        #     para_cidade  = Matriz_cidades[formiga][index+1]
        #     # cabo_proximo = Matriz_layer[formiga][index+1]

        #     # lista_delta_tau[cabo_atual-1][de_cidade-1, para_cidade-1, cabo_proximo-1] = 1

        #     print(f"cabo_atual {cabo_atual} ")
        #     print(f"De {de_cidade} para {para_cidade}")
        #     # # lista_delta_tau[layer-1] = 

        #     # print()
        
        # print(f"Matriz_cidades[formiga]: \n{Matriz_cidades[formiga]}")
        # print('='*50)
        # print(f"Matriz_layer formiaga[{formiga}]: \n{Matriz_layer[formiga]}")
        # print(f"Matriz_cidades formiaga[{formiga}]: \n{Matriz_cidades[formiga]}")
        # print(f"delta_tau formiaga[{formiga}]")
        # print_matrix3d(delta_tau,condutores)
        # print('='*50)

        ...
    
    tau = (1-rho)*tau + delta_tau
    print('='*50)
    print(f"tau: ")
    print_matrix3d(tau,condutores)
    print('='*50)

    # for cabo in range(NCabos):
    

        # delta_tau = delta_tau + matriz_caminho(Matriz_Infor[formiga]) * 1/FuncObj[formiga]
        

# print(f"Cidades_disponiveis: \n{Cidades_disponiveis}")
# # print(f"matriz {matriz.shape}")
# print_matrix3d(matriz)
    print('\n' + '='*50 + '\n')
# # print_matrix3d(numerador)
# # print(f"denominador: { denominador}")
# print_matrix3d(probabilidade)
# print(f"probabilidade total: {np.sum(probabilidade)}")
    print(f"Matriz_layer: \n{Matriz_layer}")
    print(f"Matriz_cidades: \n{Matriz_cidades}")
    print(f"FuncObj: \n{FuncObj}")

# intervalos = criar_roleta_3d(probabilidade)




# proxima_cidade, proximo_cabo = girar_roleta(intervalos)

# print(f"proxima_cidade: {proxima_cidade}")
# print(f"proximo_cabo: {proximo_cabo}")


# ================================
# RESULTADOS FINAIS
# ================================
print('\n' + '='*50)
print('RESULTADO FINAL')
print('='*50)

print(f"O melhor resultado é: {melhor_resultado[0]:.2f}")
print(f"O melhor caminho é: {melhor_resultado[1]}")