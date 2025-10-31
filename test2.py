import numpy as np
import random

# ======== CONFIGURAÇÃO PADRÃO ========
random.seed(0)
np.set_printoptions(precision=4, suppress=True)

# ======== CLASSE PRINCIPAL ========
class ACOStepDebugger:
    """
    Implementação detalhada do método ACO com foco na depuração.
    Mostra passo a passo o cálculo de probabilidades, escolha de caminhos
    e atualização da matriz de feromônio.
    """
    def __init__(self, dist, alpha=0.5, beta=0.5, rho=0.5, Q=1.0, n_ants=None, seed=0):
        self.dist = np.array(dist, dtype=float)
        self.n = self.dist.shape[0]
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.n_ants = n_ants if n_ants is not None else self.n
        random.seed(seed)
        np.random.seed(seed)

        # Inicializa o feromônio (1 em todas as arestas, exceto diagonal)
        self.tau = np.ones_like(self.dist) - np.eye(self.n)

        # Calcula a heurística (η = 1/d)
        self.eta = np.zeros_like(self.dist)
        for i in range(self.n):
            for j in range(self.n):
                if i != j and self.dist[i, j] != 0:
                    self.eta[i, j] = 1.0 / self.dist[i, j]

    # === ETAPA 1: cálculo matricial dos numeradores ===
    def _numerator_matrix(self):
        """τ^α * η^β para cada (i,j)."""
        return (self.tau ** self.alpha) * (self.eta ** self.beta)

    # === ETAPA 2: cálculo do vetor de probabilidades ===
    def _prob_vector_for_ant(self, current_city, visited_mask, numerator_matrix):
        """Calcula vetor de probabilidade de transição."""
        num_row = numerator_matrix[current_city].copy()
        num_row[visited_mask] = 0.0
        denom = num_row.sum()
        probs = np.zeros_like(num_row)
        if denom > 0:
            probs = num_row / denom
        return probs, num_row, denom

    # === ETAPA 3: construção dos caminhos das formigas ===
    def _construct_solutions(self, stochastic=True, debug=False):
        tours = []
        numerator_matrix = self._numerator_matrix()

        if debug:
            print("\nMatriz de distâncias (d_ij):\n", self.dist)
            print("\nMatriz de atratividade (η = 1/d):\n", np.round(self.eta, 4))
            print("\nMatriz de feromônio inicial (τ):\n", np.round(self.tau, 4))
            print("\nMatriz numerador (τ^α * η^β):\n", np.round(numerator_matrix, 6))
            print("\n--- Início da construção de soluções ---\n")

        for k in range(self.n_ants):
            start = k % self.n
            visited = np.zeros(self.n, dtype=bool)
            visited[start] = True
            tour = [start]
            current = start

            if debug:
                print(f"\nFormiga {k+1} iniciando na cidade {start}")

            while not visited.all():
                probs, num_row, denom = self._prob_vector_for_ant(current, visited, numerator_matrix)

                if debug:
                    print(f"\n  Cidade atual: {current}")
                    print("  Numerador (após máscara):", np.round(num_row, 6))
                    print("  Denominador (∑ numeradores):", np.round(denom, 6))
                    print("  Vetor de probabilidades:", np.round(probs, 6))

                available = np.where(~visited)[0]
                available_probs = probs[available]

                if stochastic:
                    next_city = random.choices(available.tolist(), weights=available_probs.tolist(), k=1)[0]
                else:
                    next_city = available[np.argmax(available_probs)]

                tour.append(next_city)
                visited[next_city] = True

                if debug:
                    print(f"  Próxima cidade escolhida: {next_city}")

                current = next_city

            tour.append(start)
            L = sum(self.dist[tour[i], tour[i+1]] for i in range(len(tour)-1))
            tours.append((tour, L))

            if debug:
                print(f"\nFormiga {k+1} finalizou tour: {tour}  Comprimento: {L:.4f}")
                print("-"*50)

        return tours

    # === ETAPA 4: atualização do feromônio ===
    def _update_pheromone(self, tours, debug=False):
        delta = np.zeros_like(self.tau)
        for tour, L in tours:
            if L > 0:
                contribution = self.Q / L
                for i in range(len(tour)-1):
                    a, b = tour[i], tour[i+1]
                    delta[a, b] += contribution
                    delta[b, a] += contribution  # grafo simétrico

        if debug:
            print("\nMatriz Δτ (depósitos):\n", np.round(delta, 6))
            print("Matriz τ antes da evaporação:\n", np.round(self.tau, 6))

        # Evaporação + depósito
        self.tau = (1 - self.rho) * self.tau + delta

        if debug:
            print("Matriz τ após atualização:\n", np.round(self.tau, 6))

    # === LOOP PRINCIPAL ===
    def run_iterations(self, iterations=3, debug_each_iteration=True):
        best_tour = None
        best_len = float('inf')

        for it in range(iterations):
            if debug_each_iteration:
                print("\n" + "="*40)
                print(f"ITERAÇÃO {it+1}/{iterations}")
                print("="*40)

            tours = self._construct_solutions(debug=debug_each_iteration)
            if debug_each_iteration:
                print("\nTours construídos:")
                for i, (t, L) in enumerate(tours):
                    print(f"  Formiga {i+1}: {t}, L = {L:.4f}")

            self._update_pheromone(tours, debug=debug_each_iteration)

            for t, L in tours:
                if L < best_len:
                    best_len = L
                    best_tour = t.copy()

        print("\n=== RESULTADO FINAL ===")
        print("Melhor tour encontrado:", best_tour)
        print("Comprimento total:", round(best_len, 4))
        print("\nMatriz final de feromônio (τ):\n", np.round(self.tau, 6))
        return best_tour, best_len


# ======== EXECUÇÃO DO EXEMPLO ========
dist_matrix = [
    [0,   1,   2.2, 2.5, 3.0],
    [1,   0,   1.5, 2.5, 3.0],
    [2.2, 1.5, 0,   3.0, 2.2],
    [2.5, 2.5, 3.0, 0,   1.0],
    [3.0, 3.0, 2.2, 1.0, 0  ]
]

aco = ACOStepDebugger(dist_matrix, alpha=0.5, beta=0.5, rho=0.5, Q=1.0, seed=0)
best_tour, best_len = aco.run_iterations(iterations=3, debug_each_iteration=True)
