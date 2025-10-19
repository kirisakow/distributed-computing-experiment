# multi_core.py
import time
import random
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def estimate_pi_chunk(n_points):
    inside = 0
    for _ in range(n_points):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1:
            inside += 1
    return inside

def estimate_pi_parallel(total_points, n_cores=None):
    n_cores = n_cores or cpu_count()
    chunk_size = total_points // n_cores
    
    start = time.time()
    with Pool(n_cores) as pool:
        results = list(tqdm(
            pool.imap(estimate_pi_chunk, [chunk_size] * n_cores),
            total=n_cores,
            desc=f"Computing ({n_cores} cores)"
        ))
    elapsed = time.time() - start
    
    pi_estimate = 4 * sum(results) / total_points
    return pi_estimate, elapsed

if __name__ == "__main__":
    TOTAL_POINTS = 100_000_000
    
    # Single core
    print("Single core:")
    start = time.time()
    result = estimate_pi_chunk(TOTAL_POINTS)
    elapsed = time.time() - start
    pi_single = 4 * result / TOTAL_POINTS
    print(f"π ≈ {pi_single:.6f}, Time: {elapsed:.2f}s\n")
    
    # Multi core
    print("Multi core:")
    pi_multi, elapsed_multi = estimate_pi_parallel(TOTAL_POINTS)
    print(f"π ≈ {pi_multi:.6f}, Time: {elapsed_multi:.2f}s")
    print(f"Speedup: {elapsed/elapsed_multi:.2f}x")

