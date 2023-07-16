import socket
import time
import math

def receive_file(client_socket, filename, packet_size, file_size):
    # Contador de pacotes
    i = 0
    # Abrindo arquivo, e não existir, o cria
    file = open(filename, 'wb')
    
    # print(math.ceil(file_size/packet_size))
    
    # Começa contador de tempo de execução da comunicação
    start = time.time()
    
    while i < math.ceil(file_size/packet_size):
        # Recebe e escreve os dados, a partir do tamanho de packet_size
        data = client_socket.recv(packet_size)
        
        if not data:
            break
        
        file.write(data)
        
        # Print de debug
        # print("pacote", i)
        i+=1
    end = time.time()
    file.close()
    
    # data = client_socket.recv(1024)
    # print(data)
    
    # Printando no servidor
    print('Arquivo', filename, 'recebido com sucesso com', i, 'pacotes.')
    print('Tomou tempo de', end-start)

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
            
            # Recebe o tamanho do arquivo
            file_size = client_socket.recv(1024).decode()
            print(file_size)
            
            # Função de sincronização
            # Sem isso, ele estava enviando tanto o tamanho do pacote quanto outras informações pela parte do cliente
            # Então eu fiz um pedido de espera, para que as cosias começassem adequadamente
            sync = "yes"
            client_socket.send(sync.encode())
            file_size = int(file_size)
            
            # Chama função para receber o arquivo
            receive_file(client_socket, filename, packet_size, file_size)
            
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
