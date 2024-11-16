import os
import platform

def run():
    system = platform.system()
    if system == "Windows":
        os.system('cls')
    else:
        os.system('clear')

description = "Clear the console screen"
