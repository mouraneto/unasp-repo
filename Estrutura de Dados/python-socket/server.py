import socket
import threading
import time

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

def telegram_client(conn, addr):
    return


def handle_client(conn, addr):
    def send(msg):
        try:
            conn.sendall((msg + "\n").encode("utf-8"))
        except:
            pass
    menu = open("unasp-repo\Estrutura de Dados\python-socket\menu.txt", "r", encoding="utf-8").read()

    print(f"[+] Conexão: {addr}")
    
    send(menu)
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


            if msg.lower() == "desligar":
                send("desligar")
                break

            try:
                nums = list(map(int, msg.split()))
                sorted_nums = bubblesort(nums)
                send(f"Ordenado com bubble sort: {sorted_nums}")
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
