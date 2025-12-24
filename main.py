import argparse

from honeypot.SSH.honeypot import start_honey

def main():    
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', type=str, required=True, help='IP address to bind the honeypot to')
    parser.add_argument('-p', '--port', type=int, required=True, help='Port to listen on')
    parser.add_argument('-s', '--ssh', action="store_true") # Can treat flag as boolean
    parser.add_argument('-w', '--http', action="store_true")
    args = parser.parse_args()
    
    try:
        if args.ssh:
            print(f"[-] Booting SSH honeypot on {args.address}:{args.port}...")
            start_honey(args.address, args.port)
        elif args.http:
            print("[-] Booting HTTP WordPress Honeypot...")
            # Start HTTP honeypot here
        else:
            print("[!] Select honeypot type")
    except Exception as e:
        print(f'[E] Parser Error: {e}')
                
if __name__ == "__main__": 
    main()