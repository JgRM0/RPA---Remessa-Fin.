# Monitor de Remessas

> RPA em Python que monitora a pasta Downloads em tempo real, detecta arquivos `.rem` gerados pelo ERP web e move automaticamente para a pasta do Nexxera (software bancário), registrando log de cada movimentação.

## O problema

A migração do ERP legado para uma versão web reintroduziu uma etapa manual no fluxo do Financeiro: o arquivo `.rem` da remessa bancária passou a cair na pasta **Downloads**, e o colaborador precisava localizá-lo e arrastar até a pasta do Nexxera antes de enviar ao banco.

Etapa pequena, mas com custo real:
- Trabalho braçal repetido várias vezes ao dia
- Margem para erro humano (pasta errada, esquecimento, arquivo duplicado)
- Dependência da atenção do usuário em uma tarefa puramente mecânica

A equipe responsável pelo ERP classificou como limitação técnica do ambiente web. Esta automação resolve a regressão pelo lado do desktop.

## A solução

Um executável que roda em segundo plano e:

1. Observa a pasta **Downloads** em tempo real usando `watchdog`
2. Detecta quando um arquivo `.rem` é finalizado (evento de renomeação que o navegador dispara ao concluir o download)
3. Move o arquivo para a pasta configurada do Nexxera
4. Registra a movimentação em log com data e hora
5. Mostra uma interface mínima em `tkinter` com botão de encerrar

O usuário inicia o executável uma vez e esquece que ele existe. Quando gera uma remessa no ERP, o arquivo já aparece na pasta certa.

## Stack

| Lib | Função |
|---|---|
| `watchdog` | Monitoramento da pasta em tempo real via eventos |
| `os` / `shutil` | Manipulação de arquivos e diretórios |
| `tkinter` | Interface gráfica com botão de encerrar |
| `datetime` | Timestamp dos logs |
| `pyinstaller` | Empacotamento em `.exe` |

## Arquitetura

O projeto segue a regra **um arquivo, uma responsabilidade**:

```
monitor-remessas/
├── modulos/
│   ├── config.py      → caminhos, extensões monitoradas, parâmetros
│   ├── motor.py       → lógica de movimentação e log
│   ├── monitor.py     → handler do watchdog
│   └── interface.py   → janela tkinter
└── main.py            → ponto de entrada
```

- **`config.py`** é o único ponto de mudança para regras de negócio. Pasta de destino, extensões monitoradas e categorias ficam aqui.
- **`motor.py`** não sabe que a interface existe. Pode ser testado isoladamente.
- **`monitor.py`** apenas detecta e delega ao motor — não processa nada.
- **`interface.py`** é uma camada fina, só renderiza e dispara o encerramento.

## Como rodar (desenvolvimento)

Requer Python 3.12 (Pillow/pyscreeze ainda têm incompatibilidades pontuais com 3.14).

```bash
pip install watchdog --default-timeout=1000
```

Ajuste o caminho de destino em `modulos/config.py`:

```python
CATEGORIAS = {
    'Remessas': {
        'tipos': ['.rem'],
        'caminho': r'C:\caminho\para\pasta\do\nexxera'
    }
}
```

Execute:

```bash
python main.py
```

## Empacotamento em .exe

```bash
pyinstaller --onefile --noconsole --name="MonitorRemessas" main.py
```

O executável final fica em `dist/MonitorRemessas.exe`. O usuário só precisa dar dois cliques.

## Detalhe técnico relevante

No Windows, navegadores baixam arquivos com extensão temporária (`.crdownload`, `.tmp`) e **renomeiam** para a extensão final quando o download conclui. Por isso o handler escuta `on_moved` em vez de `on_created` — é o evento que garante que o `.rem` está pronto para ser movido.

```python
def on_moved(self, event):
    if pegar_tipo(event.dest_path) in CATEGORIAS['Remessas']['tipos']:
        time.sleep(2)  # margem de segurança para o sistema liberar o handle
        criar_pastas_e_mover_arquivos(...)
```

## Status

Em produção no setor Financeiro do Grupo SL.

## Autor

João Gabriel Menezes — Assistente de Negócios | Ciência da Computação (UNIFOR)
