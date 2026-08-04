import time

def interactive_sleep(seconds: int):
    """
    Support functionality to induce an artificial 'sleep' to the code in order to wait for resources to be available
    Args:
        seconds (int): number of seconds to sleep for
    """
    dots = ""
    for i in range(seconds):
        dots += "."
        print(dots, end="\r")
        time.sleep(1)