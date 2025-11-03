# flake8: noqa
import numpy as np

def inverter_matriz(matriz_2d):
    '''Retorna os elementos da matriz de entrada invertidos (1/x)'''
    Eye = np.eye(matriz_2d.shape[0])
    K = matriz_2d + Eye
    K = 1/K
    return K - Eye



# ==========================================
# CONFIGURAÇÕES ACO
# ==========================================
q = 10         # quantidade de feromônio depositada
s = 0.01       # taxa de evaporação do feromônio
fer = 0.1      # Quantidade de feromonio inicial
a0 = 1         # Parâmetro de influência do feromônio inicial
b = 1          # Parâmetro de influência de distância
err = 10e-4    # Erro tolerado

fo = 10        # Número de formigas simuladas
iteracoes = 5  # Número máximo de iterações


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

NCidades = d.shape[0]
y        = d.shape[1]


print(f"NCidades:{NCidades}")

#Definição da matriz Tau com os feromônios iniciais
Feromonio = np.ones((NCidades,NCidades)) *0.001

#Definição da matriz que armazenará os caminhos percorridos
Matriz_Infor      = np.zeros((fo, NCidades), dtype=int)            #Matriz de caminhos original
Matriz_Infor_Temp = Matriz_Infor                              #Matriz de caminhos que serão alterados

#Definição da matriz de probabilidades 
prob = np.zeros((fo, NCidades))

#Calculo da matriz de atratividade
n = inverter_matriz(d)



inter=1
while inter <= iteracoes:
    #Definição da função objetivo
    FuncObj      = np.zeros((fo,1))

    #Definição da matriz de caminhos de cada formiga
    Matriz_Infor = np.zeros((fo,NCidades))
    print(inter)

    # print(Matriz_Infor)

    for f in range(0,fo):
        Matriz_Infor[f][1] = np.random.randint(0,NCidades)
        # print(f" Matriz_Infor({f},1):{ Matriz_Infor[f][1]}")
        Part = int(Matriz_Infor[f][1])
        ProxCidade = Part
        # print(f"type:{type(Part)}")
        # print(f"Part:{Part}")

        # print(Feromonio)
        Tot = np.sum(Feromonio[Part])
        # print(f"Tot:{Tot}")
        # print(f"f: {f}")
        # print(f"{rand}")
        for i in range(1,NCidades):
            TesteFer = 0
            while TesteFer == 0:
                teste = 0
                Roleta =np.random.random()*Tot
                TotFer = 0
                for k in range(1,NCidades):
                    TotFer = TotFer + Feromonio[ProxCidade][k]
                    if Roleta < TotFer & teste == 0:
                        ProxCidade = k
                        teste = 1
                        ...
                    ...
                TesteFer = 1
                for k in range(1,NCidades):
                    if ProxCidade == Matriz_Infor[f][k]:
                        TesteFer = 0
                if TesteFer == 1:
                    Tot = np.sum(Feromonio[ProxCidade])
                    ...
            
            Matriz_Infor[f][i] = ProxCidade
            FuncObj[f] = FuncObj[f] + k 

    inter += 1