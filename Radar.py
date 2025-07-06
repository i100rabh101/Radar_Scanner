import socket
import threading
from queue import Queue

print(r'''
██████  █████  █████   ███████ ██████
██   █ ██   ██ ██  ██  ██   ██ ██   █
██████ ███████ ██   ██ ███████ ██████
████   ██   ██ ██  ██  ██   ██ ████
██  ██ ██   ██ █████   ██   ██ ██  ██
                                         
        RADAR - Port Scanner by Sourabh Sharma
        Scan your network. Spot the open gates.
''')

# User Input Section
target = input("Enter target IP or hostname: ").strip()
port_range = input("Enter port range (e.g., 1-1024): ").strip()

# Parse port range
start_port, end_port = map(int, port_range.split('-'))

# Thread-safe queue
q = Queue()

# Lock for printing
print_lock = threading.Lock()

# Port Scan Function
def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            with print_lock:
                print(f"[✔] Port {port} is OPEN")
        sock.close()
    except socket.error:
        with print_lock:
            print(f"[✘] Cannot connect to {target}")
        return

# Thread Function
def threader():
    while True:
        port = q.get()
        scan_port(port)
        q.task_done()

# Start Thread Pool
for _ in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

# Fill queue with port numbers
for port in range(start_port, end_port + 1):
    q.put(port)

# Wait for all threads to finish
q.join()

print(f"\n[🔍] Radar scan complete for {target}")
