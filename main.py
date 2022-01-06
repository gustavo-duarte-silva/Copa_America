import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Gustavo')
st.header('Dados da Copa America de 1916 - 2021')
#Carregando os Dados e Tratamento
csv_file = 'copa_america.csv'
df = pd.read_csv(csv_file)
df = df.replace('Cheli', 'Chile')
df = df.drop(columns=['Host','Runners Up', 'Total Match', 'Own Goals', 'Total Goalscorers', 'Total Team'])
df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)

#Criando as opções de Seleção
team_names = df['Champion'].value_counts().index.tolist()
year = df['Year'].unique().tolist()
values = df['Champion'].value_counts()
team_selection = st.multiselect('Times:',
                                    team_names,
                                    default=team_names)
year_selection = st.slider('Selecione o Intervalo de Tempo:', min_value=min(year), max_value=max(year), value=(min(year),max(year)))

filter = (df['Champion'].isin(team_selection)) & (df['Year'].between(*year_selection))
filter_year_by_goal = (df['Year'].between(*year_selection))
df_year = df[filter_year_by_goal]
df_grouped = df[filter].groupby(by=['Champion']).count()
df_grouped.rename(columns={'Year': 'Wins'}, inplace = True)
df_grouped = df_grouped.reset_index()
bar_shart = px.bar(data_frame=df_grouped, x='Champion', y='Wins', text='Wins')
line_shart = px.line(data_frame=df_year, x='Year', y='Total Goal')

st.subheader("Quantidade de Titulos por Time")
st.plotly_chart(bar_shart)
st.subheader("Quantidade de Gols Durante a Copa")
st.plotly_chart(line_shart)

check = st.checkbox(label='Mostrar Tabela', value = False)
if check == True:
    st.dataframe(df)
else:
    st.empty()