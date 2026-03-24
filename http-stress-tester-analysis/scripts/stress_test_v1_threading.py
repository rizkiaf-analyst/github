import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURATION ---
TARGET_URL = "http://192.168.8.118"
TOTAL_REQUESTS = 20000
MAX_THREADS = 500  
# -------------------

stats = {
    "success": 0,
    "fail": 0
}
lock = threading.Lock()

def send_request():
    try:
        # Timeout set to 5 seconds
        response = requests.get(TARGET_URL, timeout=5)
        
        with lock:
            if response.status_code == 200:
                stats["success"] += 1
            else:
                stats["fail"] += 1
    except Exception:
        with lock:
            stats["fail"] += 1

def run_test():
    print(f"[*] Start {TOTAL_REQUESTS} request to {TARGET_URL}")
    print(f"[*] Using {MAX_THREADS} Thread...")
    
    start_time = time.time()

    # Use ThreadPool for the efficient thread management
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for _ in range(TOTAL_REQUESTS):
            executor.submit(send_request)

    end_time = time.time()
    duration = end_time - start_time

    # --- SUMMARY ---
    print("\n" + "="*35)
    print("         SUMMARY REPORT")
    print("="*35)
    print(f"Total Times    : {duration:.2f} detik")
    print(f"Thread Used    : {MAX_THREADS}")
    print(f"Success (200) : {stats['sukses']}")
    print(f"Fail/Error    : {stats['gagal']}")
    
    rps = stats['success'] / duration if duration > 0 else 0
    print(f"RPS (Success)  : {rps:.2f} req/sec")
    print("="*35)

if __name__ == "__main__":
    run_test()