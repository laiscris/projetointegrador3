import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import streamlit as st
import filtros as f

# Configuração do nome da aba
st.set_page_config(
    page_title="Análise",
    page_icon="",
    layout='wide'
)

st.title('Comparação de Preço do Etanol vs Gasolina')

# Resolvendo problema do caminho do windows
base_path = os.path.dirname(__file__)
csv_path = os.path.join(base_path, 'comparacao_etanol_e_gasolina.csv')

df_comparacao = pd.read_csv(csv_path)

# Sidebar Principal / Barra Lateral
sidebar_principal = st.sidebar

# sidebar_principal.image('logo.png') # Ver como colocar a logo no topo do sidebar

# Filtros -----------------------------------------------------------------------------------
sidebar_principal.markdown('**FILTROS**:')

# Filtros de Período de Tempo
# Ano
periodo_ano = df_comparacao['ANO_SEP'].unique()
sel_anos = sidebar_principal.slider('Escolha o ano', periodo_ano.min(), periodo_ano.max(), value=(periodo_ano.min(), periodo_ano.max()))
df_filtra_ano = f.filtra_ano(df_comparacao, sel_anos)

# Mês
periodo_mes = df_filtra_ano['MÊS_SEP'].unique()
sel_meses = sidebar_principal.slider('Escolha o mês', periodo_mes.min(), periodo_mes.max(), value=(periodo_mes.min(), periodo_mes.max()))
df_filtra_mes = f.filtra_mes(df_filtra_ano, sel_meses)

df_comparacao_final = df_filtra_mes.copy()

# Criar uma coluna de data unificada para plotagem
df_comparacao_final['DATA'] = pd.to_datetime(df_comparacao_final['ANO_SEP'].astype(str) + '-' + df_comparacao_final['MÊS_SEP'].astype(str))

st.dataframe(df_comparacao_final, use_container_width=True)

# Gráfico de Linha para a Regra dos 70%
grafico_comparacao, ax = plt.subplots(figsize=(10, 5))
# Diferença percentual Etanol/Gasolina
sns.lineplot(data=df_comparacao_final, x='DATA', y='% RAZAO ETANOL_GASOLINA', color='#FFC300')

# Adicionar a linha de referência da Regra dos 70% (30% de diferença ou menos)
# Se a diferença for < 70%, o etanol é vantajoso. Se for > 70%, a gasolina é vantajosa.
plt.axhline(70, color='red', linestyle='--', linewidth=2, label='Limite de 70%')

# Adicionar Rótulos e Título
ax.set_title('Evolução da Razão Percentual do Etanol vs. Gasolina Comum - Regra dos 70%', fontsize=15)
ax.set_xlabel('Data', fontsize=12)
ax.set_ylabel('% de Razão (Base Gasolina)', fontsize=12)
ax.legend()
ax.grid(True, linestyle=':', alpha=0.6)
ax.tick_params(rotation=45)
grafico_comparacao.tight_layout()
st.pyplot(grafico_comparacao)

st.markdown('''
* Abaixo de 70%, o preço do Etanol representa menos de 70% do preço da Gasolina. Portanto, o etanol é mais vantajoso.
* Acima de 70%, o preço do Etanol representa mais de 70% do preço da Gasolina. Portanto, a gasolina compensa mais
* = 70%, indiferença energética
''')

