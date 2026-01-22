import sys
import socket
from datetime import datetime
import threading

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port)) #error indicator if 0
        if result == 0:
            print(f"port {port} is open")
            sock.close()
    except socket.error as e:
        print(f"Socket error on port {port}: {e}")
    except Exception as e:
        print(f"Unexpected error on port {port}: {e}")
    

# Main function - Argument validation target definition
def main():
    if len(sys.argv) == 2:
        target = sys.argv[1]
    else:
        print("Invlaid number of arguments")
        print("Usage: python.exe Scanner.py <target>")
        sys.exit(1)

#Resolve target hostname to an IP address
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Error: Unabled to resolve hostname error")
        sys.exit(1)
#Add a banner
    print("-" * 50)
    print(f"Scanning Target: {target}")
    print(f"Scanning time started: {str(datetime.now())}")
    print("-" * 50)
    try:
    #Use multithreading to scan ports concurrently
        threads = [""]
        for port in range(1, 65536):
            thread = threading.Thread(target=scan_port, args=(target,port))
            threads.append(thread)
            thread.start()
    #Wait for all threads to complete
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit(0)
    except socket.error as e:
        print("Socket error")
        sys.exit(1)

    print(f"\nScanning completed at: {str(datetime.now())}")

    if __name__ == "__main__":
        main()