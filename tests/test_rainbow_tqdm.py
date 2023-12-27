import sys
import os
import time
import rainbow_tqdm
from tqdm import tqdm

current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)

def test_custom_tqdm():
    total_iterations = 500
    bar_width = 100

    with tqdm(total=total_iterations, ncols=bar_width) as pbar:
        for i in range(total_iterations):
            pbar.update(1)
            time.sleep(0.05)  
    
    print("Test completed: Rainbow tqdm colored progress bar ran successfully.")

if __name__ == "__main__":
    test_custom_tqdm()

