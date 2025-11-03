import numpy as np
import random

# ================================
# PARÂMETROS DO ALGORITMO
# ================================
q = 10      # Constante de atualização do feromônio
s = 0.01    # Evaporação do feromônio
fer = 0.1   # Feromônio inicial
a0 = 1      # Parâmetro de influência de feromônio, inicial
b = 1       # Parâmetro de influência de distância
err = 10**(-4)

# Matriz de distâncias
d = np.array([
    [0, 76.5, 27.2, 100.3, 127.5, 154.7, 181.9, 209.1],
    [76.5, 0, 44.2, 98.6, 125.8, 153, 180.2, 207.4],
    [27.2, 44.2, 0, 107.1, 134.3, 161.5, 188.7, 215.9],
    [100.3, 98.6, 107.1, 0, 27.2, 54.4, 81.6, 108.8],
    [127.5, 125.8, 134.3, 27.2, 0, 27.2, 54.4, 81.6],
    [154.7, 153, 161.5, 54.4, 27.2, 0, 27.2, 54.4],
    [181.9, 180.2, 188.7, 81.6, 54.4, 27.2, 0, 27.2],
    [209.1, 207.4, 215.9, 108.8, 81.6, 54.4, 27.2, 0]
])

SETOR = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

NCidades = d.shape[0]
y = d.shape[1]
h, v = d.shape[0], d.shape[1]

# print(f"NCidades: {NCidades}, y: {y}")
# print(f"h: {h}, v: {v}")

# ================================
# INICIALIZAÇÃO
# ================================
fo = 20                                      # Número de formigas, duas por cidade
Feromonio = np.ones((NCidades, NCidades)) * 0.001  # Deposição inicial de feromonio
Matriz_Infor = np.zeros((fo, NCidades))     # Caminho das formigas
Matriz_Infor_Temp = Matriz_Infor.copy()     # Informativo das cidades
iteracoes = 5                               # Número de iterações
prob = np.zeros((fo, NCidades))             # Matriz probabilidade

K = d + np.eye(NCidades, NCidades)          # Matriz auxiliar para somar zeros
# print("Matriz K:")
# print(K)

m1 = K**(-1)                                # Invertendo termos da matriz auxiliar
n1 = m1 - np.eye(NCidades, NCidades)        # Matriz de termos inversos a distância

inter = 0
FOmin = 1000  # Valor inicial alto
MelhorCaminho = None

# ================================
# ALGORITMO PRINCIPAL
# ================================
while inter <= iteracoes:
    FuncObj = np.zeros(fo)
    Matriz_Infor = np.zeros((fo, NCidades))
    
    print(f'\n--- Iteração {inter} ---')
    
    for f in range(fo):
        # A formiga partirá de um ponto inicial aleatório
        Matriz_Infor[f, 0] = 1 + int(abs(8 * random.random()))
        Part = int(Matriz_Infor[f, 0])
        ProxCidade = Part
        Tot = np.sum(Feromonio[Part-1, :])
        
        # print(f'\nFormiga {f+1} começando na cidade {Part}')
        
        for i in range(1, h):
            TesteFer = 0
            # print(f'  Buscando cidade {i+1}, Total Feromônio: {Tot}')
            
            while TesteFer == 0:
                teste = 0
                Roleta = random.random() * Tot
                TotFer = 0.0
                
                # print(f'    Roleta: {Roleta}')
                
                for k in range(NCidades):
                    TotFer += Feromonio[ProxCidade-1, k]
                    # print(f'      Cidade {k+1}: TotFer={TotFer}')
                    
                    if Roleta < TotFer and teste == 0:
                        ProxCidade = k + 1  # +1 porque Python indexa de 0
                        teste = 1
                        # print(f'      >>> Escolhida cidade {ProxCidade}')
                
                TesteFer = 1
                # Verifica se cidade já foi visitada
                for k in range(NCidades):
                    if ProxCidade == Matriz_Infor[f, k]:
                        TesteFer = 0
                        # print(f'      Cidade {ProxCidade} repetida, tentando novamente')
                        break
                
                if TesteFer == 1:
                    Tot = np.sum(Feromonio[ProxCidade-1, :])
            
            # Armazena os caminhos percorridos
            Matriz_Infor[f, i] = ProxCidade
            
            # Armazena os custos dos caminhos percorridos
            cidade_anterior = int(Matriz_Infor[f, i-1]) - 1
            cidade_atual = int(Matriz_Infor[f, i]) - 1
            FuncObj[f] += d[cidade_anterior, cidade_atual]
        
        # print(f'  Caminho da formiga {f+1}: {Matriz_Infor[f, :]}')
        # print(f'  Distância total: {FuncObj[f]}')
        
        # Atualização do feromônio
        for k in range(1, NCidades):
            in_cidade = int(Matriz_Infor[f, k]) - 1
            fn_cidade = int(Matriz_Infor[f, k-1]) - 1
            
            # Atualização do feromônio (evaporação + depósito)
            Feromonio[in_cidade, fn_cidade] = (1 - 0.08) * Feromonio[in_cidade, fn_cidade] + 1 / FuncObj[f]
            # Feromonio[fn_cidade, in_cidade] = Feromonio[in_cidade, fn_cidade]  # Simetria
    
    # Encontra melhor solução da iteração
    for j in range(fo):
        if FuncObj[j] < FOmin and FuncObj[j] != 0:
            Min = FuncObj[j]
            Caminho = Matriz_Infor[j, :].copy()
            FOmin = Min
            MelhorCaminho = Caminho.copy()
            print(f'>>> NOVA MELHOR SOLUÇÃO: Distância = {Min:.2f}')
    
    inter += 1

# ================================
# RESULTADOS FINAIS
# ================================
print('\n' + '='*50)
print('RESULTADO FINAL')
print('='*50)

if MelhorCaminho is not None:
    print(f'Melhor distância encontrada: {FOmin:.2f}')
    print('Melhor caminho (números):', MelhorCaminho.astype(int))
    
    print('Melhor caminho (letras): ', end='')
    for cidade in MelhorCaminho:
        print(SETOR[int(cidade)-1], end=' ')
    print()
    
    # Verificação da distância
    distancia_verificada = 0
    print('\nDetalhamento do caminho:')
    for i in range(1, len(MelhorCaminho)):
        cidade_origem = int(MelhorCaminho[i-1]) - 1
        cidade_destino = int(MelhorCaminho[i]) - 1
        dist_trecho = d[cidade_origem, cidade_destino]
        distancia_verificada += dist_trecho
        print(f'{SETOR[cidade_origem]} -> {SETOR[cidade_destino]}: {dist_trecho:.1f} km')
    
    print(f'Distância total verificada: {distancia_verificada:.2f} km')
    
    # Exibe matriz de feromônio final
    print('\nMatriz de Feromônio final (primeiras 5x5):')
    print(Feromonio[:5, :5])
else:
    print('Nenhuma solução válida foi encontrada.')