# flake8: noqa
import numpy as np
import random


def criar_roleta(porcentagens):
    '''Espera receber um array de porcentagens por cidades e retorna uma lista de intervalos da roleta'''
    porcentagens = porcentagens * 100

    NCidades = d.shape[1]
    Cidades = list(range(0,NCidades))
   

    # Criar uma lista com todos os elementos (permite duplicatas)
    elementos_completos = list(zip(Cidades, porcentagens))
    
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
        # print(f"Elemento {indice} (valor {chave}): [{inicio:.2f} - {fim:.2f}] ({valor:.2f}%)")
        inicio = fim
        indice += 1

    # print(f"Soma total dos intervalos: {inicio:.2f}%")
    return intervalos

def girar_roleta(intervalos):
    valor_aleatorio = random.uniform(0, 100)

    # print(f"valor sorteado: {valor_aleatorio}")
    for inicio, fim, chave, indice in intervalos:
        if inicio <= valor_aleatorio < fim:
            return chave

    # Caso esteja exatamente no limite superior
    return intervalos[-1][2]


def matriz_caminho(caminho):
    NCidades = caminho.shape[0]
    matriz = np.zeros((NCidades, NCidades), dtype=int)

    # Extrair os pares consecutivos
    pares = [(int(caminho[i]), int(caminho[i+1])) for i in range(len(caminho)-1)]

    # Preencher com 1 nos pares especificados
    for i, j in pares:
        matriz[i-1, j-1] = 1  # -1 porque Python indexa de 0 e seus números são de 1-5
    return matriz




# ================================
# PARÂMETROS DO ALGORITMO
# ================================
q = 10      # Constante de atualização do feromônio
rho = 0.01    # Evaporação do feromônio
fer = 0.1   # Feromônio inicial
alfa = 1      # Parâmetro de influência de feromônio, inicial
beta = 2       # Parâmetro de influência de distância
err = 10**(-4)


# Matriz de distâncias
# d = np.array([
#         [0, 2, 9, 10, 7],
#         [1, 0, 6, 4, 3],
#         [15, 7, 0, 8, 3],
#         [6, 3, 12, 0, 11],
#         [9, 7, 5, 6, 0]
# ])


d = np.array([
    [0, 76.5, 27.2, 100.3, 127.5, 154.7, 181.9, 209.1],
    [76.5, 0, 44.2, 98.6, 125.8, 153, 180.2, 207.4],
    [27.2, 44.2, 0, 107.1, 134.3, 161.5, 188.7, 215.9],
    [100.3, 98.6, 107.1, 0, 27.2, 54.4, 81.6, 108.8],
    [127.5, 125.8, 134.3, 27.2, 0, 27.2, 54.4, 81.6],
    [154.7, 153, 161.5, 54.4, 27.2, 0, 27.2, 54.4],
    [181.9, 180.2, 188.7, 81.6, 54.4, 27.2, 0, 27.2],
    [209.1, 207.4, 215.9, 108.8, 81.6, 54.4, 27.2, 0]
])






CIDADES = ['A', 'B', 'C', 'D', 'E']

NCidades = d.shape[0]

# ================================
# INICIALIZAÇÃO
# ================================
num_formigas = 10                                            # Número de formigas, duas por cidade
tau = np.ones((NCidades, NCidades)) * 0.001                  # Deposição inicial de feromonio
Matriz_Infor = np.zeros((num_formigas, NCidades))            # Caminho das formigas
Matriz_Infor_Temp = Matriz_Infor.copy()                      # Informativo das cidades
iteracoes = 10                                               # Número de iterações
prob = np.zeros((num_formigas, NCidades))                    # Matriz probabilidade

K = d + np.eye(NCidades, NCidades)                           # Matriz auxiliar para somar zeros

m1 = K**(-1)                                                 # Invertendo termos da matriz auxiliar
n1 = m1 - np.eye(NCidades, NCidades)                         # Matriz de termos inversos a distância


# print(f"d: \n {d}")
# print(f"Feromonio: \n {Feromonio}")
# print(f"n: \n {n1}")

melhor_resultado = [ np.inf , [] ]

print(f"melhor: {melhor_resultado}")

# Cidades_disponiveis = list(range(0,NCidades))



for iteracao in range(iteracoes):
    print(f" ===== iteração: {iteracao} =====")   
    # '''Reinicia a matriz de cidades disponíveis a cada iteração'''
    Cidades_disponiveis = np.tile(np.arange(1,NCidades+1),(num_formigas,1))   
    
    FuncObj = np.zeros((num_formigas,1))
    # print(f"FuncObj: {FuncObj}")


    # '''Itera as formigas sobre as cidades que devem ser percorridas'''
    for cidade in range(NCidades-1):
        # '''Cabeçalho para debug de codigo'''

        # print(f" ===== Cidade: {cidade} | iteração: {iteracao} =====")   

        # '''Itera sobre as formigas, calculando a proxima cidade com base na cidade atual'''
        for formiga in range(num_formigas):
            # print(f"====== Formiga {formiga} ======")

            

            # '''Starta a matriz de probabilidades como zeros'''
            probabilidade = [0] * NCidades
            
            # '''Starta a primeira cidade, executa apenas na primeira cidade'''
            if cidade == 0:
                
                # '''Inicia todas as formigas em cidades aleatorias'''
                Matriz_Infor[formiga, 0] = random.choice(Cidades_disponiveis[formiga])

                # '''Define a cidade atual como a cidade aleatoria sorteada'''
                Cidade_atual = int(Matriz_Infor[formiga, 0])

            # '''Executa a partir da segunda cidade'''    
            else:
                # '''Define a cidade atual de acordo com o ja estabelecido'''
                Cidade_atual = int(Matriz_Infor[formiga, cidade])

            # print(f"Cidade_atual: {Cidade_atual}")
            # print(f"Cidades_disponiveis: {Cidades_disponiveis[formiga]}")

            # '''Cria mascara de cidades disponiveis, 0 para cidade indisponivel, 1 para cidade disponivel'''
            Cidades_disponiveis_list = (Cidades_disponiveis[formiga] != 0).astype(int)

            # '''Eleva todos os itens da matriz n por beta'''
            n_cidade_beta = n1[Cidade_atual-1,:] ** beta

            # '''Eleva todos os itens da matriz tau por alfa'''
            tau_cidade_alfa = tau[Cidade_atual-1,:] ** alfa

            # '''Cria a matriz n^beta * tau^alfa'''
            matriz = tau **alfa * n1 ** beta
                    
            # '''Calcula o numerador da propabilidade com mascara de cidades disponiveis'''
            numerador = matriz[Cidade_atual-1] * Cidades_disponiveis_list

            # '''Calcula o denominador da propabilidade com mascara de cidades disponiveis'''
            denominador = matriz[Cidade_atual-1] * Cidades_disponiveis_list

            # '''Soma todos os denominadores da matriz de probabilidade'''
            denominador = np.sum(denominador)


            # '''Calcula a probabilidade das proximas cidades'''
            probabilidade = matriz[Cidade_atual-1] * 1/denominador  * Cidades_disponiveis_list
            
            # print(f"Denominador: {denominador}")
            
            # print(f"probabilidade: {probabilidade}")
            # print(f"probabilidade total: {sum(probabilidade)}")

            # '''Cria roleta com intervalos para cada probabilidade'''
            intervalos = criar_roleta(probabilidade)

            # '''Gira a roleta e obtem o valor sorteado para proxima cidade'''
            sorteado = girar_roleta(intervalos)

            # '''Define a proxima cidade como valor sorteado, +1 para correção da indexação de listas no python'''
            Cidade_proxima = sorteado + 1 

            
            # print(f"Proxima cidade: {Cidade_proxima}")

            # '''Indexa a proxima cidade sorteada a matriz de caminhos'''
            Matriz_Infor[formiga, cidade + 1 ] = Cidade_proxima

    
            # '''Elimina as cidades já visitadas da matriz de cidades disponíveis '''
            linha_limpa = [0 if x == Cidade_atual else x for x in Cidades_disponiveis[formiga]]
            Cidades_disponiveis[formiga] = linha_limpa

            FuncObj[formiga] = FuncObj[formiga] + d[Cidade_atual-1 , Cidade_proxima-1 ] 
            # print(f"FuncObj[{formiga}]: {FuncObj[formiga]}")


            # print(f"\n")

    print(f"FuncObj: \n {FuncObj}")

    indice_menor_valor = np.argmin(FuncObj)

    novo_melhor_resultado = [ FuncObj[indice_menor_valor].tolist()[0] , Matriz_Infor[indice_menor_valor].tolist() ]

    if novo_melhor_resultado[0] < melhor_resultado[0]:
        melhor_resultado = novo_melhor_resultado



    print(f"Menor valor: {FuncObj[indice_menor_valor]}")
    print(f"Cidades menor valor:  {Matriz_Infor[indice_menor_valor]}")

    print(f"Melhor resultado:  {melhor_resultado}")

    delta_tau = np.zeros((NCidades, NCidades))

    for formiga in range(num_formigas):

        # print(f"========= Matriz_Infor[{formiga}] ========= \n {Matriz_Infor[formiga]}")

        delta_tau = delta_tau + matriz_caminho(Matriz_Infor[formiga]) * 1/FuncObj[formiga]
        
        # print(matriz_caminho(Matriz_Infor[formiga]))
        # #     # print(n_cidade_beta)    
        # #     # print(f"formiga: {formiga}")

        # # # print(f"Cidades_disponíveis: {Cidades_disponíveis}")

    # print(f"========= tau ========= \n {tau}")

    # print(f"========= delta_tau ========= \n {delta_tau}")

    tau = (1-rho)*tau + delta_tau

    np.set_printoptions(precision=4, floatmode='fixed')
    print(f"========= tau ========= \n {tau}")

    print(f"========= Matriz_Infor ========= \n {Matriz_Infor}")
    
    
    
# ================================
# RESULTADOS FINAIS
# ================================
print('\n' + '='*50)
print('RESULTADO FINAL')
print('='*50)

print(f"O melhor resultado é: {melhor_resultado[0]:.2f}")
print(f"O melhor caminho é: {melhor_resultado[1]}")
