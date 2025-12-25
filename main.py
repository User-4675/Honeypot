"""
Main entry point for the honeypot application.

This script parses command-line arguments to start the selected honeypot service (SSH or HTTP)
on a specified IP address and port.
"""

import argparse
from honeypot.SSH.honeypot import start_ssh_honey
from honeypot.HTTP.honeypot import run_web_honeypot


def main() -> None:
    """Parses arguments and starts the chosen honeypot service."""
    parser = argparse.ArgumentParser(
        description="A modular honeypot framework. Select a service to run.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-a",
        "--address",
        type=str,
        required=True,
        help="IP address to bind the honeypot to (e.g., 0.0.0.0 for all interfaces).",
    )
    parser.add_argument(
        "-p", "--port", type=int, required=True, help="Port to listen on."
    )
    
    # Add a mutually exclusive group for service selection
    service_group = parser.add_mutually_exclusive_group(required=True)
    service_group.add_argument(
        "-s", "--ssh", action="store_true", help="Run the SSH honeypot."
    )
    service_group.add_argument(
        "-w", "--http", action="store_true", help="Run the HTTP honeypot."
    )

    args = parser.parse_args()

    try:
        if args.ssh:
            print(f"[-] Booting SSH honeypot on {args.address}:{args.port}...")
            start_ssh_honey(address=args.address, port=args.port)
        elif args.http:
            print(f"[-] Booting HTTP WordPress Honeypot on {args.address}:{args.port}...")
            run_web_honeypot(address=args.address, port=args.port)
    except Exception as e:
        print(f"[!] An error occurred: {e}")


if __name__ == "__main__":
    main()