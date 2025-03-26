import random
import time
def human_sleep(min_time=1, max_time=5):
    delay = random.uniform(min_time, max_time)
    print(f"Sleeping for {round(delay, 2)} seconds...")
    time.sleep(delay)
    return print("Human Sleep Activated")