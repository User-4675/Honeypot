# Honeypot Project

## Overview
This project implements a modular honeypot framework with support for multiple protocols, currently including:

- SSH honeypot
- (Future) HTTP honeypot

The honeypot logs connection attempts, credentials, and commands executed by clients in a secure and organized way.

## Features
- Emulated SSH shell with command logging
- Logging of attempted usernames and passwords
- Persistent SSH host key to avoid MITM warnings
- Multi-threaded handling of multiple clients
- Modular structure for adding other protocol honeypots

## Installation
Make sure you have Python 3 installed. Then, install dependencies:

```bash
pip install paramiko argparse
```
Optionally, create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install paramiko argparse
```