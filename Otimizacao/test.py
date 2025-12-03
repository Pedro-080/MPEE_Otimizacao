class ConfiguracaoBase:
    """Classe base com configurações globais que podem ser ajustadas uma vez."""
    
    # Configurações padrão
    TAXA_JUROS = 0.05      # 5%
    MOEDA = "R$"
    LIMITE_GLOBAL = 10000
    PAIS = "Brasil"
    
    @classmethod
    def configurar_sistema(cls, **kwargs):
        """Configura os parâmetros globais do sistema UMA ÚNICA VEZ."""
        for chave, valor in kwargs.items():
            if hasattr(cls, chave.upper()):
                setattr(cls, chave.upper(), valor)
                print(f"Configuração '{chave}' definida como: {valor}")
            else:
                print(f"⚠️ Configuração '{chave}' não existe!")

class ContaBancaria(ConfiguracaoBase):
    """Classe principal que herda as configurações."""
    
    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular
        self.saldo = saldo_inicial
        self.numero_conta = self._gerar_numero_conta()
    
    # Atributo de classe para controle de contas
    _proximo_numero = 1000
    
    @classmethod
    def _gerar_numero_conta(cls):
        numero = cls._proximo_numero
        cls._proximo_numero += 1
        return numero
    
    def aplicar_juros(self):
        """Aplica juros usando a taxa configurada na classe base."""
        juros = self.saldo * self.TAXA_JUROS  # Herdado!
        self.saldo += juros
        print(f"{self.titular}: Juros de {self.MOEDA}{juros:.2f} aplicados ({self.TAXA_JUROS*100:.1f}%)")
    
    def depositar(self, valor):
        self.saldo += valor
        return f"Depósito de {self.MOEDA}{valor:.2f} realizado."
    
    def __str__(self):
        return (f"Conta {self.numero_conta} | {self.titular} | "
                f"Saldo: {self.MOEDA}{self.saldo:.2f} | "
                f"País: {self.PAIS}")

# ============ USO ============

# 1. CONFIGURAÇÃO ÚNICA ANTES DE CRIAR CONTAS
print("=== CONFIGURANDO SISTEMA ===")
ContaBancaria.configurar_sistema(
    taxa_juros=0.08,      # 8%
    moeda="US$",
    limite_global=50000,
    pais="Portugal"
)

print("\n=== CRIANDO CONTAS ===")
# 2. AGORA CRIAMOS AS CONTAS
conta1 = ContaBancaria("Ana Silva", 1500)
conta2 = ContaBancaria("Bruno Costa", 3000)
conta3 = ContaBancaria("Carla Santos", 500)

print(conta1)
print(conta2)
print(conta3)

print("\n=== APLICANDO JUROS ===")
conta1.aplicar_juros()
conta2.aplicar_juros()

# Tenta mudar configuração depois (não deve afetar contas existentes)
print("\n=== TENTANDO MUDAR CONFIGURAÇÃO TARDE ===")
ContaBancaria.TAXA_JUROS = 0.10  # 10%
conta3.aplicar_juros()  # Vai usar 10% agora!