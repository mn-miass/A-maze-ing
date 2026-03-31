import time

def display_msg(msg, sec):
    for letter in msg:
        print(letter, end="", flush=True) 
        time.sleep(sec)
    print()