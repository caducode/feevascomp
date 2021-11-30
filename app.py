
from flask import Flask
from flask import render_template
from flask import url_for
from posixpath import realpath
from pprint import pprint
from numpy import NaN
import pandas as pd
import math
import sys
import os


app = Flask(__name__)

@app.route("/")
def hello_world():
    css_file = url_for('static', filename='main.css')
    lista = compara_arquivos()
    pprint(lista)
    return render_template('index.html', css_path = css_file, lista_update= lista[0], lista_novas = lista[1] )


def compara_arquivos():
    realPathTeams = os.path.realpath("teams_feevale_digital.xlsx")
    realPathAtualizado = os.path.realpath("registro_feevale_digital.xlsx")
    FILE_PATH_NOVO = realPathAtualizado
    FILE_PATH_ANTIGO = realPathTeams 
    xl = pd.ExcelFile(FILE_PATH_NOVO)
    x2 = pd.ExcelFile(FILE_PATH_ANTIGO)

    #Carrega a planilha com os dados novos 
    df = xl.parse('Data1')
    df = df.fillna('')
    #Carrega a planilha com os dados antigos (atuais)
    df2 = x2.parse('Cursos')
    df2.dropna(subset = ['CodMateriaSiae'], inplace=True)
    df2 = df2.fillna('')
    df2['CodMateriaSiae'] = df2['CodMateriaSiae'].astype(int)


    materiasDicNova= {}
    materiaisDicAnt = {}

    print(len(df2))


    #carrega os dados em um dicionário python, usando numero da linha como indice

    for index, row in df.iterrows():
        materiasDicNova[index] = {"materia": str(row['CodMateriaSiae']),"Nome Materia":row['NomeMateria'],"Carga Horaria Total": row['CHTOTAL'],"Carga Horaria Teorica": row['CHTeorica'],"Carga Horaria Pratica": row['CHPratica'] , "Atividade a Distancia": row['Atividade à distância'], "Atividade Discente": row['Atividade Discente'], "Caracteristica": row['Caracteristica'], "Nome Dimensao": row['NomeDimensao']}

    for index2, row2 in df2.iterrows():
        materiaisDicAnt[index2] = {"materia": str(row2['CodMateriaSiae']),"Nome Materia":row2['NomeMateria'], "Carga Horaria Total": row2['CHTOTAL'],"Carga Horaria Teorica": row2['CHTeorica'],"Carga Horaria Pratica": row2['CHPratica'], "Atividade a Distancia": row2['Atividade à distância'], "Atividade Discente": row2['Atividade Discente'], "Caracteristica": row2['Caracteristica'], "Nome Dimensao": row2['NomeDimensao']}


    cont_alteracao=0
    alteracoes_arr_dic = []
    adicoes_arr_dic = []

    for i in materiaisDicAnt:
        for j in materiasDicNova:
            if((materiaisDicAnt[i]['materia']) == (materiasDicNova[j]['materia'])):
                if((str(materiaisDicAnt[i]['Carga Horaria Total']) != str(materiasDicNova[j]['Carga Horaria Total'])) or (str(materiaisDicAnt[i]['Carga Horaria Teorica']) != str(materiasDicNova[j]['Carga Horaria Teorica'])) or (str(materiaisDicAnt[i]['Carga Horaria Pratica']) != str(materiasDicNova[j]['Carga Horaria Pratica'])) or (str(materiaisDicAnt[i]['Carga Horaria Pratica']) != str(materiasDicNova[j]['Carga Horaria Pratica'])) or (str(materiaisDicAnt[i]['Atividade a Distancia']) != str(materiasDicNova[j]['Atividade a Distancia'])) or (str(materiaisDicAnt[i]['Atividade Discente']) != str(materiasDicNova[j]['Atividade Discente'])) or (str(materiaisDicAnt[i]['Caracteristica']) != str(materiasDicNova[j]['Caracteristica'])) or (str(materiaisDicAnt[i]['Nome Dimensao']) != str(materiasDicNova[j]['Nome Dimensao'])) ):
                    alteracoes_arr_dic.append({"materia": materiaisDicAnt[i]['materia'],"nome materia": materiaisDicAnt[i]['Nome Materia']})
                    #verifica em qual coluna ocorreu alteração
                    if(str(materiaisDicAnt[i]['Carga Horaria Total']) != str(materiasDicNova[j]['Carga Horaria Total'])):
                        alteracoes_arr_dic[cont_alteracao].update({"Carga Horaria Total": str(materiaisDicAnt[i]['Carga Horaria Total']), "Carga Horaria Total - Atualizada": str(materiasDicNova[j]['Carga Horaria Total'])})
                    if(str(materiaisDicAnt[i]['Carga Horaria Teorica']) != str(materiasDicNova[j]['Carga Horaria Teorica'])):
                        alteracoes_arr_dic[cont_alteracao].update({"Carga Horaria Teorica": str(materiaisDicAnt[i]['Carga Horaria Teorica']), "Carga Horaria Teorica - Atualizada": str(materiasDicNova[j]['Carga Horaria Teorica'])})
                    if(str(materiaisDicAnt[i]['Carga Horaria Pratica']) != str(materiasDicNova[j]['Carga Horaria Pratica'])):
                        alteracoes_arr_dic[cont_alteracao].update({"Carga Horaria Pratica": str(materiaisDicAnt[i]['Carga Horaria Pratica']), "Carga Horaria Pratica - Atualizada": str(materiasDicNova[j]['Carga Horaria Pratica'])})    
                    if(str(materiaisDicAnt[i]['Atividade a Distancia']) != str(materiasDicNova[j]['Atividade a Distancia'])):
                        alteracoes_arr_dic[cont_alteracao].update({"Atividade a Distancia": str(materiaisDicAnt[i]['Atividade a Distancia']), "Atividade a Distancia - Atualizada": str(materiasDicNova[j]['Atividade a Distancia'])})    
                    if(str(materiaisDicAnt[i]['Atividade Discente']) != str(materiasDicNova[j]['Atividade Discente'])):
                        alteracoes_arr_dic[cont_alteracao].update({"Atividade Discente": str(materiaisDicAnt[i]['Atividade Discente']), "Atividade Discente - Atualizada": str(materiasDicNova[j]['Atividade Discente'])})
                    if(str(materiaisDicAnt[i]['Caracteristica']) != str(materiasDicNova[j]['Caracteristica'])):
                        alteracoes_arr_dic[cont_alteracao].update({"Caracteristica": str(materiaisDicAnt[i]['Caracteristica']), "Caracteristica - Atualizada": str(materiasDicNova[j]['Caracteristica'])})
                    if(str(materiaisDicAnt[i]['Nome Dimensao']) != str(materiasDicNova[j]['Nome Dimensao'])):
                        alteracoes_arr_dic[cont_alteracao].update({"Nome Dimensao": str(materiaisDicAnt[i]['Nome Dimensao']), "Nome Dimensao - Atualizada": str(materiasDicNova[j]['Nome Dimensao'])})
                    cont_alteracao += 1
    
    #verifica inclusão novas disciplinas 
    listAtualizada = []
    listAntiga = []
    resultado_comparacao = []

    for i in materiasDicNova:
        listAtualizada.append(materiasDicNova[i]['materia'])

    for j in materiaisDicAnt:
        listAntiga.append(materiaisDicAnt[j]['materia'])

    for i in listAtualizada:
        if i not in listAntiga:
            for j in materiasDicNova:
                if(i == materiasDicNova[j]['materia']):
                    adicoes_arr_dic.append(materiasDicNova[j])
    print("------ novas -------")
    pprint(adicoes_arr_dic)
    resultado_comparacao.append(alteracoes_arr_dic)
    resultado_comparacao.append(adicoes_arr_dic)
                    
    return resultado_comparacao




@app.route("/home")
def compara_file():
    return "<h3>Teste de envio</h3>"