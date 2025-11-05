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
iteracoes = 2                                  # Número de iterações
prob = np.zeros((num_formigas, NCidades))                    # Matriz probabilidade

K = d + np.eye(NCidades, NCidades)                 # Matriz auxiliar para somar zeros

m1 = K**(-1)                                # Invertendo termos da matriz auxiliar
n1 = m1 - np.eye(NCidades, NCidades)        # Matriz de termos inversos a distância


# print(f"d: \n {d}")
# print(f"Feromonio: \n {Feromonio}")
# print(f"n: \n {n1}")



# Cidades_disponiveis = list(range(0,NCidades))
Cidades_disponiveis = np.tile(np.arange(1,NCidades+1),(num_formigas,1))   



# print(Matriz_Infor) 
for iteracao in range(iteracoes):



    # '''Matriz que armazena o percurso de cada formiga'''
    # Matriz_Infor = np.zeros((num_formigas, NCidades), dtype=int)

    # Cidades_disponiveis = np.tile(np.arange(1,NCidades+1),(num_formigas,1))

    # for cidade in Cidades_disponiveis:
    #     print(f"type cidade: {type(cidade)}")

    for formiga in range(num_formigas):
        print(f" ===== Formiga: {formiga}  iteração: {iteracao} =====")
        probabilidade = [0] * NCidades
        

        if iteracao == 0:


            # print(f"Cidades_disponíveis:\n {Cidades_disponiveis}")


            '''Inicia todas as formigas saindo da cidade 0'''
            Matriz_Infor[formiga, 0] = random.choice(Cidades_disponiveis[formiga])

            # lista = Cidades_disponiveis[formiga].tolist()
            # lista = [x for x in lista if x != 0]

            # Matriz_Infor[formiga, 0] = random.choice([x for x in lista if x != 0])

            

            Cidade_atual = int(Matriz_Infor[formiga, 0])
            
            


            # print(f"Cidade_atual:iteracao {Cidade_atual}") 
        else:
            # print(f"Cidades_disponíveis: {Cidades_disponiveis}")
            Cidade_atual = int(Matriz_Infor[formiga, iteracao])
            
            ...


        print(f"Cidade_atual: {Cidade_atual}") 


        # print(f"Cidades_disponíveis pré: \n{Cidades_disponiveis}")

        '''Elimina as cidades já visitadas da matriz de cidades disponíveis'''
        linha_limpa = [0 if x == Cidade_atual else x for x in Cidades_disponiveis[formiga]]
        print(f"linha_limpa: {linha_limpa}")
        Cidades_disponiveis[formiga] = linha_limpa





        print(f"Cidades_disponíveis pós: \n{Cidades_disponiveis}")
        # print(f"========= Matriz_Infor ========= \n {Matriz_Infor}")
        # Cidade_atual = int(Matriz_Infor[formiga, 0])

        
        

        # Cidades_disponiveis.remove(Cidade_atual)


        # 


        n_cidade_beta = n1[Cidade_atual-1,:] ** beta
        tau_cidade_alfa = tau[Cidade_atual-1,:] ** alfa


        # numerador = n_cidade_beta * tau_cidade_alfa

        # print(f"========= n1 ========= \n {n1}")

        # print(f"n_cidade_beta {Cidade_atual-1}  : {n_cidade_beta}")
        # print(f"tau_cidade_alfa {Cidade_atual-1}: {tau_cidade_alfa}")

        
        matriz = tau **alfa * n1 ** beta
        
        Cidades_unitarias = [0 if x == 0 else 1 for x in Cidades_disponiveis[formiga]]

        numerador = matriz[Cidade_atual-1] * Cidades_unitarias

        print(f"numerador {Cidade_atual-1}      : {numerador}")


        # denominador = np.sum(matriz[Cidade_atual-1, Cidades_disponiveis[formiga]-1])
        denominador = matriz[Cidade_atual-1]
        denominador = np.sum(matriz[Cidade_atual-1])

        # denominador_parcial = matriz[Cidade_atual-1, Cidades_disponiveis[formiga]-1]

        # print(f"Cidades_disponiveis[formiga]-1: {Cidades_disponiveis[formiga]-1}")
        # print(f"denominador_parcial: {denominador_parcial}") 

        probabilidade = matriz[Cidade_atual-1] * 1/denominador
        
        print(f"Cidades_disponiveis:\n {Cidades_disponiveis}") 

        

        # np.set_printoptions(precision=4, floatmode='fixed')
        # print(f"========= matriz ========= \n {matriz}")
        # print(f"matriz[{Cidade_atual}]: {matriz[Cidade_atual,:]}")
               
        # print(f"Cidade_atual: {Cidade_atual}") 
        # print(f"Cidades_disponíveis: {Cidades_disponiveis}")
        print(f"Denominador: {denominador}")
        print(f"probabilidade: {probabilidade}")
        print(f"probabilidade total: {sum(probabilidade)}")

        intervalos = criar_roleta(probabilidade)

        sorteado = girar_roleta(intervalos)

        Cidade_proxima = sorteado
        print(f"Cidade_atual: {Cidade_atual}")
        print(f"Cidade_proxima: {Cidade_proxima}")
        # print(f"========= Matriz_Infor pre locado========= \n {Matriz_Infor}")

        Matriz_Infor[formiga, iteracao + 1 ] = Cidade_proxima

        print(f"========= Matriz_Infor ========= \n {Matriz_Infor}")
 



        print(f"\n")





    # #     # Cidades_disponiveis.remove(Cidade_atual)





    # #     # print(n_cidade_beta)    
    # #     # print(f"formiga: {formiga}")

    # # # print(f"Cidades_disponíveis: {Cidades_disponíveis}")
    # print(Matriz_Infor) 
    print(f"iteracao:{iteracao}") 