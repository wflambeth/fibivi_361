import socket
import random
import pickle

HOST = '127.0.0.1'
PORT = 29222

def make_colors(count):
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    output = []

    for i in range(count):
        val = "#"
        for j in range(6):
            val += chars[random.randint(0,15)]
        output.append(val)

    return output

def main():
    mysoc = socket.socket()
    mysoc.bind((HOST, PORT))
    mysoc.listen(1)
    print("Listening...")

    while True:
        connec, addr = mysoc.accept()

        print("Connection from: " + str(addr))
        data = connec.recv(1024).decode()
        count = int(data)
        print("Got count: " + data)
        colors = make_colors(count)
        datastream = pickle.dumps(colors)
        print("Sending colors...")
        connec.send(datastream)
        
if __name__ == '__main__':
    main()
