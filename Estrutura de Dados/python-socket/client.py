import socket
import threading

# host = input("DIgite seu ip")
host = "localhost"
# if host == "":
#     host = "ec2-56-124-114-137.sa-east-1.compute.amazonaws.com"
    
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print("Servidor:", data.decode('utf-8'))
            if data.decode('utf-8').lower() == "desligar":
                print("Conexão encerrada pelo servidor.")
                sock.close()
                break

        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, PORT))
    print("Conectado ao servidor.")

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    while True:
        msg = input("Você: ")
        if msg.lower() == 'sair':
            break
        client.sendall(msg.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    main()
