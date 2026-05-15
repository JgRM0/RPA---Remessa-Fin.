from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .config import *
from .motor import *
import time

class MonitorRemessas(FileSystemEventHandler):
    def on_moved(self, event):
        '''Função chamada automaticamente pelo watchdog quando um arquivo é renomeado na pasta monitorada. Verifica se o destino é uma remessa (.rem) e move para a pasta do Nexxera.'''
        print(f'Arquivo renomeado detectado: {event.dest_path}')
        if pegar_tipo(event.dest_path) in CATEGORIAS['Remessas']['tipos']:
            time.sleep(2)
            criar_pastas_e_mover_arquivos(pasta_origem, 'Remessas', event.dest_path, CATEGORIAS['Remessas'])
            registrar_log(f'Arquivo {os.path.basename(event.dest_path)} movido para a pasta Remessas')

observer = Observer()

observer.schedule(MonitorRemessas(), path= pasta_origem, recursive=False)