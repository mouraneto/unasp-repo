import socket
import threading


#teste de mudança


choose_host = input("Digite o ip do Host, ou enter para 'localhost'")
HOST = choose_host if choose_host != "" else "localhost"
PORT = 5000


def receiver(sock):
    """Recebe mensagens do servidor com tratamento de erros"""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[!] Conexão encerrada pelo servidor.")
                break

            text = data.decode("utf-8").strip()
            if text:
                print("\nServidor:", text)
                print("> ", end="", flush=True)

            if text.lower() == "desligar":
                print("[!] Servidor encerrou.")
                break

        except socket.timeout:
            print("\n[!] Timeout na conexão com o servidor.")
            break
        except ConnectionResetError:
            print("\n[!] Conexão perdida pelo servidor.")
            break
        except OSError as e:
            print(f"\n[!] Erro de conexão: {e}")
            break
        except Exception as e:
            print(f"\n[!] Erro ao receber dados: {e}")
            break
    
    try:
        sock.close()
    except:
        pass


def main():
    """Função principal com tratamento de desconexão"""
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # Timeout de 10 segundos
        sock.connect((HOST, PORT))
        sock.settimeout(120)  # Aumentar timeout após conexão

        print(f"[+] Conectado em {HOST}:{PORT}")

        threading.Thread(target=receiver, args=(sock,), daemon=True).start()

        while True:
            try:
                msg = input("> ").strip()
                if not msg:
                    continue
                if msg.lower() == "sair":
                    try:
                        sock.sendall(msg.encode("utf-8"))
                    except:
                        pass
                    print("[+] Desconectando...")
                    break

                sock.sendall(msg.encode("utf-8"))
            
            except BrokenPipeError:
                print("\n[!] Conexão foi encerrada pelo servidor.")
                break
            except OSError as e:
                print(f"\n[!] Erro ao enviar dados: {e}")
                break
            except KeyboardInterrupt:
                print("\n[+] Cliente encerrado pelo usuário.")
                try:
                    sock.sendall(b"sair")
                except:
                    pass
                break
            except Exception as e:
                print(f"\n[!] Erro: {e}")
                break

    except ConnectionRefusedError:
        print(f"[!] Não foi possível conectar a {HOST}:{PORT}. Servidor não está disponível.")
    except socket.timeout:
        print(f"[!] Timeout ao tentar conectar a {HOST}:{PORT}.")
    except OSError as e:
        print(f"[!] Erro de conexão: {e}")
    except Exception as e:
        print(f"[!] Erro inesperado: {e}")
    finally:
        if sock:
            try:
                sock.close()
            except:
                pass
        print("[+] Conexão fechada.")


if __name__ == "__main__":
    main()
