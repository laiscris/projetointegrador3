import pandas as pd
import streamlit as st
import os

# Datasets
# Resolvendo problema do caminho do windows
base_path = os.path.dirname(__file__)
csv_path = os.path.join(base_path, 'precos_tratado.csv')
df_tratado = pd.read_csv(csv_path)

# Filtra de acordo com a escolha de combustível
@st.cache_data
def filtra_combustivel(escolha_combustivel):
    return df_tratado[df_tratado.PRODUTO.isin(escolha_combustivel)]

# Filtra de acordo com a escolha de ano
@st.cache_data
def filtra_ano(df_filtra_combustivel, escolha_ano):
    inicio = escolha_ano[0]
    fim = escolha_ano[1]
    return df_filtra_combustivel[(df_filtra_combustivel.ANO_SEP >= inicio) & (df_filtra_combustivel.ANO_SEP <= fim)].copy()

# Filtra de acordo com a escolha do mes
@st.cache_data
def filtra_mes(df_filtra_ano, escolha_mes):
    if escolha_mes is None:
        return df_filtra_ano
    
    inicio = escolha_mes[0]
    fim = escolha_mes[1]
    
    return df_filtra_ano[(df_filtra_ano.MÊS_SEP >= inicio) & (df_filtra_ano.MÊS_SEP <= fim)].copy()

# Filtra o dataset inteiro de acordo com a escolha de combustível e períodos de ano e mês
@st.cache_data
def filtra_dataset(combustivel, ano, mes):

    try:
        # Filtra o tipo de combustível, Obrigatório
        if len(combustivel) == 0:
            print('Escolha pelo menos um tipo de combustível.')
            df_filtrado = pd.DataFrame()
        else:
            df_filtra_combustivel = filtra_combustivel(combustivel) 
            df_filtra_ano = filtra_ano(df_filtra_combustivel, ano)
            df_filtrado = filtra_mes(df_filtra_ano, mes)

    except ValueError as e:
        print(f'Erro ao filtrar o dataset: {e}')
    
    return df_filtrado

# Testando
print(filtra_dataset(['ETANOL HIDRATADO'], [2013, 2015], [1, 4]))
