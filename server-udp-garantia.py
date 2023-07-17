import socket
import time

def receive_file(client_socket, filename, packet_size):
    # Contador de pacotes
    i = 0
    file = open(filename, 'wb')
    start = time.time()
    while True:
        # Recebendo os valores do cliente
        data, address = client_socket.recvfrom(packet_size)
        client_socket.sendto(b'Recebido', address)
        # Condição de parada
        if not data:
            break
        file.write(data)
        # print("pacote", i)
        i+=1
        # Mensagem que indicia o recebimento do pacote
        
    end = time.time()
    file.close()
    print('Arquivo', filename, ', vindo de', address[0], 'recebido com sucesso com', i, 'pacotes.')
    print('Tomou tempo de', end-start)


def main():
    host = socket.gethostname()  # Endereço IP do servidor
    port = 12345  # Porta a ser usada pelo servidor

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print('Aguardando mensagens...')

    while True:
        try:
            server_socket.settimeout(120)
            data, address = server_socket.recvfrom(1024)
            server_socket.settimeout(None)
            data = data.decode()
            if data == 'enviar':
                # Recebe o nome do arquivo
                filename, address = server_socket.recvfrom(1024)
                filename = 'saida_' + filename.decode()
                
                # Recebe o tamanho do arquivo
                packet_size, address = server_socket.recvfrom(1024)
                packet_size = int(packet_size.decode())
                
                # Recebe o tamanho do arquivo
                file_size, address = server_socket.recvfrom(1024)
                file_size = int(file_size)
                
                # Chama a função para receber o arquivo
                receive_file(server_socket, filename, packet_size)
                
            else:
                print('Mensagem recebida do cliente', address, ':', data)
        except socket.timeout:
            server_socket.close()

if __name__ == '__main__':
    main()