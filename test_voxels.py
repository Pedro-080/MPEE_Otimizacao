# flake8: noqa
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def criar_formigueiro_pesos(n_familias=3, n_cidades=5):
    """Cria formigueiro 3D apenas com os pesos"""
    formigueiro = np.random.rand(n_familias, n_cidades, n_cidades)
    
    # Diagonal zero (não há deslocamento para mesma cidade)
    for k in range(n_familias):
        np.fill_diagonal(formigueiro[k], 0)
    
    return formigueiro

def visualizar_pesos_3d(formigueiro):
    """Visualiza apenas os pesos no espaço 3D"""
    
    n_familias, n_cidades, _ = formigueiro.shape
    
    fig = plt.figure(figsize=(15, 10))
    
    # VISUALIZAÇÃO 1: Pontos 3D com cores por peso
    ax1 = fig.add_subplot(121, projection='3d')
    
    # Criar arrays de coordenadas
    i_coords, j_coords, k_coords = [], [], []
    pesos = []
    
    for k in range(n_familias):
        for i in range(n_cidades):
            for j in range(n_cidades):
                if i != j:  # Ignorar diagonal
                    i_coords.append(i)
                    j_coords.append(j)
                    k_coords.append(k)
                    pesos.append(formigueiro[k, i, j])
    
    # Converter para arrays numpy
    i_coords = np.array(i_coords)
    j_coords = np.array(j_coords)
    k_coords = np.array(k_coords)
    pesos = np.array(pesos)
    
    # Plotar pontos com cores baseadas nos pesos
    scatter = ax1.scatter(i_coords, k_coords, j_coords, 
                         c=pesos, cmap='viridis', s=100, alpha=0.8)
    
    # Adicionar valores nos pontos
    for idx in range(len(i_coords)):
        if pesos[idx] > 0.5:  # Apenas pesos altos para não poluir
            ax1.text(i_coords[idx], k_coords[idx], j_coords[idx], 
                    f'{pesos[idx]:.2f}', fontsize=8, ha='center', va='center')
    
    ax1.set_xlabel('Cidade Origem (i)')
    ax1.set_ylabel('Família (k)')
    ax1.set_zlabel('Cidade Destino (j)')
    ax1.set_title('PESOS - Visualização 3D\n(Tamanho e Cor = Peso)')
    plt.colorbar(scatter, ax=ax1, label='Valor do Peso')
    
    # VISUALIZAÇÃO 2: Superfície 3D dos pesos
    ax2 = fig.add_subplot(122, projection='3d')
    
    # Criar meshgrid para superfície
    I, K = np.meshgrid(range(n_cidades), range(n_familias))
    
    # Plotar superfície para um j fixo (j=2 como exemplo)
    j_fixo = 2
    Z = np.zeros((n_familias, n_cidades))
    
    for k in range(n_familias):
        for i in range(n_cidades):
            Z[k, i] = formigueiro[k, i, j_fixo]
    
    surf = ax2.plot_surface(I, K, Z, cmap='hot', alpha=0.8,
                           linewidth=0, antialiased=True)
    
    # Adicionar pontos na superfície
    for k in range(n_familias):
        for i in range(n_cidades):
            ax2.text(i, k, Z[k, i] + 0.02, f'{Z[k, i]:.2f}', 
                    fontsize=7, ha='center', va='bottom')
    
    ax2.set_xlabel('Cidade Origem (i)')
    ax2.set_ylabel('Família (k)')
    ax2.set_zlabel(f'Peso para j={j_fixo}')
    ax2.set_title(f'Superfície de Pesos\n(Destino Fixo: cidade {j_fixo})')
    plt.colorbar(surf, ax=ax2, label='Valor do Peso')
    
    plt.tight_layout()
    plt.show()

def visualizar_pesos_barras_3d(formigueiro):
    """Visualização com barras 3D representando os pesos"""
    
    n_familias, n_cidades, _ = formigueiro.shape
    
    fig = plt.figure(figsize=(16, 6))
    
    # Para cada família, criar um subplot 3D
    for familia in range(n_familias):
        ax = fig.add_subplot(1, n_familias, familia + 1, projection='3d')
        
        # Criar coordenadas para as barras
        x_pos, y_pos = np.meshgrid(range(n_cidades), range(n_cidades))
        x_pos = x_pos.flatten()
        y_pos = y_pos.flatten()
        z_pos = np.zeros_like(x_pos)
        
        # Valores dos pesos
        pesos = formigueiro[familia].flatten()
        
        # Dimensões das barras
        dx = dy = 0.8 * np.ones_like(z_pos)
        dz = pesos
        
        # Plotar barras
        bars = ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, 
                       color=plt.cm.viridis(pesos), alpha=0.7)
        
        # Adicionar valores no topo das barras
        for i, (x, y, z) in enumerate(zip(x_pos, y_pos, dz)):
            if z > 0.1:  # Apenas para barras significativas
                ax.text(x + 0.4, y + 0.4, z + 0.02, f'{z:.2f}', 
                       fontsize=6, ha='center', va='bottom')
        
        ax.set_xlabel('Cidade i')
        ax.set_ylabel('Cidade j')
        ax.set_zlabel('Peso')
        ax.set_title(f'Família {familia}\nMatriz de Pesos 3D')
        ax.set_xticks(range(n_cidades))
        ax.set_yticks(range(n_cidades))
        ax.set_zlim(0, 1)
    
    plt.tight_layout()
    plt.show()

def visualizar_heatmap_3d(formigueiro):
    """Visualização tipo heatmap 3D dos pesos"""
    
    n_familias, n_cidades, _ = formigueiro.shape
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Criar dados para o heatmap 3D
    i_idx, j_idx, k_idx = np.meshgrid(
        range(n_cidades), 
        range(n_cidades), 
        range(n_familias),
        indexing='ij'
    )
    
    # Achatar os arrays
    i_flat = i_idx.flatten()
    j_flat = j_idx.flatten() 
    k_flat = k_idx.flatten()
    pesos_flat = formigueiro.flatten()
    
    # Filtrar apenas pesos não-zero (excluir diagonal)
    mask = (i_flat != j_flat) & (pesos_flat > 0)
    i_filtrado = i_flat[mask]
    j_filtrado = j_flat[mask]
    k_filtrado = k_flat[mask]
    pesos_filtrado = pesos_flat[mask]
    
    # Plotar heatmap 3D
    scatter = ax.scatter(i_filtrado, k_filtrado, j_filtrado, 
                        c=pesos_filtrado, cmap='plasma', 
                        s=pesos_filtrado * 200,  # Tamanho proporcional ao peso
                        alpha=0.8, edgecolors='black', linewidth=0.5)
    
    # Configurações do gráfico
    ax.set_xlabel('Cidade Origem (i)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Família (k)', fontsize=12, fontweight='bold')
    ax.set_zlabel('Cidade Destino (j)', fontsize=12, fontweight='bold')
    ax.set_title('HEATMAP 3D - PESOS DO FORMIGUEIRO', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Adicionar grade
    ax.set_xticks(range(n_cidades))
    ax.set_yticks(range(n_familias))
    ax.set_zticks(range(n_cidades))
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax, shrink=0.6, aspect=20)
    cbar.set_label('Valor do Peso', fontsize=12, fontweight='bold')
    
    # Ângulo de visualização
    ax.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    plt.show()

# EXECUTAR TODAS AS VISUALIZAÇÕES
print("=== VISUALIZAÇÃO DOS PESOS EM 3D ===\n")

# Criar formigueiro
formigueiro = criar_formigueiro_pesos(n_familias=3, n_cidades=5)

print(f"Forma do formigueiro: {formigueiro.shape}")
print(f"Peso médio: {np.mean(formigueiro):.3f}")
print(f"Peso máximo: {np.max(formigueiro):.3f}")
print(f"Peso mínimo: {np.min(formigueiro):.3f}")

# Visualização 1: Pontos 3D
print("\n1. Visualização com Pontos 3D...")
visualizar_pesos_3d(formigueiro)

# Visualização 2: Barras 3D
print("2. Visualização com Barras 3D...")
visualizar_pesos_barras_3d(formigueiro)

# Visualização 3: Heatmap 3D
print("3. Visualização Heatmap 3D...")
visualizar_heatmap_3d(formigueiro)

# Mostrar matrizes resumidas
print("\n=== MATRIZES DE PESOS (Resumo) ===")
for k in range(formigueiro.shape[0]):
    print(f"\nFamília {k}:")
    print("i\\j", end="")
    for j in range(formigueiro.shape[2]):
        print(f" {j:>6}", end="")
    print()
    for i in range(formigueiro.shape[1]):
        print(f" {i}  ", end="")
        for j in range(formigueiro.shape[2]):
            print(f" {formigueiro[k,i,j]:.3f}", end="")
        print()