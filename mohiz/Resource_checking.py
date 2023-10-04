import time
import subprocess
from memory_profiler import profile

@profile
def run_script(script_name):
    start_time = time.time()
    subprocess.call(["python", script_name])
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    script1_time = run_script("client_input.py")
    script2_time = run_script("Getting_images.py")

    print(f"Script 1 execution time: {script1_time} seconds")
    print(f"Script 2 execution time: {script2_time} seconds")

    if script1_time < script2_time:
        print("Script 1 is faster.")
    elif script1_time > script2_time:
        print("Script 2 is faster.")
    else:
        print("Both scripts have the same execution time.")
