
import logging
import paramiko

# --- SSH server implementation used by Paramiko ---
class Server(paramiko.ServerInterface):

    # Called when the Server object is created
    # Stores client metadata (not required for SSH itself)
    def __init__(self, client_ip, client_port):
        self.client_ip = client_ip
        self.client_port = client_port
        self.input_username = None
        self.input_password = None

    # Called when the client tries to authenticate using a password
    # Returning AUTH_SUCCESSFUL means "accept any username/password"
    def check_auth_password(self, username, password):
        self.input_username = username
        self.input_password = password
        
        logging.getLogger("SSHCreds").info(
            f"Address={self.client_ip}:{self.client_port} USER={username} PASS={password}"
        )
        
        return paramiko.AUTH_SUCCESSFUL

    # Called when the client requests a new channel
    # SSH supports many channel types; we only allow "session"
    # Returning OPEN_SUCCEEDED allows the channel to be created
    def check_channel_request(self, kind: str, chanid: str) -> int:
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED

        # Reject all other channel types (port forwarding, exec, subsystems)
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    # Tells the client which authentication methods are supported
    # In this case, only password authentication is allowed
    def get_allowed_auths(self, username):
        return "password"

    # Called when the client requests an interactive shell
    # Returning True allows the client to start typing commands
    def check_channel_shell_request(self, channel):
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True  # Accept PTY request
