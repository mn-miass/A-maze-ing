import time

def display_msg(msg, sec=0.001):
    for letter in msg:
        print(letter, end="", flush=True) 
        time.sleep(sec)
    print()