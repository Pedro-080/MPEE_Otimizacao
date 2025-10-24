# flake8: noqa

from cabos import OXLIP, GOLDENTUFT, COSMOS, ORCHID, ARBUTUS , ANEMONE, MAGNOLIA, MARIGOLD
import numpy as np

Pot_aero_MW = 6
Pot_circ_MW = 18
FP          = 0.95
FC_100      = 1 

# DADOS DE ENTRADA
comprimento = np.array([
[   0,1000,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[1000,   0,1000,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[   0,1000,   0,1000,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[   0,   0,1000,   0,1000,   0,   0,   0,   0,   0,   0,   0,   0],
[   0,   0,   0,1000,   0,1000,   0,   0,   0,   0,   0,   0,   0],
[   0,   0,   0,   0,1000,   0,1000,   0,   0,   0,   0,   0,   0],
[   0,   0,   0,   0,   0,1000,   0,1000,   0,   0,   0,   0,   0],
[   0,   0,   0,   0,   0,   0,1000,   0,1000,   0,   0,   0,   0],
[   0,   0,   0,   0,   0,   0,   0,1000,   0,1000,   0,   0,   0],
[   0,   0,   0,   0,   0,   0,   0,   0,1000,   0,1000,   0,   0],
[   0,   0,   0,   0,   0,   0,   0,   0,   0,1000,   0,1000,   0],
[   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,1000,   0,1000],
[   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,1000,   0]
])



agrupamento = np.array([
[   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[   1,   0,   2,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[   0,   2,   0,   3,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[   0,   0,   3,   0,   3,   0,   0,   0,   0,   0,   0,   0,   0],
[   0,   0,   0,   3,   0,   3,   0,   0,   0,   0,   0,   0,   0],
[   0,   0,   0,   0,   3,   0,   3,   0,   0,   0,   0,   0,   0],
[   0,   0,   0,   0,   0,   3,   0,   3,   0,   0,   0,   0,   0],
[   0,   0,   0,   0,   0,   0,   3,   0,   3,   0,   0,   0,   0],
[   0,   0,   0,   0,   0,   0,   0,   3,   0,   3,   0,   0,   0],
[   0,   0,   0,   0,   0,   0,   0,   0,   3,   0,   3,   0,   0],
[   0,   0,   0,   0,   0,   0,   0,   0,   0,   3,   0,   3,   0],
[   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   3,   0,   3],
[   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   3,   0]
])

Pot_acumulado_MW = agrupamento * Pot_aero_MW

perdas_OXLIP      = OXLIP.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_GOLDENTUFT = GOLDENTUFT.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_COSMOS     = COSMOS.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_ORCHID     = ORCHID.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_ARBUTUS    = ARBUTUS.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_ANEMONE    = ANEMONE.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_MAGNOLIA   = MAGNOLIA.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)
perdas_MARIGOLD   = MARIGOLD.array_calcular_perdas_percent(comprimento, Pot_acumulado_MW, Pot_circ_MW, FP, FC_100)


# print(perdas_OXLIP)
# print(perdas_MARIGOLD)