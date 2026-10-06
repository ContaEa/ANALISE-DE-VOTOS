import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuração Nativa da Página
st.set_page_config(page_title="Analytics Eleitoral - Amapá", layout="wide", page_icon="🗳️")

st.title("📊 Painel de Business Intelligence - Cruzamento Eleitoral")
st.markdown("---")

# 2. Pipeline de Dados Otimizado (Apenas com Pandas)
@st.cache_data
def load_and_clean_data():
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
    
    # Sanitização de strings
    df1['municipio'] = df1['municipio'].str.lower().str.strip()
    df2['municipio'] = df2['municipio'].str.lower().str.strip()
    df1['atendente'] = df1['atendente'].str.upper().str.strip()
    
    return df1, df2

df_clients, df_urnas = load_and_clean_data()

# 3. Sidebar de Filtros Principais
st.sidebar.header("🎯 Filtros de Controle")
all_municipios = sorted(df_urnas['municipio'].unique())
selected_municipio = st.sidebar.selectbox("Selecione o Município:", all_municipios)

# Filtragem Dinâmica
df_c_filtered = df_clients[df_clients['municipio'] == selected_municipio]
df_u_filtered = df_urnas[df_urnas['municipio'] == selected_municipio]

# 4. Processamento de Proporções Eleitorais
total_clientes_mun = len(df_c_filtered)
votos_marcio = df_u_filtered['marcio'].sum() if not df_u_filtered.empty else 0
votos_liliane = df_u_filtered['liliane'].sum() if not df_u_filtered.empty else 0
votos_acacio = df_u_filtered['acácio'].sum() if not df_u_filtered.empty else 0
total_votos_mun = votos_marcio + votos_liliane + votos_acacio

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
        'Total Estimado': int(total_votos_mun * proporcao)
    })

df_performance = pd.DataFrame(atendente_data)

# 5. Renderização dos KPIs de Desempenho
st.subheader(f"📈 Panorama Geral - {selected_municipio.upper()}")
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Clientes no Município", f"{total_clientes_mun} u")
with kpi2:
    st.metric("Votos Totais nas Urnas", f"{total_votos_mun} votos")
with kpi3:
    indice = (total_clientes_mun / total_votos_mun * 100) if total_votos_mun > 0 else 0
    st.metric("Índice de Penetração", f"{indice:.2f}%")

st.markdown("---")

# 6. Geração do Mapa de Calor via Pandas Styler (Nativo e Sem Erros)
st.subheader("🔥 Mapa de Calor Eleitoral: Atendentes x Candidatos")
if not df_performance.empty:
    # Construção da matriz para o mapa de calor
    df_heat = df_performance.set_index('Atendente')[['Marcio', 'Liliane', 'Acácio']]
    
    # Aplicação de estilo de gradiente de calor diretamente na tabela
    styled_heat = df_heat.style.background_gradient(cmap='YlOrRd').format("{:.0f}")
    
    st.dataframe(styled_heat, use_container_width=True)
else:
    st.warning("Sem registros suficientes para calcular cruzamentos neste município.")

st.markdown("---")

# 7. Ranking de Conversão por Atendente
st.subheader("🏆 Ranking de Conversão por Atendente")
if not df_performance.empty:
    selected_candidato = st.selectbox("Selecione o Filtro de Alvo:", ['Total Estimado', 'Marcio', 'Liliane', 'Acácio'])
    
    df_performance['% Representação de Votos'] = (df_performance[selected_candidato] / total_votos_mun * 100).round(2) if total_votos_mun > 0 else 0
    ranking_final = df_performance[['Atendente', 'Clientes Cadastrados', selected_candidato, '% Representação de Votos']]
    
    st.dataframe(ranking_final.sort_values(by=selected_candidato, ascending=False), use_container_width=True)
