import socket
import pickle

HOST = '127.0.0.1'
PORT = 29222
COUNT = '5'

def main():
    print("Requesting colors...")
    mysoc = socket.socket()
    mysoc.connect((HOST, PORT))

    count = COUNT
    mysoc.send(count.encode())
    data = mysoc.recv(1024)
    colors = pickle.loads(data)
    print("Got colors")
    print(colors)

    return colors

if __name__ == "__main__":
    main()