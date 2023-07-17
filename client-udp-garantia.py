import socket
import os

def send_file(client_socket, filename, packet_size, host, port):
    with open(filename, 'rb') as file:
        while True:
            data = file.read(packet_size)
            if not data:
                break
            client_socket.sendto(data, (host, port))
            
            #Esperando a confirmação de recebimento do server
            try:
                client_socket.settimeout(1) # Define um timeout de 1 segundo para receber
                _, _ = client_socket.recvfrom(1024)
            except socket.timeout:
                print('Timeout: Pacote não recebido, retransmitindo...')
                continue
            
        # Envia uma mensagem vazia para indicar o final do arquivo
        client_socket.sendto(b'', (host, port))
    print('Arquivo', filename, 'enviado com sucesso.')

def main():
    host = '192.168.100.111'  # Endereço IP do servidor
    port = 12345  # Porta usada pelo servidor

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        message = input('Digite uma mensagem para enviar ao servidor (ou "enviar" para enviar um arquivo, "sair" para encerrar): ')
        if message == 'sair':
            client_socket.shutdown(socket.SHUT_RDWR)
            break
        elif message == 'enviar':
            # Envia a mensagem para o servidor
            client_socket.sendto(message.encode(), (host, port))
            # Obtém o nome do arquivo a ser enviado
            filename = input('Digite o nome do arquivo a ser enviado: ')
            # Envia o nome do arquivo para o servidor
            client_socket.sendto(filename.encode(), (host, port))
            # Obtém o tamannho do pacote a ser enviado
            packet_size = int(input('Digite o tamanho do pacote (100, 500 ou 1000 bytes): '))
            # Envia o tamanho do pacote para o servidor
            client_socket.sendto(str(packet_size).encode(), (host, port))
            
            # Obtém o tamanho do arquivo
            file_size = os.path.getsize(filename)
            print(file_size, end="\n\n")
            # Envia o tamanho do arquivo para o servidor
            client_socket.sendto(str(file_size).encode(), (host, port))
            
            # Chama a função para enviar o arquivo
            send_file(client_socket, filename, packet_size, host, port)
            
            # Recebe confirmação de término de recebimento
            
        else:
            client_socket.sendto(message.encode(), (host, port))

    client_socket.close()

if __name__ == '__main__':
    main()