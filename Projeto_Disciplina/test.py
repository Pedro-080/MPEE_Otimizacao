import numpy as np
import matplotlib.pyplot as plt

# 1. Definir a função
def crescimento_exponencial(x, a=1, b=1):
    """
    Função que vale 0 em x=0 e cresce exponencialmente para x>0.
    f(x) = a * (exp(b*x) - 1)
    """
    return  a * (np.exp(b * (x-2)) - 1)

# 2. Criar valores de x
x = np.linspace(0, 5, 100)  # 100 pontos entre 0 e 5

# 3. Calcular y para diferentes parâmetros
y1 = crescimento_exponencial(x, a=1, b=0.5)   # Crescimento mais suave
y2 = crescimento_exponencial(x, a=1, b=1.0)   # Crescimento padrão
y3 = crescimento_exponencial(x, a=1, b=1.5)   # Crescimento mais acentuado
y4 = crescimento_exponencial(x, a=2, b=5)   # Maior amplitude

# 4. Configurar o gráfico
plt.figure(figsize=(10, 6))

# Plotar cada curva
plt.plot(x, y1, 'b-', linewidth=2, label=r'$b=0.5, a=1$')
plt.plot(x, y2, 'r-', linewidth=2, label=r'$b=1.0, a=1$ (padrão)')
plt.plot(x, y3, 'g-', linewidth=2, label=r'$b=1.5, a=1$')
plt.plot(x, y4, 'm--', linewidth=2, label=r'$b=1.0, a=2$')

# Destacar o ponto x=0
plt.scatter([0], [0], color='black', zorder=5, s=50)
plt.annotate('f(0) = 0', xy=(0, 0), xytext=(0.3, 2),
             arrowprops=dict(arrowstyle='->', color='black'))

# Configurações do gráfico
plt.xlabel('x', fontsize=12)
plt.ylabel('f(x)', fontsize=12)
plt.title('Função Exponencial: f(x) = a × (exp(b·x) - 1)', fontsize=14)
plt.legend(loc='upper left', fontsize=10)
plt.grid(True, alpha=0.3)

# Definir limites dos eixos
plt.xlim(0, 5)
plt.ylim(0, 150)

# Adicionar grade secundária
plt.minorticks_on()
plt.grid(which='minor', alpha=0.2)

# 5. Mostrar o gráfico
plt.tight_layout()
plt.show()

# 6. (Opcional) Mostrar alguns valores numéricos
print("\nValores da função para b=1.0, a=1:")
print("x = 0.0 → f(x) =", crescimento_exponencial(0.0, 1, 1))
print("x = 1.0 → f(x) =", crescimento_exponencial(1.0, 1, 1))
print("x = 2.0 → f(x) =", crescimento_exponencial(2.0, 1, 1))
print("x = 3.0 → f(x) =", crescimento_exponencial(3.0, 1, 1))
print("x = 4.0 → f(x) =", crescimento_exponencial(4.0, 1, 1))
print("x = 5.0 → f(x) =", crescimento_exponencial(5.0, 1, 1))