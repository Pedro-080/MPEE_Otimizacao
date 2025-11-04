import numpy as np
import random

class ACO_TSP:
    def __init__(self, distancias, n_formigas=10, alpha=1, beta=2, rho=0.5, Q=100, iteracoes=100):
        """
        Inicializa o algoritmo ACO para TSP
        
        Parâmetros:
        distancias: matriz de distâncias
        n_formigas: número de formigas
        alpha: influência do feromônio
        beta: influência da informação heurística (1/distância)
        rho: taxa de evaporação do feromônio
        Q: constante para atualização do feromônio
        iteracoes: número de iterações
        """
        self.distancias = np.array(distancias)
        self.n = len(distancias)
        self.n_formigas = n_formigas
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.iteracoes = iteracoes
        
        # Inicializa matriz de feromônios
        self.feromonio = np.ones((self.n, self.n))
        
        # Calcula matriz heurística (1/distância)
        self.heuristica = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if i != j and distancias[i][j] > 0:
                    self.heuristica[i][j] = 1.0 / distancias[i][j]
                else:
                    self.heuristica[i][j] = 0
    
    def executar(self):
        """Executa o algoritmo ACO"""
        melhor_rota = None
        melhor_distancia = float('inf')
        historico_melhores = []
        
        for iteracao in range(self.iteracoes):
            todas_rotas = []
            todas_distancias = []
            
            # Cada formiga constrói uma rota
            for formiga in range(self.n_formigas):
                rota, distancia = self._construir_rota()
                todas_rotas.append(rota)
                todas_distancias.append(distancia)
                
                # Atualiza melhor rota global
                if distancia < melhor_distancia:
                    melhor_distancia = distancia
                    melhor_rota = rota.copy()
            
            # Atualiza feromônios
            self._atualizar_feromonio(todas_rotas, todas_distancias)
            
            historico_melhores.append(melhor_distancia)
            
            if iteracao % 20 == 0:
                print(f"Iteração {iteracao}: Melhor distância = {melhor_distancia}")
        
        return melhor_rota, melhor_distancia, historico_melhores
    
    def _construir_rota(self):
        """Uma formiga constrói uma rota completa"""
        # Começa de uma cidade aleatória
        cidade_atual = random.randint(0, self.n - 1)
        rota = [cidade_atual]
        distancia_total = 0
        cidades_visitadas = set([cidade_atual])
        
        # Visita todas as cidades
        while len(rota) < self.n:
            proxima_cidade = self._escolher_proxima_cidade(cidade_atual, cidades_visitadas)
            distancia_total += self.distancias[cidade_atual][proxima_cidade]
            rota.append(proxima_cidade)
            cidades_visitadas.add(proxima_cidade)
            cidade_atual = proxima_cidade
        
        # Volta para a cidade inicial
        distancia_total += self.distancias[rota[-1]][rota[0]]
        
        return rota, distancia_total
    
    def _escolher_proxima_cidade(self, cidade_atual, cidades_visitadas):
        """Escolhe a próxima cidade baseada na regra de transição"""
        probabilidades = []
        cidades_disponiveis = []
        
        # Calcula probabilidades para todas as cidades não visitadas
        for j in range(self.n):
            if j not in cidades_visitadas:
                # Calcula probabilidade usando regra de transição
                feromonio = self.feromonio[cidade_atual][j] ** self.alpha
                heuristica = self.heuristica[cidade_atual][j] ** self.beta
                probabilidade = feromonio * heuristica
                probabilidades.append(probabilidade)
                cidades_disponiveis.append(j)
        
        # Normaliza probabilidades
        soma_probabilidades = sum(probabilidades)
        if soma_probabilidades > 0:
            probabilidades = [p / soma_probabilidades for p in probabilidades]
        else:
            # Se todas as probabilidades forem zero, distribui uniformemente
            probabilidades = [1.0 / len(cidades_disponiveis)] * len(cidades_disponiveis)
        
        # Escolhe próxima cidade usando roleta
        return random.choices(cidades_disponiveis, weights=probabilidades)[0]
    
    def _atualizar_feromonio(self, todas_rotas, todas_distancias):
        """Atualiza a matriz de feromônios"""
        # Evaporação
        self.feromonio *= (1 - self.rho)
        
        # Atualização baseada na qualidade das rotas
        for rota, distancia in zip(todas_rotas, todas_distancias):
            deposito = self.Q / distancia  # Quanto melhor a rota, mais feromônio
            
            for i in range(len(rota)):
                cidade_atual = rota[i]
                proxima_cidade = rota[(i + 1) % len(rota)]
                self.feromonio[cidade_atual][proxima_cidade] += deposito
                self.feromonio[proxima_cidade][cidade_atual] += deposito  # Matriz simétrica

def main():
    # Matriz de distâncias fornecida
    distancias = [
        [0, 2, 9, 10, 7],
        [1, 0, 6, 4, 3],
        [15, 7, 0, 8, 3],
        [6, 3, 12, 0, 11],
        [9, 7, 5, 6, 0]
    ]
    
    print("Matriz de Distâncias:")
    for linha in distancias:
        print(linha)
    print()
    
    # Parâmetros do algoritmo
    n_formigas = 15
    alpha = 1      # Influência do feromônio
    beta = 3       # Influência da informação heurística
    rho = 0.3      # Taxa de evaporação
    Q = 100        # Constante de depósito de feromônio
    iteracoes = 200
    
    # Executa o algoritmo
    aco = ACO_TSP(distancias, n_formigas, alpha, beta, rho, Q, iteracoes)
    melhor_rota, melhor_distancia, historico = aco.executar()
    
    print("\n" + "="*50)
    print("RESULTADO FINAL:")
    print("="*50)
    print(f"Melhor rota encontrada: {melhor_rota}")
    print(f"Distância total: {melhor_distancia}")
    
    # Mostra a rota detalhada
    print("\nRota detalhada:")
    cidades = ['A', 'B', 'C', 'D', 'E']  # Nomes para as cidades
    for i in range(len(melhor_rota)):
        cidade_atual = melhor_rota[i]
        proxima_cidade = melhor_rota[(i + 1) % len(melhor_rota)]
        distancia_trecho = distancias[cidade_atual][proxima_cidade]
        print(f"  {cidades[cidade_atual]} → {cidades[proxima_cidade]} : {distancia_trecho}")
    
    print(f"\nDistância total: {melhor_distancia}")

if __name__ == "__main__":
    main()