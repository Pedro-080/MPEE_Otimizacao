class Configurar:
    """Classe base com configurações globais que podem ser ajustadas uma vez."""
    
    # Configurações padrão
    Pot_aero_MW  = 6
    FP           = 0.95                                       # Fator de potencia 
    FC       = 1                                              # Fator de capacidade considerado. 1 = 100%
    perda_maxima_percent = 2                                  # Pedra máxima global tolerada em porcentagem.  2 = 2%  

    @classmethod
    def Setup_projeto(cls, **kwargs):
        """Configura os parâmetros globais do sistema."""
        for chave, valor in kwargs.items():
            if hasattr(cls, chave.upper()):
                setattr(cls, chave.upper(), valor)
                print(f"Configuração '{chave}' definida como: {valor}")
            else:
                print(f"⚠️ Configuração '{chave}' não existe!")

class Circuito(Configurar):
    """Classe principal que herda as configurações."""

    # Método inicializador (construtor)
    def __init__(self, comprimento, agrupamento):
        self.comprimento = comprimento     #Matriz de inicialização das distancias
        self.agrupamento = agrupamento     #Matriz de inicialização dos agrupamentos

        ...

    def __str__(self):
        return (f"comprimento: \n {self.comprimento} ")