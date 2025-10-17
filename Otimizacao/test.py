def funcao_ajustavel(expressao, x):
    """
    Avalia uma expressão matemática para um dado valor de x
    
    Args:
        expressao (str): Expressão como "x**2", "2*x + 1", etc.
        x (float): Valor de entrada
    
    Returns:
        float: Resultado da expressão
    """
    return eval(expressao)

# Exemplos de uso
print(funcao_ajustavel("x**2", 5))        # 25
print(funcao_ajustavel("2*x + 1", 3))     # 7
print(funcao_ajustavel("x**3 - 2*x", 2))  # 4