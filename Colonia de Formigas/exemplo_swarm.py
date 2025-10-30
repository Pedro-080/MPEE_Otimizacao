# flake8: noqa
import numpy as np
import random

class ACO:
    def __init__(self, dist_matrix, alpha=0.5, beta=0.5, rho=0.5, Q=1, n_ants=None):
        self.dist = np.array(dist_matrix, dtype=float)
        self.n = self.dist.shape[0]
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.n_ants = n_ants if n_ants else self.n  # uma formiga por cidade

        # Inicializa matriz de feromônio
        self.tau = np.ones_like(self.dist) - np.eye(self.n)
        self.eta = np.zeros_like(self.dist)
        # Calcula atratividade
        for i in range(self.n):
            for j in range(self.n):
                if i != j and self.dist[i, j] != 0:
                    self.eta[i, j] = 1 / self.dist[i, j]

    def _probabilities(self, current_city, visited):
        """Calcula as probabilidades de transição para uma formiga."""
        mask = np.ones(self.n, dtype=bool)
        mask[list(visited)] = False
        tau = self.tau[current_city, mask]
        eta = self.eta[current_city, mask]
        numerator = (tau ** self.alpha) * (eta ** self.beta)
        denominator = np.sum(numerator)
        probs = numerator / denominator
        available_cities = np.arange(self.n)[mask]
        return available_cities, probs

    def _construct_solution(self, start_city):
        """Constrói um tour completo a partir de uma cidade inicial."""
        visited = {start_city}
        tour = [start_city]
        current = start_city

        while len(visited) < self.n:
            available, probs = self._probabilities(current, visited)
            next_city = random.choices(available, weights=probs)[0]
            tour.append(next_city)
            visited.add(next_city)
            current = next_city

        # Retorna ao ponto inicial
        tour.append(start_city)
        return tour

    def _tour_length(self, tour):
        """Calcula o comprimento total do tour."""
        return sum(self.dist[tour[i], tour[i + 1]] for i in range(len(tour) - 1))

    def _update_pheromone(self, tours):
        """Atualiza os feromônios segundo as regras de evaporação e depósito."""
        delta_tau = np.zeros_like(self.tau)
        for tour, Lk in tours:
            for i in range(len(tour) - 1):
                a, b = tour[i], tour[i + 1]
                delta_tau[a, b] += self.Q / Lk
                delta_tau[b, a] += self.Q / Lk  # grafo simétrico

        # Evaporação e atualização
        self.tau = (1 - self.rho) * self.tau + delta_tau

    def run(self, iterations=1, verbose=True):
        """Executa o algoritmo por N iterações."""
        best_tour, best_len = None, float("inf")

        for it in range(iterations):
            tours = []
            for k in range(self.n_ants):
                start_city = k % self.n
                tour = self._construct_solution(start_city)
                Lk = self._tour_length(tour)
                tours.append((tour, Lk))
                if Lk < best_len:
                    best_tour, best_len = tour, Lk

            self._update_pheromone(tours)

            if verbose:
                print(f"\nIteração {it+1}")
                for i, (t, L) in enumerate(tours):
                    print(f"Formiga {i+1}: Tour={t}, L={L:.2f}")
                print("Nova matriz de feromônio:\n", np.round(self.tau, 4))
                print(f"Melhor solução até agora: {best_tour}, comprimento={best_len:.2f}")

        return best_tour, best_len




# Matriz de distâncias do exemplo (página 18 do PDF)
dist_matrix = [
    [0, 1, 2.2, 2.5, 3.0],
    [1, 0, 1.5, 2.5, 3.0],
    [2.2, 1.5, 0, 3.0, 2.2],
    [2.5, 2.5, 3.0, 0, 1.0],
    [3.0, 3.0, 2.2, 1.0, 0]
]

aco = ACO(dist_matrix, alpha=0.5, beta=0.5, rho=0.5, Q=1)
best_tour, best_len = aco.run(iterations=5)

print("\n=== RESULTADO FINAL ===")
print("Melhor rota:", best_tour)
print("Comprimento total:", round(best_len, 4))