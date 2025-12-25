"""
Provides a fake interactive shell for the SSH honeypot.

This module simulates a simple command-line environment to interact with
attackers, logging all commands they execute.
"""

import logging
import paramiko

# A mapping of fake commands to their simulated output.
# This can be easily extended to add more commands.
FAKE_COMMANDS = {
    b"pwd": b"/home/user\r\n",
    b"whoami": b"user\r\n",
    b"id": b"uid=1000(user) gid=1000(user) groups=1000(user),27(sudo)\r\n",
    b"ls": b"passwords.txt\tsecret_folder\r\n",
    b"ls -la": b"total 8\r\ndrwxr-xr-x 2 user user 4096 Dec 1 10:00 .\r\ndrwxr-xr-x 3 root root 4096 Nov 28 09:00 ..\r\n-rw-r--r-- 1 user user   12 Dec 1 10:00 passwords.txt\r\ndrwxr-xr-x 2 user user    0 Dec 1 10:00 secret_folder\r\n",
    b"cat passwords.txt": b"admin:password123\r\n",
    b"uname -a": b"Linux ubuntu 5.15.0-52-generic #58-Ubuntu SMP Thu Oct 13 09:46:43 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux\r\n",
}


def emulated_shell(channel: paramiko.Channel, client_ip: str, session_logger: logging.Logger) -> None:
    
    session_logger.info("Starting emulated shell.")
    
    prompt = b"$ "
    channel.send(prompt)
    command = b""

    try:
        while True:
            char = channel.recv(1)
            if not char:  # Client disconnected
                session_logger.info("Client disconnected.")
                break

            # Echo back the character for an interactive feel
            channel.send(char)

            if char in (b"\r", b"\n"):
                # Handle carriage return (execute command)
                command_str = command.strip()
                channel.send(b"\r\n")

                if command_str:
                    session_logger.info(f"Command executed: '{command_str.decode(errors='ignore')}'")
                    
                    if command_str == b"exit":
                        channel.send(b"logout\r\n")
                        break
                    
                    # Get the response from our fake command dictionary
                    response = FAKE_COMMANDS.get(command_str, b"command not found: " + command_str + b"\r\n")
                    channel.send(response)

                channel.send(prompt)
                command = b""
            elif char == b"\x7f":  # Handle backspace
                if command:
                    command = command[:-1]
                    # Move cursor back, print space, move back again
                    channel.send(b"\b \b")
            else:
                command += char

    except Exception as e:
        session_logger.error(f"Error in shell loop: {e}", exc_info=True)
    finally:
        session_logger.info("Closing shell.")
        channel.close()