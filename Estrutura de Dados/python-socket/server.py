import socket
import threading
import requests
from menu import MENU
from time import sleep
from telegram_config import BOT_TOKEN, ADMIN_ID

URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

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
    url_get = URL + "/getUpdates"
    response = requests.get(url_get,params={}, verify=False)
    response = response.json()
    text = response['result'][-1]['message']['text']
    id = response['result'][-1]['message']['from']['id']



    return text, id




def handle_client(conn, addr):
    def send(msg):
        try:
            conn.sendall((msg + "\n").encode("utf-8"))
        except:
            pass
    
    def telegramSendMessage(conn, id, msg):
        url_send = URL + "/sendMessage"
        params = {
            "chat_id": id,
            "text": msg
        }
        response = requests.post(url_send,params=params, verify=False)
        return response
 

    print(f"[+] Conexão: {addr}")
    
    send(MENU)
    conn.settimeout(120)

    while True:
        try:
            data = conn.recv(1024)

            if not data:
                break

            msg = data.decode("utf-8").strip()

            if msg.lower() == "sair":
                send("Conexão encerrada.")
                return 0
            
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
                    if msg.lower() == "sair":
                        send("Telegram encerrado")
                        break
                    


                    
                    print(telegram_msg)
                    if msg:
                        telegramSendMessage(conn, telegram_id, f"Mensagem recebida: {msg}")
                        last_id = "client"
                    sleep(1)




            if msg.lower() == "desligar":
                send("desligar")
                break

            try:
                nums = list(map(int, msg.split()))
                sorted_nums = bubblesort(nums)
                send(f"Ordenado com bubble sort: {sorted_nums}")
                send("Fechando conexão em 0.5 segundos...")
                sleep(0.5)
                send("Conexão encerrada.")
                conn.close()

            except ValueError:
                send("Envie apenas números separados por espaço.")

        except socket.timeout:
            print(f"[-] Timeout {addr}")
            break
        except ConnectionResetError:
            print(f"[-] Conexão perdida: {addr}")
            break
        except Exception as e:
            print(f"Erro [{addr}]: {e}")
            break

    conn.close()
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
