# flake8: noqa
from cabos import OXLIP, GOLDENTUFT, COSMOS, ORCHID, ARBUTUS , ANEMONE, MAGNOLIA, MARIGOLD
import numpy as np
import pandas as pd
import random
import sys
import matplotlib.pyplot as plt
import heapq

def calcular_mascara_cidades_disponiveis(Cidades_disponiveis,num_cidades, Layers_disponiveis_list):


    Cidades_disponiveis_index = np.unique(Cidades_disponiveis)
    Cidades_disponiveis_index = Cidades_disponiveis_index[Cidades_disponiveis_index != 0]
    Cidades_disponiveis_index = np.subtract(Cidades_disponiveis_index, 1)


    range_cidades = [x for x in range(0,num_cidades)]
    Cidades_disponiveis_index = Cidades_disponiveis_index.tolist()

    lista_cidades = []

    for cidade in range_cidades:
        if cidade in Cidades_disponiveis_index:
            lista_cidades.append(1)
        else:
            lista_cidades.append(0)

    base = np.zeros((NCidades,NCidades),dtype=int)
    base[cidade_atual-1] = lista_cidades
    
    matriz = np.stack([base]*7,axis=2)

    matriz = base[:, :, np.newaxis] * Layers_disponiveis_list[np.newaxis, np.newaxis, :]

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

    num_layers = matrix_3d.shape[2]

    for layer in range(num_layers):
        if condutores != []:
            print(f'Condutor: {condutores[layer]}')
        else:
            print(f'index {layer}')
        np.set_printoptions(precision=4, floatmode='fixed')
        print(matrix_3d[:,:,layer])

def print_matrix3d_percent(matrix_3d,condutores=[]):

    soma_matrix_3d = np.sum(matrix_3d)


    num_layers = matrix_3d.shape[2]


    for layer in range(num_layers):
        if condutores != []:
            print(f'Condutor: {condutores[layer]}')
        else:
            print(f'index {layer}')
        np.set_printoptions(precision=4, floatmode='fixed')
        
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

    # if Debug_Roleta:
    #     print(f"Valor sorteado: {valor_aleatorio:.4f}")
    #     print("=" * 50)
    for inicio, fim, coordenada, indice in intervalos:
        if inicio <= valor_aleatorio < fim:
            cidade_escolhida = coordenada[1]
            layer_escolhida = coordenada[2]
            if Debug_Roleta:
                print(f"Valor sorteado: {valor_aleatorio:.4f} - layer selecionado {layer_escolhida+1}")
                print("=" * 50)
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

def display_matrix3d_compact(matrix_3d, condutores=None, titulo = None,n_samples=5, start_index=1, zero_as_dash=True):
    """
    Exibe amostra do array 3D de forma compacta.
    
    Parâmetros:
    -----------
    matrix_3d : array 3D numpy
        Array tridimensional a ser exibido
    condutores : list, opcional
        Nomes das camadas/layers
    n_samples : int, default=5
        Número de linhas a serem mostradas
    start_index : int, default=1
        Índice inicial (0 ou 1) para linhas e colunas
    zero_as_dash : bool, default=True
        Se True, substitui valores 0 por "-"
    """

    
    n_linhas, n_colunas, n_layers = matrix_3d.shape
    
    # print(f"📊 Array 3D - Shape: {matrix_3d.shape}")
    print("=" * 50)
    if titulo != None:
        print(f"Matriz de {titulo}")

    for layer in range(n_layers):
        layer_name = condutores[layer] if condutores and layer < len(condutores) else f'Layer_{layer}'
        
        # Pegar amostra das primeiras linhas
        sample_data = matrix_3d[:min(n_colunas, n_linhas), :, layer]
        
        # Criar DataFrame
        df_sample = pd.DataFrame(sample_data)
        
        # Ajustar índices se necessário
        if start_index == 1:
            df_sample.index = df_sample.index + 1
            df_sample.columns = df_sample.columns + 1
        
        print(f"\n🔹 {layer_name}")

        if n_linhas > n_colunas:
            print(f"[Mostrando {n_colunas} de {n_linhas} linhas]")
        
        # Configurar formatação
        with pd.option_context('display.float_format', lambda x: f'{x:.4f}'):
            if zero_as_dash:
                # Criar cópia para não modificar os dados originais
                df_display = df_sample.copy()
                
                # Substituir valores próximos de zero por "-"
                # Usamos np.isclose para lidar com possíveis erros de ponto flutuante
                mask_zero = np.isclose(df_display.values, 0, atol=1e-10)
                df_display = df_display.astype(object)  # Converter para object para misturar strings e números
                df_display.values[mask_zero] = "-"
                
                print(df_display)
            else:
                print(df_sample)
    
    print("\n" + "=" * 50)

def gerar_graficos(dados_simulacao,num_formigas,top_melhores_iteracoes,top_melhores_perdas,top_melhores_custos):
    iteracoes = dados_simulacao[0]

    lista_de_formigas = list(range(num_formigas))
    lista_iteracoes = list(set(iteracoes))


    perdas_por_formiga = [[] for _ in range(num_formigas)]    
    custo_por_formiga  = [[] for _ in range(num_formigas)]    


    for formiga in lista_de_formigas:
        for index, formiga_atual in enumerate(dados_simulacao[1]):
            if formiga_atual == formiga:
                perdas_por_formiga[formiga].append(dados_simulacao[2][index])   
                custo_por_formiga[formiga].append(dados_simulacao[4][index]) 


    plt.figure(figsize=(12, 7))

    # Plotar múltiplas séries
    # PRIMEIRO GRÁFICO (acima)
    plt.subplot(2, 1, 1)  # 2 linhas, 1 coluna, gráfico 1
    plt.plot(lista_iteracoes, perdas_por_formiga[0], linestyle='-', linewidth=1, label='Formiga 0', color='blue')
    plt.plot(lista_iteracoes, perdas_por_formiga[1], linestyle='-', linewidth=1, label='Formiga 1', color='red')
    plt.plot(lista_iteracoes, perdas_por_formiga[2], linestyle='-', linewidth=1, label='Formiga 2', color='green')
    plt.plot(lista_iteracoes, perdas_por_formiga[3], linestyle='-', linewidth=1, label='Formiga 3', color='orange')
    plt.plot(lista_iteracoes, perdas_por_formiga[4], linestyle='-', linewidth=1, label='Formiga 4', color='gray')

    plt.title('Evolução das Perdas por Formiga', fontsize=16, fontweight='bold')
    plt.xlabel('Iteração', fontsize=14)
    plt.ylabel('Perdas', fontsize=14)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=12, loc='upper left')

    plt.plot(top_melhores_iteracoes, top_melhores_perdas,
            'ro',                    # 'r'=vermelho, 'o'=círculo, SEM '-' (sem linha)
            markersize=6,           # Tamanho do marcador
            markeredgecolor='black', # Cor da borda
            markeredgewidth=1,       # Espessura da borda
            label='Melhores pontos')


    # SEGUNDO GRÁFICO (abaixo)
    plt.subplot(2, 1, 2)  # 2 linhas, 1 coluna, gráfico 2
    plt.plot(lista_iteracoes, custo_por_formiga[0], linestyle='-', linewidth=1, label='Formiga 0', color='blue')
    plt.plot(lista_iteracoes, custo_por_formiga[1], linestyle='-', linewidth=1, label='Formiga 1', color='red')
    plt.plot(lista_iteracoes, custo_por_formiga[2], linestyle='-', linewidth=1, label='Formiga 2', color='green')
    plt.plot(lista_iteracoes, custo_por_formiga[3], linestyle='-', linewidth=1, label='Formiga 3', color='orange')
    plt.plot(lista_iteracoes, custo_por_formiga[4], linestyle='-', linewidth=1, label='Formiga 4', color='gray')

    plt.plot(top_melhores_iteracoes, top_melhores_custos,
            'ro',                    # 'r'=vermelho, 'o'=círculo, SEM '-' (sem linha)
            markersize=6,           # Tamanho do marcador
            markeredgecolor='black', # Cor da borda
            markeredgewidth=1,       # Espessura da borda
            label='Melhores pontos')


    plt.title('Custo por Formiga', fontsize=16, fontweight='bold')
    plt.xlabel('Iteração', fontsize=14)
    plt.ylabel('Custo R$', fontsize=14)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=12, loc='upper left')
    # ESCALA LOGARÍTMICA NO EIXO Y
    plt.yscale('log')


    # Ajustar layout para não sobrepor
    plt.tight_layout()
    plt.show()

def melhores_resultados(dados_simulacao, tamanho_podium=10):

    dados_iteracao = dados_simulacao[0]
    dados_formiga  = dados_simulacao[1]
    dados_perdas   = dados_simulacao[2]
    dados_layers   = dados_simulacao[3]
    dados_custos   = dados_simulacao[4]



    # Converter durante a ordenação
    combinados = list(zip(dados_iteracao,dados_formiga,dados_perdas, dados_layers, dados_custos))
    melhores = sorted(combinados, key=lambda x: float(x[4]))[:tamanho_podium]

    top_melhores_iteracoes = []
    top_melhores_perdas = []
    top_melhores_custos = []

    print(f"Os {tamanho_podium} melhores custos com suas ordens de introdução:")
    for iteracao, formiga, perda, layers, custo in melhores:
        top_melhores_iteracoes.append(iteracao)
        top_melhores_perdas.append(perda)
        top_melhores_custos.append(custo)
        print(f"• Custo R${custo:.2f} com perda {perda:.2f}% com as layers {layers} na iteracao {iteracao} da formiga {formiga}")

    return top_melhores_iteracoes, top_melhores_perdas, top_melhores_custos


# ================================
# INFORMAÇÃO DOS CIRCUITOS
# ================================
'''Matriz com a distancia entre cada vértice'''
# Ainda é preciso tratar o codigo para permitir matrizes não padroes
comprimento_c1 = np.array([
    [ 0.0,1000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0,1000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0,1000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0,1000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0,1000.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,1000.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,1000.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,1000.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,1000.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,1000.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
])

'''Matriz com agrupamento_c1 entre cada vértice'''
agrupamento_c1 = np.array([
    [ 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

])

# ================================
# DADOS DO CIRCUITO
# ================================
Pot_aero_MW  = 6                                          # Potencia por aerogerador
Pot_circ_MW  = np.max(agrupamento_c1) * Pot_aero_MW          # Potencia total do circuito
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
q = 1e3     #fator de multiplicação do ganho de feromonio delta_tau
rho = 0.5   # Evaporação do feromônio
fer = 0.0001   # Feromônio inicial
fer_max = 1

alfa = 1      # Parâmetro de influência de feromônio, inicial
beta = 9       # Parâmetro de influência de distância

iteracoes = 100                                                # Número de iterações
num_formigas = 5                                             # Número de formigas, duas por cidade

Fator_de_custo = 0.05


#ajuste fino de função escalonada
A_ajuste = 1    #controla o incremento vertical A(e^(bx)-1)
B_ajuste = 2    #controla o incremento exponencial



# ================================
# PARÂMETROS DE DEBUG!!!
# ================================

Debug_Roleta     = False    #True para exibir no log, as seleçoes da roleta
Debug_tau        = False    #True para exibir no log, os passos da matriz tau
Debug_formiga    = False    #True para exibir no log, os passos de cada formiga
Debug_layers     = False    #True para exibir no log, os cabos selecionados em cada iteracao
Debug_delta_tau  = True    #True para exibir no log, os passos da matriz delta_tau
Debug_perdas     = False    #True para exibir no log, a matriz de perdas em cada iteração
Debug_resultados = True     #True para exibir no log, todos os resultados

condutores = ['OXLIP','GOLDENTUFT', 'ORCHID', 'MAGNOLIA', 'MARIGOLD']

Pot_acumulado_MW_3d = agrupamento_c1 * Pot_aero_MW



perdas_OXLIP      = OXLIP.array_calcular_perdas_percent(comprimento_c1, Pot_acumulado_MW_3d, Pot_circ_MW, FP, FC)
perdas_GOLDENTUFT = GOLDENTUFT.array_calcular_perdas_percent(comprimento_c1, Pot_acumulado_MW_3d, Pot_circ_MW, FP, FC)
perdas_ORCHID     = ORCHID.array_calcular_perdas_percent(comprimento_c1, Pot_acumulado_MW_3d, Pot_circ_MW, FP, FC)
perdas_MAGNOLIA   = MAGNOLIA.array_calcular_perdas_percent(comprimento_c1, Pot_acumulado_MW_3d, Pot_circ_MW, FP, FC)
perdas_MARIGOLD   = MARIGOLD.array_calcular_perdas_percent(comprimento_c1, Pot_acumulado_MW_3d, Pot_circ_MW, FP, FC)

peso_OXLIP        = OXLIP.array_calcular_massa_ton(comprimento_c1)
peso_GOLDENTUFT   = GOLDENTUFT.array_calcular_massa_ton(comprimento_c1)
peso_ORCHID       = ORCHID.array_calcular_massa_ton(comprimento_c1)
peso_MAGNOLIA     = MAGNOLIA.array_calcular_massa_ton(comprimento_c1)
peso_MARIGOLD     = MARIGOLD.array_calcular_massa_ton(comprimento_c1)



pesos = np.stack([
    peso_OXLIP,
    peso_GOLDENTUFT,
    peso_ORCHID,
    peso_MAGNOLIA,
    peso_MARIGOLD
], axis=2)


perdas = np.stack([
    perdas_OXLIP,
    perdas_GOLDENTUFT,
    perdas_ORCHID,
    perdas_MAGNOLIA,
    perdas_MARIGOLD
], axis=2)


NCidades = comprimento_c1.shape[0]
NCabos   = pesos.shape[2]


tau = np.ones((NCidades, NCidades,NCabos)) * fer         # Deposição inicial de feromonio
comprimento_c1_3d = np.stack([comprimento_c1]*NCabos, axis = 2)




'''O custo está sendo calculado usando apenas o preço do aluminio'''
Custo_peso_cabos = pesos * Custo_ton_Al
Custo_perdas     = perdas/100 * Pot_circ_MWh_ano * FC * Preco_MHh * Fator_de_custo




Custo = Custo_peso_cabos + Custo_perdas


'''Descomentar para verificar as matrizes de custo de cabos e perdas'''
# display_matrix3d_compact(Custo_peso_cabos,condutores,"Custo cabos")
# display_matrix3d_compact(Custo_perdas,condutores,"Custo perdas")



n = calcular_n(Custo)                                        # Matriz de termos inversos a distância


linhas, colunas = np.where(comprimento_c1 != 0)               #Extrai as cidades, duplicando a que possuem multiplos caminhos
colunas = np.add(colunas,1)                                #Adiciona 1 ao índice de todas as cidades, evitando começar em 0
colunas = np.insert(colunas,0,1)                           #Adiciona a primeira cidade como 1

N_cidades_totais = len(colunas.tolist())                                           #Conta o numero de cidades mesmo que duplicadas
Layers_disponiveis = np.tile(np.arange(1,NCabos+1),(num_formigas,1))  


num_passos = np.count_nonzero(comprimento_c1)

melhor_resultado = [ np.inf , [] , [], np.inf]  #massa total, layers percorridos, caminho percorrido, perda total


contador_parada = 0


# Salva a referência original do stdout (o console)
stdout_original = sys.stdout

analise_perdas = []   #variavel auxiliar do Debug_resultado

dados_para_grafico = [[], [], [], [], []] # Matriz auxiliar para gerar graficos


# Abre o arquivo em modo de escrita ('w'). 
# Tudo o que for impresso a partir daqui será direcionado para ele.
with open('log_circuito_unico.txt', 'w', encoding='utf-8') as arquivo_log:
    sys.stdout = arquivo_log  # Redireciona stdout para o arquivo

    for iteracao in range(1,iteracoes+1):
        print('='*40 +"Iteração: "+ str(iteracao) + '='*40)
        Matriz_layer = np.zeros((num_formigas, N_cidades_totais-1),dtype = int)                     # Caminho das formigas pelos layers
        Matriz_cidades = np.zeros((num_formigas, len(colunas.tolist())),dtype = int)              # Caminho das formigas pelos layers
        
        Layers_disponiveis = np.tile(np.arange(1,NCabos+1),(num_formigas,1))
        Cidades_disponiveis = np.tile(sorted(colunas.tolist()),(num_formigas,1)) 

        for passo in range(1, num_passos+1):
            # print(f"passo atual:{passo}")


            for formiga in range(num_formigas):
                if Debug_formiga:
                    print('='*20 +"formiga: ["+ str(formiga) + "] - passo [" + str(passo) +"]" +'='*20)


                if passo == 1 :
                    cidade_atual = 1
                    # '''Inicia todas as formigas em cidades aleatorias'''
                    # Matriz_layer[formiga, 0] = random.choice(Layers_disponiveis[formiga])
                    
                    Matriz_cidades[formiga, passo-1] = cidade_atual

                    # '''Define a cidade atual como a cidade aleatoria sorteada'''
                    # cabo_atual = int(Matriz_layer[formiga, 0])

                # '''Executa a partir da segunda cidade'''   
                else:
                    cidade_atual =  Matriz_cidades[formiga, passo-1]

                # print(f"cidade_atual: {cidade_atual} ")
                # print(f"cabo_atual: {cabo_atual} ")

                Cidades_disponiveis[formiga] = Remover_elemento(Cidades_disponiveis[formiga],cidade_atual)

                maior_layer_atual = max(Matriz_layer[formiga])

                '''Remove os cabos inferiores aos já escolhidos, descomentar para testar '''
                Layers_disponiveis[formiga] = np.where(Layers_disponiveis[formiga] < maior_layer_atual, 0, Layers_disponiveis[formiga])


                Layers_disponiveis_list = (Layers_disponiveis[formiga] != 0).astype(int)
                

                matriz = tau ** alfa * n ** beta
                
                mascara_cidades_disponiveis = calcular_mascara_cidades_disponiveis(Cidades_disponiveis[formiga],NCidades, Layers_disponiveis_list)


                numerador = matriz * mascara_cidades_disponiveis
                denominador = np.sum(numerador)


                '''Calcula a probabilidade das proximas cidades'''
                probabilidade = matriz * 1/denominador  * mascara_cidades_disponiveis
                
                # display_matrix3d_compact(probabilidade,condutores,"Probabilidade")

                intervalos = criar_roleta_3d(probabilidade, Debug_Roleta)
                proxima_cidade, proximo_cabo = girar_roleta(intervalos, Debug_Roleta)
                # proxima_cidade, cabo_escolhido = girar_roleta(intervalos, Debug_Roleta)                
                
                proxima_cidade = proxima_cidade + 1                                     #corrige o indice        
                proximo_cabo = proximo_cabo + 1                                         #corrige o indice   

                Matriz_layer[formiga, passo-1] = proximo_cabo
                print(f"Matriz_layer: {Matriz_layer[formiga,:]}")

                Matriz_cidades[formiga, passo] = proxima_cidade

                cabo_atual = proximo_cabo

        


        delta_tau = np.zeros((NCidades, NCidades, NCabos))

        # Matriz_layer = Matriz_layer[:, :-1]   #Remove o ultimo elemento, não necessário!
        

        FuncCusto          = np.zeros((num_formigas,3))
        FuncPerdas_percent = np.zeros((num_formigas,1))

        for formiga in range(num_formigas):

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
            Custo_perdas  = perdas_totais_MWh * FC * Preco_MHh * Fator_de_custo

            FuncPerdas_percent[formiga] = perdas_totais_percent

            # Custo_perdas       = perdas_formiga_MWh  * Preco_MHh * FC #* Vida_util_anos
            Custo_perdas_valor = np.sum(Custo_perdas)

            if perdas_totais_percent > perda_maxima_percent:
                '''A função A(e^(B*x)-1) acrescenta um incremento exponencial para valores maiores que a perda maxima adimissivel'''
                FuncCusto[formiga, 1] = Custo_em_Al + Custo_perdas * A_ajuste*(np.exp(B_ajuste*(perdas_totais_percent-perda_maxima_percent)-1))
            else:
                FuncCusto[formiga, 1] = 0

            FuncCusto[:, -1] = np.sum(FuncCusto[:, :-1], axis=1)     # Define a ultima coluna como a soma das colunas anteriores

            if Debug_delta_tau:
                display_matrix3d_compact(delta_tau,condutores,"delta_tau")


            delta_tau = delta_tau + caminho_3d  * q /(FuncCusto[formiga, -1])

            analise_perdas.append(f"iteracao {iteracao} - formiga {formiga} - perdas {perdas_totais_percent:.2f} - layers {layers} - Custo {FuncCusto[formiga, -1]:.2f}")

            dados_para_grafico[0].append(iteracao)
            dados_para_grafico[1].append(formiga)
            dados_para_grafico[2].append(perdas_totais_percent)
            dados_para_grafico[3].append(layers)
            dados_para_grafico[4].append(FuncCusto[formiga, -1])
            


        indice_menor_valor = np.argmin(FuncCusto[:,-1])
        novo_melhor_resultado = [ FuncCusto[indice_menor_valor].tolist()[-1] , Matriz_layer[indice_menor_valor].tolist(), Matriz_cidades[indice_menor_valor].tolist(), FuncPerdas_percent[indice_menor_valor,0]]


        if novo_melhor_resultado[0] < melhor_resultado[0]:
            melhor_resultado = novo_melhor_resultado
            contador_parada = 0
        else:
            contador_parada+=1



        if contador_parada >= iteracoes * 0.5:
            print(f"Convergiu em {iteracao} iterações!")
            break

        # teste = tau + delta_tau

        delta_tau = np.clip(delta_tau, None, fer_max)

        tau = (1-rho)*tau + delta_tau

        if Debug_perdas:
            print(f"perdas percentuais: {FuncPerdas_percent}")

        if Debug_tau:
            # print('='*50)
            # print_matrix3d_percent(tau,condutores)
            display_matrix3d_compact(tau,condutores,"Tau")

            # print('='*50)

        if Debug_delta_tau:
            display_matrix3d_compact(delta_tau,condutores,"Delta tau")


        
        if Debug_layers:
            print("=========== Layer percorridos ============")
            for index, layers in enumerate(Matriz_layer):
                print(f"Formiga [{index+1:02d}]: {layers}")

    # Ao sair do bloco 'with', o arquivo é fechado automaticamente.
    # No entanto, o sys.stdout ainda aponta para ele, então restauramos explicitamente.



    if Debug_resultados:
        print('\n' + '='*50)
        print('RESULTADOS')
        print('='*50)
        for item in analise_perdas:
            print(item)

    sys.stdout = stdout_original




# Prints a partir daqui voltam a aparecer no console normalmente


print('\n' + '='*50)
print('RESULTADO FINAL')
print('='*50)

top_melhores_iteracoes, top_melhores_perdas, top_melhores_custos =  melhores_resultados(dados_para_grafico)

gerar_graficos(dados_para_grafico, 
                num_formigas, 
                top_melhores_iteracoes,
                top_melhores_perdas,
                top_melhores_custos
                )