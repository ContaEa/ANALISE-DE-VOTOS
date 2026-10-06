import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuração da Página do Streamlit
st.set_page_config(page_title="Analytics Eleitoral - Amapá", layout="wide", page_icon="🗳️")

st.title("📊 Painel de Business Intelligence - Cruzamento Eleitoral")
st.markdown("---")

# 2. Pipeline de Dados Otimizado (Cache Ativo)
@st.cache_data
def load_and_clean_data():
    # Estruturação e normalização automática das strings e dados das planilhas enviadas
    # Simulação baseada exatamente nos seus_dados e urnas mapeadas fornecidos
    
    clients_raw = {
        'Cliente': ['VANUBIA', 'RAIMUNDO', 'GIZELE', 'LIVIA', 'NICOLY', 'MANOEL', 'JORGE', 'ALINE', 'MARCOS', 'EZENI'],
        'atendente': ['LEILA BEATRIZ', 'LEILA BEATRIZ', 'BRENDA MONTEIRO', 'NAUINE MARTINS', 'RANUELY CAMPOS', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'ILETE BALIEIRO'],
        'municipio': ['Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Macapá', 'Macapá', 'Santana', 'Santana', 'Tartarugalzinho']
    }
    
    urnas_raw = [
        {'municipio': 'itaubal', 'marcio': 134, 'liliane': 66, 'acácio': 1333},
        {'municipio': 'macapá', 'marcio': 89, 'liliane': 49, 'acácio': 1141},
        {'municipio': 'santana', 'marcio': 4, 'liliane': 3, 'acácio': 197},
        {'municipio': 'tartarugalzinho', 'marcio': 133, 'liliane': 994, 'acácio': 602},
        {'municipio': 'vitoria do jari', 'marcio': 22, 'liliane': 0, 'acácio': 70}
    ]
    
    df1 = pd.DataFrame(clients_raw)
    df2 = pd.DataFrame(urnas_raw)
    
    # Sanitização e normalização de strings para evitar problemas de índices em joins
    df1['municipio'] = df1['municipio'].str.lower().str.strip()
    df2['municipio'] = df2['municipio'].str.lower().str.strip()
    df1['atendente'] = df1['atendente'].str.upper().str.strip()
    
    return df1, df2

df_clients, df_urnas = load_and_clean_data()

# 3. Sidebar de Filtros Principais
st.sidebar.header("🎯 Filtros de Controle")
all_municipios = sorted(df_urnas['municipio'].unique())
selected_municipio = st.sidebar.selectbox("Selecione o Município (Filtro Principal):", all_municipios)

# Filtragem Dinâmica por Escopo de Município
df_c_filtered = df_clients[df_clients['municipio'] == selected_municipio]
df_u_filtered = df_urnas[df_urnas['municipio'] == selected_municipio]

# 4. Cálculo de Índices e Proporções de Votos
total_clientes_mun = len(df_c_filtered)
votos_marcio = df_u_filtered['marcio'].sum() if not df_u_filtered.empty else 0
votos_liliane = df_u_filtered['liliane'].sum() if not df_u_filtered.empty else 0
votos_acacio = df_u_filtered['acácio'].sum() if not df_u_filtered.empty else 0
total_votos_mun = votos_marcio + votos_liliane + votos_acacio

# Distribuição Proporcional dos Votos pelo volume de Clientes de cada Atendente
atendente_counts = df_c_filtered['atendente'].value_counts()
atendente_data = []

for atendente, count in atendente_counts.items():
    proporcao = count / total_clientes_mun if total_clientes_mun > 0 else 0
    atendente_data.append({
        'Atendente': atendente,
        'Clientes Cadastrados': count,
        'Marcio': int(votos_marcio * proporcao),
        'Liliane': int(votos_liliane * proporcao),
        'Acácio': int(votos_acacio * proporcao),
        'Total Geral Estimado': int(total_votos_mun * proporcao)
    })

df_performance = pd.DataFrame(atendente_data)

# 5. Renderização dos KPIs
st.subheader(f"📈 Panorama Geral - {selected_municipio.upper()}")
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Total de Clientes no Município", f"{total_clientes_mun} u")
with kpi2:
    st.metric("Total de Votos no Município", f"{total_votos_mun} votos")
with kpi3:
    indice = (total_clientes_mun / total_votos_mun * 100) if total_votos_mun > 0 else 0
    st.metric("Índice de Penetração (Clientes/Votos)", f"{indice:.2f}%")

st.markdown("---")

# 6. Geração do Mapa de Calor Cruzado (Heatmap)
st.subheader("🔥 Mapa de Calor Eleitoral: Atendentes x Candidatos")
if not df_performance.empty:
    df_melted = df_performance.melt(id_vars=['Atendente'], value_vars=['Marcio', 'Liliane', 'Acácio'],
                                    var_name='Candidato', value_name='Votos')
    
    pivot_heat = df_melted.pivot(index='Atendente', columns='Candidato', values='Votos').fillna(0)
    
    fig_heatmap = px.imshow(pivot_heat,
                            labels=dict(x="Candidato", y="Atendente", color="Volume de Votos"),
                            text_auto=True,
                            color_continuous_scale='YlOrRd')
    st.plotly_chart(fig_heatmap, use_container_width=True)
else:
    st.warning("Sem dados cadastrais suficientes para mapear a performance dos atendentes neste município.")

st.markdown("---")

# 7. Ranking dos Atendentes com Filtro por Candidato
st.subheader("🏆 Ranking de Conversão por Atendente")
if not df_performance.empty:
    selected_candidato = st.selectbox("Selecione o Candidato para o Ranking:", ['Total Geral Estimado', 'Marcio', 'Liliane', 'Acácio'])
    
    df_performance['% Representação de Votos'] = (df_performance[selected_candidato] / total_votos_mun * 100).round(2) if total_votos_mun > 0 else 0
    ranking_final = df_performance[['Atendente', 'Clientes Cadastrados', selected_candidato, '% Representação de Votos']]
    
    st.dataframe(ranking_final.sort_values(by=selected_candidato, ascending=False), use_container_width=True)
