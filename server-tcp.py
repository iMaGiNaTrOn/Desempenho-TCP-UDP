import socket
import time
import math

def tcp():
    # Configurar o endereço do servidor
    host = socket.gethostname()  # Endereço IP do servidor
    port = 12345  # Porta a ser usada pelo servidor

    # Cria um objeto socket TCP/IP
    # socket.SOCK_STREAM indica que é uma conexão TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o socket com o endereço e porta definidos
    server_socket.bind((host, port))

    # Define o servidor para ouvir conexões
    server_socket.listen(1)

    print('Aguardando conexão...')

    # Aceita a conexão do cliente
    client_socket, client_address = server_socket.accept()
    print('Conexão estabelecida com:', client_address)

    while True:
        # Recebe dados do cliente
        data = client_socket.recv(1024).decode()
        if not data:
            break
        elif data == 'enviar':
            # Recebe nome do arquivo
            filename = client_socket.recv(1024).decode()
            # Recebe o tamanho do pacote
            packet_size = int(client_socket.recv(1024).decode())
            
            while True:
                # Recebe o tamanho do arquivo
                file_size = int(client_socket.recv(1024).decode())
                
            
                client_socket.send(str(file_size).encode())
                sync = client_socket.recv(1024)
                if sync == b'OK':
                    break
                else:
                    continue
            
            print('Tamanho do arquivo:', file_size)
            i = 0
    
            # Começa contador de tempo de execução da comunicação
            start = time.time()
            
            with open(filename, 'wb') as file:
                while i < file_size:
                    # Recebe e escreve os dados, a partir do tamanho de packet_size
                    data = client_socket.recv(packet_size)
                    # print(data)
                    file.write(data)
                        
                    # Print de debug
                    if len(data) != packet_size:
                        i += len(data)
                    else:
                        i += packet_size
                    
            end = time.time()
            
            # Printando no servidor
            print('Arquivo', filename, 'recebido com sucesso com', i, 'pacotes.')
            print('Tomou tempo de', end-start)
            
            data = 'Pacote recebido com sucesso'
        else:
            print('Mensagem recebida do cliente:', data)

        # Envia uma resposta ao cliente
        response = 'Recebido: ' + data
        client_socket.send(response.encode())

    # Fecha a conexão com o cliente
    client_socket.close()

    # Fecha o socket do servidor
    server_socket.close()

if __name__ == '__main__':
    tcp()