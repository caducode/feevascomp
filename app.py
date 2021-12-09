
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
    print("entrou metodo compara")
    lista = compara_arquivos()
    print("executou metodo de comparação")
    return render_template('index.html', css_path = css_file, lista_update= lista)


def compara_arquivos():
    pd.set_option('display.max_columns', 4)
    realPathTeams = os.path.realpath("teams_feevale_digital.xlsx")
    realPathAtualizado = os.path.realpath("registro_feevale_digital.xlsx")
    FILE_PATH_NOVO = realPathAtualizado
    FILE_PATH_ANTIGO = realPathTeams 
    df = pd.read_excel(FILE_PATH_NOVO, sheet_name='Data1', dtype='str')
    df2 = pd.read_excel(FILE_PATH_ANTIGO, sheet_name='Cursos' , dtype='str')

    df = df.fillna('')
    df2 = df2.fillna('')

    class LinhaAlterada:
        cod_curriculo=""
        nome_curso=""
        nome_estrutura=""
        cod_materia=""
        nome_comp=""
        ch_total=""
        ch_total_old=""
        ch_teorica=""
        ch_teorica_old=""
        ch_pratica=""
        ch_pratica_old=""
        atividade_dist=""
        atividade_dist_old=""
        atividade_disc=""
        atividade_disc_old=""
        caracte=""
        caracte_old=""
        nome_dimensao=""
        nome_dimensao_old=""


    antigaListagem = df2[['CodCurriculo', 'NomeCurso', 'NomeEstrutura', 'CodMateriaSiae', 'NomeMateria', 'CHTOTAL', 'CHTeorica', 'CHPratica', 'Atividade à distância', 'Atividade Discente', 'Caracteristica', 'NomeDimensao' ]]
    novaListagem =  df[['CodCurriculo', 'NomeCurso', 'NomeEstrutura', 'CodMateriaSiae', 'NomeMateria', 'CHTOTAL', 'CHTeorica', 'CHPratica', 'Atividade à distância', 'Atividade Discente', 'Caracteristica', 'NomeDimensao' ]]
    contador=0
    data=[]
    for row in novaListagem.itertuples():
        for row2 in antigaListagem.itertuples():
            if((row.CodMateriaSiae == row2.CodMateriaSiae) & (row.NomeCurso == row2.NomeCurso) & (row.CodCurriculo == row2.CodCurriculo) ):
                if((row.CHTOTAL !=  row2.CHTOTAL ) | (row.CHTeorica != row2.CHTeorica) | (row.CHPratica != row2.CHPratica) | (row._9 != row2._9) | (row._10 != row2._10) | (row.NomeDimensao != row2.NomeDimensao) | (row.Caracteristica != row2.Caracteristica)  ):
                    
                    objrow = LinhaAlterada()
                    objrow.cod_curriculo= row.CodCurriculo
                    objrow.nome_curso= row.NomeCurso
                    objrow.nome_estrutura = row.NomeEstrutura
                    objrow.cod_materia = row.CodMateriaSiae
                    objrow.nome_comp = row.NomeMateria
                    
                    if(row.CHTOTAL !=  row2.CHTOTAL ):
                        objrow.ch_total = row.CHTOTAL 
                        objrow.ch_total_old = row2.CHTOTAL
                    if(row.CHTeorica != row2.CHTeorica):
                        objrow.ch_teorica =  row.CHTeorica
                        objrow.ch_teorica_old = row2.CHTeorica
                    if(row.CHPratica != row2.CHPratica):
                        objrow.ch_pratica = row.CHPratica 
                        objrow.ch_pratica_old  = row2.CHPratica
                    if(row._9 != row2._9):
                        objrow.atividade_dist = row._9 
                        objrow.atividade_dist_old = row2._9
                    if(row._10 != row2._10):
                        objrow.atividade_disc = row._10 
                        objrow.atividade_disc_old = row2._10
                    if(row.NomeDimensao != row2.NomeDimensao):
                        objrow.nome_dimensao =  row.NomeDimensao 
                        objrow.nome_dimensao_old = row2.NomeDimensao
                    if(row.Caracteristica != row2.Caracteristica):
                        objrow.caracte =  row.Caracteristica 
                        objrow.caracte_old = row2.Caracteristica
                    
                    data.append(objrow)
    return data




@app.route("/home")
def compara_file():
    return "<h3>Teste de envio</h3>"