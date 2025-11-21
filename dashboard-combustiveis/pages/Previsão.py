import streamlit as st
import filtros as f

st.set_page_config(
    page_title="Predição",
    page_icon="",
)

st.title('Dashboard de Análise e Previsão do Preço de Combustíveis')

df_previsao = None # Criar dataset de previsão

# Sidebar Principal / Barra Lateral
sidebar_principal = st.sidebar

# sidebar_principal.image('logo.png') # Ver como colocar a logo no topo do sidebar

# Filtros -----------------------------------------------------------------------------------
sidebar_principal.markdown('**FILTROS**:')
# Filtro de Combustível
combustiveis = df_previsao['PRODUTO'].unique()
selecao_comb = sidebar_principal.multiselect('Tipo de Combustível', options=combustiveis, default=combustiveis)

# Filtros de Período de Tempo
periodo_ano = df_previsao['ANO_SEP'].unique()

# Ano
sel_anos = sidebar_principal.slider('Escolha o ano', periodo_ano.min(), periodo_ano.max(), value=(periodo_ano.min(), periodo_ano.max()))
df_filtra_dataset = f.filtra_dataset(combustivel=selecao_comb, ano=sel_anos, mes=None)

# Mês
periodo_mes = df_filtra_dataset['MÊS_SEP'].unique()
sel_meses = sidebar_principal.slider('Escolha o mês', periodo_mes.min(), periodo_mes.max(), value=(periodo_mes.min(), periodo_mes.max()))

# Filtra o dataset de acordo com a escolha da seleção múltipla
df_filtra_dataset = f.filtra_dataset(selecao_comb, sel_anos, sel_meses)