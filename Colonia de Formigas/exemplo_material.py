# flake8: noqa
import numpy as np
import random

# ==========================================
# DADOS DO EXEMPLO 5x5
# ==========================================
# Matriz de custos (distâncias) entre as 5 cidades
custos = np.array([
    [0,   2,   4,   1,   3],   # A
    [2,   0,   5,   2,   4],   # B  
    [4,   5,   0,   3,   2],   # C
    [1,   2,   3,   0,   6],   # D
    [3,   4,   2,   6,   0]    # E
])

NCidades = custos.shape[0]

# ==========================================
# CONFIGURAÇÕES ACO
# ==========================================
NFormigas = 10
Iteracoes = 30
alpha = 1      # influência do feromônio
beta = 2       # influência da heurística (1/custo)
rho = 0.5      # taxa de evaporação (50%)
Q = 10         # quantidade de feromônio depositada

# ==========================================
# INICIALIZAÇÃO DO FEROMÔNIO E HEURÍSTICA
# ==========================================
# Matriz de feromônio (simétrica)
feromonio = np.ones((NCidades, NCidades)) * 0.1
np.fill_diagonal(feromonio, 0)  # diagonal principal = 0

# Matriz de atratividade (heurística) = 1/custo
atratividade = np.zeros((NCidades, NCidades))


for i in range(NCidades):
    for j in range(NCidades):
        if i != j and custos[i, j] > 0:
            atratividade[i, j] = 1.0 / custos[i, j]

# print("==========atratividade==========")
# print(atratividade)


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================
def custo_total(caminho, matriz_custos):
    """Calcula o custo total do caminho (ciclo completo)"""
    total = 0
    for i in range(len(caminho)):
        cidade_atual = caminho[i]
        cidade_proxima = caminho[(i + 1) % len(caminho)]  # volta ao início
        total += matriz_custos[cidade_atual, cidade_proxima]
    return int(total)  # Converte para int Python

def escolher_proxima_cidade(cidade_atual, cidades_visitadas, feromonio, atratividade):
    """Escolhe a próxima cidade com base na regra de probabilidade do ACO"""
    cidades_disponiveis = [c for c in range(NCidades) if c not in cidades_visitadas]
    
    if not cidades_disponiveis:
        return None  # Todas as cidades foram visitadas
    
    probabilidades = []
    
    for cidade in cidades_disponiveis:
        # Calcula a probabilidade não normalizada
        tau = feromonio[cidade_atual, cidade] ** alpha
        eta = atratividade[cidade_atual, cidade] ** beta
        probabilidades.append((cidade, tau * eta))
    
    # Normaliza as probabilidades
    soma_probabilidades = sum(p[1] for p in probabilidades)
    # print(f"soma_probabilidades: {soma_probabilidades}")
    # print(f"probabilidades: \n {probabilidades}")

    
    if soma_probabilidades == 0:
        # Se todas as probabilidades forem zero, escolhe aleatoriamente
        return random.choice(cidades_disponiveis)
    
    probabilidades_normalizadas = [(cidade, prob/soma_probabilidades) 
                                 for cidade, prob in probabilidades]
    
    # Escolhe baseado nas probabilidades
    cidades, probs = zip(*probabilidades_normalizadas)
    escolha = random.choices(cidades, weights=probs)[0]
    
    return escolha

# ==========================================
# SIMULAÇÃO DAS FORMIGAS
# ==========================================
melhor_caminho = None
melhor_custo = float('inf')
historico_melhores = []

print("=== ALGORITMO ACO PARA PROBLEMA 5x5 ===\n")
print("Matriz de custos:")
print(custos)
print(f"\nConfiguração: {NFormigas} formigas, {Iteracoes} iterações")
print(f"Parâmetros: α={alpha}, β={beta}, ρ={rho}, Q={Q}\n")

for iteracao in range(Iteracoes):
    caminhos_formigas = []
    custos_formigas = []
    
    # Cada formiga constrói uma solução
    for formiga in range(NFormigas):
        # Escolhe cidade inicial aleatória
        cidade_inicial = random.randint(0, NCidades - 1)
        caminho = [cidade_inicial]
        cidades_visitadas = set([cidade_inicial])
        
        # Constrói o caminho visitando todas as cidades
        while len(caminho) < NCidades:
            cidade_atual = caminho[-1]
            proxima_cidade = escolher_proxima_cidade(
                cidade_atual, cidades_visitadas, feromonio, atratividade
            )
            
            if proxima_cidade is not None:
                caminho.append(proxima_cidade)
                cidades_visitadas.add(proxima_cidade)
            else:
                break
        
        # Fecha o ciclo (volta à cidade inicial)
        caminho_completo = caminho + [caminho[0]]
        custo = custo_total(caminho_completo, custos)
        
        caminhos_formigas.append(caminho_completo)
        custos_formigas.append(custo)
        
        # Atualiza melhor solução global
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_caminho = caminho_completo.copy()
    
    # EVAPORAÇÃO do feromônio
    feromonio *= (1 - rho)
    
    # DEPÓSITO de feromônio pelas formigas
    for caminho, custo in zip(caminhos_formigas, custos_formigas):
        delta_tau = Q / custo
        
        for i in range(len(caminho) - 1):
            cidade_atual = caminho[i]
            cidade_proxima = caminho[i + 1]
            
            # Atualiza feromônio em ambas as direções (matriz simétrica)
            feromonio[cidade_atual, cidade_proxima] += delta_tau
            feromonio[cidade_proxima, cidade_atual] += delta_tau
    
    # Armazena histórico - CONVERTE para int Python
    historico_melhores.append(int(melhor_custo))
    
    # Mostra progresso - CONVERTE custo_medio para float Python
    custo_medio = float(np.mean(custos_formigas))
    print(f"Iteração {iteracao+1:2d}: Melhor = {int(melhor_custo):2d}, Médio = {custo_medio:5.2f}")

# ==========================================
# RESULTADOS FINAIS
# ==========================================
print("\n" + "="*50)
print("RESULTADO FINAL")
print("="*50)

# Mapeia números para letras para melhor visualização
nomes_cidades = ['A', 'B', 'C', 'D', 'E']

print(f"\nMelhor caminho encontrado:")
caminho_formatado = " → ".join([nomes_cidades[c] for c in melhor_caminho])
print(caminho_formatado)

print(f"\nCusto total: {int(melhor_custo)}")

# Mostra detalhes do percurso
print(f"\nDetalhes do percurso:")
for i in range(len(melhor_caminho) - 1):
    cidade_atual = melhor_caminho[i]
    cidade_proxima = melhor_caminho[i + 1]
    custo_trecho = custos[cidade_atual, cidade_proxima]
    print(f"  {nomes_cidades[cidade_atual]} → {nomes_cidades[cidade_proxima]}: custo = {int(custo_trecho)}")

# Matriz de feromônio final (arredondada)
print(f"\nMatriz de feromônio final (arredondada):")
print(np.round(feromonio, 3))

# Evolução do melhor custo - AGORA vai mostrar valores normais
print(f"\nEvolução do melhor custo: {historico_melhores}")

# Verifica se encontrou a solução ótima conhecida
print(f"\nSoluções conhecidas:")
print("A → D → B → E → C → A: custo = 1+2+4+2+4 = 13")
print("B → A → D → C → E → B: custo = 2+1+3+2+4 = 12")
print(f"Melhor encontrado: {int(melhor_custo)}")