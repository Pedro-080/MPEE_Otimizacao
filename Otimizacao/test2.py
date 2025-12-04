import numpy as np
import pandas as pd

# Baseado no que você mostrou na mensagem:
# Você quer este resultado:
"""
      condutor  row  col  
0   Condutor_A    1   11      
1   Condutor_A    2   12      
2   Condutor_A    3   13      
3   Condutor_B    4   14      
4   Condutor_B    5   15      
5   Condutor_B    6   16      
6   Condutor_C    7   17      
7   Condutor_C    8   18  
8   Condutor_C    9   19
"""

# Criar array com os valores EXATOS:
arr_exato = np.array([
    # Con= np.array([
    # Condutor A: 3 linhas, 2 colunas
    [[1, 11, 21],    # linha 0 do condutor A
     [2, 12, 22],    # linha 1 do condutor A  
     [3, 13, 23]],   # linha 2 do condutor A
    
    # Condutor B: 3 linhas, 2 colunas
    [[4, 14, 24],    # linha 0 do condutor B
     [5, 15, 25],    # linha 1 do condutor B
     [6, 16,  26]],   # linha 2 do condutor B
    
    # Condutor C: 3 linhas, 2 colunas  
    [[7, 17,  27],    # linha 0 do condutor C
     [8, 18, 28],    # linha 1 do condutor C
     [9, 19,  29]]    # linha 2 do condutor C
])  # Shape: (3, 3, 2) -> 3 condutores × 3 linhas × 2 colunas

condutores = ['Condutor_A', 'Condutor_B', 'Condutor_C']

# Função específica para o formato que você quer:
def criar_df_do_exemplo(arr, condutores):
    """Cria DataFrame exatamente como no seu exemplo."""
    n_condutores, n_linhas, n_colunas = arr.shape
    
    dados = []
    for i, condutor in enumerate(condutores):
        matriz = arr[i]
        for linha in matriz:
            # Cada linha tem 2 valores: [valor1, valor2]
            dados.append({
                'condutor': condutor,
                'row': linha[0],  # Primeiro valor vai para 'row'
                'col': linha[1]   # Segundo valor vai para 'col'
            })
    
    return pd.DataFrame(dados)

# Testar
df_exemplo = criar_df_do_exemplo(arr_exato, condutores)
print("\nDataFrame EXATAMENTE como seu exemplo:")
print(df_exemplo)
print("\nTipo de dados:")
print(df_exemplo.dtypes)