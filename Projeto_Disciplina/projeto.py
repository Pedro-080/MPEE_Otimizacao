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

def print_matrix3d_percent(matrix_3d,condutores=[]):
    # num_linhas =  matrix_3d.shape[0]
    # num_colunas =  matrix_3d.shape[1]
    soma_matrix_3d = np.sum(matrix_3d)
    # print(f"soma_matrix_3d percent: {soma_matrix_3d}")

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

        # valor = matrix_3d[:,:,layer]/soma_matrix_3d
        # Substituir zeros usando np.where()
        # arr_str = np.where(arr == 0, '-', arr.astype(str))
        
        print(matrix_3d[:,:,layer]/soma_matrix_3d)



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

def criar_roleta_3d(probabilidade,Debug_Roleta = False):
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
            if Debug_Roleta:
                # print('============ ROLETA ============')
                print(f"Elemento {indice+1} (coord {coordenada_print}): [{inicio:.4f} - {fim:.4f}] ({probabilidade:.4f}%)")
            inicio = fim
            indice += 1
    
    # print(f"Soma total dos intervalos: {inicio:.4f}%")
    return intervalos

def girar_roleta(intervalos,Debug_Roleta = False):
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

    if Debug_Roleta:
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
# INFORMAÇÃO DOS CIRCUITOS
# ================================
'''Matriz com a distancia entre cada vértice'''
# Ainda é preciso tratar o codigo para permitir matrizes não padroes
comprimento = np.array([
    [    0, 1000,    0,    0,    0 ],
    [    0,    0, 3000,    0,    0],
    [    0,   0,    0, 5000,    0],
    [    0,   0,    0,    0, 1000],
    [    0,    0,    0,    0,    0]
])

'''Matriz com agrupamento entre cada vértice'''
agrupamento = np.array([
    [    0,    1,    0,    0,    0],
    [    0,    0,    2,    0,    0],
    [    0,    0,    0,    3,    0],
    [    0,    0,    0,    0,    3],
    [    0,    0,    0,    0,    0]
])


# ================================
# DADOS DO CIRCUITO
# ================================
Pot_aero_MW  = 6                                          # Potencia por aerogerador
Pot_circ_MW  = np.max(agrupamento) * Pot_aero_MW          # Potencia total do circuito
Pot_circ_MWh_ano = Pot_circ_MW * 24 * 365                 # Potencia total máxima gerada por ano a 100% 
FP           = 0.95                                       # Fator de potencia 
FC       = 1                                              # Fator de capacidade considerado. 1 = 100%
perda_maxima_percent = 2                                  # Pedra máxima global tolerada em porcentagem.  2 = 2%
Vida_util_anos = 30                                       # Vida util considerada para o empreendimento. 30 = 30 anos

Custo_ton_Al = 15000                                      # Custo por tonelada de aluminio. 15000 = 15000   R$/ton
Preco_MHh = 386.41                                        # Preço da energia por MWh.        386.51 = 386.51 r$/kWh


# ================================
# PARÂMETROS DO ALGORITMO
# ================================
q = 1e5     #fator de multiplicação do ganho de feromonio delta_tau
rho = 0.6   # Evaporação do feromônio
fer = 0.1   # Feromônio inicial
fer_max = 2 * rho
alfa = 1      # Parâmetro de influência de feromônio, inicial
beta = 5       # Parâmetro de influência de distância

iteracoes = 50                                              # Número de iterações
num_formigas = 5                                             # Número de formigas, duas por cidade

# ================================
# PARÂMETROS DE DEBUG!!!
# ================================

Debug_Roleta     = False       #True para exibir, False para não exibir
Debug_tau        = True      #True para exibir, False para não exibir
Debug_formiga    = False      #True para exibir, False para não exibir
Debug_layers     = True      #True para exibir, False para não exibir
Debug_delta_tau  = True


condutores = ['OXLIP', 'ORCHID',  'MARIGOLD']

Pot_acumulado_MW_3d = agrupamento * Pot_aero_MW



perdas_OXLIP      = OXLIP.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW_3d, Pot_circ_MW, FP, FC)
perdas_ORCHID     = ORCHID.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW_3d, Pot_circ_MW, FP, FC)
perdas_MARIGOLD   = MARIGOLD.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW_3d, Pot_circ_MW, FP, FC)

peso_OXLIP        = OXLIP.array_calcular_massa_ton(comprimento)
peso_ORCHID       = ORCHID.array_calcular_massa_ton(comprimento)
peso_MARIGOLD     = MARIGOLD  .array_calcular_massa_ton(comprimento)



pesos = np.stack([
    peso_OXLIP,
    peso_ORCHID,
    peso_MARIGOLD
], axis=2)


perdas = np.stack([
    perdas_OXLIP,
    perdas_ORCHID,
    perdas_MARIGOLD
], axis=2)

# print("========= Perdas =========")
# print_matrix3d(perdas,condutores)

NCidades = comprimento.shape[0]
NCabos   = pesos.shape[2]


tau = np.ones((NCidades, NCidades,NCabos)) * fer         # Deposição inicial de feromonio
comprimento_3d = np.stack([comprimento]*NCabos, axis = 2)



"""
Debug de variáveis de custo

Args:
    comprimento_3d   : Matriz empilhada das distancias consideradas, distancias em metros (m).
    pesos            : Matriz empilhada dos pesos totais calculados, pesos em toneladas (ton).
    Custo_ton_Al     : Custo por tonelada de alumínio, em ($/ton).

    perdas           : Matriz empilhada com as perdas percentuais, perdas em porcentagem (%).
    Pot_circ_MWh_ano : Potencia total calculada para o circuito, em (MWh/ano).
    FC               : Fator de capacidade utilizado na análise, adimensional.
    Preco_MHh        : Preço por MHh estimado, ($/MWh)
    Vida_util_anos   : Tempo de vida do empreendimento, em anos (ano)

"""



'''O custo está sendo calculado usando apenas o preço do aluminio'''
Custo_peso_cabos = pesos * Custo_ton_Al
Custo_perdas     = perdas/100 * Pot_circ_MWh_ano * FC * Preco_MHh

Custo = Custo_peso_cabos #+ Custo_perdas




# print(f"Pot_circ_MWh_ano: {Pot_circ_MWh_ano}")

# print("=========== Custos perdas ============")
# print_matrix3d(Custo_perdas,condutores)

# print("=========== Custos cabos ============")
# print_matrix3d(Custo_peso_cabos,condutores)

# print("=========== Custos total ============")
# print_matrix3d(Custo,condutores)


n = calcular_n(Custo)                                        # Matriz de termos inversos a distância


linhas, colunas = np.where(comprimento != 0)               #Extrai as cidades, duplicando a que possuem multiplos caminhos
colunas = np.add(colunas,1)                                #Adiciona 1 ao índice de todas as cidades, evitando começar em 0
colunas = np.insert(colunas,0,1)                           #Adiciona a primeira cidade como 1

N_cidades_totais = len(colunas.tolist())                                           #Conta o numero de cidades mesmo que duplicadas
Layers_disponiveis = np.tile(np.arange(1,NCabos+1),(num_formigas,1))  

'''Versão correta - Descomentar apos testes'''
'''É preciso alterar o codigo para permitir o uso de matrizes não padrões'''
num_passos = np.count_nonzero(comprimento)
# print(f"num_passos pre: {num_passos}")
# num_passos = 4


melhor_resultado = [ np.inf , [] , [], np.inf]  #massa total, layers percorridos, caminho percorrido, perda total

top_resultados = np.zeros((10,4))       # [[vertices], [condutores],[preco_rateado],[preco_final]

# print(f"top results: {top_10_resultados}")

for iteracao in range(1,iteracoes+1):
    print('='*40 +"Iteração: "+ str(iteracao) + '='*40)
    Matriz_layer = np.zeros((num_formigas, N_cidades_totais),dtype = int)                     # Caminho das formigas pelos layers
    Matriz_cidades = np.zeros((num_formigas, len(colunas.tolist())),dtype = int)              # Caminho das formigas pelos layers
    
    Layers_disponiveis = np.tile(np.arange(1,NCabos+1),(num_formigas,1))
    Cidades_disponiveis = np.tile(sorted(colunas.tolist()),(num_formigas,1)) 

    for passo in range(1, num_passos+1):
        # print(f"passo atual:{passo}")


        for formiga in range(num_formigas):
            if Debug_formiga:
                print('='*20 +"formiga: ["+ str(formiga) + "] - passo [" + str(passo) +"]" +'='*20)


            if passo == 1:
                cidade_atual = 1
                # '''Inicia todas as formigas em cidades aleatorias'''
                Matriz_layer[formiga, 0] = random.choice(Layers_disponiveis[formiga])
                Matriz_cidades[formiga, passo-1] = cidade_atual

                # '''Define a cidade atual como a cidade aleatoria sorteada'''
                cabo_atual = int(Matriz_layer[formiga, 0])

            # '''Executa a partir da segunda cidade'''   
            else:
                cidade_atual =  Matriz_cidades[formiga, passo-1]
        
            Cidades_disponiveis[formiga] = Remover_elemento(Cidades_disponiveis[formiga],cidade_atual)

                
            '''Remove os cabos inferiores aos já escolhidos '''
            Layers_disponiveis[formiga] = np.where(Layers_disponiveis[formiga] < cabo_atual, 0, Layers_disponiveis[formiga])


            Layers_disponiveis_list = (Layers_disponiveis[formiga] != 0).astype(int)
            

            matriz = tau ** alfa * n ** beta
            
            mascara_cidades_disponiveis = calcular_mascara_cidades_disponiveis(Cidades_disponiveis[formiga],NCidades, Layers_disponiveis_list)


            numerador = matriz * mascara_cidades_disponiveis
            denominador = np.sum(numerador)

            # print(f"Cidades_disponiveis[formiga]: {Cidades_disponiveis[formiga]}")
            # print_matrix3d(mascara_cidades_disponiveis,condutores)

            '''Calcula a probabilidade das proximas cidades'''
            probabilidade = matriz * 1/denominador  * mascara_cidades_disponiveis
            
            # print('='*50)
            # print_matrix3d(probabilidade)
            # print('='*50)

            # print(f"Layers_disponiveis[{formiga}]: {Layers_disponiveis[formiga]}")
            # print(f"Cidade atual: {cidade_atual}")
            # print(f"cabo_atual: {cabo_atual}")

            intervalos = criar_roleta_3d(probabilidade, Debug_Roleta)
            proxima_cidade, proximo_cabo = girar_roleta(intervalos, Debug_Roleta)
            proxima_cidade = proxima_cidade + 1                                     #corrige o indice        
            proximo_cabo = proximo_cabo + 1                                         #corrige o indice   

            Matriz_layer[formiga, passo] = proximo_cabo
            Matriz_cidades[formiga, passo] = proxima_cidade


            # FuncCusto[formiga, 0 ] = FuncCusto[formiga] + Custo[cidade_atual-1 , proxima_cidade-1 ,cabo_atual -1] 

            cabo_atual = proximo_cabo




    delta_tau = np.zeros((NCidades, NCidades, NCabos))

    Matriz_layer = Matriz_layer[:, :-1]
    # print_matrix3d(delta_tau)

    FuncCusto          = np.zeros((num_formigas,3))
    FuncPerdas_percent = np.zeros((num_formigas,1))


    


    for formiga in range(num_formigas):
        print(f"=== Matriz_layer[{formiga}] ===\n{Matriz_layer[formiga]}")

        caminhos   = Matriz_cidades[formiga]
        layers     = Matriz_layer[formiga]
        caminho_3d = matriz_caminho_3d(caminhos, layers,NCabos)

        '''Calcula o custo do aluminio'''
        Massa_total_Al = np.sum(caminho_3d * pesos)
        Custo_em_Al = Massa_total_Al * Custo_ton_Al
        FuncCusto[formiga, 0] = Custo_em_Al

        '''Calcula o custo das perdas'''
        perdas_formiga_percent = caminho_3d * perdas                               # Cria uma mascara da matriz de perdas em porcentagem
        perdas_formiga_MWh     = perdas_formiga_percent/100 * Pot_circ_MWh_ano         # Cria uma mascara da matriz de perdas em MWh
        perdas_totais_percent  = np.sum(perdas_formiga_percent)      
        perdas_totais_MWh      = np.sum(perdas_formiga_MWh)

        # print(f"perdas_totais_MWh: {perdas_totais_MWh}")
        # print_matrix3d(perdas_formiga_MWh,condutores)


        # perdas_MWh_ano = perdas_totais_percent/100 * Pot_circ_MWh_ano * FC

        FuncPerdas_percent[formiga] = perdas_totais_percent

        Custo_perdas       = perdas_formiga_MWh  * Preco_MHh * FC #* Vida_util_anos
        Custo_perdas_valor = np.sum(Custo_perdas)

        # print("=========== INICIO DEBUG Custo_perdas ============")

        # print_matrix3d(Custo_perdas,condutores)


        # print(f"Custo_perdas minimizado: {Custo_perdas}")
        
        # print(f"type(Custo_perdas): {type(Custo_perdas)}")

        if perdas_totais_percent > perda_maxima_percent:
            # print(f"calculo de perdas: {perdas_totais_percent:.2f}-{perda_maxima_percent:.2f}={perdas_totais_percent - perda_maxima_percent}")
            # perda_excedente_percent = (perdas_totais_percent - perda_maxima_percent)
            '''Comentado para teste'''
            # FuncCusto[formiga, 1] =  Custo_perdas_valor
            FuncCusto[formiga, 1] = 2 * Custo_em_Al
        else:
            FuncCusto[formiga, 1] = 0

        
        

        # print(f"Pot_circ_MW: {Pot_circ_MW}")
        
        # print(f"Peso em Al: {Massa_total_Al:.2f}ton - Custo Aluminio: ${Custo_em_Al:,.2f}")
        # print(f"Perda total: {perdas_totais_percent:.2f}% - Perda total: {perdas_MWh_ano  }MWh/ano - Custo com perda: ${(Custo_perda):,.2f}")
        # print(f"Custo total: ${np.sum(FuncCusto[formiga, :]):,.2f}")

        
        # caminho_3d = matriz_caminho_3d(caminhos, layers,NCabos)
        # print(f"shape matriz_caminho_3d: {caminho_3d.shape}")
        # print("matriz_caminho_3d")
        # print_matrix3d(caminho_3d,condutores)
        
        FuncCusto[:, -1] = np.sum(FuncCusto[:, :-1], axis=1)     # Define a ultima coluna como a soma das colunas anteriores

        print(f"custo total aqui: {FuncCusto[formiga, -1]}")

        # print(f"total em Al :{Massa_total_Al:.4f} ton")
        # print(f"Custo em Al da formiga :[{formiga:02d}]: {Custo_em_Al:.4f}")

        # print_matrix3d(perdas_formiga_percent)
        # print(f"Perdas totais: {perdas_totais}")

        delta_tau = delta_tau + caminho_3d  * q /(FuncCusto[formiga, -1])

        # if perdas_totais <= perda_maxima_percent:
        #     print(f"perdas_totais: {perdas_totais}")
        #     delta_tau = delta_tau + caminho_3d  * 1/FuncCusto[formiga]

    

    indice_menor_valor = np.argmin(FuncCusto[:,-1])
    print(f"indice_menor_valor: {indice_menor_valor}")

    novo_melhor_resultado = [ FuncCusto[indice_menor_valor].tolist()[0] , Matriz_layer[indice_menor_valor].tolist(), Matriz_cidades[indice_menor_valor].tolist(), FuncPerdas_percent[indice_menor_valor,0]]

    

    #massa total, layers percorridos, caminho percorrido, perda total


    if novo_melhor_resultado[0] < melhor_resultado[0]:
        melhor_resultado = novo_melhor_resultado

    # teste = tau + delta_tau

    delta_tau = np.clip(delta_tau, None, fer_max)

    tau = (1-rho)*tau + delta_tau

    

    if Debug_tau:
        print('='*50)
        print(f"tau percent: ")
        print_matrix3d_percent(tau,condutores)
        # print(f"tau: ")
        # print_matrix3d(tau,condutores)

        print('='*50)

    if Debug_delta_tau:
        print('='*50)
        # print(f"delta_tau percent: ")
        # print_matrix3d_percent(delta_tau,condutores)
        print(f"delta_tau: ")
        print_matrix3d(delta_tau,condutores)

        print('='*50)

    # print(f"tau + delta tau :")
    # print_matrix3d(teste)

# print_matrix3d(probabilidade)
# print(f"probabilidade total: {np.sum(probabilidade)}")
    # print(f"Matriz_layer: \n{Matriz_layer}")
    if Debug_layers:
        print("=========== Layer percorridos ============")
        for index, layers in enumerate(Matriz_layer):
            print(f"Formiga [{index+1:02d}]: {layers}")

    print("=========== FuncCusto ============")
    print(FuncCusto)

    print("=========== FuncPerdas_percent ============")
    print(FuncPerdas_percent)

# print(f"proxima_cidade: {proxima_cidade}")
# print(f"proximo_cabo: {proximo_cabo}")




# ================================
# RESULTADOS FINAIS
# ================================
# melhor_resultado[1].pop()
# melhor_resultado[1] = melhor_resultado[1][-1]


print('\n' + '='*50)
print('RESULTADO FINAL')
print('='*50)

print(f"O melhor resultado é: {melhor_resultado[0]:.4f}")
print(f"A uma perda percentual de: {melhor_resultado[3]:.2f}%")
print(f"O melhor caminho é através dos condutores: {melhor_resultado[1]:}")
print(f"O melhor caminho é através dos vértices  : {melhor_resultado[2]}")

