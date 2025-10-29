# flake8: noqa
import numpy as np
import random
from dados_entrada import perdas_OXLIP, perdas_GOLDENTUFT,perdas_COSMOS,perdas_ORCHID,perdas_ARBUTUS,perdas_ANEMONE,perdas_MAGNOLIA,perdas_MARIGOLD



# ==========================================
# CONFIGURAÇÕES ACO
# ==========================================
NFormigas = 20
Iteracoes = 10
alpha = 1      # influência do feromônio
beta = 1       # influência da heurística (1/distância)
rho = 0.1      # taxa de evaporação
Q = 100        # quantidade de feromônio depositada

# ==========================================
# MATRIZ 3D (camadas de perdas)
# ==========================================
camadas = np.stack([
    perdas_OXLIP,
    perdas_GOLDENTUFT,
    perdas_COSMOS,
    perdas_ORCHID,
    perdas_ARBUTUS,
    perdas_ANEMONE,
    perdas_MAGNOLIA,
    perdas_MARIGOLD
], axis=2)

NCidades = camadas.shape[0]
NCabos = camadas.shape[2]

# Inicializar feromônio e heurística
feromonio = np.ones_like(camadas)
atratividade = np.zeros_like(camadas)
atratividade[camadas > 0] = 1.0 / camadas[camadas > 0]  #Calcula n em todas as camadas

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================
def custo_total(caminho, camadas):
    """Soma total das perdas considerando as camadas escolhidas"""
    total = 0
    for (i, j, k) in caminho:
        total += camadas[i, j, k]
    return total

def escolher_proxima_cidade(atual, cidades_disponiveis, feromonio, atratividade, camada_atual):
    """Escolhe a próxima cidade e camada com base em probabilidade ponderada,
       respeitando a regra: só pode ir para camada >= camada_atual"""
    probs = []
    for prox in cidades_disponiveis:
        for camada in range(camada_atual, NCabos):  # camada atual ou superior
            if atratividade[atual, prox, camada] > 0:  # caminho válido
                tau = feromonio[atual, prox, camada] ** alpha
                eta = atratividade[atual, prox, camada] ** beta
                probs.append((prox, camada, tau * eta))
    
    if not probs:
        # fallback: escolher aleatoriamente dentro da limitação
        prox = random.choice(cidades_disponiveis)
        camada = random.randint(camada_atual, NCabos-1)
        return prox, camada

    # Normaliza probabilidades
    soma = sum([p[2] for p in probs])
    probs = [(c, k, p / soma) for (c, k, p) in probs]

    escolha = random.choices(probs, weights=[p[2] for p in probs])[0]
    return escolha[0], escolha[1]

# ==========================================
# SIMULAÇÃO DAS FORMIGAS
# ==========================================
melhor_caminho = None
melhor_custo = np.inf

for iter in range(Iteracoes):
    caminhos_formigas = []
    custos = []

    for f in range(NFormigas):
        cidades = list(range(NCidades))
        # print(f"Cidades: {cidades}")

        atual = random.choice(cidades)
        cidades.remove(atual)
        caminho = []

        camada_atual = 0  # começa na camada mínima

        while cidades:
            prox, camada = escolher_proxima_cidade(atual, cidades, feromonio, atratividade, camada_atual)
            caminho.append((atual, prox, camada))
            atual = prox
            cidades.remove(atual)
            camada_atual = camada  # atualiza a camada atual da formiga
        # print(caminho)

        # Fecha o ciclo
        camada_volta = random.randint(camada_atual, NCabos-1)
        caminho.append((atual, caminho[0][0], camada_volta))

        custo = custo_total(caminho, camadas)
        print(f"custo: {custo}")    
        caminhos_formigas.append(caminho)
        custos.append(custo)

        if custo < melhor_custo:
            melhor_custo = custo
            melhor_caminho = caminho
    print(f"=========================")
    # Atualiza feromônio
    feromonio *= (1 - rho)
    for caminho, custo in zip(caminhos_formigas, custos):
        for (i, j, k) in caminho:
            feromonio[i, j, k] += Q / custo

    print(f"Iteração {iter+1}: melhor custo = {melhor_custo:.3f}")

# ==========================================
# RESULTADOS
# ==========================================
print("\nMelhor caminho encontrado:")
for (i, j, k) in melhor_caminho:
    print(f"{i} -> {j} (camada {k})")
print(f"Custo total: {melhor_custo:.3f}")


