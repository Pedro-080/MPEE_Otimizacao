# flake8: noqa
import matplotlib.pyplot as plt
import numpy as np
import random

class Geracao:
    def __init__(self, elementos_b02, funcao, tamanho_cromossomo, debug=False, iteracao_num=0):
        self.elementos_b02 = elementos_b02
        self.elementos_b10 = self.binary_to_decimal(elementos_b02)
        self.funcao_alvo = funcao
        self.resultados = self._calc_funcao(funcao)
        self.porcentagens = self._calc_percentual_selecao(self.resultados)
        self.dicionario_valores = self._dict_valores()
        self.intervalos_roleta = self.criar_roleta()
        self.tamanho_cromossomo = tamanho_cromossomo
        self.elementos_decendentes_b02 = None
        self.elementos_decendentes_b10 = None
        self.chance_mutacao_percent = 1    
        self.chance_crossover_percent = 60
        self.debug = debug
        self.iteracao_num = iteracao_num
        
        if self.debug:
            self._debug_inicial()
        
        self.decendentes_b02, self.processos_geracao = self.gerar_decendentes()
        self.decendentes_b10 = self.binary_to_decimal(self.decendentes_b02)
        
        if self.debug:
            self._debug_final()

    def _debug_inicial(self):
        """Debug da população inicial da geração"""
        print(f"\n{'='*80}")
        print(f"GERAÇÃO {self.iteracao_num} - POPULAÇÃO INICIAL")
        print(f"{'='*80}")
        print(f"{'Ind':<4} {'Binário':<10} {'Decimal':<8} {'f(x)=x²':<10} {'% Seleção':<12}")
        print(f"{'-'*50}")
        
        for i, (binario, decimal, resultado, porcentagem) in enumerate(
            zip(self.elementos_b02, self.elementos_b10, self.resultados, self.porcentagens)):
            print(f"{i:<4} {binario:<10} {decimal:<8} {resultado:<10.2f} {porcentagem:<12.2f}%")
        
        print(f"\nIntervalos da Roleta:")
        for inicio, fim, valor, indice in self.intervalos_roleta:
            print(f"  [{inicio:6.2f} - {fim:6.2f}] -> {valor:2d} (índice {indice})")

    def _debug_final(self):
        """Debug da população final da geração"""
        print(f"\n{'='*80}")
        print(f"GERAÇÃO {self.iteracao_num} - POPULAÇÃO FINAL (DESCENDENTES)")
        print(f"{'='*80}")
        print(f"{'Ind':<4} {'Binário':<10} {'Decimal':<8} {'Pais':<15} {'Crossover':<10} {'Mutações':<10}")
        print(f"{'-'*60}")
        
        for i, (binario, decimal, processo) in enumerate(
            zip(self.decendentes_b02, self.decendentes_b10, self.processos_geracao)):
            
            pais_str = f"{processo['pai']},{processo['mae']}"
            crossover_str = "Sim" if processo['crossover'] else "Não"
            mutacoes_str = str(processo['posicoes_mutacao']) if processo['mutacao'] else "Nenhuma"
            
            print(f"{i:<4} {binario:<10} {decimal:<8} {pais_str:<15} {crossover_str:<10} {mutacoes_str:<10}")

    def _dict_valores(self):
        chaves = self.elementos_b10
        valores = self.porcentagens
        elementos = dict(zip(chaves, valores))
        elementos = dict(sorted(elementos.items(), key=lambda item: item[1], reverse=True))
        return elementos

    def binary_to_decimal(self, binaries_list):
        retorno = []
        for num in binaries_list:
            decimal_value = int(num, 2)
            retorno.append(decimal_value)
        return retorno

    def _calc_funcao(self, expressao):
        y = [eval(expressao) for x in self.elementos_b10]
        return y

    def _calc_percentual_selecao(self, valores_y):
        sum_y = sum(valores_y)
        percent_y = [num/sum_y*100 for num in valores_y]
        return percent_y

    def criar_roleta(self):
        elementos_completos = list(zip(self.elementos_b10, self.porcentagens))
        elementos_ordenados = sorted(elementos_completos, key=lambda x: x[1])
        
        intervalos = []
        inicio = 0
        indice = 0

        for chave, valor in elementos_ordenados:
            fim = inicio + valor
            intervalos.append((inicio, fim, chave, indice))
            inicio = fim
            indice += 1

        return intervalos

    def girar_roleta(self):
        intervalos = self.intervalos_roleta
        valor_aleatorio = random.uniform(0, 100)

        for inicio, fim, chave, indice in intervalos:
            if inicio <= valor_aleatorio < fim:
                return chave

        return intervalos[-1][2]

    def gerar_decendentes(self):
        Tamanho_populacao = len(self.elementos_b02)
        elementos_decendentes_b02 = []
        processos_geracao = []  # Para armazenar o histórico de como cada descendente foi gerado

        if self.debug:
            print(f"\nPROCESSO DE SELEÇÃO E CRUZAMENTO - GERAÇÃO {self.iteracao_num}")
            print(f"{'-'*60}")

        for decendente in range(Tamanho_populacao):
            pai = self.girar_roleta()
            mae = self.girar_roleta()
            
            # Realizar crossover e obter informações detalhadas
            resultado_crossover, info_crossover = self.realizar_crossover_com_info(pai, mae)
            
            # Realizar mutação e obter informações detalhadas
            resultado_mutacao, info_mutacao = self.realizar_mutacao_com_info(resultado_crossover)
            
            elementos_decendentes_b02.append(resultado_mutacao)
            
            # Armazenar informações do processo
            processo = {
                'pai': pai,
                'mae': mae,
                'crossover': info_crossover['realizado'],
                'posicao_corte': info_crossover['posicao_corte'],
                'mutacao': info_mutacao['realizada'],
                'posicoes_mutacao': info_mutacao['posicoes']
            }
            processos_geracao.append(processo)
            
            if self.debug:
                crossover_str = f"Sim (corte em {info_crossover['posicao_corte']})" if info_crossover['realizado'] else "Não"
                mutacao_str = f"Sim (posições {info_mutacao['posicoes']})" if info_mutacao['realizada'] else "Não"
                print(f"Descendente {decendente+1}: Pai={pai}, Mãe={mae}, "
                      f"Crossover={crossover_str}, Mutação={mutacao_str}")

        return elementos_decendentes_b02, processos_geracao

    def realizar_crossover_com_info(self, Pai, Mae):
        """Versão do crossover que retorna informações detalhadas"""
        Chance_crossover = self.chance_crossover_percent
        valor_aleatorio = random.uniform(0, 100)
        
        info = {
            'realizado': False,
            'posicao_corte': None
        }
        
        if valor_aleatorio <= Chance_crossover:
            if not isinstance(Pai, int) or not isinstance(Mae, int):
                raise ValueError("Ambos os números devem ser inteiros")

            bin_Pai_original = bin(Pai)[2:]
            bin_Mae_original = bin(Mae)[2:]

            tamanho_Pai = len(bin_Pai_original)
            tamanho_Mae = len(bin_Mae_original)

            max_tamanho = max(tamanho_Pai, tamanho_Mae, self.tamanho_cromossomo)
            bin_Pai_preenchido = bin_Pai_original.zfill(max_tamanho)
            bin_Mae_preenchido = bin_Mae_original.zfill(max_tamanho)

            posicao_corte = random.randint(1, max_tamanho - 1)

            parte1_bin1 = bin_Pai_preenchido[:posicao_corte]
            parte2_bin2 = bin_Mae_preenchido[posicao_corte:]

            novo_binario = parte1_bin1 + parte2_bin2
            
            info['realizado'] = True
            info['posicao_corte'] = posicao_corte
            
            return novo_binario, info
        else:
            info['realizado'] = False
            return bin(Pai)[2:].zfill(self.tamanho_cromossomo), info

    def realizar_mutacao_com_info(self, elemento_b02):
        """Versão da mutação que retorna informações detalhadas"""
        chance_mutacao = self.chance_mutacao_percent

        elemento_b02_mutado = []
        posicoes_mutadas = []
        
        for posicao, digito in enumerate(elemento_b02):
            valor_aleatorio = random.uniform(0, 100)

            if valor_aleatorio <= chance_mutacao:
                if digito == '0':
                    elemento_b02_mutado.append('1')
                    posicoes_mutadas.append(posicao)
                elif digito == '1':
                    elemento_b02_mutado.append('0')
                    posicoes_mutadas.append(posicao)
            else: 
                elemento_b02_mutado.append(digito)
                
        elemento_b02_mutado = ''.join(elemento_b02_mutado)
        
        info = {
            'realizada': len(posicoes_mutadas) > 0,
            'posicoes': posicoes_mutadas
        }
        
        return elemento_b02_mutado, info

    @classmethod
    def executar_iteracoes(cls, Populacao_inicial, funcao, tamanho_cromossomo, num_iteracoes=3, debug=False):
        """
        Executa múltiplas iterações da classe com opção de debug
        """
        resultados = []
        lista_atual = Populacao_inicial
        
        print(f"\n{'#'*80}")
        print(f"INÍCIO DO ALGORITMO GENÉTICO")
        print(f"População inicial: {lista_atual}")
        print(f"Função alvo: {funcao}")
        print(f"Tamanho do cromossomo: {tamanho_cromossomo}")
        print(f"Número de iterações: {num_iteracoes}")
        print(f"{'#'*80}")
        
        for iteracao in range(num_iteracoes):
            instancia = cls(lista_atual, funcao, tamanho_cromossomo, debug=debug, iteracao_num=iteracao+1)
            
            lista_atual_b02 = instancia.decendentes_b02
            lista_atual_b10 = instancia.decendentes_b10
            resultados.append(lista_atual_b10.copy())
            
            if not debug:  # Se debug estiver desligado, mostra apenas um resumo
                print(f"\nGeração {iteracao + 1}: {lista_atual_b10}")
            
            lista_atual = lista_atual_b02
        
        print(f"\n{'#'*80}")
        print(f"FIM DO ALGORITMO GENÉTICO")
        print(f"Resultado final: {resultados[-1]}")
        print(f"{'#'*80}")
        
        return resultados

def funcao_x2(x):
    return x**2

if __name__ == '__main__':
    Tamanho_cromossomo = 5
    funcao_alvo = "x**3"

    Populacao_inicial = ['11001', '01111', '01110', '01010']

    # Executar com debug detalhado
    print("EXECUÇÃO COM DEBUG DETALHADO:")
    Executar_Geracoes = Geracao.executar_iteracoes(
        Populacao_inicial, funcao_alvo, Tamanho_cromossomo, 
        num_iteracoes=50, debug=True
    )

    # print("\n\n" + "="*80)
    # print("EXECUÇÃO SEM DEBUG (APENAS RESUMO):")
    # Executar_Geracoes = Geracao.executar_iteracoes(
    #     Populacao_inicial, funcao_alvo, Tamanho_cromossomo, 
    #     num_iteracoes=2, debug=False
    # )