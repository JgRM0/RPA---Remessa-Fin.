from modulos.motor import *
from modulos.config import *
from modulos.monitor import *
from modulos.interface import *

Pasta_Origem, nome_arquivo, tamanho = Inicializar()

varrer_pasta(nome_arquivo, tamanho)

observer.start()

iniciar_interface(observer)

varrer_pasta(nome_arquivo, tamanho)