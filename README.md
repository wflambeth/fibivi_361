# fibivi

# The Colors microservice

This is a microservice dedicated to serving six-digit hex codes, formatted for use as CSS colors. It takes a single integer, in string format, and returns
an array of hex codes, of length (integer). 

## Format

Calls to the microservice must be made via OS socket connection. The string containing the integer must be encoded using standard UTF-8 binary encoding. 

Responses will consist of an array of strings, binary-encoded using the Python standard library's pickle module. They must be decoded using the same module. 

## UML Diagram

![Screenshot_20230209_194949](https://user-images.githubusercontent.com/13874701/217996199-fb6e6c73-8cb4-4813-8dc2-2312e8b24a19.png)

## Example: Request
    mysoc = socket.socket()
    mysoc.connect((HOST, PORT))
    count = '2'
    mysoc.send(count.encode())


## Example: Response
    data = mysoc.recv(1024)
    colors = pickle.loads(data)
    print(colors) # ['#05FF77', '0810FD']
