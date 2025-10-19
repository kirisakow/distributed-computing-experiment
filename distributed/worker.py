# worker.py
import socket
import pickle
import random
from tqdm import tqdm

def estimate_pi_chunk(n_points):
    inside = 0
    for _ in tqdm(range(n_points), desc="Computing"):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1:
            inside += 1
    return inside

def run_worker(server_ip, port=5000):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))
    
    chunk_size = pickle.loads(client.recv(4096))
    print(f"Received task: {chunk_size:,} points")
    
    result = estimate_pi_chunk(chunk_size)
    client.send(pickle.dumps(result))
    client.close()
    print("Result sent to server")

if __name__ == "__main__":
    SERVER_IP = "192.168.1.100"  # Change to your server's IP
    run_worker(SERVER_IP)

