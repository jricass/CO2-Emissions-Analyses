import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="centered", page_title="Análise de Emissões de CO2")

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

df = load_data()

st.title("Dashboard Simples: Análise de Emissões de CO2")
st.markdown("Uma visão geral das distribuições das variáveis do dataset.")

st.header("Dicionário de Dados")
st.markdown("Descrição das colunas presentes no dataset:")

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
st.dataframe(tabela_descritiva, use_container_width=True)


st.header("Distribuição das Variáveis Numéricas")
st.markdown("Selecione uma variável para visualizar sua distribuição em um histograma.")

colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

variavel_selecionada = st.selectbox(
    "Selecione a variável:",
    options=colunas_numericas,
    index=colunas_numericas.index('emissoes_co2_g_km') # Começa com a principal
)

if variavel_selecionada:
    fig = px.histogram(
        df, 
        x=variavel_selecionada, 
        nbins=50,
        title=f'Distribuição de {variavel_selecionada}'
    )
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig, use_container_width=True)

st.info("Fim do dashboard. Este é um layout simplificado focado na exploração de distribuições.")

