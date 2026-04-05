import time
import fcntl

with open("config.txt", "r") as file:
    fcntl.flock(file, fcntl.LOCK_EX)  # shared lock → allows other readers, blocks writers
    try:
        time.sleep(1)
        print(file.readline())
        time.sleep(10)
        print(file.read())
    finally:
        fcntl.flock(file, fcntl.LOCK_UN)  # always unlock even if exception occurs