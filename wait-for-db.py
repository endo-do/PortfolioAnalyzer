import socket, sys,  time

host = sys.argv[1]
port = int(sys.argv[2])

while True:
    try:
        s = socket.create_connection((host, port), 2)
        s.close()
        print(f"Connected to {host}:{port}")
        break
    except Exception as e:
        print(f"Waiting for {host}:{port}... {e}")
        time.sleep(1)