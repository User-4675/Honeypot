"""
Core of the SSH honeypot server.

This module sets up a socket to listen for incoming SSH connections, and for
each connection, it spawns a new thread to handle the client's session. It uses
Paramiko to implement the SSH protocol.
"""

import socket
import threading
import logging
import paramiko
from typing import Tuple

from honeypot.core.logging import setup_logger
from honeypot.core.key import get_RSA_key
from honeypot.SSH.server import SSHServer
from honeypot.SSH.shell import emulated_shell

# Configure loggers for SSH activities.
auth_logger = logging.getLogger("ssh.auth")
session_logger = logging.getLogger("ssh.session")

# This banner can be customized to mimic a specific SSH server version.
SSH_BANNER: str = "SSH-2.0-OpenSSH_9.1"


def handle_client(client_socket: socket.socket, client_addr: Tuple[str, int], host_key: paramiko.RSAKey) -> None:
    """
    Manages an individual client connection from start to finish.
    """
    client_ip, client_port = client_addr
    session_logger.info(f"Connection received from {client_ip}:{client_port}")

    try:
        transport = paramiko.Transport(client_socket)
        transport.local_version = SSH_BANNER
        
        # Pass the auth logger to the server interface to log credentials.
        server_interface = SSHServer(client_ip, client_port, auth_logger)
        
        transport.add_server_key(host_key)
        transport.start_server(server=server_interface)

        # Wait for the client to open a channel (e.g., a shell).
        channel = transport.accept(timeout=100)
        if channel is None:
            session_logger.warning(f"No channel was opened by {client_ip}. Closing connection.")
            return

        # Send a welcome banner to the client.
        banner = b"Welcome to Ubuntu 24.04.3 LTS (Noble Numbat) x86_64\r\n\r\n"
        channel.send(banner)

        # Start the emulated shell, passing the session logger.
        emulated_shell(channel, client_ip, session_logger)

    except (paramiko.SSHException, EOFError) as e:
        session_logger.warning(f"SSH protocol error from {client_ip}: {e}")
    except Exception as e:
        session_logger.error(f"An unexpected error occurred with client {client_ip}: {e}", exc_info=True)

    finally:
        try:
            transport.close()
        except Exception:
            # The transport may already be closed.
            pass
        client_socket.close()
        session_logger.info(f"Connection from {client_ip}:{client_port} closed.")


def listen_for_connections(address: str, port: int, host_key: paramiko.RSAKey) -> None:
    """
    Binds a socket and listens for incoming TCP connections, spawning threads for each.
    """
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((address, port))
        server_socket.listen(100)
        session_logger.info(f"SSH honeypot listening on {address}:{port}...")
    except Exception as e:
        session_logger.critical(f"Failed to bind or listen on {address}:{port}: {e}", exc_info=True)
        return

    while True:
        try:
            client_socket, client_addr = server_socket.accept()
            thread = threading.Thread(
                target=handle_client, args=(client_socket, client_addr, host_key)
            )
            thread.daemon = True
            thread.start()
        except Exception as e:
            session_logger.error(f"Error accepting connections: {e}", exc_info=True)


def start_ssh_honey(address: str, port: int) -> None:
    """
    Initializes and starts the SSH honeypot service.
    """
    # Set up the loggers before starting the server.
    global auth_logger, session_logger
    auth_logger = setup_logger("ssh.auth", "ssh/credentials.log")
    session_logger = setup_logger("ssh.session", f"ssh/session_{address}_{port}.log")

    host_key = get_RSA_key()
    listen_for_connections(address, port, host_key)