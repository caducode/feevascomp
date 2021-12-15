
from flask import Flask, flash, request, redirect, url_for,render_template
from posixpath import realpath
from pprint import pprint
from numpy import NaN
import pandas as pd
import math
import sys
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

@app.route("/")
def hello_world():
    css_file = url_for('static', filename='main.css')
    print("entrou metodo compara")
    lista = compara_arquivos()
    print("executou metodo de comparação")
    return render_template('index.html', css_path = css_file, lista_update= lista[0], lista_novos= lista[1])

@app.route("/file_old", methods=['GET', 'POST'])
def file_old():
    if(request.method == 'POST'):
        print(request.files)
        if 'file_old' not in request.files:
            flash('Problema no envio do arquivo')
            return redirect(request.url)
        file = request.files['file_old']
        if file.filename == '':
            flash('Arquivo não selecionado')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print('entrou aqui', file.filename)
            filename = secure_filename(file.filename)
            file.save('/'.join(['uploads', filename]))
            return redirect('/')
    return redirect('/')

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

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
    
    class LinhaAdd:
        cod_curriculo=""
        nome_curso=""
        nome_estrutura=""
        cod_materia=""
        nome_comp=""
        ch_total=""
        ch_teorica=""
        ch_pratica=""
        atividade_dist=""
        atividade_disc=""
        caracte=""
        nome_dimensao=""


    antigaListagem = df2[['CodCurriculo', 'NomeCurso', 'NomeEstrutura', 'CodMateriaSiae', 'NomeMateria', 'CHTOTAL', 'CHTeorica', 'CHPratica', 'Atividade à distância', 'Atividade Discente', 'Caracteristica', 'NomeDimensao' ]]
    novaListagem =  df[['CodCurriculo', 'NomeCurso', 'NomeEstrutura', 'CodMateriaSiae', 'NomeMateria', 'CHTOTAL', 'CHTeorica', 'CHPratica', 'Atividade à distância', 'Atividade Discente', 'Caracteristica', 'NomeDimensao' ]]
    contador=0
    data=[]
    data2=[]
    finalList = []
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
    finalList.append(data)

    #verifica novas disciplinas:
    for row3 in novaListagem.itertuples():
        if(row3.CodMateriaSiae not in list(antigaListagem['CodMateriaSiae'])):
            objrow2 = LinhaAdd()
            objrow2.cod_curriculo= row3.CodCurriculo
            objrow2.nome_curso= row3.NomeCurso
            objrow2.nome_estrutura = row3.NomeEstrutura
            objrow2.cod_materia = row3.CodMateriaSiae
            objrow2.nome_comp = row3.NomeMateria
            objrow2.ch_total =   row3.CHTOTAL 
            objrow2.ch_teorica =   row3.CHTeorica  
            objrow2.ch_pratica =  row3.CHPratica 
            objrow2.atividade_dist =  row3._9 
            objrow2.atividade_disc = row3._10 
            objrow2.nome_dimensao =  row3.NomeDimensao
            objrow2.caracte = row3.Caracteristica 
            data2.append(objrow2)
    finalList.append(data2)
    


    return finalList




@app.route("/home")
def compara_file():
    return "<h3>Teste de envio</h3>"