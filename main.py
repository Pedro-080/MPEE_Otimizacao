# flake8: noqa
import matplotlib.pyplot as plt
import numpy as np
import random


class Geracao:
    def __init__(self, elementos_b02, funcao,tamanho_cromossomo):
        self.elementos_b02 = elementos_b02                          # Define os atributo da instância
        self.elementos_b10 = self.binary_to_decimal(elementos_b02)  #
        self.funcao_alvo = funcao
        self.resultados =  self._calc_funcao(funcao)
        self.porcentagens = self._calc_percentual_selecao(self.resultados)
        self.dicionario_valores = self._dict_valores()
        self.intervalos_roleta = self.criar_roleta()
        self.tamanho_cromossomo = tamanho_cromossomo
        self.elementos_decendentes_b02 = None
        self.elementos_decendentes_b10 = None
        self.chance_mutacao_percent = 1    
        self.chance_crossover_percent = 60
        self.decendentes_b02 = self.gerar_decendentes()
        self.decendentes_b10 = self.binary_to_decimal(self.decendentes_b02)


    def _dict_valores(self):
        chaves  = self.elementos_b10
        valores = self.porcentagens
        elementos = dict(zip(chaves, valores))
        elementos = dict(sorted(elementos.items(), key=lambda item: item[1], reverse=True))  #Ordena o dicionario com base nas porcentagens
        return elementos          
        ...

    def binary_to_decimal(self, binaries_list):
        retorno = []
        for num in binaries_list:
           decimal_value = int(num, 2)
           retorno.append(decimal_value)
        return retorno
    
    # def _sum_elementos(self, elementos_b10):
        sum_elementos_b10 = 0
        for num in elementos_b10:
            sum_elementos_b10+=num      
        
        return sum_elementos_b10
    
    def _percent_elemento(self):
        soma_elementos = self._sum_elementos()
        percent_elemento = [num/soma_elementos for num in self.elementos_b10 ]
        return percent_elemento
        ...

    def _calc_funcao(self,expressao):
        """
        Avalia uma expressão matemática para um dado valor de x
        
        Args:
            expressao (str): Expressão como "x**2", "2*x + 1", etc.
            x (float): Valor de entrada
        
        Returns:
            float: Resultado da expressão
        """

        y = [eval(expressao) for x in self.elementos_b10]
        return y

    def _calc_percentual_selecao(self,valores_y):
        sum_y = sum(valores_y)
        percent_y = [num/sum_y*100 for num in valores_y]
        return percent_y  
        ...

    # def selecionar_pais(self):


        Pai_01 = self.roleta_basica()
        Pai_02 = self.roleta_basica()
        
        print(f"Pai 01: {Pai_01}")
        print(f"Pai 02: {Pai_02}")
        # valores_y = self.resultados
        # sum_y = self._sum_elementos(valores_y)
        # percent_y = [num/sum_y for num in valores_y]

        return 
        ...

    def criar_roleta(self):
        # Criar uma lista com todos os elementos (permite duplicatas)
        elementos_completos = list(zip(self.elementos_b10, self.porcentagens))
        
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

    def girar_roleta(self):
        intervalos = self.intervalos_roleta
        valor_aleatorio = random.uniform(0, 100)

        for inicio, fim, chave, indice in intervalos:
            if inicio <= valor_aleatorio < fim:
                return chave

        # Caso esteja exatamente no limite superior
        return intervalos[-1][2]

        # if valor_aleatorio == 100:
        #     # return intervalos[-1][2], valor_aleatorio
        #     return intervalos[-1][2]




    def gerar_decendentes(self):
        Tamanho_populacao = int(len(self.elementos_b02))
        elementos_decendentes_b02 = []


        for decendente in range(1,Tamanho_populacao+1):
            Pai = self.girar_roleta()
            Mae = self.girar_roleta()
            # print(f"Pai: {Pai}")
            # print(f"Mae: {Mae}")
            elementos_decendentes_b02.append(self.realizar_crossover(Pai,Mae))
            # self.realizar_crossover(Pai,Mae)
            # print(f"decendente {decendente}")
            ...
        # for i in range(1, 5):
        #     print(f"Execução {i}")
        #     # print(f"Tamanho da população é {len(self.elementos_b02)}")
        #     ...
        elementos_decendentes_b02_mutados = []
        for elemento in elementos_decendentes_b02:
            elementos_decendentes_b02_mutados.append(self.realizar_mutacao(elemento))



        return elementos_decendentes_b02_mutados

    def realizar_crossover(self, Pai, Mae):
        Chance_crossover = self.chance_crossover_percent
        valor_aleatorio = random.uniform(0, 100)
        
        if valor_aleatorio <= Chance_crossover:
            if not isinstance(Pai, int) or not isinstance(Mae, int):
                raise ValueError("Ambos os números devem ser inteiros")

            # Conversão para binário
            bin_Pai_original = bin(Pai)[2:]
            bin_Mae_original = bin(Mae)[2:]

            tamanho_Pai = len(bin_Pai_original)
            tamanho_Mae = len(bin_Mae_original)

            # Preencher com zeros se necessário
            max_tamanho = max(tamanho_Pai, tamanho_Mae,self.tamanho_cromossomo)
            bin_Pai_preenchido = bin_Pai_original.zfill(max_tamanho)
            bin_Mae_preenchido = bin_Mae_original.zfill(max_tamanho)

            # Sortear posição de corte
            posicao_corte = random.randint(1, max_tamanho - 1)

            # Realizar crossover
            parte1_bin1 = bin_Pai_preenchido[:posicao_corte]  # Primeira parte do binário 1
            parte2_bin2 = bin_Mae_preenchido[posicao_corte:]  # Segunda parte do binário 2

            novo_binario = parte1_bin1 + parte2_bin2

            return novo_binario
        else:
            return bin(Pai)[2:].zfill(self.tamanho_cromossomo)

    def realizar_mutacao (self, elemento_b02):
        chance_mutacao = self.chance_mutacao_percent

        elemento_b02_mutado = []
        for digito in elemento_b02:
            valor_aleatorio = random.uniform(0, 100)
            # print(f"mutacao chance: {valor_aleatorio}")

            if valor_aleatorio <= chance_mutacao:
                if digito == '0':
                    elemento_b02_mutado.append('1')
                elif digito == '1':
                    elemento_b02_mutado.append('0')               
            else: 
                elemento_b02_mutado.append(digito)
        elemento_b02_mutado = ''.join(elemento_b02_mutado)
        # print (elemento_b02_mutado)
        # print(f"in: {elemento_b02}")
        # print(f"mutado: {elemento_b02_mutado}")
        return elemento_b02_mutado


        # print(type(elemento_b02))        
        ...

    @classmethod
    def executar_iteracoes(cls, Populacao_inicial, funcao, tamanho_cromossomo ,num_iteracoes=3 ):
        """
        Executa múltiplas iterações da classe
        """
        resultados = []
        lista_atual = Populacao_inicial        

        print(f"Entrada inicial: {lista_atual}")
        
        for iteracao in range(num_iteracoes):
            # Cria nova instância com a lista atual
            instancia = cls(lista_atual,
                            funcao,
                            tamanho_cromossomo)


            # Executa a operação
            lista_atual_b02 = instancia.decendentes_b02
            lista_atual_b10 = instancia.decendentes_b10
            resultados.append(lista_atual_b10.copy())
            # print(f"Iteração {iteracao + 1}: {lista_atual_b02}")
            print(f"Iteração {iteracao + 1}: {lista_atual_b10}")
            # print(f"Interval {iteracao + 1}: {instancia.intervalos_roleta}")
        
        return resultados


def funcao_x2(x):
    return x**2

if __name__ == '__main__':
    Tamanho_cromossomo = 5

    limites  = np.arange(0, 32, 0.125)  # passo de 0.125
    funcao_alvo = "x**2"

    Populacao_inicial = ['11001', 
                         '01111',
                         '01110',
                         '01010'
                         ]


    Executar_Geracoes = Geracao.executar_iteracoes(Populacao_inicial,funcao_alvo,Tamanho_cromossomo,1000)
    print(f"\nResultado final: {Executar_Geracoes[-1]}")





    # G1 = Geracao(Populacao_inicial,funcao_alvo,Tamanho_cromossomo)


    # print(f"Input G1: {G1.elementos_b02}")
    # print(f"Input G1: {G1.elementos_b10}")
    # print(f"output G1: {G1.decendentes_b02}")
    # print(f"output G1: {G1.decendentes_b10}")


    # # print(f"{G1.selecionar_pais()}")
    # # print(G1.criar_roleta())



    # G2 = Geracao(G1.decendentes_b02,funcao_alvo,Tamanho_cromossomo)

    # # print(f"intervalos: {G2.intervalos_roleta}")

    # # for num in range (1,100):
    # #     print(f"{num}: {G2.girar_roleta()}")

    # print(f"Input G2: {G2.elementos_b02}")
    # print(f"Input G2: {G2.elementos_b10}")
    # print(f"output G2: {G2.decendentes_b02}")
    # print(f"output G2: {G2.decendentes_b10}")

    # G3 = Geracao(G2.decendentes_b02,funcao_alvo,Tamanho_cromossomo)
    # print(f"Input G3: {G3.elementos_b02}")
    # print(f"Input G3: {G3.elementos_b10}")
    # print(f"output G3: {G3.decendentes_b02}")
    # print(f"output G3: {G3.decendentes_b10}")

    # G4 = Geracao(G3.decendentes_b02,funcao_alvo,Tamanho_cromossomo)
    # print(f"Input G4: {G4.elementos_b02}")
    # print(f"Input G4: {G4.elementos_b10}")
    # print(f"output G4: {G4.decendentes_b02}")
    # print(f"output G4: {G4.decendentes_b10}")

    # G5 = Geracao(G4.decendentes_b02,funcao_alvo,Tamanho_cromossomo)
    # print(f"Input G5: {G5.elementos_b02}")
    # print(f"Input G5: {G5.elementos_b10}")
    # print(f"output G5: {G5.decendentes_b02}")
    # print(f"output G5: {G5.decendentes_b10}")





    # print(f"Input G2: {G2.elementos_b02}")
    # print(f"Input G2: {G2.elementos_b10}")

    # # print(f"output G2: {G2.decendentes_b02}")
    # # print(f"output G2: {G2.decendentes_b10}")

    # G3 = Geracao(G2.decendentes_b02,funcao_alvo,Tamanho_cromossomo)


    # # print(G1.roleta_basica())
    # G1.gerar_decendentes()

    # print(G1.decendentes_b02)
    # print(G1.decendentes_b10)


    


    # print(decendentes)

    # print(decendentes)

    # print(G1.binary_to_decimal(decendentes))
    # print(G1.girar_roleta())

    # print(G1._sum_elementos())
    # print(G1._percent_elemento())

    # print(G1.resultados)
    # print(G1.porcentagens)



    # print(G1.selecionar_pais())

    # for elemento in G1.elementos_b02:
    #     print(f"{elemento} : {elemento_decimal}: {funcao(elemento_decimal)}")

