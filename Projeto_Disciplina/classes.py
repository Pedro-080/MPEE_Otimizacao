# flake8: noqa
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import math
import random

#funcoes auxiliares

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

def calcular_mascara_cidades_disponiveis(Cidades_disponiveis,num_cidades, Layers_disponiveis_list,cidade_atual):

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

    base = np.zeros((num_cidades,num_cidades),dtype=int)
    base[cidade_atual-1] = lista_cidades
    
    matriz = np.stack([base]*7,axis=2)

    # Modificação: criar matriz 3D com cada camada multiplicada pelo respectivo valor
    matriz = base[:, :, np.newaxis] * Layers_disponiveis_list[np.newaxis, np.newaxis, :]

    # print(f"Cidades_disponiveis_list:{Cidades_disponiveis_list}")
    # print_matrix3d(matriz)
    # # print(matriz)
    # print('*'*50)
    return matriz

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











class Configurar:
    """Classe base com configurações globais que podem ser ajustadas uma vez."""
    
    # Configurações padrão
    POT_AERO_MW   = 6
    FP           = 0.95                                       # Fator de potencia 
    FC       = 1                                              # Fator de capacidade considerado. 1 = 100%
    PERDA_MAXIMA_PERCENT = 2                                  # Pedra máxima global tolerada em porcentagem.  2 = 2%  
    CONDUTORES = []
    Q   = 1e5,         # fator de multiplicação do ganho de feromonio delta_tau
    RHO = 0.6,         # Evaporação do feromônio
    FER = 0.1,         # Feromônio inicial
    FER_MAX = 1.2, 
    ALFA = 1,          # Parâmetro de influência de feromônio, inicial
    BETA = 5,          # Parâmetro de influência de distância
    ITERACOES = 50,    # Número de iterações
    Custo_ton_Al = 15000                                      # Custo por tonelada de aluminio. 15000 = 15000   R$/ton
    Preco_MHh = 386.41                                        # Preço da energia por MWh.        386.51 = 386.51 r$/kWh

    # NUM_FORMIGAS = 5   # Número de formigas, duas por cidade

    


    @classmethod
    def Setup_projeto(cls, **kwargs):
        """Configura os parâmetros globais do sistema."""
        for chave, valor in kwargs.items():
            if hasattr(cls, chave.upper()):
                setattr(cls, chave.upper(), valor)
                print(f"Configuração '{chave}' definida como: {valor}")
            else:
                print(f"⚠️ Configuração '{chave}' não existe!")





class Circuito(Configurar):
    """Classe principal que herda as configurações."""

    # Método inicializador (construtor)
    def __init__(self, identificação, comprimento , agrupamento ):
        self.identificação = identificação
        self.comprimento = comprimento     #Matriz de inicialização das distancias
        self.agrupamento = agrupamento     #Matriz de inicialização dos agrupamentos
        self.perdas = self.calcular_perdas()
        self.pesos = self.calcular_pesos()
        self.num_passos = np.count_nonzero(comprimento)
        self.num_formigas = self.num_passos
        self.Matriz_layer = np.zeros((self.num_formigas, self.num_passos),dtype = int)
        self.NCidades = self.comprimento.shape[0]
        self.NCabos   = self.pesos.shape[2]
        self.tau = np.ones((self.NCidades, self.NCidades,self.NCabos)) * self.FER         # Deposição inicial de feromonio
        self.Pot_circ_MW = np.max(agrupamento) * self.POT_AERO_MW
        
        self.custos = self.calcular_custos()
        self.n = self.calcular_n(self.custos)

        self.delta_tau = np.zeros((self.NCidades, self.NCidades, self.NCabos))

        self.Matriz_layer = None
        self.Matriz_cidades = None

    def __str__(self):
        return (f"Circuito {self.identificação} ")

    def calcular_n(self, matriz):
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


    def exibir_comprimento(self):
        dados = self.comprimento
        if dados is None:
            print(f"Comprimento não atribuido ao circuito {self.identificação}")    

        else:
            # Criar Data  Frame
            nome_colunas = [f"{i+1}" for i in range(dados.shape[1])] \
                if len(dados.shape) > 1 else ["Valores"]

            df = pd.DataFrame(dados, columns = nome_colunas, index = range(1,len(dados)+1))
            print(f"Comprimento do {self.identificação}:")
            print(df)


    def exibir_agrupamento(self):
        dados = self.agrupamento
        if dados is None:
            print(f"\nAgrupamento não atribuido ao circuito {self.identificação}")     

        else:
            # Criar Data  Frame
            nome_colunas = [f"{i+1}" for i in range(dados.shape[1])] \
                if len(dados.shape) > 1 else ["Valores"]

            df = pd.DataFrame(dados, columns = nome_colunas, index = range(1,len(dados)+1))
            print(f"\nAgrupamento do {self.identificação}:")
            print(df)

    def exibir_matriz3d(self,dados):
        condutores = self.CONDUTORES
        n_condutores, n_linhas, n_colunas = dados.shape
        nomes_colunas = [f'col_{i}' for i in range(n_colunas)]

        # Achatar o array
        dados_flat = dados.reshape(-1, n_colunas)

        # Criar nomes de condutores repetidos
        condutores_repetidos = np.repeat(condutores, n_linhas)

        # Criar DataFrame
        df = pd.DataFrame(dados_flat, columns=nomes_colunas)
        df.insert(0, 'condutor', condutores_repetidos)
        
        return df
        ...

    def calcular_perdas(self):
        # print(f"tipo self.agrupamento:\n{self.agrupamento}")

        Pot_acumulado_MW_3d = self.agrupamento * self.POT_AERO_MW
        Pot_circ_MW  = np.max(self.agrupamento) * self.POT_AERO_MW
        FP  = self.FP
        FC = self.FC

        perdas_por_condutor = []

        for condutor in self.CONDUTORES:
            perda = condutor.array_calcular_perdas_percent(self.comprimento, Pot_acumulado_MW_3d, Pot_circ_MW, FP, FC)
            perdas_por_condutor.append(perda)

        perdas = np.stack(perdas_por_condutor, axis=2)
        return perdas

    def calcular_pesos(self):
        
        peso_por_condutor = []
        
        for condutor in self.CONDUTORES:
            peso = condutor.array_calcular_massa_ton(self.comprimento)
            peso_por_condutor.append(peso)
            
        pesos = np.stack(peso_por_condutor, axis=2)
        return pesos
    
    def calcular_custos(self):
        Custo_ton_Al = self.Custo_ton_Al
        Pot_circ_MWh_ano = self.Pot_circ_MW * 24 * 365
        FC = self.FC
        Preco_MHh = self.Preco_MHh

        '''O custo está sendo calculado usando apenas o preço do aluminio'''
        Custo_peso_cabos = self.pesos * Custo_ton_Al
        Custo_perdas     = self.perdas/100 * Pot_circ_MWh_ano * FC * Preco_MHh

        Custo = Custo_peso_cabos #+ Custo_perdas
        
        return Custo
        ...

    def iterar_circuito(self):
        '''
        Variaveis de debug
        '''
        Debug_Roleta     = True      #True para exibir, False para não exibir
        Debug_tau        = False      #True para exibir, False para não exibir
        Debug_formiga    = False      #True para exibir, False para não exibir
        Debug_layers     = False      #True para exibir, False para não exibir
        Debug_delta_tau  = False      #True para exibir, False para não exibir



        print(f"iterando sobre o circuito {self.identificação}")

        NCidades = self.NCidades
        NCabos = self.NCabos

        num_formigas = self.num_formigas
        num_passos = self.num_passos
        

        linhas, colunas = np.where(self.comprimento != 0)               #Extrai as cidades, duplicando a que possuem multiplos caminhos
        colunas = np.add(colunas,1)                                #Adiciona 1 ao índice de todas as cidades, evitando começar em 0
        colunas = np.insert(colunas,0,1)                           #Adiciona a primeira cidade como 1

        N_cidades_totais = len(colunas.tolist())                                           #Conta o numero de cidades mesmo que duplicadas
        Layers_disponiveis = np.tile(np.arange(1,NCabos+1),(num_formigas,1))  

        Matriz_layer = np.zeros((self.num_formigas, N_cidades_totais),dtype = int)                     # Caminho das formigas pelos layers
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
                    # Inicia todas as formigas em layers aleatorias
                    Matriz_layer[formiga, 0] = random.choice(Layers_disponiveis[formiga])
                    Matriz_cidades[formiga, passo-1] = cidade_atual

                    # Define o cabo atual
                    cabo_atual = int(Matriz_layer[formiga, 0])
                else:
                    cidade_atual =  Matriz_cidades[formiga, passo-1]

            print(f"cidades disponíveis:")

            Cidades_disponiveis[formiga] = Remover_elemento(Cidades_disponiveis[formiga],cidade_atual)
            


            #Remove os cabos inferiores aos já escolhidos
            Layers_disponiveis[formiga] = np.where(Layers_disponiveis[formiga] < cabo_atual, 0, Layers_disponiveis[formiga])

            Layers_disponiveis_list = (Layers_disponiveis[formiga] != 0).astype(int)




            matriz = self.tau ** self.ALFA * self.n ** self.BETA

            mascara_cidades_disponiveis = calcular_mascara_cidades_disponiveis(Cidades_disponiveis[formiga],NCidades, Layers_disponiveis_list, cabo_atual)

            numerador = matriz * mascara_cidades_disponiveis
            denominador = np.sum(numerador)

            #Calcula a probabilidade das proximas cidades
            probabilidade = matriz * 1/denominador  * mascara_cidades_disponiveis

            intervalos = criar_roleta_3d(probabilidade, Debug_Roleta)
            proxima_cidade, proximo_cabo = girar_roleta(intervalos, Debug_Roleta)
            proxima_cidade = proxima_cidade + 1                                     #corrige o indice        
            proximo_cabo = proximo_cabo + 1                                         #corrige o indice   

            Matriz_layer[formiga, passo] = proximo_cabo
            Matriz_cidades[formiga, passo] = proxima_cidade

            cabo_atual = proximo_cabo

        self.Matriz_layer = Matriz_layer
        self.Matriz_cidades = Matriz_cidades

        return None

class Cabo():
    def __init__(self, ID,condutor, peso_kgkm, RCA, XL,ampacidade):
        self.id        = ID
        self.condutor  = condutor
        self.peso_kgkm = peso_kgkm
        self.RCA       = RCA
        self.XL        = XL
        self.ampacidade= ampacidade
    
    def __str__(self) :
        return self.id
    
    def _resitencia_ohm(self, comprimento_m):
        RCA_ohm = comprimento_m * self.RCA /1000
        # print(f"RCA_ohm: {RCA_ohm}")
        return RCA_ohm

    def _corrente_A(self, potencia_MW, FP, FC=1):
        return ((potencia_MW * 1000) / (34.5 * math.sqrt(3) * FP)) * FC
        
    def _perdas_W(self, comprimento, potencia_MW, FP, FC=1):
        corrente = self._corrente_A(potencia_MW, FP, FC)
        RCA_ohm  = self._resitencia_ohm(comprimento)
    
        return 3 * RCA_ohm * corrente**2

    def _perdas_MWh_ano(self, comprimento, potencia_MW, FP, FC=1):
        perdas_W = self._perdas_W(comprimento, potencia_MW, FP, FC)
        return (perdas_W * 24 * 365)/1000000
        ...

    def _perdas_percent (self, comprimento, potencia_MW, potencia_total_MW, FP, FC=1 ):
        Potencia_total_MWh_ano = potencia_total_MW * 24 * 365
        perdas_MWh_ano = self._perdas_MWh_ano(comprimento, potencia_MW, FP, FC=1)
        resultado = perdas_MWh_ano / Potencia_total_MWh_ano * 100
        return np.round(resultado,4)
        ...


    def array_calcular_perdas_percent(self, comprimentos_array, potencias_array, potencia_total_MW, FP, FC=1):
        """
        Calcula perdas para arrays de comprimentos e potências.
        
        Args:
            comprimentos_array: np.array de comprimentos em metros
            potencias_array: np.array de potências em MW
            FP: Fator de potência (scalar)
            FC: Fator de carga (scalar)
            
        Returns:
            dict: Dicionário com arrays de resultados
        """
        # Garantir que são arrays numpy
        comprimentos = np.asarray(comprimentos_array)
        potencias = np.asarray(potencias_array)
        
        # Verificar dimensões compatíveis para broadcasting
        if comprimentos.ndim == 1 and potencias.ndim == 1:
            # Criar meshgrid para todas as combinações
            comprimentos_grid, potencias_grid = np.meshgrid(comprimentos, potencias, indexing='ij')
        else:
            comprimentos_grid = comprimentos
            potencias_grid = potencias
        
        # Calcular todos os resultados de uma vez
        # correntes = self._corrente_A(potencias_grid, FP, FC)
        # perdas_W = self._perdas_W(comprimentos_grid, potencias_grid, FP, FC)
        # perdas_MWh_ano = self._perdas_MWh_ano(comprimentos_grid, potencias_grid, FP, FC)
        perdas_percent = self._perdas_percent(comprimentos_grid, potencias_grid, potencia_total_MW, FP,FC )

        # def _perdas_percent (self, comprimento, potencia_MW, potencia_total_MW, FP, FC=1 ):


        return perdas_percent

    def array_calcular_massa_ton(self,comprimentos_array):
        """
        Calcula a massa equivalente em toneladas para o trecho específico.
        
        Args:
            comprimentos_array: np.array de comprimentos em metros
            
        Returns:
            massa: array com massa de cada trecho
        """
        peso_kg_km = self.peso_kgkm
        peso_ton_m = peso_kg_km * 1e-6   #Conversão de kg/km para ton/m

        array_peso = comprimentos_array * peso_ton_m

        return array_peso