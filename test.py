# flake8: noqa
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Gerar 5 matrizes 5x5 (camadas 0 a 4) ---
A = np.arange(1, 26).reshape(5, 5)
B = np.arange(26, 51).reshape(5, 5)
C = np.arange(51, 76).reshape(5, 5)
D = np.arange(76, 101).reshape(5, 5)
E = np.arange(101, 126).reshape(5, 5)

# --- Empilhar para formar matriz 3D ---
M = np.stack([A, B, C, D, E])  # shape (5, 5, 5)

# --- Criar coordenadas (x, y, z) ---
z, y, x = np.indices(M.shape)

# --- Transformar tudo em vetores 1D ---
x = x.flatten()
y = y.flatten()
z = z.flatten()
values = M.flatten()

# --- Plotagem 3D ---
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter(
    x, y, z,
    c=values,          # cor = valor numérico
    cmap='plasma',
    s=60,
    edgecolor='k'
)

# --- Configurações ---
ax.set_xlabel('Coluna (j)')
ax.set_ylabel('Linha (i)')
ax.set_zlabel('Camada (k)')
ax.set_title('Matriz 3D composta por 5 matrizes 5×5')
fig.colorbar(sc, ax=ax, label='Valor da matriz')

# --- Melhor ângulo de visualização ---
ax.view_init(elev=25, azim=40)

plt.show()
