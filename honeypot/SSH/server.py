"""
A custom Paramiko server interface that logs authentication attempts.

This class accepts any password for any username and logs the credentials.
It only permits 'session' channels (i.e., shells) and denies other request
types like port forwarding.
"""
import logging
import paramiko


class SSHServer(paramiko.ServerInterface):

    def __init__(self, client_ip: str, client_port: int, logger: logging.Logger):
        self.client_ip = client_ip
        self.client_port = client_port
        self.auth_logger = logger

    def check_auth_password(self, username: str, password: str) -> int:
        """
        Called when a client attempts to authenticate with a password.

        This method unconditionally accepts the authentication and logs the
        credentials used.
        """
        self.auth_logger.info(
            f"Login attempt from {self.client_ip}:{self.client_port} - "
            f"Username: '{username}', Password: '{password}'"
        )
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind: str, chanid: int) -> int:
        """
        Called when the client requests a channel.
        Only 'session' channels are permitted.
        """
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def get_allowed_auths(self, username: str) -> str:
        """
        Specifies the allowed authentication methods.
        """
        return "password"

    def check_channel_shell_request(self, channel: paramiko.Channel) -> bool:
        """
        Called when the client requests an interactive shell.
        """
        return True

    def check_channel_pty_request(
        self,
        channel: paramiko.Channel,
        term: bytes,
        width: int,
        height: int,
        pixelwidth: int,
        pixelheight: int,
        modes: bytes,
    ) -> bool:
        """
        Called when the client requests a pseudo-terminal.
        """
        return True
