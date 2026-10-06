import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuração de Layout e Janela do Navegador
st.set_page_config(page_title="BI Eleitoral - Análise de Manchas", layout="wide", page_icon="🗳️")

st.title("📊 Painel Analítico de BI - Cruzamento de Manchas e Conversão Eleitoral")
st.markdown("Monitorização de penetração das bases cadastrais consolidadas face aos votos oficiais apurados em urna.")
st.markdown("---")

# 2. Pipeline de Dados Integrado (Carga Direta das 3 Novas Planilhas Completas)
@st.cache_data
def load_and_consolidate_datasets():
    # PLANILHA 1: Dados Análise (Base Cadastral Geral)
    dados_analise_raw = [
        {'mun': 'Amapá', 'atend': 'BRENDA MONTEIRO', 'votos': 13},
        {'mun': 'Amapá', 'atend': 'ILETE BALIEIRO', 'votos': 2},
        {'mun': 'Amapá', 'atend': 'LEILA BEATRIZ', 'votos': 23},
        {'mun': 'Amapá', 'atend': 'NAUINE MARTINS', 'votos': 1},
        {'mun': 'Amapá', 'atend': 'PEDRO LOBATO', 'votos': 6},
        {'mun': 'Amapá', 'atend': 'RANUELY CAMPOS', 'votos': 1},
        {'mun': 'Calçoene', 'atend': 'ANE TOLOSA', 'votos': 8},
        {'mun': 'Calçoene', 'atend': 'BRENDA MONTEIRO', 'votos': 8},
        {'mun': 'Calçoene', 'atend': 'EDSON GOMES', 'votos': 7},
        {'mun': 'Calçoene', 'atend': 'LEILA BEATRIZ', 'votos': 55},
        {'mun': 'Calçoene', 'atend': 'MAIZA PEREIRA', 'votos': 1},
        {'mun': 'Cutias', 'atend': 'FERNANDO SANTOS', 'votos': 155},
        {'mun': 'Ferreira Gomes', 'atend': 'ADRIELE RODRIGUES', 'votos': 2},
        {'mun': 'Ferreira Gomes', 'atend': 'BRENDA MONTEIRO', 'votos': 8},
        {'mun': 'Ferreira Gomes', 'atend': 'FERNANDO SANTOS', 'votos': 20},
        {'mun': 'Ferreira Gomes', 'atend': 'ILETE BALIEIRO', 'votos': 91},
        {'mun': 'Ferreira Gomes', 'atend': 'JARCILENE SOUZA', 'votos': 19},
        {'mun': 'Ferreira Gomes', 'atend': 'JOSIVAN SILVA', 'votos': 2},
        {'mun': 'Ferreira Gomes', 'atend': 'LEILA BEATRIZ', 'votos': 30},
        {'mun': 'Ferreira Gomes', 'atend': 'NAUINE MARTINS', 'votos': 1},
        {'mun': 'Itaubal', 'atend': 'BRENDA MONTEIRO', 'votos': 37},
        {'mun': 'Itaubal', 'atend': 'FERNANDO SANTOS', 'votos': 9},
        {'mun': 'Itaubal', 'atend': 'JARCILENE SOUZA', 'votos': 1},
        {'mun': 'Itaubal', 'atend': 'JOSIVAN SILVA', 'votos': 21},
        {'mun': 'Itaubal', 'atend': 'LEILA BEATRIZ', 'votos': 3},
        {'mun': 'Laranjal do Jari', 'atend': 'BRENDA MONTEIRO', 'votos': 15},
        {'mun': 'Laranjal do Jari', 'atend': 'EDSON GOMES', 'votos': 99},
        {'mun': 'Laranjal do Jari', 'atend': 'LEILA BEATRIZ', 'votos': 16},
        {'mun': 'Laranjal do Jari', 'atend': 'NAUINE MARTINS', 'votos': 5},
        {'mun': 'Macapá', 'atend': 'ADRIELE RODRIGUES', 'votos': 29},
        {'mun': 'Macapá', 'atend': 'ALESSANDRA GOMES', 'votos': 3},
        {'mun': 'Macapá', 'atend': 'ANE TOLOSA', 'votos': 29},
        {'mun': 'Macapá', 'atend': 'ANTHONY SOUTO', 'votos': 1},
        {'mun': 'Macapá', 'atend': 'ANTÔNIO NASCIMENTO', 'votos': 7},
        {'mun': 'Macapá', 'atend': 'BRENDA MONTEIRO', 'votos': 192},
        {'mun': 'Macapá', 'atend': 'EDSON GOMES', 'votos': 22},
        {'mun': 'Macapá', 'atend': 'EMILY ALMEIDA', 'votos': 9},
        {'mun': 'Macapá', 'atend': 'FERNANDO SANTOS', 'votos': 22},
        {'mun': 'Macapá', 'atend': 'ILETE BALIEIRO', 'votos': 24},
        {'mun': 'Macapá', 'atend': 'JOSIVAN SILVA', 'votos': 102},
        {'mun': 'Macapá', 'atend': 'LEILA BEATRIZ', 'votos': 438},
        {'mun': 'Macapá', 'atend': 'MAIZA PEREIRA', 'votos': 50},
        {'mun': 'Macapá', 'atend': 'MIRLY QUEIROZ', 'votos': 364},
        {'mun': 'Macapá', 'atend': 'NAUINE MARTINS', 'votos': 82},
        {'mun': 'Macapá', 'atend': 'PEDRO LOBATO', 'votos': 8},
        {'mun': 'Macapá', 'atend': 'RANUELY CAMPOS', 'votos': 11},
        {'mun': 'Mazagão', 'atend': 'ADRIELE RODRIGUES', 'votos': 16},
        {'mun': 'Mazagão', 'atend': 'BRENDA MONTEIRO', 'votos': 147},
        {'mun': 'Mazagão', 'atend': 'EDSON GOMES', 'votos': 9},
        {'mun': 'Mazagão', 'atend': 'FERNANDO SANTOS', 'votos': 8},
        {'mun': 'Mazagão', 'atend': 'ILETE BALIEIRO', 'votos': 1},
        {'mun': 'Mazagão', 'atend': 'JOSIVAN SILVA', 'votos': 24},
        {'mun': 'Mazagão', 'atend': 'LEILA BEATRIZ', 'votos': 9},
        {'mun': 'Mazagão', 'atend': 'MIRLY QUEIROZ', 'votos': 189},
        {'mun': 'Mazagão', 'atend': 'NAUINE MARTINS', 'votos': 58},
        {'mun': 'Mazagão', 'atend': 'PEDRO LOBATO', 'votos': 1},
        {'mun': 'Oiapoque', 'atend': 'BRENDA MONTEIRO', 'votos': 20},
        {'mun': 'Oiapoque', 'atend': 'NAUINE MARTINS', 'votos': 14},
        {'mun': 'Pedra Branca do Amapari', 'atend': 'ADRIELE RODRIGUES', 'votos': 12},
        {'mun': 'Pedra Branca do Amapari', 'atend': 'ALESSANDRA GOMES', 'votos': 2},
        {'mun': 'Pedra Branca do Amapari', 'atend': 'ANTÔNIO NASCIMENTO', 'votos': 8},
        {'mun': 'Pedra Branca do Amapari', 'atend': 'BRENDA MONTEIRO', 'votos': 64},
        {'mun': 'Pedra Branca do Amapari', 'atend': 'EDSON GOMES', 'votos': 2},
        {'mun': 'Pedra Branca do Amapari', 'atend': 'ILETE BALIEIRO', 'votos': 1},
        {'mun': 'Pedra Branca do Amapari', 'atend': 'LEILA BEATRIZ', 'votos': 6},
        {'mun': 'Pedra Branca do Amapari', 'atend': 'MIRLY QUEIROZ', 'votos': 2},
        {'mun': 'Porto Grande', 'atend': 'ADRIELE RODRIGUES', 'votos': 4},
        {'mun': 'Porto Grande', 'atend': 'BRENDA MONTEIRO', 'votos': 136},
        {'mun': 'Porto Grande', 'atend': 'EDSON GOMES', 'votos': 6},
        {'mun': 'Porto Grande', 'atend': 'FERNANDO SANTOS', 'votos': 18},
        {'mun': 'Porto Grande', 'atend': 'LEILA BEATRIZ', 'votos': 11},
        {'mun': 'Porto Grande', 'atend': 'NAUINE MARTINS', 'votos': 7},
        {'mun': 'Pracuúba', 'atend': 'ALESSANDRA GOMES', 'votos': 27},
        {'mun': 'Pracuúba', 'atend': 'BRENDA MONTEIRO', 'votos': 79},
        {'mun': 'Pracuúba', 'atend': 'FERNANDO SANTOS', 'votos': 2},
        {'mun': 'Pracuúba', 'atend': 'LEILA BEATRIZ', 'votos': 10},
        {'mun': 'Santana', 'atend': 'ADRIELE RODRIGUES', 'votos': 63},
        {'mun': 'Santana', 'atend': 'ALESSANDRA GOMES', 'votos': 5},
        {'mun': 'Santana', 'atend': 'BRENDA MONTEIRO', 'votos': 74},
        {'mun': 'Santana', 'atend': 'EDSON GOMES', 'votos': 35},
        {'mun': 'Santana', 'atend': 'EMILY ALMEIDA', 'votos': 1},
        {'mun': 'Santana', 'atend': 'FERNANDO SANTOS', 'votos': 20},
        {'mun': 'Santana', 'atend': 'ILETE BALIEIRO', 'votos': 7},
        {'mun': 'Santana', 'atend': 'JARCILENE SOUZA', 'votos': 7},
        {'mun': 'Santana', 'atend': 'JOSIVAN SILVA', 'votos': 23},
        {'mun': 'Santana', 'atend': 'LEILA BEATRIZ', 'votos': 214},
        {'mun': 'Santana', 'atend': 'MIRLY QUEIROZ', 'votos': 1},
        {'mun': 'Santana', 'atend': 'NAUINE MARTINS', 'votos': 27},
        {'mun': 'Serra do Navio', 'atend': 'BRENDA MONTEIRO', 'votos': 24},
        {'mun': 'Serra do Navio', 'atend': 'JARCILENE SOUZA', 'votos': 1},
        {'mun': 'Serra do Navio', 'atend': 'LEILA BEATRIZ', 'votos': 15},
        {'mun': 'Serra do Navio', 'atend': 'NAUINE MARTINS', 'votos': 1},
        {'mun': 'Tartarugalzinho', 'atend': 'ANE TOLOSA', 'votos': 6},
        {'mun': 'Tartarugalzinho', 'atend': 'BRENDA MONTEIRO', 'votos': 29},
        {'mun': 'Tartarugalzinho', 'atend': 'FERNANDO SANTOS', 'votos': 22},
        {'mun': 'Tartarugalzinho', 'atend': 'JOSIVAN SILVA', 'votos': 4},
        {'mun': 'Tartarugalzinho', 'atend': 'LEILA BEATRIZ', 'votos': 19},
        {'mun': 'Tartarugalzinho', 'atend': 'MAIZA PEREIRA', 'votos': 18},
        {'mun': 'Tartarugalzinho', 'atend': 'MIRLY QUEIROZ', 'votos': 178},
        {'mun': 'Tartarugalzinho', 'atend': 'NAUINE MARTINS', 'votos': 9},
        {'mun': 'Vitória do Jari', 'atend': 'BRENDA MONTEIRO', 'votos': 5},
        {'mun': 'Vitória do Jari', 'atend': 'EDSON GOMES', 'votos': 85},
        {'mun': 'Vitória do Jari', 'atend': 'JARCILENE SOUZA', 'votos': 21},
        {'mun': 'Vitória do Jari', 'atend': 'JOSIVAN SILVA', 'votos': 7},
        {'mun': 'Vitória do Jari', 'atend': 'LEILA BEATRIZ', 'votos': 41},
        {'mun': 'Vitória do Jari', 'atend': 'NAUINE MARTINS', 'votos': 37},
        {'mun': 'Vitória do Jari', 'atend': 'PEDRO LOBATO', 'votos': 1}
    ]

    # PLANILHA 2: Análise Convertidos (Base Qualificada de Última Milha)
    convertidos_raw = [
        {'mun': 'Amapá', 'atend': 'RAY', 'votos': 2},
        {'mun': 'Itaubal', 'atend': 'ADELSON', 'votos': 10},
        {'mun': 'Itaubal', 'atend': 'ANE TOLOSA', 'votos': 50},
        {'mun': 'Itaubal', 'atend': 'GLENDA', 'votos': 1},
        {'mun': 'Laranjal do Jari', 'atend': 'EDSON', 'votos': 33},
        {'mun': 'Macapá', 'atend': 'AYENN TEIXEIRA SILVA', 'votos': 6},
        {'mun': 'Macapá', 'atend': 'BRENDA', 'votos': 21},
        {'mun': 'Macapá', 'atend': 'FERNANDO SANTOS', 'votos': 28},
        {'mun': 'Macapá', 'atend': 'ILETE', 'votos': 15},
        {'mun': 'Macapá', 'atend': 'JOSIVAN', 'votos': 25},
        {'mun': 'Macapá', 'atend': 'LUANNA', 'votos': 25},
        {'mun': 'Macapá', 'atend': 'MEL', 'votos': 32},
        {'mun': 'Macapá', 'atend': 'VAL', 'votos': 1},
        {'mun': 'Mazagão', 'atend': 'FERNANDO SANTOS', 'votos': 20},
        {'mun': 'Mazagão', 'atend': 'JOSIVAN', 'votos': 1},
        {'mun': 'Porto Grande', 'atend': 'JOSIVAN', 'votos': 3},
        {'mun': 'Santana', 'atend': 'ADRYELLY SILVA DA SILVA', 'votos': 31},
        {'mun': 'Santana', 'atend': 'FERNANDO SANTOS', 'votos': 22},
        {'mun': 'Santana', 'atend': 'JOSIVAN', 'votos': 3},
        {'mun': 'Santana', 'atend': 'MEL', 'votos': 9},
        {'mun': 'Santana', 'atend': 'VAL', 'votos': 16},
        {'mun': 'Tartarugalzinho', 'atend': 'ROSIVETE', 'votos': 7},
        {'mun': 'Tartarugalzinho', 'atend': 'FERNANDO SANTOS', 'votos': 37},
        {'mun': 'Tartarugalzinho', 'atend': 'SUELENE', 'votos': 19},
        {'mun': 'Vitória do Jari', 'atend': 'LEANDRO DOS SANTOS SILVA', 'votos': 15}
    ]

    urnas_raw = [
        {'municipio': 'Itaubal', 'marcio': 134, 'liliane': 66, 'acácio': 1333},
        {'municipio': 'Macapá', 'marcio': 89, 'liliane': 49, 'acácio': 1141},
        {'municipio': 'Santana', 'marcio': 4, 'liliane': 3, 'acácio': 197},
        {'municipio': 'Tartarugalzinho', 'marcio': 133, 'liliane': 994, 'acácio': 602},
        {'municipio': 'Laranjal do Jari', 'marcio': 22, 'liliane': 0, 'acácio': 70},
        {'municipio': 'Porto Grande', 'marcio': 365, 'liliane': 38, 'acácio': 3479},
        {'municipio': 'Amapá', 'marcio': 555, 'liliane': 26, 'acácio': 1545},
        {'municipio': 'Mazagão', 'marcio': 342, 'liliane': 78, 'acácio': 9545}
    ]

    df_da = pd.DataFrame(dados_analise_raw)
    df_cv = pd.DataFrame(convertidos_raw)
    df_ur = pd.DataFrame(urnas_raw)

    # Padronização de strings indexadas para chaves estáveis
    for df in [df_da, df_cv]:
        df['mun_id'] = df['mun'].str.lower().str.replace(" ", "").str.strip()
        df['atend_id'] = df['atend'].str.upper().str.strip()
        
    df_ur['mun_id'] = df_ur['municipio'].str.lower().str.replace(" ", "").str.strip()
    return df_da, df_cv, df_ur

df_dados_analise, df_convertidos, df_urnas = load_and_consolidate_datasets()

# 3. Sidebar de Governança Estrita - Filtros Globais com "TODOS"
st.sidebar.header("🎯 Governança Eleitoral")

# Filtro 1: Município
list_municipios = sorted(list(df_urnas['municipio'].unique()))
list_municipios.insert(0, "TODOS")
sel_municipio = st.sidebar.selectbox("1. Escopo Geográfico (Município):", list_municipios, index=0)

# Resolução de escopo baseado na seleção do município
m_id = sel_municipio.lower().replace(" ", "").strip()
if sel_municipio == "TODOS":
    df_da_f = df_dados_analise.copy()
    df_cv_f = df_convertidos.copy()
    df_ur_f = df_urnas.copy()
else:
    df_da_f = df_dados_analise[df_dados_analise['mun_id'] == m_id]
    df_cv_f = df_convertidos[df_convertidos['mun_id'] == m_id]
    df_ur_f = df_urnas[df_urnas['mun_id'] == m_id]

# Filtro 2: Atendente
list_atendentes = sorted(list(set(df_da_f['atend_id'].unique()) | set(df_cv_f['atend_id'].unique())))
list_atendentes.insert(0, "TODOS")
sel_atendente = st.sidebar.selectbox("2. Gestor Operacional (Atendente):", list_atendentes, index=0)

# Filtro 3: Candidatos Alvo (Marcio, Liliane, Acácio)
sel_candidato = st.sidebar.selectbox("3. Candidato Alvo (Filtro Urna):", ["TODOS", "Marcio", "Liliane", "Acácio"], index=0)

# Aplicação dinâmica das regras de filtragem de Atendente
if sel_atendente != "TODOS":
    df_da_f = df_da_f[df_da_f['atend_id'] == sel_atendente]
    df_cv_f = df_cv_f[df_cv_f['atend_id'] == sel_atendente]

# 4. Processamento Teórico das Manchas
votos_marcio = int(df_ur_f['marcio'].sum())
votos_liliane = int(df_ur_f['liliane'].sum())
votos_acacio = int(df_ur_f['acácio'].sum())

if sel_candidato == "Marcio":
    teto_urnas = votos_marcio
elif sel_candidato == "Liliane":
    teto_urnas = votos_liliane
elif sel_candidato == "Acácio":
    teto_urnas = votos_acacio
else:
    teto_urnas = votos_marcio + votos_liliane + votos_acacio

votos_dados_analise = int(df_da_f['votos'].sum())
votos_convertidos = int(df_cv_f['votos'].sum())

# 5. Painel Geral de Métricas e KPIs
st.subheader(f"📈 Sumário Operacional Executivo — {sel_municipio.upper()}")
k1, k2, k3 = st.columns(3)

with k1:
    st.metric("Mancha 1: Votos Reais Urna", f"{teto_urnas} v")
with k2:
    aprov_da = (votos_dados_analise / teto_urnas * 100) if teto_urnas > 0 else 0
    st.metric("Mancha 2: Votos Dados Análise", f"{votos_dados_analise} v", f"Aproveitamento: {aprov_da:.2f}%")
with k3:
    aprov_cv = (votos_convertidos / teto_urnas * 100) if teto_urnas > 0 else 0
    st.metric("Mancha 3: Votos Convertidos", f"{votos_convertidos} v", f"Conversão Final: {aprov_cv:.2f}%")

st.markdown("---")

# 6. Renderização Gráfica do Mapa de Manchas (HTML5 e CSS Inline Autônomo)
st.subheader("🔥 Distribuição Geométrica Digital das Manchas de Calor")

if teto_urnas > 0:
    max_width = 100
    w_da = min(max_width, max(15, int((votos_dados_analise / teto_urnas) * 100))) if votos_dados_analise > 0 else 5
    w_cv = min(max_width, max(10, int((votos_convertidos / teto_urnas) * 100))) if votos_convertidos > 0 else 5

    # Strings de percentagem formatadas isoladamente para evitar conflitos na f-string
    p_da_str = f"{aprov_da:.2f}%"
    p_cv_str = f"{aprov_cv:.2f}%"

    manchas_html = f"""
    <div style='display: flex; flex-direction: column; gap: 20px; width: 100%; padding: 15px; background: #111; border-radius: 8px;'>
        <div style='width: 100%; background: rgba(220, 53, 69, 0.9); color: white; padding: 25px; border-radius: 6px; font-family: sans-serif;'>
            <span style='font-size: 14px; text-transform: uppercase; font-weight: bold;'>&#9899; MANCHA 1: Urnas Mapeadas (Teto Base)</span>
            <h2 style='margin: 5px 0 0 0; color: white;'>{teto_urnas} Votos Computados</h2>
            <p style='margin: 5px 0 0 0; font-size:13px; opacity:0.8;'>Marcio: {votos_marcio} | Liliane: {votos_liliane} | Acácio: {votos_acacio}</p>
        </div>
        <div style='width: {w_da}%; min-width: 250px; background: rgba(255, 193, 7, 0.9); color: black; padding: 20px; border-radius: 6px; font-family: sans-serif;'>
            <span style='font-size: 13px; text-transform: uppercase; font-weight: bold;'>&#128993; MANCHA 2: Volume Dados Análise</span>
            <h3 style='margin: 5px 0 0 0; color: black;'>{votos_dados_analise} Votos Mapeados</h3>
            <span style='background: black; color: #ffc107; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; display: inline-block; margin-top: 5px;'>Eficiência: {p_da_str}</span>
        </div>
        <div style='width: {w_cv}%; min-width: 200px; background: rgba(40, 167, 69, 0.9); color: white; padding: 18px; border-radius: 6px; font-family: sans-serif;'>
            <span style='font-size: 12px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold;'>&#128994; MANCHA 3: Desempenho Convertidos</span>
            <h4 style='margin: 5px 0 0 0; color: white;'>{votos_convertidos} Votos Qualificados</h4>
            <span style='background: white; color: #28a745; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; display: inline-block; margin-top: 5px;'>Conversão Real: {p_cv_str}</span>
        </div>
    </div>
    """
    st.write(manchas_html, unsafe_allow_html=True)
else:
    st.info("O filtro selecionado resultou em zero votos no teto das urnas oficiais.")

st.markdown("---")

# 7. Geração de Rankings por Atendentes (Geral e Proporcional)
st.subheader("🏆 Ranking de Desempenho e Conversão por Atendente")

if not df_da_f.empty:
    # Agrupamento e cálculo de participações
    rank_df = df_da_f.groupby('atend_id')['votos'].sum().reset_index()
    rank_df.columns = ['Atendente', 'Votos Conquistados']
    rank_df['% Proporção sobre Urnas'] = (rank_df['Votos Conquistados'] / teto_urnas * 100).round(2) if teto_urnas > 0 else 0
    st.dataframe(rank_df.sort_values(by='Votos Conquistados', ascending=False), use_container_width=True)
else:
    st.warning("Sem registros cadastrais sob os filtros selecionados.")

# 8. FERRAMENTA DE BACKUP INTEGRADA
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Backup do Código Fonte")
with open(__file__, "r", encoding="utf-8") as f:
    source_code = f.read()

st.sidebar.download_button(
    label="📥 Descarregar arquivo .py",
    data=source_code,
    file_name="app.py",
    mime="text/x-python"
)
