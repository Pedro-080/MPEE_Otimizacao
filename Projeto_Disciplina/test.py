import numpy as np
import pandas as pd

class DadosFormatados:
    """
    Classe wrapper que mantém os dados como numpy array
    mas exibe como DataFrame formatado quando impressa.
    """
    def __init__(self, dados_array, nome_colunas=None, titulo="Dados"):
        self._array = np.asarray(dados_array)
        self._nome_colunas = nome_colunas
        self.titulo = titulo
        self._df_cache = None
    
    @property
    def array(self):
        """Acesso direto ao array numpy."""
        return self._array
    
    def _get_dataframe(self):
        """Cria DataFrame com cache."""
        if self._df_cache is None:
            dados = self._array
            
            if dados.ndim == 1:
                dados = dados.reshape(-1, 1)
            
            if self._nome_colunas is None:
                if dados.shape[1] == 1:
                    colunas = ['Valor']
                else:
                    colunas = [f'Col{i+1}' for i in range(dados.shape[1])]
            else:
                colunas = self._nome_colunas[:dados.shape[1]]
            
            self._df_cache = pd.DataFrame(
                dados,
                columns=colunas,
                index=range(1, len(dados) + 1)
            )
            self._df_cache.index.name = 'ID'
        
        return self._df_cache
    
    def __str__(self):
        """Exibe como DataFrame formatado."""
        df = self._get_dataframe()
        
        # Estilo personalizado
        estilo = """
        ╔══════════════════════════════════════════════════════════╗
        ║                     {:^40} ║
        ╠══════════════════════════════════════════════════════════╣
        {}
        ╠══════════════════════════════════════════════════════════╣
        ║ {:^56} ║
        ╚══════════════════════════════════════════════════════════╝
        """.format(
            self.titulo,
            df.to_string().replace('\n', '\n        ║ '),
            f"Total: {len(df)} registros"
        )
        
        return estilo
    
    def __repr__(self):
        return f"DadosFormatados(shape={self._array.shape}, titulo='{self.titulo}')"
    
    # Delega operações numpy ao array subjacente
    def __getitem__(self, key):
        return self._array[key]
    
    def __len__(self):
        return len(self._array)
    
    def __array__(self):
        return self._array
    
    @property
    def shape(self):
        return self._array.shape
    
    @property
    def ndim(self):
        return self._array.ndim
    
    def to_dataframe(self):
        return self._get_dataframe().copy()

class Homem:
    def __init__(self, nome, idade, forca, resistencia):
        self.nome = nome
        self.idade = idade
        
        # dados é uma instância de DadosFormatados
        self.dados = DadosFormatados(
            dados_array=np.array([
                [forca, resistencia],
                [forca * 0.9, resistencia * 1.1],
                [forca * 1.1, resistencia * 0.9]
            ]),
            nome_colunas=['Força Muscular', 'Resistência'],
            titulo=f"DADOS FÍSICOS - {nome.upper()}"
        )
    
    def __str__(self):
        return f"Homem: {self.nome}, {self.idade} anos"

class Mulher:
    def __init__(self, nome, idade, flexibilidade, equilibrio):
        self.nome = nome
        self.idade = idade
        
        self.dados = DadosFormatados(
            dados_array=np.array([
                [flexibilidade, equilibrio],
                [flexibilidade * 1.2, equilibrio * 0.8],
                [flexibilidade * 0.8, equilibrio * 1.2]
            ]),
            nome_colunas=['Flexibilidade', 'Equilíbrio'],
            titulo=f"DADOS FLEXIBILIDADE - {nome.upper()}"
        )
    
    def __str__(self):
        return f"Mulher: {self.nome}, {self.idade} anos"

# Teste
print("=== TESTE CLASSE HOMEM ===")
joao = Homem("João", 30, 85.5, 72.3)

print("\n1. print(joao):")
print(joao)

print("\n2. print(joao.dados):")
print(joao.dados)  # Exibe DataFrame formatado!

print("\n3. Ainda funciona como array:")
print(f"   Tipo: {type(joao.dados.array)}")
print(f"   Shape: {joao.dados.shape}")
print(f"   Primeiro valor: {joao.dados[0, 0]}")

print("\n=== TESTE CLASSE MULHER ===")
maria = Mulher("Maria", 28, 92.1, 88.4)
print(maria.dados)  # Formatação específica para mulher