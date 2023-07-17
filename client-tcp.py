import socket
import os
import math

def send_file(client_socket, filename, packet_size):
    print(filename)
    file = open(filename, 'rb')
    i = 0
    while True:
        data = file.read(packet_size)
        if not data: 
            print('Entrei no if de parada.')
            break
        client_socket.send(data)
        # print("pacote", i)
        i += 1
    # print("Enviando pacote vazio")
    # client_socket.send(b'')
    print('Arquivo', filename, 'enviado com sucesso.')
    file.close()

def main():
    # Configurar o endereço do servidor
    host = '192.168.100.111'  # Endereço IP do servidor
    port = 12345  # Porta usada pelo servidor

    # Cria um objeto socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta ao servidor remoto
    client_socket.connect((host, port))

    while True:
        # Obtém uma mensagem do usuário
        message = input('Digite uma mensagem para enviar ao servidor (ou "enviar" para enviar um arquivo, e "sair" para encerrar): ')
        if message == 'sair':
            client_socket.shutdown(socket.SHUT_RDWR)
            break
        elif message == 'enviar':
            # Envia a mensagem para o servidor
            client_socket.send(message.encode())
            
            # Obtém o nome do arquivo a ser enviado
            filename = input('Digite o nome do arquivo a ser enviado: ')
            
            # Envia o nome do arquivo para o servidor
            client_socket.send(filename.encode())
            
            # Seleciona o tamanho do pacote
            packet_size = int(input('Digite o tamanho do pacote (100, 500 ou 1000 bytes): '))
            
            # Envia o tamanho do pacote
            client_socket.send(str(packet_size).encode())
            
            # Obtém o tamanho do arquivo
            file_size = os.path.getsize(filename)
            
            # Obtém a quantidade de pacotes máximo no arquivo, com base no tamanho escolhido
            total_packets = math.ceil(file_size/packet_size)
            print(total_packets)
            client_socket.send(str(total_packets).encode())
            
            sync = client_socket.recv(1024)
            # Chama a função para enviar o arquivo
            send_file(client_socket, filename, packet_size)
        
        else:
            # Envia a mensagem ao servidor
            client_socket.send(message.encode())

        # Recebe a resposta do servidor
        response = client_socket.recv(1024).decode()

        print('Resposta do servidor:', response)

    # Fecha a conexão com o servidor
    client_socket.close()

if __name__ == '__main__':
    main()
