import tkinter as tk

def iniciar_interface(observer):
    janela = tk.Tk()
    janela.title('Monitor de Remessas')
    janela.geometry('300x150')
    janela.resizable(False, False)

    label = tk.Label(janela, text='Monitoramento ativo...', font=('Arial', 10))
    label.place(relx=0.5, rely=0.35, anchor='center')

    botao = tk.Button(janela, text='Parar aplicação', width=20, height=2,
                      bg='#c0392b', fg='white', font=('Arial', 10, 'bold'),
                      command=lambda: [observer.stop(), janela.destroy()])
    botao.place(relx=0.5, rely=0.65, anchor='center')

    janela.mainloop()