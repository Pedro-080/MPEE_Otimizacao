import numpy as np
import matplotlib.pyplot as plt

# COLÔNIA DE FORMIGAS
# PROBLEMA DO CAIXEIRO VIAJANTE

# Matriz de distâncias
MAPAD = np.array([
    [0, 76.5, 27.2, 100.3, 127.5, 154.7, 181.9, 209.1],
    [76.5, 0, 44.2, 98.6, 125.8, 153, 180.2, 207.4],
    [27.2, 44.2, 0, 107.1, 134.3, 161.5, 188.7, 215.9],
    [100.3, 98.6, 107.1, 0, 27.2, 54.4, 81.6, 108.8],
    [127.5, 125.8, 134.3, 27.2, 0, 27.2, 54.4, 81.6],
    [154.7, 153, 161.5, 54.4, 27.2, 0, 27.2, 54.4],
    [181.9, 180.2, 188.7, 81.6, 54.4, 27.2, 0, 27.2],
    [209.1, 207.4, 215.9, 108.8, 81.6, 54.4, 27.2, 0]
])

SETOR = np.array(['PA', 'CT', 'PC', 'PD', 'PE', 'PF', 'PG', 'PH'])

# Obter número de cidades
NCidades = MAPAD.shape[0]

NFormigas = 20

# Inicialização de matrizes
Feromonio = np.ones((NCidades, NCidades))
Atratividade = np.ones((NCidades, NCidades))
CAMINHO = np.zeros((NFormigas, NCidades), dtype=int)
Matriz_Infor = np.zeros((NCidades, NCidades))
Matriz_Infor_Temp = Matriz_Infor.copy()

alpha = 1
betta = 1
iteracoes = 100

PROBABILIDADE = np.zeros((NFormigas, NCidades))

# Função para exibir informações das variáveis
def mostrar_informacoes():
    print("=== INFORMAÇÕES DO SISTEMA ===")
    print(f"Número de cidades: {NCidades}")
    print(f"Número de formigas: {NFormigas}")
    print(f"Número de iterações: {iteracoes}")
    print(f"Alpha (feromônio): {alpha}")
    print(f"Beta (heurística): {betta}")
    print()
    
    print("Setores:")
    for i, setor in enumerate(SETOR):
        print(f"  {i}: {setor}")
    
    print(f"\nMatriz de distâncias MAPAD ({MAPAD.shape}):")
    print(MAPAD)
    
    print(f"\nMatriz de feromônio ({Feromonio.shape}):")
    print(Feromonio)
    
    print(f"\nMatriz CAMINHO ({CAMINHO.shape}):")
    print(CAMINHO)
    
    print(f"\nMatriz PROBABILIDADE ({PROBABILIDADE.shape}):")
    print(PROBABILIDADE)

# Função para calcular atratividade baseada na distância
def calcular_atratividade(matriz_distancias):
    """Calcula a atratividade como o inverso da distância"""
    atratividade = np.zeros_like(matriz_distancias)
    for i in range(matriz_distancias.shape[0]):
        for j in range(matriz_distancias.shape[1]):
            if i != j and matriz_distancias[i, j] > 0:
                atratividade[i, j] = 1.0 / matriz_distancias[i, j]
            else:
                atratividade[i, j] = 0
    return atratividade

# Função para inicializar caminhos aleatórios
def inicializar_caminhos(n_formigas, n_cidades):
    """Inicializa caminhos aleatórios para as formigas"""
    caminhos = np.zeros((n_formigas, n_cidades), dtype=int)
    for i in range(n_formigas):
        caminhos[i] = np.random.permutation(n_cidades)
    return caminhos

# Função para calcular custo de um caminho
def calcular_custo(caminho, matriz_distancias):
    """Calcula o custo total de um caminho"""
    custo = 0
    for i in range(len(caminho) - 1):
        custo += matriz_distancias[caminho[i], caminho[i + 1]]
    # Adiciona o retorno à cidade inicial
    custo += matriz_distancias[caminho[-1], caminho[0]]
    return custo

# Exemplo de uso das funções
if __name__ == "__main__":
    # Mostrar informações iniciais
    mostrar_informacoes()
    
    # Calcular atratividade
    Atratividade = calcular_atratividade(MAPAD)
    print(f"\nMatriz de Atratividade ({Atratividade.shape}):")
    print(Atratividade)
    
    # Inicializar caminhos aleatórios
    CAMINHO = inicializar_caminhos(NFormigas, NCidades)
    print(f"\nCaminhos iniciais das formigas:")
    for i in range(min(5, NFormigas)):  # Mostrar apenas as primeiras 5 formigas
        caminho_setores = [SETOR[cidade] for cidade in CAMINHO[i]]
        custo = calcular_custo(CAMINHO[i], MAPAD)
        print(f"Formiga {i+1}: {caminho_setores} -> Custo: {custo:.2f}")
    
    # Calcular custos de todos os caminhos
    print(f"\nCustos de todos os caminhos:")
    custos = [calcular_custo(CAMINHO[i], MAPAD) for i in range(NFormigas)]
    for i in range(NFormigas):
        print(f"Formiga {i+1}: {custos[i]:.2f}")
    
    # Encontrar melhor caminho inicial
    melhor_idx = np.argmin(custos)
    melhor_caminho = CAMINHO[melhor_idx]
    melhor_custo = custos[melhor_idx]
    
    print(f"\nMelhor caminho inicial:")
    caminho_setores = [SETOR[cidade] for cidade in melhor_caminho]
    print(f"Formiga {melhor_idx + 1}: {caminho_setores}")
    print(f"Custo: {melhor_custo:.2f}")
    
    # Visualização da matriz de distâncias
    plt.figure(figsize=(10, 8))
    plt.imshow(MAPAD, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='Distância')
    plt.title('Matriz de Distâncias - MAPAD')
    plt.xticks(range(NCidades), SETOR)
    plt.yticks(range(NCidades), SETOR)
    
    # Adicionar valores nas células
    for i in range(NCidades):
        for j in range(NCidades):
            plt.text(j, i, f'{MAPAD[i, j]:.1f}', 
                    ha='center', va='center', 
                    color='white' if MAPAD[i, j] > 100 else 'black')
    
    plt.tight_layout()
    plt.show()