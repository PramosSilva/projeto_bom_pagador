import streamlit as st
import pandas as pd
import numpy as np


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

st.title("Sistema Bom Pagador")
st.markdown("## Sistema de avalição de clientes.")
st.text("Apresentação geral dos dados coletados.")

# Importando dataset externo que esta armazendo no drive.
st.markdown("Base de dados de clientes externos.")
df_ext = pd.read_csv('/home/rafael/git/projeto_bom_pagador/dataset/banco_externo.csv', index_col="ID")
st.dataframe(df_ext.head(5))

st.markdown("Base de dados de clientes interno.")
df_inter = pd.read_csv("/home/rafael/git/projeto_bom_pagador/dataset/banco_interno.csv", index_col="ID")
st.dataframe(df_inter.head(5))

def get_data():
    return pd.read_csv("/home/rafael/git/projeto_bom_pagador/dataset/base_balanceada.csv")

#----------------- Classificação do cliente utilizando algoritmos ---------------------------------------#
# Função para treinar o modelo
def train_model():
    df = get_data()
    x = df.drop(['ID','Situacao'], axis=1)
    y = df['Situacao']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    clf = GaussianNB()
    clf.fit(x_train, y_train)
    return clf

# Treinando o modelo.
model = train_model()

# Campos de entrada de dados do cliente.
st.sidebar.subheader("Dados do clientes a ser avaliado")
renda_anual = st.sidebar.number_input("Renda Anual", value=0)

sexo = st.sidebar.selectbox("Sexo", ['Masculino', 'Feminino'])
sexo = 1 if sexo == "Masculino" else 2

educa = st.sidebar.selectbox("Educação", [ "Pós-Graduação", "Universitário", "Ensino Médio", "Outros"])
if educa == "Pós-Graduação":
    educa = 1
elif educa == "Universitário": 
    educa = 2 
elif educa == "Ensino Médio": 
    educa = 3 
else:
    educa = 4

estado_civil = st.sidebar.selectbox("Estado Civil", ['Casado', 'Solteiro', 'Outros'])
if estado_civil == "Casado":
    estado_civil = 0
elif estado_civil == "Solteiro":
    estado_civil = 1
else:
    estado_civil = 2


idade = st.sidebar.number_input("Idade", value=0)
tempo_empr =st.sidebar.number_input("Tempo de Empresa", value=0)

# st.write(renda_anual, sexo, educa, estado_civil, idade, tempo_empr)

# Inserindo um botao na tela
btn_predict = st.sidebar.button("Realizar consluta")

# Realizar a consulta quando o botao for acionado
if btn_predict:
    result = model.predict([[renda_anual, sexo, educa, estado_civil, idade, tempo_empr]])
    sit = "Aprovado" if result[0] == 0 else "Reprovado"
    st.sidebar.write("O cliente foi ",sit)    

#-------------- Fim da Classifcação ---------------------------------------------#

#-----------------Apresentação dos dados --------------------------------------#   

st.write("A base de clientes externos possui ", df_ext['Renda Anual'].count() , "e a base de clientes interna possui ", df_inter['Renda Anual'].count())

df = get_data()
st.text('Contagem de clientes de acordo com o sexo.')
sex = df['Sexo'].value_counts()
st.write(sex.rename({1:"Masculino", 2:"Feminino"}, axis='index'))






