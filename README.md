# Python Honeypot

A simple, extensible SSH and HTTP honeypot designed to capture and log malicious activity, providing insights into attacker techniques.

## Overview

This honeypot simulates common services to attract and log automated attacks. By analyzing the collected data, you can understand common attack vectors, exploited vulnerabilities, and the types of credentials attackers use.

- The **SSH honeypot** emulates a standard SSH server, providing an interactive shell and logging all commands executed by an attacker.
- The **HTTP honeypot** mimics a WordPress admin login page (`/wp-admin`), a common target for brute-force attacks, and logs all attempted credentials.

## Features

-   **SSH Honeypot**:
    -   Emulates a fully interactive SSH shell.
    -   Logs connection details (IP address, username, password).
    -   Records every command from the attacker's session.
    -   Uses a persistent RSA key to appear consistent to return visitors.
-   **HTTP Honeypot**:
    -   Simulates a WordPress admin login page to capture credential stuffing and brute-force attacks.
    -   Logs submitted usernames and passwords.
    -   Built with Flask for a lightweight and stable web server.
-   **Detailed Auditing**:
    -   Saves detailed, timestamped logs for each session in the `audits` directory.
    -   Logs are organized by service (`HTTP` or `SSH`) for analysis.
-   **Modular Design**: Easily extend the framework with new honeypot services.

## Installation

Ensure you have Python 3.6+ installed on your system.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/honeypot.git
    cd honeypot
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The honeypot is controlled via command-line arguments. You must specify the service to run (`-s` / `--ssh` or `-w`/`--http`) and the address/port to bind to.

**To run the SSH honeypot:**
```bash
python main.py -s -a 0.0.0.0 -p 2222
```
*Note: Running on ports below 1024 (like the default SSH port 22) requires root privileges.*

**To run the HTTP honeypot:**
```bash
python main.py -w -a 0.0.0.0 -p 8080
```

## Auditing and Logs

All activity is logged in the `audits/` directory, separated by service.

-   **SSH Logs**: `audits/ssh/`
    -   Each connection creates a log file named with the session ID and timestamp.
    -   These files contain the client's IP address, the credentials they used, and a full transcript of the commands they executed.

-   **HTTP Logs**: `audits/http/`
    -   A central `credentials.txt` file logs all submitted usernames and passwords along with the attacker's IP and a timestamp.