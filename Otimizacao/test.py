import numpy as np
import pandas as pd

def array_3d_to_dataframe_com_nomes(arr, condutores, nomes_colunas=None):
    """
    Versão que permite especificar nomes para cada coluna de valores.
    
    Args:
        arr: array 3D shape (n_condutores, n_linhas, n_colunas)
        condutores: lista de nomes dos condutores
        nomes_colunas: lista de nomes para as colunas de valores
    
    Returns:
        DataFrame com colunas nomeadas
    """
    n_condutores, n_linhas, n_colunas = arr.shape
    
    # Verificar consistência
    if len(condutores) != n_condutores:
        raise ValueError(f"Array tem {n_condutores} condutores, mas foram fornecidos {len(condutores)} nomes")
    
    # Se nomes_colunas não for fornecido, criar padrão
    if nomes_colunas is None:
        nomes_colunas = [f'col_{i}' for i in range(n_colunas)]
    elif len(nomes_colunas) != n_colunas:
        raise ValueError(f"Array tem {n_colunas} colunas, mas foram fornecidos {len(nomes_colunas)} nomes")
    
    # Achatar o array
    dados_flat = arr.reshape(-1, n_colunas)
    
    # Criar nomes de condutores repetidos
    condutores_repetidos = np.repeat(condutores, n_linhas)
    
    # Criar DataFrame
    df = pd.DataFrame(dados_flat, columns=nomes_colunas)
    df.insert(0, 'condutor', condutores_repetidos)
    
    return df

# Exemplo com nomes personalizados:
print("=" * 60)
print("EXEMPLO COM NOMES PERSONALIZADOS")
print("=" * 60)

arr_teste = np.array([
    [[0.01, 0.02, 0.03], [0.04, 0.05, 0.06], [0.07, 0.08, 0.09]],  # OXLIP
    [[0.10, 0.11, 0.12], [0.13, 0.14, 0.15], [0.16, 0.17, 0.18]],  # ORCHID
    [[0.19, 0.20, 0.21], [0.22, 0.23, 0.24], [0.25, 0.26, 0.27]]   # MARIGOLD
])

condutores = ['OXLIP', 'ORCHID', 'MARIGOLD']
nomes_colunas = ['perda_min', 'perda_media', 'perda_max']

df_personalizado = array_3d_to_dataframe_com_nomes(arr_teste, condutores, nomes_colunas)
print(f"Array shape: {arr_teste.shape}")
print(f"DataFrame shape: {df_personalizado.shape}")
print(df_personalizado)