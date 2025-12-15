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


def print_matrix3d_as_dataframe(matrix_3d, condutores=None, max_rows=10, precision=4):
    """
    Exibe um array 3D como DataFrames separados para cada layer/condutor.
    Similar à função print_matrix3d, mas usando DataFrames pandas.
    
    Args:
        matrix_3d: array numpy 3D shape (n_linhas, n_colunas, n_layers)
        condutores: lista de nomes dos condutores (opcional)
        max_rows: número máximo de linhas a exibir por DataFrame
        precision: número de casas decimais para floats
    """
    n_linhas, n_colunas, n_layers = matrix_3d.shape
    
    # Configurar opções de exibição do pandas
    pd.set_option('display.max_rows', max_rows)
    pd.set_option('display.precision', precision)
    pd.set_option('display.float_format', lambda x: f'{x:.{precision}f}')
    
    print(f"Array 3D shape: ({n_linhas}, {n_colunas}, {n_layers})")
    print(f"Total de elementos: {matrix_3d.size}")
    print("=" * 60)
    
    for layer in range(n_layers):
        print("\n" + "-" * 50)
        
        # Determinar o título
        if condutores is not None and len(condutores) > layer:
            title = f"Condutor: {condutores[layer]}"
        else:
            title = f"Layer {layer}"
        print(f"{title}")
        
        # Extrair a matriz 2D desta layer
        matrix_2d = matrix_3d[:, :, layer]
        
        # Criar DataFrame
        df = pd.DataFrame(matrix_2d)
        
        # Adicionar nomes às colunas e índice se for pequeno o suficiente
        if n_colunas <= 20:
            df.columns = [f'Col_{i}' for i in range(n_colunas)]
        
        if n_linhas <= 50:
            df.index = [f'Linha_{i}' for i in range(n_linhas)]
        
        # Exibir o DataFrame
        print(f"Shape: {matrix_2d.shape}")
        print(df)
        
        # Estatísticas básicas
        if n_linhas * n_colunas > 1:  # Só mostrar stats se tiver mais de 1 elemento
            print(f"\nEstatísticas:")
            print(f"  Média: {matrix_2d.mean():.{precision}f}")
            print(f"  Desvio padrão: {matrix_2d.std():.{precision}f}")
            print(f"  Mínimo: {matrix_2d.min():.{precision}f}")
            print(f"  Máximo: {matrix_2d.max():.{precision}f}")
    
    # Resetar configurações do pandas
    pd.reset_option('display.max_rows')
    pd.reset_option('display.precision')
    pd.reset_option('display.float_format')
    
    print("\n" + "=" * 60)
    print("Exibição concluída.")

# Função alternativa: DataFrame único com MultiIndex
def matrix3d_to_single_dataframe(matrix_3d, condutores=None):
    """
    Converte array 3D em um único DataFrame com MultiIndex.
    
    Args:
        matrix_3d: array numpy 3D shape (n_linhas, n_colunas, n_layers)
        condutores: lista de nomes dos condutores
    
    Returns:
        DataFrame com MultiIndex [layer, linha]
    """
    n_linhas, n_colunas, n_layers = matrix_3d.shape
    
    # Criar nomes padrão se não fornecidos
    if condutores is None:
        condutores = [f'Layer_{i}' for i in range(n_layers)]
    
    # Criar lista de DataFrames para cada layer
    dfs = []
    
    for layer in range(n_layers):
        # Criar DataFrame para esta layer
        df_layer = pd.DataFrame(matrix_3d[:, :, layer])
        
        # Adicionar coluna de layer
        df_layer['layer'] = condutores[layer] if layer < len(condutores) else f'Layer_{layer}'
        
        # Reset index para ter coluna de linha
        df_layer = df_layer.reset_index().rename(columns={'index': 'linha'})
        
        # Fazer melt para formato longo
        df_melted = df_layer.melt(
            id_vars=['layer', 'linha'],
            var_name='coluna',
            value_name='valor'
        )
        
        dfs.append(df_melted)
    
    # Concatenar todos os DataFrames
    df_final = pd.concat(dfs, ignore_index=True)
    
    # Reordenar colunas
    df_final = df_final[['layer', 'linha', 'coluna', 'valor']]
    
    return df_final

# # Função para exibição compacta
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
        sample_data = matrix_3d[:min(n_samples, n_linhas), :, layer]
        
        # Criar DataFrame
        df_sample = pd.DataFrame(sample_data)
        
        # Ajustar índices se necessário
        if start_index == 1:
            df_sample.index = df_sample.index + 1
            df_sample.columns = df_sample.columns + 1
        
        print(f"\n🔹 {layer_name}")

        if n_linhas > n_samples:
            print(f"[Mostrando {n_samples} de {n_linhas} linhas]")
        
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






def iniciar_circuito_01():
    comprimento = np.array([
    [    0, 1000,    0,    0,    0 ],
    [    0,    0, 3000,    10,    0],
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


    perdas_Circuito_01 = Circuito_01.perdas

    num_iteracoes = Circuito.ITERACOES

    for iteracao in range(1,num_iteracoes + 1):


        for passo_c1 in range(1,Circuito_01.num_passos +1 ):

            for formiga_c1 in range(Circuito_01.num_formigas):
                
                if passo_c1 == 1:
                    cidade_atual = 1

            ...
        ...

    linhas, colunas = np.where(Circuito_01.comprimento != 0)               #Extrai as cidades, duplicando a que possuem multiplos caminhos
    colunas = np.add(colunas,1)                                #Adiciona 1 ao índice de todas as cidades, evitando começar em 0
    colunas = np.insert(colunas,0,1)                           #Adiciona a primeira cidade como 1

    print(f"linhas: {linhas}")
    print(f"colunas: {colunas}")

    print(f"len(colunas.tolist(): {len(colunas.tolist())}")

    # Circuito_01.iterar_circuito()

    

    # print(f"numero de passos {Circuito_01.num_passos}")

    # Circuito_01.exibir_comprimento()
    # Circuito_01.exibir_agrupamento()


    perdas_test = Circuito_01.perdas

    # print(f"numero de iteracoes: {Circuito.ITERACOES}")


    pesos_test = Circuito_01.pesos


    # display_matrix3d_compact(pesos_test,condutores,"Pesos")

    # Custos = Circuito_01.calcular_custos()
    # display_matrix3d_compact(Custos,condutores,"Custos")


    Circuito_01.iterar_circuito()



    # print(f"teste: {Circuito.CONDUTORES}")

    # Circuito_01.exibir_matriz3d(perdas_test)
    # print_matrix3d(perdas_test)

    # print_matrix3d_as_dataframe(perdas_test)

    # display_matrix3d_compact(perdas_test,condutores,"Perdas")
    # print_matrix3d(perdas_test)

    # print(Circuito_01.CONDUTORES[0])

    # print(Circuito_02.calcular_pesos())

    # print(Circuito_01.comprimento)

