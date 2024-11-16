import os
import platform

def run(_ = None):
    system = platform.system()
    if system == "Windows":
        os.system('cls')
    else:
        os.system('clear')
