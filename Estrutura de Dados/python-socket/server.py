import socket
import threading
import sys
import time
from concurrent.futures import ThreadPoolExecutor as Thread

HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
PORT = 5000       # Porta para escutar conexões
starttime = time.time()



    

def handle_client(conn, addr):
    def sendMsg(msg): conn.sendall((msg+"\n").encode('utf-8'))
    
    


    print(f"[+] Nova conexão: {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode('utf-8')
            print(f"{addr}: {msg}")

            if msg == 'teste':
                sendMsg("Mensagem de teste recebida.")

            elif msg.lower() == 'sair':
                sendMsg("Conexão encerrada pelo cliente.")
                break

            elif msg.lower() == 'desligar':
                sendMsg("desligar")
                conn.close()
                sys.exit()
                return 0
            
            # elif isinstance(eval(msg.lower()), list):
            #     sorted_list = bubblesort(eval(msg.lower()))
            #     sendMsg(f"Números ordenados: {sorted_list}")

            else:
                sendMsg(f"Eco: {msg}")

        except Exception as e:
            print(f"Erro ao lidar com {addr}: {e}")
            break

    print(f"[-] Conexão encerrada: {addr}")

def send_telegram():
    pass

def bubblesort(list:list):
    n = len(list)
    for i in range(n):
        for j in range(0, n-i-1):
            if list[j] > list[j+1]:
                list[j], list[j+1] = list[j+1], list[j]
    print(list)
    return list




def main():
    """Server é um objeto socket que escuta conexões de clientes e responde a mensagens, ele precisa
    ser criado com 2 argumentos: o primeiro é o que indica que será um tipo de conexão utilizando ipv4, tanto o endereço quando a 
    porta precisam ser declaradas. 
    O segundo argumento indica que será uma conexão do tipo TCP, que é orientada a conexão, ou seja,
    antes de enviar dados, é necessário estabelecer uma conexão entre cliente e servidor.
    bind é o método que vincula o socket a um endereço e porta específicos, permitindo que o servidor escute conexões
    listen é o método que coloca o socket em modo de escuta, aguardando conexões de clientes.
    accept é o método que aceita uma conexão de um cliente, retornando um novo socket para comunicação com o cliente
    e o endereço do cliente.

    """


    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.bind((HOST, PORT))
    server.listen()
    print(f"Servidor escutando em {HOST}:{PORT}")
    
    on = True
    # while on:

    #     conn, addr = server.accept()
    #     # with Thread() as executor:
    #     #     executor.submit(handle_client, conn, addr)


        
    #     thread = threading.Thread(target=handle_client, args=(conn, addr))
    #     thread.start()


    

    
    with Thread() as executor:
        while True:
            conn, addr = server.accept()
            if conn:    
                future = executor.submit(handle_client, conn, addr)
                if future.result() == 0:
                    server.close()
                    break



        





if __name__ == "__main__":
    main()
