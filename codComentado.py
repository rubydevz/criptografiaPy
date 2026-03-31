#observação se voce criptografar e perder a chave, voce perde seu arquivo
#para funcionar é precisor instalar a biblioteca cryptography por meio do pip install no terminal
import tkinter as tk #biblioteca de interface
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet #biblioteca de criptografia, utiliza AES 256
import os

#Lógica do programa
def selecionar_arquivo():
    caminho = filedialog.askopenfilename(title="Selecione o arquivo")
    if caminho:
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, caminho)

def criptografar_arquivo():
    caminho = entrada_arquivo.get()
    if not caminho or not os.path.exists(caminho):
        messagebox.showerror("Erro", "Selecione um arquivo válido!")
        return

    try:
        chave = Fernet.generate_key() #aqui é gerada a chave
        f = Fernet(chave)

        with open(caminho, "rb") as file:
            dados = file.read()

        dados_cripto = f.encrypt(dados) #é criptografado o arquivo

        with open(caminho, "wb") as file:
            file.write(dados_cripto) #subscreve o arquivo original pelo criptografado

        # Exibe a chave para o usuário copiar
        entrada_texto.delete("1.0", tk.END)
        entrada_texto.insert(tk.END, chave.decode())
        messagebox.showinfo("Sucesso", "Arquivo Criptografado! COPIE A CHAVE ABAIXO.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao criptografar: {e}")

def descriptografar_arquivo():
    caminho = entrada_arquivo.get()
    # Pega a chave que o usuário colou no campo de texto
    chave_usuario = entrada_texto.get("1.0", tk.END).strip().encode()

    if not caminho or not os.path.exists(caminho):
        messagebox.showerror("Erro", "Selecione o arquivo criptografado!")
        return
    if not chave_usuario:
        messagebox.showerror("Erro", "Insira a chave no campo de texto!")
        return

    try:
        f = Fernet(chave_usuario)
        
        with open(caminho, "rb") as file:
            dados_cripto = file.read()

        # Tenta descriptografar
        dados_originais = f.decrypt(dados_cripto)

        with open(caminho, "wb") as file:
            file.write(dados_originais)

        messagebox.showinfo("Sucesso", "Arquivo restaurado com sucesso!")
    except Exception:
        messagebox.showerror("Erro", "Chave inválida ou arquivo corrompido!")

#Interface Gráfica utilizando o tkinter
root = tk.Tk()
root.title("Criptografia v1.0") #titulo da interface
root.geometry("550x450") #tamanho da janela
root.configure(padx=20, pady=20)

# Seleção de Arquivo
tk.Label(root, text="1. Arquivo alvo:", font=("Arial", 10, "bold")).pack(anchor="w")
frame_arq = tk.Frame(root)
frame_arq.pack(fill="x", pady=5)
entrada_arquivo = tk.Entry(frame_arq, width=40)
entrada_arquivo.pack(side="left", expand=True, fill="x", padx=(0, 5))
btn_arq = tk.Button(frame_arq, text="Procurar", command=selecionar_arquivo)
btn_arq.pack(side="right")

# Campo de Chave
tk.Label(root, text="2. Chave de Segurança (Gerada ou para Inserir):", font=("Arial", 10, "bold")).pack(anchor="w", pady=(15, 0))
entrada_texto = tk.Text(root, height=4, font=("Courier", 10))
entrada_texto.pack(fill="x", pady=5)

#Botões de criptografar e descriptografar
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=20)

btn_lock = tk.Button(frame_botoes, text="CRIPTOGRAFAR", bg="#d32f2f", fg="white", 
                     font=("Arial", 10, "bold"), width=20, height=2, command=criptografar_arquivo)
btn_lock.grid(row=0, column=0, padx=10)

btn_unlock = tk.Button(frame_botoes, text="DESCRIPTOGRAFAR", bg="#2e7d32", fg="white", 
                       font=("Arial", 10, "bold"), width=20, height=2, command=descriptografar_arquivo)
btn_unlock.grid(row=0, column=1, padx=10)

tk.Label(root, text="Aviso: Não perca a chave, ou o arquivo será irrecuperável.", fg="gray").pack(side="bottom")

root.mainloop() #para a interface funcionar, o tkinter precisa estar em loop infinito
