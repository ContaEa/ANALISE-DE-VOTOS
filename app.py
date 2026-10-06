import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuração Nativa do Ambiente
st.set_page_config(page_title="Analytics Eleitoral - Amapá", layout="wide", page_icon="🗳️")

st.title("📊 Painel de BI Eleitoral - Árvore Completa (Amapá)")
st.markdown("---")

# 2. Pipeline de Carga e Consolidação Massiva de Dados Reais
@st.cache_data
def load_and_clean_data():
    # Mapeamento consolidado e integral de Clientes x Atendentes por Município
    clients_raw = {
        'Cliente': [
            # Amapá
            'VANUBIA DOS SANTOS ABREU', 'RAIMUNDO CORREA NOBRE', 'GIZELE SANTOS SOUZA', 'RAIMUNDO CORREA NOBRE',
            'LIVIA CELIA MENDES', 'NICOLY PALHETA DE BARROS', 'ALERRANDRO BARBOSA DE OLIVEIRA', 'MANOEL CABRALZINHO SOUZA DOS SANTOS',
            'JORGE FELIPE BARBOSA COSTA', 'EMANUEL DAVY SILVA MOREIRA', 'LEONILSON CASTRO', 'ALINE VITORIA NUNES ARRUDA',
            'VANUBIA DOS SANTOS ABREU', 'MARCOS VINICIUS FARIAS SENA', 'GIZELE SANTOS SOUZA', 'GIRLANE SANTOS DE SOUZA',
            'TAINA CASTRO SANTANA', 'JEDIELSON CASTOR DE FREITAS', 'JOSI DOS SANTOS CASTRO', 'LEONILSON CASTRO',
            'JOSE ALBINO DOS SANTOS', 'MARIA LUCIDIA FORTUNATO DA SILVA', 'SAMYLLE RIANNE COSTA DOS SANTOS', 'MARCOS VINICIUS FARIAS SENA',
            'TAINA CASTRO SANTANA', 'ALINE VITORIA NUNES ARRUDA', 'EZENI SILVA DA PAIXAO', 'ALERRANDRO BARBOSA DE OLIVEIRA',
            'IVANIL DOS PASSOS BRITO', 'CLAUSIDETE CAMPOS DOS SANTOS', 'MARIA LUCIDIA FORTUNATO DA SILVA', 'ANA FABIOLA ALMEIDA CORREA',
            'ANA FABIOLA ALMEIDA CORREA', 'DAYANE COSTA CORREIA', 'EZENI SILVA DA PAIXAO', 'MANOEL CABRALZINHO SOUZA DOS SANTOS',
            'RAIMUNDO CORREA NOBRE', 'NELMA DE LIMA SOUZA', 'FRANCIELE DOS SANTOS QUARESMA', 'EMANUEL DAVY SILVA MOREIRA',
            'THALICIA FERNANDA BRITO SILVA', 'CARLA HIORRANA BRITO SILVA', 'IVANELSON MAGAVE AMADOR', 'GESSICA CRISTINA BARBOSA MACIEL',
            'ISMAEL SALES RAMOS', 'MARIA NEUZA OLIVEIRA DA SILVA',
            # Calçoene
            'BENEDITO COSTA BARBOSA', 'ALINE CRISTINA DE NAZARÉ CORDEIRO DUTRA', 'HELIO LACERDA DOS SANTOS', 'ALEXANDRO ALVES PINHEIRO',
            'MARIA EDUARDA DOS SANTOS RODRIGUES', 'IRENILDES GOMES SILVA', 'ALINE CRISTINA DE NAZARÉ CORDEIRO DUTRA', 'MARIA ELIANA MIRANDA DE SOUSA',
            'MARIA LUIZA SOUZA MARINHO', 'JOSE RIBAMAR DA CRUZ RODRIGUES', 'ALICE FEITOSA DOS SANTOS', 'ALEXANDRO ALVES PINHEIRO',
            # Cutias
            'EDIANE DA SILVA FERREIRA', 'LIA SILVA COSTA', 'THAYSSA TOLOSA PEREIRA', 'RAISSA PEREIRA DOS SANTOS',
            # Ferreira Gomes
            'SAMUEL YAGO DOS SANTOS QUARESMA', 'JOVANA DOS SANTOS NASCIMENTO', 'RAIMUNDA FARAILDE SILVA', 'LANA DOS SANTOS RODRIGUES',
            # Itaubal
            'ROSIVAL RODRIGUES SENA', 'PAULO DOS SANTOS TEIXEIRA', 'MARIA DE JESUS DE OLIVEIRA SOUZA', 'RAIMUNDA TEIXEIRA PANTOJA',
            'MARIA EDUARDA BARBOSA COSTA', 'MARIA CLARA SOUZA BRITO', 'ANDRYA LORENA CAMPOS PEREIRA', 'ANDRYA LORENA CAMPOS PEREIRA',
            # Laranjal do Jari
            'DECIZIENE FLEXA PINTO', 'ELIZEU DE SOUZA MENDES', 'DARA NICOLY LIMA DA SILVA DOS SANTOS', 'RENATA EMANUELE BRAGANÇA SANTOS',
            # Macapá
            'DARCIVALDO DOS PASSOS BASTOS', 'ANTONIO RODRIGUES SIQUEIRA FILHO', 'MARIA GUACIMARA CORREIA DOS SANTOS', 'RUAN LEITÃO BORGES',
            'NAELI COSTA DA COSTA', 'KEMILLY MARIA ROCHA PINHEIRO', 'ELIANE DOS SANTOS RAMOS', 'MAYLON HENRIQUE DOS REIS LIRA',
            # Mazagão
            'GLEICILENE DA SILVA MIRANDA', 'ÉVILI DE OLIVEIRA MIRANDA', 'ELIVANA BELO DA SILVA', 'CAMILA VITORIA CARDOSO FURTADO',
            # Oiapoque
            'RAIMUNDA CARDOSO DUARTE', 'OSVALDO DO NASCIMENTO GONÇALVES', 'JOSÉ FERREIRA PINHEIRO', 'TIBURCIO SOUZA E SILVA',
            # Pedra Branca do Amapari
            'RAYSSA DE ALMEIDA COSTA', 'GABRIEL ARCANJO COSTA NERY', 'SUZANA DOS SANTOS MONTELES', 'ANANITA BARBOSA DE ALMEIDA',
            # Porto Grande
            'VALMIR ANGELO MONTEIRO', 'GABRIELLE THAISSA PANTOJA DA SILVA', 'ANDRENA LIMA COSTA', 'ANNA RHAQUEL MARQUES MENEZES',
            # Pracuúba
            'ELSILEIDE PAIXÃO RAMOS', 'ADRIANA TAVARES LEAL', 'MAYCON BRIAN PASSOS COSTA', 'CARLOS RAIMUNDO PENHA FARIAS',
            # Santana
            'FRANCISCO RAIMUNDO RODRIGUES', 'CLELIA CARMEM BRAZIL DE OLIVEIRA', 'ALAÍSO NONATO GOMES', 'ISAAC BENICIO SILVA DE SOUZA',
            'JOSÉ ALVES SILVA', 'JOYCE LOPES RODRIGUES', 'LIENE DA SILVA COSTA', 'ENIVALDO MAGNO CAMPOS',
            # Tartarugalzinho
            'MARCILENE SOUZA DA SILVA', 'EDNA VIANA DA SILVA', 'LILLIA GOMES CARDIM', 'MARIA ANTONIA SOUSA NOGUEIRA',
            # Vitória do Jari
            'FRANCISCO EDILSON DA SILVA CALDEIRA', 'ODACINEIDE DA COSTA SARGES', 'CAMILA DUTRA DA COSTA', 'CLEDIVANE CARDOSO DE FREITAS'
        ],
        'atendente': [
            # Amapá
            'LEILA BEATRIZ', 'LEILA BEATRIZ', 'BRENDA MONTEIRO', 'LEILA BEATRIZ',
            'NAUINE MARTINS', 'RANUELY CAMPOS', 'NÃO INFORMADO', 'LEILA BEATRIZ',
            'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ',
            'LEILA BEATRIZ', 'LEILA BEATRIZ', 'BRENDA MONTEIRO', 'BRENDA MONTEIRO',
            'NÃO INFORMADO', 'BRENDA MONTEIRO', 'BRENDA MONTEIRO', 'BRENDA MONTEIRO',
            'BRENDA MONTEIRO', 'BRENDA MONTEIRO', 'BRENDA MONTEIRO', 'LEILA BEATRIZ',
            'BRENDA MONTEIRO', 'LEILA BEATRIZ', 'ILETE BALIEIRO', 'NÃO INFORMADO',
            'PEDRO LOBATO', 'PEDRO LOBATO', 'PEDRO LOBATO', 'PEDRO LOBATO',
            'PEDRO LOBATO', 'PEDRO LOBATO', 'ILETE BALIEIRO', 'LEILA BEATRIZ',
            'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ',
            'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ',
            'LEILA BEATRIZ', 'LEILA BEATRIZ',
            # Calçoene
            'EDSON GOMES', 'EDSON GOMES', 'EDSON GOMES', 'EDSON GOMES',
            'EDSON GOMES', 'EDSON GOMES', 'EDSON GOMES', 'LEILA BEATRIZ',
            'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ',
            # Cutias
            'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS',
            # Ferreira Gomes
            'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ', 'LEILA BEATRIZ',
            # Itaubal
            'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS',
            'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS',
            # Laranjal do Jari
            'EDSON GOMES', 'EDSON GOMES', 'EDSON GOMES', 'EDSON GOMES',
            # Macapá
            'ADRIELE RODRIGUES', 'ADRIELE RODRIGUES', 'BRENDA MONTEIRO', 'JOSIVAN SILVA',
            'JOSIVAN SILVA', 'JOSIVAN SILVA', 'FERNANDO SANTOS', 'FERNANDO SANTOS',
            # Mazagão
            'EDSON GOMES', 'EDSON GOMES', 'EDSON GOMES', 'EDSON GOMES',
            # Oiapoque
            'NAUINE MARTINS', 'NAUINE MARTINS', 'NAUINE MARTINS', 'NAUINE MARTINS',
            # Pedra Branca do Amapari
            'EDSON GOMES', 'EDSON GOMES', 'ALESSANDRA GOMES', 'ALESSANDRA GOMES',
            # Porto Grande
            'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'BRENDA MONTEIRO',
            # Pracuúba
            'FERNANDO SANTOS', 'BRENDA MONTEIRO', 'ALESSANDRA GOMES', 'NÃO INFORMADO',
            # Santana
            'JOSIVAN SILVA', 'ADRIELE RODRIGUES', 'EDSON GOMES', 'JOSIVAN SILVA',
            'NAUINE MARTINS', 'NAUINE MARTINS', 'JOSIVAN SILVA', 'JOSIVAN SILVA',
            # Tartarugalzinho
            'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS', 'FERNANDO SANTOS' ,
            # Vitória do Jari
            'LEILA BEATRIZ', 'EDSON GOMES', 'EDSON GOMES', 'EDSON GOMES'
        ],
        'municipio': [
            'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá', 'Amapá',
            'Calçoene', 'Calçoene', 'Calçoene', 'Calçoene', 'Calçoene', 'Calçoene', 'Calçoene', 'Calçoene', 'Calçoene', 'Calçoene', 'Calçoene', 'Calçoene',
            'Cutias', 'Cutias', 'Cutias', 'Cutias',
            'Ferreira Gomes', 'Ferreira Gomes', 'Ferreira Gomes', 'Ferreira Gomes',
            'Itaubal', 'Itaubal', 'Itaubal', 'Itaubal', 'Itaubal', 'Itaubal', 'Itaubal', 'Itaubal',
            'Laranjal do Jari', 'Laranjal do Jari', 'Laranjal do Jari', 'Laranjal do Jari',
            'Macapá', 'Macapá', 'Macapá', 'Macapá', 'Macapá', 'Macapá', 'Macapá', 'Macapá',
            'Mazagão', 'Mazagão', 'Mazagão', 'Mazagão',
            'Oiapoque', 'Oiapoque', 'Oiapoque', 'Oiapoque',
            'Pedra Branca do Amapari', 'Pedra Branca do Amapari', 'Pedra Branca do Amapari', 'Pedra Branca do Amapari',
            'Porto Grande', 'Porto Grande', 'Porto Grande', 'Porto Grande',
            'Pracuúba', 'Pracuúba', 'Pracuúba', 'Pracuúba',
            'Santana', 'Santana', 'Santana', 'Santana', 'Santana', 'Santana', 'Santana', 'Santana',
            'Tartarugalzinho', 'Tartarugalzinho', 'Tartarugalzinho', 'Tartarugalzinho',
            'Vitória do Jari', 'Vitória do Jari', 'Vitória do Jari', 'Vitória do Jari'
        ]
    }
    
    # Consolidação completa dos votos por Município (Extraído da planilha "urnas mapeadas")
    urnas_raw = [
        {'municipio': 'amapá', 'marcio': 19, 'liliane': 5, 'acácio': 56},
        {'municipio': 'calçoene', 'marcio': 0, 'liliane': 0, 'acácio': 0},
        {'municipio': 'cutias', 'marcio': 0, 'liliane': 0, 'acácio': 0},
        {'municipio': 'ferreiragomes', 'marcio': 0, 'liliane': 0, 'acácio': 0},
        {'municipio': 'itaubal', 'marcio': 134, 'liliane': 66, 'acácio': 1333},
{'municipio': 'laranjaldojari', 'marcio': 8991, 'liliane': 0, 'acácio': 4518},
{'municipio': 'macapá', 'marcio': 6328, 'liliane': 3862, 'acácio': 68171},
{'municipio': 'mazagão', 'marcio': 9545, 'liliane': 342, 'acácio': 78},
{'municipio': 'oiapoque', 'marcio': 0, 'liliane': 0, 'acácio': 0},
{'municipio': 'pedrabrancadoamapari', 'marcio': 0, 'liliane': 0, 'acácio': 0},
{'municipio': 'portogrande', 'marcio': 1, 'liliane': 0, 'acácio': 0},
{'municipio': 'pracuúba', 'marcio': 0, 'liliane': 0, 'acácio': 0},
{'municipio': 'santana', 'marcio': 32, 'liliane': 6, 'acácio': 394},
{'municipio': 'tartarugalzinho', 'marcio': 216, 'liliane': 1512, 'acácio': 952},
{'municipio': 'vitória do jari', 'marcio': 29, 'liliane': 2, 'acácio': 151}
]
df1 = pd.DataFrame(clients_raw)
df2 = pd.DataFrame(urnas_raw)
# Higienização de strings para compatibilidade matemática de joins e buscas
df1['municipio_id'] = df1['municipio'].str.lower().str.replace(" ", "").str.strip()
df2['municipio_id'] = df2['municipio'].str.lower().str.replace(" ", "").str.strip()
df1['atendente'] = df1['atendente'].str.upper().str.strip()
return df1, df2
df_clients, df_urnas = load_and_clean_data()
st.sidebar.header("🎯 Parâmetros Analíticos")
all_municipios = sorted(df_clients['municipio'].unique())
selected_municipio = st.sidebar.selectbox("Selecione o Município:", all_municipios)
selected_id = selected_municipio.lower().replace(" ", "").strip()
df_c_filtered = df_clients[df_clients['municipio_id'] == selected_id]
df_u_filtered = df_urnas[df_urnas['municipio_id'] == selected_id]
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
'Marcio (Estimado)': int(votos_marcio * proporcao),
'Liliane (Estimado)': int(votos_liliane * proporcao),
'Acácio (Estimado)': int(votos_acacio * proporcao),
'Total Estimado': int(total_votos_mun * proporcao)
})
df_performance = pd.DataFrame(atendente_data)
st.subheader(f"📈 Panorama Estrutural - {selected_municipio.upper()}")
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
st.metric("Clientes Ativos Mapeados", f"{total_clientes_mun} u")
with kpi2:
st.metric("Votos Consolidados nas Urnas", f"{total_votos_mun} votos")
with kpi3:
indice = (total_clientes_mun / total_votos_mun * 100) if total_votos_mun > 0 else 0
st.metric("Taxa de Penetração Comercial", f"{indice:.2f}%" if total_votos_mun > 0 else "0.00% (Sem Votos)")
st.markdown("---")
st.subheader("🔥 Mapa de Calor Eleitoral: Atendentes x Candidatos")
if not df_performance.empty and total_votos_mun > 0:
df_heat = df_performance[['Atendente', 'Marcio (Estimado)', 'Liliane (Estimado)', 'Acácio (Estimado)']].copy()
max_val = df_heat[['Marcio (Estimado)', 'Liliane (Estimado)', 'Acácio (Estimado)']].max().max()
if max_val == 0: max_val = 1
html_table = ""
html_table += ""
html_table += "Atendente"
html_table += "Marcio"
html_table += "Liliane"
html_table += "Acácio"
html_table += ""
for _, row in df_heat.iterrows():
html_table += f"{row['Atendente']}"
for cand in ['Marcio (Estimado)', 'Liliane (Estimado)', 'Acácio (Estimado)']:
val = row[cand]
alpha = (val / max_val) * 0.85  # Normalização dinâmica de opacidade
html_table += f"<td style='border: 1px solid #ddd; background-color: rgba(220, 53, 69, {alpha:.2f}); color: {'#000' if alpha < 0.4 else '#fff'}; font-weight: bold;'>{val}"
html_table += ""
html_table += ""
st.write(html_table, unsafe_allow_html=True)
else:
st.info(f"O município de {selected_municipio.upper()} não possui histórico de votação mapeado ou o volume de votos nas seções é zero.")
st.markdown("---")
st.subheader("🏆 Ranking de Conversão por Atendente")
if not df_performance.empty:
selected_candidato = st.selectbox("Selecione o Candidato para Filtrar o Ranking:", ['Total Estimado', 'Marcio (Estimado)', 'Liliane (Estimado)', 'Acácio (Estimado)'])
df_performance['% Proporção sobre as Urnas'] = (df_performance[selected_candidato] / total_votos_mun * 100).round(2) if total_votos_mun > 0 else 0
ranking_final = df_performance[['Atendente', 'Clientes Cadastrados', selected_candidato, '% Proporção sobre as Urnas']]
st.dataframe(ranking_final.sort_values(by=selected_candidato, ascending=False), use_container_width=True)