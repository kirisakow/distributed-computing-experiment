# server.py
import socket
import pickle
import time
from tqdm import tqdm

def run_server(total_points, n_workers, port=5000):
    chunk_size = total_points // n_workers
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(n_workers)
    print(f"Server listening on port {port}...")
    
    start = time.time()
    results = []
    
    with tqdm(total=n_workers, desc="Collecting results") as pbar:
        for _ in range(n_workers):
            conn, addr = server.accept()
            conn.send(pickle.dumps(chunk_size))
            result = pickle.loads(conn.recv(4096))
            results.append(result)
            conn.close()
            pbar.update(1)
    
    elapsed = time.time() - start
    pi_estimate = 4 * sum(results) / total_points
    
    print(f"\nπ ≈ {pi_estimate:.6f}")
    print(f"Time: {elapsed:.2f}s")
    server.close()

if __name__ == "__main__":
    run_server(total_points=100_000_000, n_workers=3)

