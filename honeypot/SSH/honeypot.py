import socket
import threading
import paramiko

from honeypot.core.logging import init_logger 
from honeypot.core.key import get_RSA_key
from honeypot.SSH.shell import emulated_shell
from honeypot.SSH.server import Server

SSH_BANNER = "SSH-2.0-OpenSSH_9.1"

def client_handle(client, addr, host_key):
    client_ip = addr[0]
    client_port = addr[1]
    print(f'{client_ip}:{client_port} has connected to server.')
    
    try:
        
        transport = paramiko.Transport(client)
        transport.local_version = SSH_BANNER
        server = Server(client_ip=client_ip, client_port=client_port)
        
        transport.add_server_key(host_key)
        transport.start_server(server=server)
        
        channel = transport.accept(100) # Wait 100s to open channel
        if channel is None:
            print("No chanel was opened")
            return

        standard_banner = b'Welcome to Ubuntu 24.04.3 LTS (Noble Numbat) x86_64\r\n\r\n'
        channel.send(standard_banner)
        
        emulated_shell(channel, client_ip)
                
    except Exception as e:
        print(f'Error from {client_ip}: {e}')

    finally:
        try:
            transport.close()
        except Exception as e:
            print(f'Error occured while closing transport: {e}')
        client.close()

def honeypot(address, port, host_key):
    
    # Set socket for IPv4 and TCP Connection
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    # This allows the socket to bind to a port that is still marked as in use by the OS, typically due to recently closed connections.
    sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to ip address and port
    sockfd.bind((address, port))
    
    # Set limit for connections
    sockfd.listen(100)
    print(f'SSH server listeing on port {port}...')
    
    while True:
        try:
            # Accept a connection
            client, addr = sockfd.accept()
            
            # Spawn a thread and start it
            ssh_thread = threading.Thread(target=client_handle, args=(client, addr, host_key))
            ssh_thread.start()
            
        except Exception as e:
            print(f'{e}')

def start_honey(server_ip, server_port):
    init_logger("SSHCreds", "audits/credentials.log")
    init_logger("SSHCmds", "audits/actions.log")
    honeypot(server_ip, server_port, get_RSA_key())