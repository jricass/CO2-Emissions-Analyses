import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(layout="wide", page_title="Análise de Emissões de CO2")

@st.cache_data
def load_data():
    df = pd.read_csv('CO2 Emissions_Canada.csv')
    new_columns = {
        'Make': 'marca',
        'Model': 'modelo',
        'Vehicle Class': 'classe_veiculo',
        'Engine Size(L)': 'tamanho_motor_l',
        'Cylinders': 'cilindros',
        'Transmission': 'transmissao',
        'Fuel Type': 'tipo_combustivel',
        'Fuel Consumption City (L/100 km)': 'consumo_cidade_l_100km',
        'Fuel Consumption Hwy (L/100 km)': 'consumo_estrada_l_100km',
        'Fuel Consumption Comb (L/100 km)': 'consumo_combinado_l_100km',
        'Fuel Consumption Comb (mpg)': 'consumo_combinado_mpg',
        'CO2 Emissions(g/km)': 'emissoes_co2_g_km'
    }
    df.rename(columns=new_columns, inplace=True)
    return df

def get_base64_image(image_path):
  with open(image_path, "rb") as img_file:
      return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_image("assets/github.png")

df = load_data()

st.title("🚗 Análise de Emissões de CO2 no Canadá")
st.markdown("---")

c1, c2 = st.columns([1.5, 4])

c1.markdown('### Sobre o Data Frame')
c1.markdown('O Data Frame utilizado consiste em registros de emissões de CO2 de veículos no Canadá. O Data Frame é proveniente do Kaggle e você pode acessa-lo por [aqui](https://www.kaggle.com/datasets/padhmant/co2-emission-by-vehicles).')

c1.markdown('### Repositório do Projeto')
c1.markdown("Acesse o repositório deste projeto no [GitHub](https://github.com/jricass/CO2-Emissions-Analyses).") 

c1.markdown(
    f"""
    <style>
        .img-github {{
            width: auto;
            max-height: 201px;
            border-radius: 8px;
        }}
    </style>
    <a href="https://github.com/jricass/CO2-Emissions-Analyses"><img src="data:image/png;base64,{img_base64}" class="img-github"/><a>
    """,
    unsafe_allow_html=True
)

c2.markdown('# Dicionário de Dados')
descricoes = {
    "Coluna": [
        "marca", "modelo", "classe_veiculo", "tamanho_motor_l", "cilindros",
        "transmissao", "tipo_combustivel", "consumo_cidade_l_100km",
        "consumo_estrada_l_100km", "consumo_combinado_l_100km",
        "consumo_combinado_mpg", "emissoes_co2_g_km"
    ],
    "Descrição": [
        "Fabricante do veículo",
        "Modelo específico do veículo",
        "Categoria do veículo (ex: SUV, COMPACT)",
        "Tamanho do motor em litros (L)",
        "Número de cilindros do motor",
        "Tipo de transmissão e número de marchas",
        "Tipo de combustível (X, Z, D, E, N)",
        "Consumo de combustível na cidade (L/100 km)",
        "Consumo de combustível na estrada (L/100 km)",
        "Consumo de combustível combinado (55% cidade, 45% estrada)",
        "Consumo combinado em Milhas por Galão (MPG)",
        "Emissões de CO2 em gramas por quilômetro (g/km)"
    ]
}
tabela_descritiva = pd.DataFrame(descricoes)
c2.dataframe(tabela_descritiva, use_container_width=True)
st.markdown('---')

st.sidebar.title("📓 Filtros")

marcas_unicas = sorted(df["marca"].unique())
selecao_marcas = st.sidebar.multiselect("🚗 Marca", options=marcas_unicas, default=marcas_unicas)

classes_unicas = sorted(df["classe_veiculo"].unique())
selecao_classes = st.sidebar.multiselect("🚙 Classe do Veículo", options=classes_unicas, default=classes_unicas)

combustiveis_unicos = sorted(df["tipo_combustivel"].unique())
selecao_combustivel = st.sidebar.multiselect("⛽ Tipo de Combustível", options=combustiveis_unicos, default=combustiveis_unicos)

filtro = df[df["marca"].isin(selecao_marcas) & df["classe_veiculo"].isin(selecao_classes) & df["tipo_combustivel"].isin(selecao_combustivel)]

st.markdown("# 📈 Métricas Gerais")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Veículos", len(filtro))
col2.metric("Emissão Média de CO2 (g/km)", f"{filtro['emissoes_co2_g_km'].mean():.2f}")
col3.metric("Consumo Médio (L/100km)", f"{filtro['consumo_combinado_l_100km'].mean():.2f}")
st.markdown('---')


st.header("Distribuição das Variáveis Numéricas")
st.markdown("Selecione uma variável para visualizar sua distribuição em um histograma.")

colunas_numericas = filtro.select_dtypes(include=['float64', 'int64']).columns.tolist()

variavel_selecionada = st.selectbox(
    "Selecione a variável:",
    options=colunas_numericas,
    index=colunas_numericas.index('emissoes_co2_g_km') 
)

if variavel_selecionada:
    fig = px.histogram(
        filtro,
        x=variavel_selecionada, 
        nbins=50,
        title=f'Distribuição de {variavel_selecionada}'
    )
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig, use_container_width=True)



st.markdown('---')
graph1, graph2 = st.columns([1,1])

graph1.markdown("## 🚙 Classes de Veículos Mais Frequentes")
classes_veiculos = filtro["classe_veiculo"].value_counts().reset_index()
classes_veiculos.columns = ["Classe", "Quantidade"]
fig_pie1 = px.pie(classes_veiculos, values="Quantidade", names="Classe", title="Distribuição por Classe de Veículo")
graph1.plotly_chart(fig_pie1)

graph2.markdown("## ⛽ Tipos de Combustível Mais Frequentes")
tipos_combustivel = filtro["tipo_combustivel"].value_counts().reset_index()
tipos_combustivel.columns = ["Tipo de Combustível", "Frequência"]
fig_pie2 = px.pie(tipos_combustivel, values="Frequência", names="Tipo de Combustível", title="Distribuição por Tipo de Combustível", hole=0.5)
graph2.plotly_chart(fig_pie2)

st.markdown('---')

