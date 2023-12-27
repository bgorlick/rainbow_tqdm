import threading
import time
import rainbow_tqdm
from tqdm import tqdm

def progress_bar_thread(bar_id, total_iterations=400, bar_width=100, frequency=1.55):
    with tqdm(total=total_iterations, ncols=bar_width, desc=f'Bar {bar_id}') as pbar:
        for _ in range(total_iterations):
            pbar.update(1)
            #time.sleep(frequency)  # Optional - Sleep duration controlled by frequency
            time.sleep(0.03)
def main():
    threads = []
    num_bars = 40
    frequencies = [0.05, 0.1, 0.15, 0.2, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.5, 5.5, 0.4, 0.45, 1.5, 2.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2.5, 1.5, 1.6, 1.7]

    for i in range(num_bars):
        thread = threading.Thread(target=progress_bar_thread, args=(i+1, 300, 120, frequencies[i]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All progress bars completed.")

if __name__ == "__main__":
    main()
