import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import filtros as f

# Configuração do nome da aba
st.set_page_config(
    page_title="Análise",
    page_icon="",
    layout='wide'
)

# Título do Dashboard
st.title('Dashboard de Análise e Previsão do Preço de Combustíveis')

# Datasets
# Resolvendo problema do caminho do windows
base_path = os.path.dirname(__file__)
csv_path = os.path.join(base_path, 'precos_tratado.csv')
df_tratado = pd.read_csv(csv_path)

# Sidebar Principal / Barra Lateral
sidebar_principal = st.sidebar

# sidebar_principal.image('logo.png') # Ver como colocar a logo no topo do sidebar

# Filtros -----------------------------------------------------------------------------------
sidebar_principal.markdown('**FILTROS**:')
# Filtro de Combustível
combustiveis = df_tratado['PRODUTO'].unique()
selecao_comb = sidebar_principal.multiselect('Tipo de Combustível', options=combustiveis, default=combustiveis)

# Filtros de Período de Tempo
# Ano
periodo_ano = df_tratado['ANO_SEP'].unique()
sel_anos = sidebar_principal.slider('Escolha o ano', periodo_ano.min(), periodo_ano.max(), value=(periodo_ano.min(), periodo_ano.max()))
df_filtra_dataset = f.filtra_dataset(combustivel=selecao_comb, ano=sel_anos, mes=None)

# Mês
periodo_mes = df_filtra_dataset['MÊS_SEP'].unique()
sel_meses = sidebar_principal.slider('Escolha o mês', periodo_mes.min(), periodo_mes.max(), value=(periodo_mes.min(), periodo_mes.max()))

# Filtra o dataset de acordo com a escolha da seleção múltipla
df_filtra_dataset = f.filtra_dataset(selecao_comb, sel_anos, sel_meses)
df_filtra_dataset['DATA'] = pd.to_datetime(df_filtra_dataset['ANO_SEP'].astype(str) + '-' + df_filtra_dataset['MÊS_SEP'].astype(str))

# Métricas --------------------------------------------------------------------------------------
preco_medio_revenda = df_filtra_dataset.groupby('PRODUTO')['PREÇO MÉDIO REVENDA'].mean()

# Linha com 3 Colunas e 3 Containeres
row1 = st.columns(len(selecao_comb))
cont = 0
for col in row1:
    container = col.container(border=True)
    container.write(f'Preço Médio de Revenda - {combustiveis[cont]}')
    container.markdown(f'### **R${round(preco_medio_revenda[cont], 2)}**')
    
    # Mostra o preço mais alto e o mais baixo no período selecionado
    df = df_filtra_dataset[df_filtra_dataset.PRODUTO == combustiveis[cont]]
    row2 = container.columns(2)
    row2[0].markdown(f'Mínimo: **R${round(df['PREÇO MÉDIO REVENDA'].min(), 2)}**')
    row2[1].markdown(f'Máximo: **R${round(df['PREÇO MÉDIO REVENDA'].max(), 2)}**')
    cont+=1


# Gráficos -----------------------------------------------------------------------------------

# Configurações gerais
mapa_cores = {
    'ETANOL HIDRATADO': '#ADD8E6', # Azul clarinho
    'GASOLINA COMUM': '#FF7F00',   # Laranja
    'OLEO DIESEL': '#FFBF00' # Âmbar
    }

# Estilo de Tema
sns.set_theme(style="whitegrid") 
sns.despine()

# Preço Médio Revenda  
container1 = st.container()
col1, col2 = container1.columns([2, 1])

with col1:
    # Gráfico de linha de Comparação de Preço Médio
    plt.figure(figsize=(8,3))
    grafico_linha, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=df_filtra_dataset, x=df_filtra_dataset['ANO_SEP'].astype(str), y='PREÇO MÉDIO REVENDA', hue='PRODUTO', marker='o', palette=mapa_cores, ax=ax)
    ax.set_title('Evolução do Preço Médio de Revenda de Combustíveis ao Longo dos Anos', size=15)
    ax.set_xlabel('Ano')
    ax.set_ylabel('Preço Médio (R$/l)')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title='Produto')
    grafico_linha.tight_layout()

    col1.pyplot(grafico_linha)

with col2:
    # Boxplot de Preço médio por Ano
    boxplot_ano, ax = plt.subplots(figsize=(10,5))
    sns.boxplot(data=df_filtra_dataset, x="ANO_SEP", y="PREÇO MÉDIO REVENDA", hue="PRODUTO", palette=mapa_cores)
    ax.set_title('Evolução de Preço Médio de Revenda Ao Longo dos Anos', size=20)
    ax.set_xlabel('Ano')
    ax.set_ylabel('Preço R$')
    ax.legend(title='Produto')
    boxplot_ano.tight_layout()

    col2.pyplot(boxplot_ano)

    # Boxplot de Preço médio por mês
    boxplot_meses, ax = plt.subplots(figsize=(10,5))
    sns.boxplot(data=df_filtra_dataset, x="MÊS_SEP", y="PREÇO MÉDIO REVENDA", hue="PRODUTO", palette=mapa_cores)
    ax.set_title('Evolução de Preço Médio de Revenda Ao Longo dos Meses', size=20)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Preço R$')
    ax.legend(title='Produto')
    boxplot_meses.tight_layout()

    col2.pyplot(boxplot_meses)

df_preco_medio = df_filtra_dataset.loc[:, ['PRODUTO', 'DATA', 'PREÇO MÉDIO REVENDA', 'PREÇO MÍNIMO REVENDA', 'PREÇO MÁXIMO REVENDA']]

# Expander para mostrar df
mostrar_df = st.expander('Marque para exibir o DataFrame', expanded=False,)
mostrar_df.subheader("DataFrame de Preço Médio de Revenda")
mostrar_df.dataframe(df_preco_medio)

# Desvio Padrão
st.divider()

st.markdown('## Variação do Preço Médio de Revenda')
container2 = st.container(border=False)
col1, col2 = container2.columns([1, 2])

with col1:
    for i in range(len(selecao_comb)):
        container = st.container(border=True)
        container.write('a')

with col2:
    # Gráfico de Linha para Desvio Padrão por ano
    lin_std_ano, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df_filtra_dataset, x=df_filtra_dataset['ANO_SEP'].astype(str), y='DESVIO PADRÃO REVENDA', hue='PRODUTO', marker='o', palette=mapa_cores)
    ax.set_title('Média de Desvio Padrão de Revenda Para cada Combustível ao longo dos Anos', size=20)
    ax.set_xlabel('Ano')
    ax.set_ylabel('Média de Desvio Padrão (R$/l)')
    ax.legend(title='Tipo de Combustível')
    lin_std_ano.tight_layout()
    col2.pyplot(lin_std_ano)

    # Gráfico de Linha para Desvio Padrão por mês
    lin_std_mes, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df_filtra_dataset, x=df_filtra_dataset['MÊS_SEP'].astype(str), y='DESVIO PADRÃO REVENDA', hue='PRODUTO', marker='o', palette=mapa_cores)
    ax.set_title('Média de Desvio Padrão de Revenda Para cada Combustível ao longo dos Meses', size=20)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Média de Desvio Padrão (R$/l)')
    lin_std_mes.tight_layout()
    col2.pyplot(lin_std_mes)

df_variacao = df_filtra_dataset.loc[:, ['PRODUTO', 'DATA', 'DESVIO PADRÃO REVENDA', 'COEF DE VARIAÇÃO REVENDA']]

# Expander para mostrar df
mostrar_df = st.expander('Marque para exibir o DataFrame', expanded=False,)
mostrar_df.subheader("DataFrame de Variação de Preço Médio de Revenda")
mostrar_df.dataframe(df_variacao)