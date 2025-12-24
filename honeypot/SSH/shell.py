
import logging

# --- Emulated Shell ---
def emulated_shell(channel, client_ip):
    channel.send(b'$ ')
    command = b""


    while True:
        char = channel.recv(1)
        channel.send(char)
        
        if not char:
            channel.close()
        
        command += char
        if char == b'\r':
            inpt = command.strip()
            
            if inpt == b'exit':
                response = b'\nBye!\r\n'
                channel.close()
                return
            elif inpt == b'pwd':
                response = b'\n\\usr\\local\\\r\n'
            elif inpt == b'whoami':
                response = b'\nuser5645\r\n'
            elif inpt == b'ls':
                response = b'\npasswords.txt\r\n'
            elif inpt == b'cat passwords.txt':
                response = b'\nsecret\r\n'
            else:
                response = b'\n' + bytes(inpt) + b'\r\n'
                                
            logging.getLogger("SSHCmds").info(
                f'{client_ip} attempted to run `{str(inpt, 'utf-8')}` command'
            )
            channel.send(response)
            channel.send(b'$ ')
            command = b""
        