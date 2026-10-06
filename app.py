import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuração de Performance e Layout da Página
st.set_page_config(page_title="BI Eleitoral - Mapeamento de Manchas", layout="wide", page_icon="🗳️")

st.title("🎯 Painel Analítico de BI - Aproveitamento de Votos por Manchas")
st.markdown("Análise de penetração e conversão de bases cadastrais sobre o total de votos apurados por município.")
st.markdown("---")

# 2. Pipeline de Dados Integrado e Higienizado (Dados Reais das Planilhas)
@st.cache_data
def load_all_datasets():
    # PLANILHA 1: Seus Dados (Base Geral)
    seus_dados_raw = {
        'Cliente': ['VANUBIA DOS SANTOS', 'RAIMUNDO CORREA', 'GIZELE SANTOS', 'RAIMUNDO CORREA', 'LIVIA CELIA', 'NICOLY PALHETA', 'ALERRANDRO BARBOSA', 'MANOEL CABRALZINHO', 'JORGE FELIPE', 'EMANUEL DAVY', 'LEONILSON CASTRO', 'ALINE VITORIA', 'BENEDITO COSTA', 'ALINE CRISTINA', 'HELIO LACERDA', 'EDIANE DA SILVA', 'LIA SILVA', 'SAMUEL YAGO', 'JOVANA DOS SANTOS', 'ROSIVAL RODRIGUES', 'PAULO DOS SANTOS', 'DECIZIENE FLEXA', 'ELIZEU DE SOUZA', 'DARCIVALDO DOS PASSOS', 'ANTONIO RODRIGUES', 'GLEICILENE DA SILVA', 'ÉVILI DE OLIVEIRA', 'RAIMUNDA CARDOSO', 'OSVALDO DO NASCIMENTO', 'RAYSSA DE ALMEIDA', 'GABRIEL ARCANJO', 'VALMIR ANGELO', 'GABRIELLE THAISSA', 'ELSILEIDE PAIXÃO', 'ADRIANA TAVARES', 'FRANCISCO RAIMUNDO', 'CLELIA CARMEM', 'MARCILENE SOUZA', 'EDNA VIANA', 'FRANCISCO EDILSON', 'ODACINEIDE DA COSTA'],
        'Parceiro': ['HELLANA MEDEIROS', 'HELLANA MEDEIROS', 'HELLANA MEDEIROS', 'HELLANA MEDEIROS', 'EVERALDO PIRES', 'VALTINHO SANTANA', 'DILVANA', 'DILVANA', 'DILVANA', 'JOSÉ WALKER', 'JOSÉ WALKER', 'ANA BEATRIZ', 'ALCEMIRA TAVARES', 'ALCEMIRA TAVARES', 'ALCEMIRA TAVARES', 'JACTÃ', 'JACTÃ', 'FABIO', 'FABIO', 'TATIANE MORAES', 'MARIANE SILVA', 'NEURA', 'NEURA', 'MARIANE SANTOS', 'MARIANE SANTOS', 'TATIANE MORAES', 'TATIANE MORAES', 'KELTIANE MARQUES', 'KELTIANE MARQUES', 'MARIANE SILVA', 'MARIANE SILVA', 'JACKELINE BATISTA', 'JACKELINE BATISTA', 'FERNANDO SANTOS', 'RANUELY ESCRITÓRIO', 'TATIANE MORAES', 'ROSA INEZ', 'TAIS GOMES', 'TAIS GOMES', 'NEURA', 'NEURA'],
        'Atendente': ['LEILA BEATRIZ', 'LEILA BEATRIZ', 'BRENDA MONTEIRO', 'LEILA BEATRIZ', 'NAUINE MARTINS', 'RANUELY CAMPOS', 'NÃO INFORMADO', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'EDSON GOMES', 'EDSON GOMES', 'EDSON GOMES', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'EDSON GOMES', 'EDSON GOMES', 'ADRIELE RODRIGUES', 'ADRIELE RODRIGUES', 'EDSON GOMES', 'EDSON GOMES', 'NAUINE MARTINS', 'NAUINE MARTINS', 'EDSON GOMES', 'EDSON GOMES', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'BRENDA MONTEIRO', 'JOSIVAN SILVA', 'ADRIELE RODRIGUES', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'LEILA BEATRIZ', 'EDSON GOMES'],
        'Municipio': ['Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Calçoene', 'Calçoene', 'Calçoene', 'Cutias', 'Cutias', 'Ferreira Gomes', 'Ferreira Gomes', 'Itaubal', 'Itaubal', 'Laranjal do Jari', 'Laranjal do Jari', 'Macapá', 'Macapá', 'Mazagão', 'Mazagão', 'Oiapoque', 'Oiapoque', 'Pedra Branca do Amapari', 'Pedra Branca do Amapari', 'Porto Grande', 'Porto Grande', 'Pracuúba', 'Pracuúba', 'Santana', 'Santana', 'Tartarugalzinho', 'Tartarugalzinho', 'Vitória do Jari', 'Vitória do Jari']
    }

    # PLANILHA 2: Convertidos (Base Qualificada com Seção e Zona)
    convertidos_raw = {
        'Cliente': ['Tatiane Moraes', 'Margarida Moraes', 'Maria Antônia Ramos', 'Marciane Moraes', 'Sofia Moraes', 'tamires kevelim', 'edivania conceição', 'vitoria conceição', 'guilherme linho', 'tryla barros', 'antonio Santana lopes', 'ana maria da silva', 'josivan campos correa', 'maiara costa souza', 'mailom campos', 'nerivaldo maciel', 'elusley rezende', 'Iranilson da Silva', 'Pedro Paulo dos Santos', 'Civaldo Pacheco', 'Domingos Moraes', 'José Maria Moraes', 'Wellington Lemos', 'klever luan', 'Edson Gomes', 'Neuraci pereira', 'Lana Furtado', 'Neikson Nicolau', 'MARIA DO SOCORRO', 'OSVALDO QUEIROZ'],
        'Parceiro': ['FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'ADRYELLY SILVA', 'ADRYELLY SILVA', 'ADRYELLY SILVA', 'ADRYELLY SILVA', 'ADRYELLY SILVA', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'SUELENE', 'SUELENE', 'ANE TOLOSA', 'ANE TOLOSA', 'ANE TOLOSA', 'JOSIVAN', 'JOSIVAN', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'EDSON', 'EDSON', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'AYENN TEIXEIRA', 'AYENN TEIXEIRA'],
        'Atendente': ['FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'ADRYELLY SILVA', 'ADRYELLY SILVA', 'ADRYELLY SILVA', 'ADRYELLY SILVA', 'ADRYELLY SILVA', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'SUELENE', 'SUELENE', 'ANE TOLOSA', 'ANE TOLOSA', 'ANE TOLOSA', 'JOSIVAN', 'JOSIVAN', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'EDSON ', 'EDSON ', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'AYENN TEIXEIRA', 'AYENN TEIXEIRA'],
        'Municipio': ['Macapá', 'Macapá', 'Macapá', 'Macapá', 'Macapá', 'Santana', 'Santana', 'Santana', 'Santana', 'Santana', 'Santana', 'Santana', 'Tartarugalzinho', 'Tartarugalzinho', 'Tartarugalzinho', 'Tartarugalzinho', 'Tartarugalzinho', 'Itaubal', 'Itaubal', 'Itaubal', 'Macapá', 'Macapá', 'Macapá', 'Macapá', 'Laranjal do Jari', 'Laranjal do Jari', 'Mazagão', 'Mazagão', 'Macapá', 'Macapá']
    }

    # PLANILHA 3: Urnas Mapeadas (Teto Eleitoral Oficial)
    urnas_raw = [
        {'municipio': 'Itaubal', 'marcio': 134, 'liliane': 66, 'acácio': 1333},
        {'municipio': 'Macapá', 'marcio': 89, 'liliane': 49, 'acácio': 1141},
        {'municipio': 'Santana', 'marcio': 4, 'liliane': 3, 'acácio': 197},
        {'municipio': 'Tartarugalzinho', 'marcio': 133, 'liliane': 994, 'acácio': 602},
        {'municipio': 'Laranjal do jari', 'marcio': 22, 'liliane': 0, 'acácio': 70},
        {'municipio': 'Porto Grande', 'marcio': 365, 'liliane': 38, 'acácio': 3479},
        {'municipio': 'Amapá', 'marcio': 555, 'liliane': 26, 'acácio': 1545},
        {'municipio': 'Mazagão', 'marcio': 342, 'liliane': 78, 'acácio': 9545}
    ]

    df_sd = pd.DataFrame(seus_dados_raw)
    df_cv = pd.DataFrame(convertidos_raw)
    df_ur = pd.DataFrame(urnas_raw)

    for df in [df_sd, df_cv, df_ur]:
        df['municipio_id'] = df['Municipio' if 'Municipio' in df.columns else 'municipio'].str.lower().str.strip()
    
    df_sd['atendente_id'] = df_sd['Atendente'].str.upper().str.strip()
    df_cv['atendente_id'] = df_cv['Atendente'].str.upper().str.strip()
    df_sd['parceiro_id'] = df_sd['Parceiro'].str.upper().str.strip()
    df_cv['parceiro_id'] = df_cv['Parceiro'].str.upper().str.strip()

    return df_sd, df_cv, df_ur

df_seus_dados, df_convertidos, df_urnas = load_all_datasets()

# 3. Sidebar de Governança e Filtros Hierárquicos
st.sidebar.header("🎯 Filtros do Sistema")

# Filtro 1: Município (Agora incluindo a opção TODOS)
list_municipios = sorted(df_urnas['municipio_id'].unique())
list_municipios.insert(0, "todos")
sel_municipio = st.sidebar.selectbox("1. Selecione o Município Alvo:", list_municipios, index=0)

# Escopo Inicial baseado no Município selecionado
if sel_municipio == "todos":
    df_sd_m = df_seus_dados.copy()
    df_cv_m = df_convertidos.copy()
    df_urnas_sel = df_urnas.copy()
else:
    df_sd_m = df_seus_dados[df_seus_dados['municipio_id'] == sel_municipio]
    df_cv_m = df_convertidos[df_convertidos['municipio_id'] == sel_municipio]
    df_urnas_sel = df_urnas[df_urnas['municipio_id'] == sel_municipio]

# Filtro 2: Atendente
list_atendentes = sorted(list(set(df_sd_m['atendente_id'].unique()) | set(df_cv_m['atendente_id'].unique())))
list_atendentes.insert(0, "TODOS")
sel_atendente = st.sidebar.selectbox("2. Filtrar por Atendente:", list_atendentes)

# Filtro 3: Parceiro
list_parceiros = sorted(list(set(df_sd_m['parceiro_id'].unique()) | set(df_cv_m['parceiro_id'].unique())))
list_parceiros.insert(0, "TODOS")
sel_parceiro = st.sidebar.selectbox("3. Filtrar por Parceiro / Apontador:", list_parceiros)

# 4. Aplicação Dinâmica dos Filtros sobre as Manchas de Captação
if sel_atendente != "TODOS":
    df_sd_m = df_sd_m[df_sd_m['atendente_id'] == sel_atendente]
    df_cv_m = df_cv_m[df_cv_m['atendente_id'] == sel_atendente]

if sel_parceiro != "TODOS":
    df_sd_m = df_sd_m[df_sd_m['parceiro_id'] == sel_parceiro]
    df_cv_m = df_cv_m[df_cv_m['parceiro_id'] == sel_parceiro]

# 5. Consolidação de Votos Eleitorais
votos_marcio = int(df_urnas_sel['marcio'].sum())
votos_liliane = int(df_urnas_sel['liliane'].sum())
votos_acacio = int(df_urnas_sel['acácio'].sum())
total_votos_municipio = votos_marcio + votos_liliane + votos_acacio

# 6. Painel Executivo de Indicadores (KPIs com Índices de Aproveitamento)
st.subheader(f"📊 Desempenho Analítico — {sel_municipio.upper()}")
c1, k_m, k_sd, k_cv = st.columns(4)

count_seus_dados = len(df_sd_m)
count_convertidos = len(df_cv_m)

with c1:
    st.metric("Votos Totais Computados", f"{total_votos_municipio} v")
with k_m:
    st.metric("Teto Oficial Urna (Candidatos)", f"{total_votos_municipio} votos")
with k_sd:
    aprov_sd = (count_seus_dados / total_votos_municipio * 100) if total_votos_municipio > 0 else 0
    st.metric("Mapeados (Seus Dados)", f"{count_seus_dados} u", f"Aprov: {aprov_sd:.2f}%")
with k_cv:
    aprov_cv = (count_convertidos / total_votos_municipio * 100) if total_votos_municipio > 0 else 0
    st.metric("Mapeados (Convertidos)", f"{count_convertidos} u", f"Aprov: {aprov_cv:.2f}%")

st.markdown("---")

# 7. Renderização do Gráfico Dinâmico de Manchas Concêntricas (HTML/CSS Autônomo)
st.subheader("🔥 Mapa de Calor Eleitoral: Distribuição Geométrica das Manchas")

if total_votos_municipio > 0:
    max_box_width = 100
    width_sd = min(max_box_width, max(15, int((count_seus_dados / total_votos_municipio) * 100))) if count_seus_dados > 0 else 5
    width_cv = min(max_box_width, max(10, int((count_convertidos / total_votos_municipio) * 100))) if count_convertidos > 0 else 5

    # Isolamento de strings de percentagem com aspas simples para eliminar o SyntaxError
    p_sd_str = f"{aprov_sd:.2f}%"
    p_cv_str = f"{aprov_cv:.2f}%"

    manchas_html = f"""
    <div style='display: flex; flex-direction: column; gap: 20px; width: 100%; padding: 15px; background: #111; border-radius: 8px;'>
        <div style='width: 100%; background: rgba(220, 53, 69, 0.9); color: white; padding: 25px; border-radius: 6px; font-family: sans-serif;'>
            <span style='font-size: 14px; text-transform: uppercase; font-weight: bold;'>&#9899; MANCHA 1: Urnas Mapeadas</span>
            <h2 style='margin: 5px 0 0 0; color: white;'>{total_votos_municipio} Votos Reais</h2>
            <p style='margin: 5px 0 0 0; font-size:13px; opacity:0.8;'>Marcio: {votos_marcio} | Liliane: {votos_liliane} | Acácio: {votos_acacio}</p>
        </div>
        <div style='width: {width_sd}%; min-width: 250px; background: rgba(255, 193, 7, 0.9); color: black; padding: 20px; border-radius: 6px; font-family: sans-serif;'>
            <span style='font-size: 13px; text-transform: uppercase; font-weight: bold;'>&#128993; MANCHA 2: Seus Dados</span>
            <h3 style='margin: 5px 0 0 0; color: black;'>{count_seus_dados} Clientes</h3>
            <span style='background: black; color: #ffc107; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; display: inline-block; margin-top: 5px;'>Aproveitamento: {p_sd_str}</span>
        </div>
        <div style='width: {width_cv}%; min-width: 200px; background: rgba(40, 167, 69, 0.9); color: white; padding: 18px; border-radius: 6px; font-family: sans-serif;'>
            <span style='font-size: 12px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold;'>&#128994; MANCHA 3: Convertidos</span>
            <h4 style='margin: 5px 0 0 0; color: white;'>{count_convertidos} Clientes</h4>
            <span style='background: white; color: #28a745; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; display: inline-block; margin-top: 5px;'>Aproveitamento Final: {p_cv_str}</span>
        </div>
    </div>
    """
    st.write(manchas_html, unsafe_allow_html=True)
else:
    st.info("O município ativo não possui registros ou votos computados nas Urnas Mapeadas.")

st.markdown("---")

# 8. Tabela de Consolidação Cruzada dos Candidatos por Município
st.subheader("🏆 Detalhamento de Votos Oficiais por Município")
df_urnas_display = df_urnas[['municipio', 'marcio', 'liliane', 'acácio']].copy()
df_urnas_display.columns = ['Município', 'Votos Marcio', 'Votos Liliane', 'Votos Acácio']
st.dataframe(df_urnas_display, use_container_width=True)

# 9. FERRAMENTA DE BACKUP INTEGRADA (Gerador de download interno do código fonte)
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
