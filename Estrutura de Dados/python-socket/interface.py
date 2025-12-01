import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import threading
import urllib.request
import urllib.parse
import json

# Tentar importar configuração do Telegram, se não existir continua sem
try:
    from telegram_config import BOT_TOKEN, ADMIN_ID
    TELEGRAM_DISPONIVEL = True
except ImportError:
    TELEGRAM_DISPONIVEL = False
    BOT_TOKEN = None
    ADMIN_ID = None


class ClienteGrafico:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente Ordenador de Números - Socket")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Variáveis de controle
        self.sock = None
        self.conectado = False
        self.thread_recebimento = None
        
        # Estilo
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        # ===== Frame Principal =====
        frame_principal = ttk.Frame(root, padding="10")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.rowconfigure(5, weight=1)
        
        # ===== Seção de Conexão =====
        frame_conexao = ttk.LabelFrame(frame_principal, text="Conexão ao Servidor", padding="10")
        frame_conexao.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        frame_conexao.columnconfigure(1, weight=1)
        
        # Host
        ttk.Label(frame_conexao, text="Host:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.entrada_host = ttk.Entry(frame_conexao, width=30)
        self.entrada_host.insert(0, "localhost")
        self.entrada_host.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Botão SuperShirt
        self.botao_supershirt = ttk.Button(frame_conexao, text="SuperShirt", command=self.conectar_supershirt)
        self.botao_supershirt.grid(row=0, column=2, padx=5)
        
        # Porta
        ttk.Label(frame_conexao, text="Porta:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entrada_porta = ttk.Entry(frame_conexao, width=30)
        self.entrada_porta.insert(0, "5000")
        self.entrada_porta.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Botões de Conexão
        frame_botoes_conexao = ttk.Frame(frame_conexao)
        frame_botoes_conexao.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.botao_conectar = ttk.Button(frame_botoes_conexao, text="Conectar", command=self.conectar)
        self.botao_conectar.pack(side=tk.LEFT, padx=5)
        
        self.botao_desconectar = ttk.Button(frame_botoes_conexao, text="Desconectar", command=self.desconectar, state=tk.DISABLED)
        self.botao_desconectar.pack(side=tk.LEFT, padx=5)
        
        # Status de Conexão
        self.label_status = ttk.Label(frame_conexao, text="● Desconectado", foreground="red")
        self.label_status.grid(row=3, column=0, columnspan=2, pady=5)
        
        # ===== Seção de Entrada de Números =====
        frame_entrada = ttk.LabelFrame(frame_principal, text="Enviar Números", padding="10")
        frame_entrada.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        frame_entrada.columnconfigure(0, weight=1)
        
        ttk.Label(frame_entrada, text="Digite números separados por espaço:").pack(anchor=tk.W, pady=5)
        
        self.entrada_numeros = ttk.Entry(frame_entrada, width=50)
        self.entrada_numeros.pack(fill=tk.X, pady=5)
        self.entrada_numeros.bind("<Return>", lambda e: self.enviar_numeros())
        
        frame_botoes_entrada = ttk.Frame(frame_entrada)
        frame_botoes_entrada.pack(fill=tk.X, pady=10)
        
        self.botao_enviar = ttk.Button(frame_botoes_entrada, text="Enviar Números", command=self.enviar_numeros, state=tk.DISABLED)
        self.botao_enviar.pack(side=tk.LEFT, padx=5)
        
        self.botao_limpar = ttk.Button(frame_botoes_entrada, text="Limpar", command=lambda: self.entrada_numeros.delete(0, tk.END))
        self.botao_limpar.pack(side=tk.LEFT, padx=5)
        
        # ===== Seção de Saída =====
        frame_saida = ttk.LabelFrame(frame_principal, text="Resposta do Servidor", padding="10")
        frame_saida.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        frame_saida.columnconfigure(0, weight=1)
        frame_saida.rowconfigure(0, weight=1)
        
        # Área de texto com scroll
        self.area_saida = scrolledtext.ScrolledText(frame_saida, height=15, width=80, state=tk.DISABLED)
        self.area_saida.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botão limpar saída
        self.botao_limpar_saida = ttk.Button(frame_principal, text="Limpar Saída", command=self.limpar_saida)
        self.botao_limpar_saida.grid(row=6, column=0, pady=5)
    
    def conectar_supershirt(self):
        """Conecta ao servidor SuperShirt"""
        self.entrada_host.delete(0, tk.END)
        self.entrada_host.insert(0, "18.229.117.78")
        self.entrada_porta.delete(0, tk.END)
        self.entrada_porta.insert(0, "5000")
        self.conectar()
    
    def conectar(self):
        """Conecta ao servidor"""
        try:
            host = self.entrada_host.get().strip()
            porta = int(self.entrada_porta.get().strip())
            
            if not host:
                messagebox.showerror("Erro", "Digite um host válido!")
                return
            
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, porta))
            self.conectado = True
            
            # Atualizar interface
            self.botao_conectar.config(state=tk.DISABLED)
            self.botao_desconectar.config(state=tk.NORMAL)
            self.botao_enviar.config(state=tk.NORMAL)
            self.entrada_host.config(state=tk.DISABLED)
            self.entrada_porta.config(state=tk.DISABLED)
            self.label_status.config(text="● Conectado", foreground="green")
            
            self.adicionar_saida(f"✓ Conectado a {host}:{porta}\n")
            
            # Thread para receber mensagens
            self.thread_recebimento = threading.Thread(target=self.receber_mensagens, daemon=True)
            self.thread_recebimento.start()
            
        except ValueError:
            messagebox.showerror("Erro", "Porta deve ser um número inteiro!")
        except ConnectionRefusedError:
            messagebox.showerror("Erro", "Não foi possível conectar ao servidor!")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Erro: {str(e)}")
    
    def desconectar(self):
        """Desconecta do servidor"""
        try:
            if self.sock:
                self.sock.sendall("sair\n".encode("utf-8"))
                self.sock.close()
            
            self.conectado = False
            self.sock = None
            
            # Atualizar interface
            self.botao_conectar.config(state=tk.NORMAL)
            self.botao_desconectar.config(state=tk.DISABLED)
            self.botao_enviar.config(state=tk.DISABLED)
            self.entrada_host.config(state=tk.NORMAL)
            self.entrada_porta.config(state=tk.NORMAL)
            self.label_status.config(text="● Desconectado", foreground="red")
            
            self.adicionar_saida("✗ Desconectado do servidor\n")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao desconectar: {str(e)}")
    
    def enviar_numeros(self):
        """Envia os números para o servidor"""
        if not self.conectado:
            messagebox.showwarning("Aviso", "Você não está conectado ao servidor!")
            return
        
        numeros = self.entrada_numeros.get().strip()
        
        if not numeros:
            messagebox.showwarning("Aviso", "Digite alguns números!")
            return
        
        try:
            # Validar se são números
            partes = numeros.split()
            for parte in partes:
                int(parte)
            
            # Enviar notificação ao admin no Telegram (em thread separada)
            if TELEGRAM_DISPONIVEL:
                thread_telegram = threading.Thread(target=self._enviar_telegram, args=(numeros,), daemon=True)
                thread_telegram.start()
            
            self.sock.sendall((numeros + "\n").encode("utf-8"))
            self.adicionar_saida(f"→ Enviado: {numeros}\n")
            self.entrada_numeros.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, digite apenas números inteiros separados por espaço!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar: {str(e)}")
            self.desconectar()
    
    def _enviar_telegram(self, numeros):
        """Envia notificação ao Telegram sem bloquear a interface"""
        if not TELEGRAM_DISPONIVEL:
            return
        
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            dados = urllib.parse.urlencode({
                "chat_id": ADMIN_ID,
                "text": f"📱 Usuario enviou números via interface:\n{numeros}"
            }).encode('utf-8')
            
            requisicao = urllib.request.Request(url, data=dados)
            urllib.request.urlopen(requisicao, timeout=5)
        except Exception as e:
            print(f"[-] Erro ao enviar notificação Telegram: {e}")
    
    def receber_mensagens(self):
        """Recebe mensagens do servidor em thread separada"""
        try:
            while self.conectado and self.sock:
                data = self.sock.recv(1024)
                
                if not data:
                    self.root.after(100, self.desconectar)
                    break
                
                mensagem = data.decode("utf-8").strip()
                self.root.after(0, self.adicionar_saida, f"← Servidor: {mensagem}\n")
        
        except socket.timeout:
            if self.conectado:
                self.root.after(100, lambda: messagebox.showerror("Erro", "Timeout na conexão com o servidor"))
                self.root.after(100, self.desconectar)
        except ConnectionResetError:
            if self.conectado:
                self.root.after(100, lambda: messagebox.showerror("Erro", "Conexão perdida pelo servidor"))
                self.root.after(100, self.desconectar)
        except OSError as e:
            if self.conectado:
                self.root.after(100, lambda: messagebox.showerror("Erro de Conexão", f"Erro: {str(e)}"))
                self.root.after(100, self.desconectar)
        except Exception as e:
            if self.conectado:
                self.root.after(100, lambda: messagebox.showerror("Erro", f"Erro ao receber: {str(e)}"))
                self.root.after(100, self.desconectar)
    
    def adicionar_saida(self, texto):
        """Adiciona texto à área de saída"""
        self.area_saida.config(state=tk.NORMAL)
        self.area_saida.insert(tk.END, texto)
        self.area_saida.see(tk.END)
        self.area_saida.config(state=tk.DISABLED)
    
    def limpar_saida(self):
        """Limpa a área de saída"""
        self.area_saida.config(state=tk.NORMAL)
        self.area_saida.delete(1.0, tk.END)
        self.area_saida.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteGrafico(root)
    root.mainloop()
