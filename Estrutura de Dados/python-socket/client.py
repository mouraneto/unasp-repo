import socket
import threading


#teste de mudança


choose_host = input("Digite o ip do Host, ou enter para 'localhost'")
HOST = choose_host if choose_host != "" else "localhost"
PORT = 5000


def receiver(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break

            text = data.decode("utf-8").strip()
            print("Servidor:", text)

            if text.lower() == "desligar":
                print("Servidor encerrou.")
                break

        except:
            break

    try:
        sock.close()
    except:
        pass


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print("Conectado em {}:{}".format(HOST, PORT))

    threading.Thread(target=receiver, args=(sock,), daemon=True).start()

    while True:
        msg = input("> ").strip()
        if not msg:
            continue
        if msg.lower() == "sair":
            sock.sendall(msg.encode("utf-8"))
            break

        sock.sendall(msg.encode("utf-8"))

    sock.close()


if __name__ == "__main__":
    main()
