import threading
import time


import config
import tornado_server

def main():
    print("Welcome to phoneboard!")
    config.config()
    time.sleep(.1)

    web_t = threading.Thread(target=tornado_server.twisted)

    web_t.start()


if __name__ == '__main__':
    main()
