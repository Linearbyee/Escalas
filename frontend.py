import tkinter as tk
from tkinter import ttk

# Cores
PRIMARY_COLOR = "#2F1847"
SECONDARY_COLOR = "#8B5BE4"
BACKGROUND_COLOR = "#F0EFF4"

# Criando a janela principal
root = tk.Tk()
root.title("Sistema de Escala")
root.geometry("900x500")
root.configure(bg=BACKGROUND_COLOR)

# Criando o menu lateral
menu_frame = tk.Frame(root, bg=PRIMARY_COLOR, width=70)
menu_frame.pack(side="left", fill="y")

# Criando os botões do menu
buttons = []
icons = ["📅", "🙍", "🎭", "🚫", "⚙"]
abas = ["Escala", "Membros", "Funções", "Bloqueios", "Config"]

def mudar_aba(aba):
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    if aba == "Escala":
        tk.Label(content_frame, text="Gerenciar Escala", font=("Arial", 16), bg=BACKGROUND_COLOR).pack(pady=20)
        ttk.Button(content_frame, text="Gerar Escala", command=gerar_escala).pack()
    elif aba == "Membros":
        tk.Label(content_frame, text="Gerenciar Membros", font=("Arial", 16), bg=BACKGROUND_COLOR).pack(pady=20)
        entry_nome = ttk.Entry(content_frame)
        entry_nome.pack(pady=5)
        ttk.Button(content_frame, text="Adicionar Membro", command=lambda: adicionar_pessoa(entry_nome.get())).pack()
    elif aba == "Funções":
        tk.Label(content_frame, text="Gerenciar Funções", font=("Arial", 16), bg=BACKGROUND_COLOR).pack(pady=20)
        entry_funcao = ttk.Entry(content_frame)
        entry_funcao.pack(pady=5)
        ttk.Button(content_frame, text="Adicionar Função", command=lambda: adicionar_funcao(entry_funcao.get())).pack()
    elif aba == "Bloqueios":
        tk.Label(content_frame, text="Gerenciar Bloqueios", font=("Arial", 16), bg=BACKGROUND_COLOR).pack(pady=20)
        entry_bloqueio = ttk.Entry(content_frame)
        entry_bloqueio.pack(pady=5)
        ttk.Button(content_frame, text="Adicionar Bloqueio", command=lambda: adicionar_bloqueio(entry_bloqueio.get())).pack()
    elif aba == "Config":
        tk.Label(content_frame, text="Configurações", font=("Arial", 16), bg=BACKGROUND_COLOR).pack(pady=20)
        ttk.Button(content_frame, text="Reiniciar Dados", command=resetar_dados).pack()

for i, aba in enumerate(abas):
    btn = tk.Button(menu_frame, text=icons[i], font=("Arial", 14), bg=SECONDARY_COLOR, fg="white", bd=0, relief="flat", command=lambda a=aba: mudar_aba(a))
    btn.pack(pady=10, padx=5, ipadx=5, ipady=5, fill="x")
    buttons.append(btn)

# Criando a área central
content_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
content_frame.pack(side="left", fill="both", expand=True)

# Criando o painel direito
info_frame = tk.Frame(root, bg=PRIMARY_COLOR, width=200)
info_frame.pack(side="right", fill="y")

# Funções placeholders
def gerar_escala():
    print("Gerando escala...")

def adicionar_pessoa(nome):
    print(f"Adicionando membro: {nome}")

def adicionar_funcao(funcao):
    print(f"Adicionando função: {funcao}")

def adicionar_bloqueio(bloqueio):
    print(f"Adicionando bloqueio: {bloqueio}")

def resetar_dados():
    print("Resetando dados...")

# Inicializar a interface com a aba "Escala"
mudar_aba("Escala")

root.mainloop()
