import socket
import threading
import urllib.request
import urllib.parse
import json
from menu import MENU
from time import sleep

# Tentar importar configuração do Telegram, se não existir continua sem
try:
    from telegram_config import BOT_TOKEN, ADMIN_ID
    TELEGRAM_DISPONIVEL = True
except ImportError:
    TELEGRAM_DISPONIVEL = False
    BOT_TOKEN = None
    ADMIN_ID = None

URL = f"https://api.telegram.org/bot{BOT_TOKEN}" if TELEGRAM_DISPONIVEL else None

HOST = "0.0.0.0"
PORT = 5000


def bubblesort(seq):
    seq = seq[:]
    n = len(seq)
    for i in range(n):
        for j in range(0, n - i - 1):
            if seq[j] > seq[j + 1]:
                seq[j], seq[j + 1] = seq[j + 1], seq[j]
    return seq

def telegramGetUpdates(conn= "", addr= "", msg =""):
    if not TELEGRAM_DISPONIVEL:
        return "", ""
    
    try:
        url_get = URL + "/getUpdates"
        requisicao = urllib.request.Request(url_get)
        resposta = urllib.request.urlopen(requisicao, timeout=5)
        dados = json.loads(resposta.read().decode('utf-8'))
        text = dados['result'][-1]['message']['text']
        id = dados['result'][-1]['message']['from']['id']
        return text, id
    except Exception as e:
        print(f"[-] Erro ao obter atualizações do Telegram: {e}")
        return "", ""




def handle_client(conn, addr):
    def send(msg):
        try:
            conn.sendall((msg + "\n").encode("utf-8"))
        except socket.error as e:
            print(f"[-] Erro ao enviar para {addr}: {e}")
        except Exception as e:
            print(f"[-] Erro inesperado ao enviar para {addr}: {e}")
    
    def telegramSendMessage(conn, id, msg):
        if not TELEGRAM_DISPONIVEL:
            return False
        
        try:
            url_send = URL + "/sendMessage"
            dados = urllib.parse.urlencode({
                "chat_id": id,
                "text": msg
            }).encode('utf-8')
            requisicao = urllib.request.Request(url_send, data=dados)
            urllib.request.urlopen(requisicao, timeout=5)
            return True
        except Exception as e:
            print(f"[-] Erro ao enviar mensagem Telegram: {e}")
            return False
 

    print(f"[+] Conexão: {addr}")
    
    try:
        send(MENU)
        conn.settimeout(120)

        while True:
            try:
                data = conn.recv(1024)

                if not data:
                    print(f"[-] Cliente {addr} encerrou a conexão")
                    break

                msg = data.decode("utf-8").strip()

                if not msg:
                    continue

                if msg.lower() == "sair":
                    send("Conexão encerrada.")
                    break
                
                if msg.lower() == "info":
                    send(f"Servidor SuperShirt\nEndereço: {HOST}:{PORT}\nCliente: {addr}\n")
                    continue

                if msg.lower() == "telegram":
                    lastmsg = str()
                    last_id = str()
                    while True:
                        telegram_msg, telegram_id = telegramGetUpdates(conn, addr, msg)
                        if telegram_id == ADMIN_ID and telegram_msg != lastmsg:
                            send(telegram_msg)
                            lastmsg = telegram_msg
                        
                        data = conn.recv(1024)
                        if not data:
                            break
                        msg = data.decode("utf-8").strip()
                        if msg.lower() == "telegram sair":
                            send("Telegram encerrado")
                            break
                        
                        print(telegram_msg)
                        if msg:
                            telegramSendMessage(conn, telegram_id, f"Mensagem recebida: {msg}")
                            last_id = "client"
                        sleep(1)
                    continue

                if msg.lower() == "desligar":
                    send("desligar")
                    break

                try:
                    nums = list(map(int, msg.split()))
                    sorted_nums = bubblesort(nums)
                    
                    # Enviar notificação ao admin no Telegram
                    if TELEGRAM_DISPONIVEL:
                        try:
                            url_send = URL + "/sendMessage"
                            dados = urllib.parse.urlencode({
                                "chat_id": ADMIN_ID,
                                "text": f"📊 Cliente {addr} enviou números:\n{msg}\n\n✅ Ordenado: {sorted_nums}"
                            }).encode('utf-8')
                            requisicao = urllib.request.Request(url_send, data=dados)
                            urllib.request.urlopen(requisicao, timeout=5)
                        except Exception as e:
                            print(f"[-] Erro ao enviar notificação Telegram: {e}")
                    
                    send(f"Ordenado com bubble sort: {sorted_nums}")
                    send("Fechando conexão em 0.5 segundos...")
                    sleep(0.5)
                    send("Conexão encerrada.")
                    break

                except ValueError:
                    send("Envie apenas números separados por espaço.")

            except socket.timeout:
                print(f"[-] Timeout na conexão com {addr}")
                send("Tempo limite excedido. Encerrando conexão.")
                break
            except ConnectionResetError:
                print(f"[-] Conexão perdida abruptamente: {addr}")
                break
            except OSError as e:
                print(f"[-] Erro de socket para {addr}: {e}")
                break
            except Exception as e:
                print(f"[-] Erro inesperado para {addr}: {e}")
                break
    
    except Exception as e:
        print(f"[-] Erro crítico ao lidar com cliente {addr}: {e}")
    
    finally:
        try:
            conn.close()
        except:
            pass
        print(f"[-] Encerrado: {addr}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
