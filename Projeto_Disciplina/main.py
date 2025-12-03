# 1. CONFIGURAÇÃO ÚNICA ANTES DE CRIAR CONTAS

from classes import Configurar, Circuito

print("=== CONFIGURANDO SISTEMA ===")
Circuito.Setup_projeto(
    Pot_aero_MW  = 6,                  # Potencia por aerogerador
    FP           = 0.95,               # Fator de potencia 
    FC           = 1,                  # Fator de capacidade considerado. 1 = 100%
    perda_maxima_percent = 2 
)