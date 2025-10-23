# flake8: noqa
import numpy as np
import matplotlib.pyplot as plt
import random

class ColoniaFormigas:
    def __init__(self, matriz_distancias, setores, n_formigas=20, alpha=1, beta=2, 
                 evaporacao=0.5, Q=100, iteracoes=100):
        
        self.d = matriz_distancias
        self.SETOR = setores
        self.NCidades = len(setores)
        self.NFormigas = n_formigas
        
        # Parâmetros do algoritmo
        self.alpha = alpha  # Peso do feromônio
        self.beta = beta    # Peso da heurística
        self.evaporacao = evaporacao  # Taxa de evaporação
        self.Q = Q          # Constante de deposição
        self.iteracoes = iteracoes
        
        # Inicializar matrizes
        self.Feromonio = np.ones((self.NCidades, self.NCidades))
        self.Atratividade = self.calcular_atratividade()
        
        # Eliminar auto-conexões e conexões inexistentes
        np.fill_diagonal(self.Feromonio, 0)
        for i in range(self.NCidades):
            for j in range(self.NCidades):
                if self.d[i, j] == 0:
                    self.Feromonio[i, j] = 0
                    self.Atratividade[i, j] = 0
        
        # Histórico
        self.melhor_custo_historico = []
        self.melhor_caminho_historico = []
        
    def calcular_atratividade(self):
        """Calcula atratividade como inverso da distância"""
        atratividade = np.zeros_like(self.d, dtype=float)
        for i in range(self.NCidades):
            for j in range(self.NCidades):
                if i != j and self.d[i, j] > 0:
                    atratividade[i, j] = 1.0 / self.d[i, j]
        return atratividade
    
    def escolher_proxima_cidade(self, cidade_atual, cidades_visitadas):
        """Escolhe a próxima cidade baseada na regra de transição"""
        cidades_nao_visitadas = [j for j in range(self.NCidades) 
                               if j not in cidades_visitadas and self.d[cidade_atual, j] > 0]
        
        if not cidades_nao_visitadas:
            return -1  # Todas as cidades foram visitadas ou não há conexões
        
        # Calcular probabilidades
        probabilidades = []
        for j in cidades_nao_visitadas:
            tau = self.Feromonio[cidade_atual, j] ** self.alpha
            eta = self.Atratividade[cidade_atual, j] ** self.beta
            probabilidades.append(tau * eta)
        
        # Normalizar probabilidades
        soma_prob = sum(probabilidades)
        if soma_prob == 0:
            # Se todas probabilidades são zero, escolha aleatória
            return random.choice(cidades_nao_visitadas)
        
        probabilidades = [p / soma_prob for p in probabilidades]
        
        # Escolha por roleta
        roleta = random.random()
        acumulado = 0
        for idx, prob in enumerate(probabilidades):
            acumulado += prob
            if roleta <= acumulado:
                return cidades_nao_visitadas[idx]
        
        return cidades_nao_visitadas[-1]
    
    def construir_caminho(self):
        """Cada formiga constrói um caminho completo"""
        caminho = [0]  # Começa do primeiro setor (A01)
        cidades_visitadas = set([0])
        
        while len(caminho) < self.NCidades:
            cidade_atual = caminho[-1]
            proxima_cidade = self.escolher_proxima_cidade(cidade_atual, cidades_visitadas)
            
            if proxima_cidade == -1:
                # Não há mais cidades conectadas, completar aleatoriamente
                cidades_restantes = [j for j in range(self.NCidades) if j not in cidades_visitadas]
                if cidades_restantes:
                    proxima_cidade = random.choice(cidades_restantes)
                else:
                    break
            
            caminho.append(proxima_cidade)
            cidades_visitadas.add(proxima_cidade)
        
        return caminho
    
    def calcular_custo_caminho(self, caminho):
        """Calcula o custo total do caminho"""
        custo = 0
        for i in range(len(caminho) - 1):
            custo += self.d[caminho[i], caminho[i + 1]]
        # Adicionar retorno ao início se necessário
        # custo += self.d[caminho[-1], caminho[0]]
        return custo
    
    def atualizar_feromonio(self, caminhos, custos):
        """Atualiza a matriz de feromônio"""
        # Evaporação
        self.Feromonio *= (1 - self.evaporacao)
        
        # Deposição de feromônio
        for caminho, custo in zip(caminhos, custos):
            if custo > 0:  # Evitar divisão por zero
                delta_tau = self.Q / custo
                for i in range(len(caminho) - 1):
                    cidade_atual = caminho[i]
                    proxima_cidade = caminho[i + 1]
                    self.Feromonio[cidade_atual, proxima_cidade] += delta_tau
                    self.Feromonio[proxima_cidade, cidade_atual] += delta_tau
    
    def executar(self):
        """Executa o algoritmo completo"""
        melhor_custo_global = float('inf')
        melhor_caminho_global = None
        
        print("=== ALGORITMO DE COLÔNIA DE FORMIGAS ===")
        print(f"Estrutura: Cadeia linear de {self.NCidades} setores")
        print(f"Formigas: {self.NFormigas}, Iterações: {self.iteracoes}")
        print()
        
        for iteracao in range(self.iteracoes):
            caminhos = []
            custos = []
            
            # Cada formiga constrói um caminho
            for _ in range(self.NFormigas):
                caminho = self.construir_caminho()
                custo = self.calcular_custo_caminho(caminho)
                caminhos.append(caminho)
                custos.append(custo)
            
            # Encontrar melhor caminho desta iteração
            melhor_custo_iteracao = min(custos)
            melhor_idx = custos.index(melhor_custo_iteracao)
            melhor_caminho_iteracao = caminhos[melhor_idx]
            
            # Atualizar melhor global
            if melhor_custo_iteracao < melhor_custo_global:
                melhor_custo_global = melhor_custo_iteracao
                melhor_caminho_global = melhor_caminho_iteracao
            
            # Atualizar feromônio
            self.atualizar_feromonio(caminhos, custos)
            
            # Armazenar histórico
            self.melhor_custo_historico.append(melhor_custo_iteracao)
            self.melhor_caminho_historico.append(melhor_caminho_iteracao)
            
            # Progresso a cada 10 iterações
            if (iteracao + 1) % 10 == 0:
                caminho_setores = [self.SETOR[i] for i in melhor_caminho_iteracao]
                print(f"Iteração {iteracao + 1}: Custo = {melhor_custo_iteracao}")
                print(f"Melhor caminho: {caminho_setores}")
        
        return melhor_caminho_global, melhor_custo_global
    
    def visualizar_resultados(self):
        """Visualiza os resultados do algoritmo"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico de convergência
        ax1.plot(self.melhor_custo_historico)
        ax1.set_xlabel('Iteração')
        ax1.set_ylabel('Melhor Custo')
        ax1.set_title('Convergência do Algoritmo')
        ax1.grid(True)
        
        # Visualização da matriz de distâncias
        im = ax2.imshow(self.d, cmap='viridis', interpolation='nearest')
        ax2.set_title('Matriz de Distâncias')
        ax2.set_xticks(range(self.NCidades))
        ax2.set_yticks(range(self.NCidades))
        ax2.set_xticklabels(self.SETOR, rotation=45)
        ax2.set_yticklabels(self.SETOR)
        
        # Adicionar valores na matriz
        for i in range(self.NCidades):
            for j in range(self.NCidades):
                ax2.text(j, i, f'{self.d[i, j]}', 
                        ha='center', va='center', 
                        color='white' if self.d[i, j] > 500 else 'black')
        
        plt.colorbar(im, ax=ax2)
        plt.tight_layout()
        plt.show()

# DADOS DE ENTRADA
d = np.array([
[   0,1000,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[   0,   0,1000,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[   0,   0,   0,1000,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[   0,   0,   0,   0,1000,   0,   0,   0,   0,   0,   0,   0,   0],
[   0,   0,   0,   0,   0,1000,   0,   0,   0,   0,   0,   0,   0],
[   0,   0,   0,   0,   0,   0,1000,   0,   0,   0,   0,   0,   0],
[   0,   0,   0,   0,   0,   0,   0,1000,   0,   0,   0,   0,   0],
[   0,   0,   0,   0,   0,   0,   0,   0,1000,   0,   0,   0,   0],
[   0,   0,   0,   0,   0,   0,   0,   0,   0,1000,   0,   0,   0],
[   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,1000,   0,   0],
[   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,1000,   0],
[   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,1000],
[   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0]
])

SETOR = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'SE']

# EXECUTAR ALGORITMO
if __name__ == "__main__":
    # Criar e executar colônia
    colonia = ColoniaFormigas(d, SETOR, n_formigas=20, iteracoes=50)
    
    print("ANÁLISE DA ESTRUTURA:")
    print("Esta é uma cadeia linear onde cada setor só se conecta com seus vizinhos imediatos")
    print("A01 ↔ A02 ↔ A03 ↔ ... ↔ A12 ↔ SE")
    print("Distância entre vizinhos: 1000 unidades")
    print()
    
    # Executar algoritmo
    melhor_caminho, melhor_custo = colonia.executar()
    
    # Resultados finais
    print("\n" + "="*50)
    print("RESULTADO FINAL:")
    caminho_setores = [SETOR[i] for i in melhor_caminho]
    print(f"Melhor caminho encontrado: {caminho_setores}")
    print(f"Custo total: {melhor_custo}")
    print(f"Comprimento do caminho: {len(melhor_caminho)} setores")
    
    # Visualizar resultados
    colonia.visualizar_resultados()
    
    # Análise adicional
    print("\nANÁLISE DO PROBLEMA:")
    print("Em uma estrutura linear, o algoritmo deve encontrar a ordem natural:")
    print("A01 → A02 → A03 → ... → A12 → SE")
    print("Ou a ordem reversa, dependendo do ponto de partida")