import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualizar_matriz_3d(dados, titulo="Visualização 3D da Matriz"):
    """
    Visualiza uma matriz 3D de qualquer dimensão de forma adaptativa
    """
    # ====================================
    # 1. Obter dimensões da matriz de entrada
    # ====================================
    dim_x, dim_y, dim_z = dados.shape
    print(f"Matriz {dim_x}x{dim_y}x{dim_z}:")
    print(dados)
    
    # ====================================
    # 2. Criar figura 3D com tamanho adaptativo
    # ====================================
    fig = plt.figure(figsize=(max(8, dim_x*2), max(7, dim_y*2)))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(f"{titulo}\nDimensões: {dim_x}x{dim_y}x{dim_z}", pad=20)

    # ====================================
    # 3. Coordenadas adaptadas às dimensões
    # ====================================
    x_coords, y_coords, z_coords = np.meshgrid(
        range(dim_x), 
        range(dim_y), 
        range(dim_z),
        indexing='ij'
    )

    x = x_coords.flatten()
    y = y_coords.flatten() 
    z = z_coords.flatten()
    valores = dados.flatten()

    # ====================================
    # 4. Plotar os pontos 3D
    # ====================================
    # Tamanho dos marcadores adaptativo
    tamanho_marcador = max(100, 500 // (dim_x * dim_y * dim_z)**0.33)
    
    pontos = ax.scatter(
        x, y, z,
        c=valores,
        cmap='viridis',
        s=tamanho_marcador,
        alpha=0.8,
        edgecolors='black',
        linewidths=1.0
    )

    # ====================================
    # 5. Adicionar os valores como texto
    # ====================================
    # Tamanho da fonte adaptativo
    tamanho_fonte = max(6, 10 - (dim_x * dim_y * dim_z)**0.2)
    
    for xi, yi, zi, val in zip(x, y, z, valores):
        # Offset em Z proporcional às dimensões
        offset_z = 0.1 * max(dim_x, dim_y, dim_z)
        
        # Cor do texto baseada no valor (para contraste)
        valor_min, valor_max = valores.min(), valores.max()
        limite_contraste = (valor_max + valor_min) / 2
        
        ax.text(
            xi, yi, zi + offset_z,
            f"{val:.2f}" if isinstance(val, float) else f"{val}",
            color='white' if val > limite_contraste else 'black',
            ha='center',
            va='center',
            fontsize=tamanho_fonte,
            fontweight='bold'
        )

    # ====================================
    # 6. Ajustar visualização dos eixos (ADAPTATIVO)
    # ====================================
    ax.set_xlabel(f'Eixo X (Dimensão 0 - Size: {dim_x})')
    ax.set_ylabel(f'Eixo Y (Dimensão 1 - Size: {dim_y})') 
    ax.set_zlabel(f'Eixo Z (Dimensão 2 - Size: {dim_z})')

    # Configurar ticks dinamicamente
    ax.set_xticks(range(dim_x))
    ax.set_yticks(range(dim_y))
    ax.set_zticks(range(dim_z))

    # Limites dos eixos com margem
    margem = 0.5
    ax.set_xlim(-margem, dim_x - 1 + margem)
    ax.set_ylim(-margem, dim_y - 1 + margem)
    ax.set_zlim(-margem, dim_z - 1 + margem)

    ax.grid(True, alpha=0.3)

    # Barra de cores
    fig.colorbar(pontos, ax=ax, shrink=0.6, label='Valor')

    # ====================================
    # 7. Adicionar grade 3D (se dimensões não forem muito grandes)
    # ====================================
    if dim_x <= 5 and dim_y <= 5 and dim_z <= 5:
        for i in range(dim_x):
            for j in range(dim_y):
                ax.plot([i, i], [j, j], [0, dim_z-1], 'gray', alpha=0.1, linewidth=0.5)
        for i in range(dim_x):
            for k in range(dim_z):
                ax.plot([i, i], [0, dim_y-1], [k, k], 'gray', alpha=0.1, linewidth=0.5)
        for j in range(dim_y):
            for k in range(dim_z):
                ax.plot([0, dim_x-1], [j, j], [k, k], 'gray', alpha=0.1, linewidth=0.5)

    # ====================================
    # 8. Mostrar o gráfico
    # ====================================
    plt.tight_layout()
    plt.show()
    
    return fig, ax

# ====================================
# EXEMPLOS DE USO COM DIFERENTES DIMENSÕES
# ====================================

print("=" * 60)
print("EXEMPLO 1: Matriz 3x3x3")
print("=" * 60)
dados_3x3x3 = np.arange(1, 28).reshape((3, 3, 3))
visualizar_matriz_3d(dados_3x3x3, "Matriz 3x3x3")

print("\n" + "=" * 60)
print("EXEMPLO 2: Matriz 2x4x3")
print("=" * 60)
dados_2x4x3 = np.arange(1, 25).reshape((2, 4, 3))
visualizar_matriz_3d(dados_2x4x3, "Matriz 2x4x3")

print("\n" + "=" * 60)
print("EXEMPLO 3: Matriz 4x4x4")
print("=" * 60)
dados_4x4x4 = np.arange(1, 65).reshape((4, 4, 4))
visualizar_matriz_3d(dados_4x4x4, "Matriz 4x4x4")

print("\n" + "=" * 60)
print("EXEMPLO 4: Matriz com valores decimais")
print("=" * 60)
dados_float = np.random.rand(3, 2, 4).round(2)
visualizar_matriz_3d(dados_float, "Matriz 3x2x4 (Valores Aleatórios)")

print("\n" + "=" * 60)
print("EXEMPLO 5: Sua matriz original de plantas")
print("=" * 60)
# Simulando seus dados de plantas (substitua pelos seus dados reais)
perdas_OXLIP = np.random.rand(5, 5)
perdas_GOLDENTUFT = np.random.rand(5, 5)
perdas_COSMOS = np.random.rand(5, 5)
perdas_ORCHID = np.random.rand(5, 5)
perdas_ARBUTUS = np.random.rand(5, 5)
perdas_ANEMONE = np.random.rand(5, 5)
perdas_MAGNOLIA = np.random.rand(5, 5)
perdas_MARIGOLD = np.random.rand(5, 5)

massas = np.stack([
    perdas_OXLIP,
    perdas_GOLDENTUFT,
    perdas_COSMOS,
    perdas_ORCHID,
    perdas_ARBUTUS,
    perdas_ANEMONE,
    perdas_MAGNOLIA,
    perdas_MARIGOLD
], axis=2)

print(f"Dimensões da sua matriz de plantas: {massas.shape}")
visualizar_matriz_3d(massas, "Matriz de Perdas das Plantas")

# ====================================
# FUNÇÃO PARA VISUALIZAR APENAS UMA MATRIZ ESPECÍFICA
# ====================================
def visualizar_matriz_especifica(dados, titulo=None):
    """
    Função simplificada para usar com seus dados
    """
    if titulo is None:
        titulo = f"Matriz {dados.shape[0]}x{dados.shape[1]}x{dados.shape[2]}"
    
    return visualizar_matriz_3d(dados, titulo)

# Uso rápido com seus dados:
# visualizar_matriz_especifica(massas, "Minha Matriz de Plantas")