import os
import shutil
from datetime import datetime
from .config import *

def Inicializar():
    '''Função para inicializar o processo, listando os arquivos na pasta de origem e contando a quantidade.'''
    caminho_arquivo = [f for f in os.listdir(pasta_origem) if os.path.isfile(os.path.join(pasta_origem, f))]
    print(f'Lista de arquivos na pasta de origem: {caminho_arquivo}')
    tamanho = len(caminho_arquivo)
    print(f'Quantidade de arquivos na pasta de origem: {tamanho}')
    return pasta_origem, caminho_arquivo, tamanho

def pegar_tipo(caminho_arquivo):
    '''Função para extrair a extensão do arquivo.'''
    tipo_arquivo = os.path.splitext(caminho_arquivo)
    return tipo_arquivo[1]

def criar_pastas_e_mover_arquivos(pasta_origem, categoria, caminho_arquivo, info):
    '''Função para criar as pastas de categorias e mover os arquivos para as respectivas pastas.'''
    os.makedirs(os.path.join(info['caminho'], categoria), exist_ok=True)
    shutil.move(caminho_arquivo, os.path.join(info['caminho'], categoria, os.path.basename(caminho_arquivo)))


def registrar_log(mensagem):
    '''Função para registrar logs de movimentação de arquivos.'''
    DIR_MODULO = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(DIR_MODULO, '..', 'log_movimentacao.txt'), 'a') as log:
        horario_log = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        log.write(f'[{horario_log}] {mensagem}\n')

def varrer_pasta(nome_arquivo, tamanho):
    for i in range(tamanho):
        tipo_arquivo = pegar_tipo(nome_arquivo[i])
        print(f'Arquivo {i + 1}: {nome_arquivo[i]} - Tipo: {tipo_arquivo}')
        for categoria, info in CATEGORIAS.items():
            if tipo_arquivo in info['tipos']:
                caminho_completo = os.path.join(pasta_origem, nome_arquivo[i])
                criar_pastas_e_mover_arquivos(pasta_origem, categoria, caminho_completo, info)
                print(f'Arquivo {nome_arquivo[i]} movido para a pasta {categoria}')