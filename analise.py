
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging


sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")



def carregar_dados(caminho: str) -> pd.DataFrame:
    """Carrega e trata os dados da base de vendas."""
    try:
        df = pd.read_excel("/content/Cópia de Base de Vendas Varejo.xlsx")
        df['Data da Venda'] = pd.to_datetime(df['Data da Venda'], errors='coerce')
        df['Receita'] = df['Valor da Venda'] - df['Custo']
        df['AnoMes'] = df['Data da Venda'].dt.to_period('M')
        df['Ano'] = df['Data da Venda'].dt.year
        logging.info("Dados carregados e pré-processados com sucesso.")
        return df
    except Exception as e:
        logging.error(f"Erro ao carregar dados: {e}")
        raise


def resumo_geral(df: pd.DataFrame):
    print("\n📊 [Resumo dos Dados]")
    print(df.info())
    print("\nNulos por Coluna:\n", df.isnull().sum())
    print("\nAmostra:\n", df.sample(5))

def receita_total(df: pd.DataFrame):
    total = df['Receita'].sum()
    print(f"\n💰 Receita Total: R$ {total:,.2f}")

def receita_por_estado(df: pd.DataFrame):
    receita = df.groupby('Estado')['Receita'].sum().sort_values()
    print("\n📍 Receita por Estado:\n", receita)
    receita.plot(kind='barh', title='Receita por Estado', color='#4682B4')
    plt.xlabel("Receita (R$)")
    plt.tight_layout()
    plt.show()

def receita_por_categoria(df: pd.DataFrame):
    receita = df.groupby('Categoria')['Receita'].sum().sort_values()
    print("\n📦 Receita por Categoria:\n", receita)
    sns.barplot(x=receita.values, y=receita.index)
    plt.title("Receita por Categoria")
    plt.xlabel("Receita")
    plt.tight_layout()
    plt.show()

def receita_mensal(df: pd.DataFrame):
    receita_mensal = df.groupby('AnoMes')['Receita'].sum()
    receita_mensal.plot(marker='o')
    plt.title("Evolução Mensal da Receita")
    plt.xlabel("Ano-Mês")
    plt.ylabel("Receita (R$)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def produto_mais_vendido(df: pd.DataFrame):
    produtos = df.groupby('Produto')['Quantidade'].sum().sort_values(ascending=False)
    print("\n🛒 Produtos Mais Vendidos:\n", produtos.head(10))
    produtos.head(10).plot(kind='bar', title='Top 10 Produtos Vendidos', color='#2E8B57')
    plt.ylabel("Quantidade")
    plt.tight_layout()
    plt.show()

def receita_por_vendedor(df: pd.DataFrame):
    vendedores = df.groupby('Vendedor')['Receita'].sum().sort_values()
    print("\n👔 Receita por Vendedor:\n", vendedores)
    vendedores.plot(kind='barh', title='Receita por Vendedor', color='#A0522D')
    plt.xlabel("Receita (R$)")
    plt.tight_layout()
    plt.show()

def correlacao_desconto_receita(df: pd.DataFrame):
    sns.scatterplot(data=df, x='Desconto', y='Receita', hue='Categoria', alpha=0.7)
    plt.title("Desconto vs Receita")
    plt.tight_layout()
    plt.show()

def boxplot_receita_segmento_categoria(df: pd.DataFrame):
    sns.boxplot(data=df, x='Segmento', y='Receita', hue='Categoria')
    plt.title("Receita por Segmento e Categoria")
    plt.tight_layout()
    plt.show()


def executar_analise(caminho_arquivo: str):
    df = carregar_dados(caminho_arquivo)
    
    resumo_geral(df)
    receita_total(df)
    receita_por_estado(df)
    receita_por_categoria(df)
    receita_mensal(df)
    produto_mais_vendido(df)
    receita_por_vendedor(df)
    correlacao_desconto_receita(df)
    boxplot_receita_segmento_categoria(df)


if __name__ == "__main__":
    CAMINHO_ARQUIVO = "/mnt/data/Cópia de Base de Vendas Varejo.xlsx"
    executar_analise(CAMINHO_ARQUIVO)
