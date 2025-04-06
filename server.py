import socket
import subprocess
import argparse

def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s
    except socket.error as e:
        print(f"Could not create socket due to {e}")
        exit(0)

def argument_parser():
    port = 5000
    ip = ''
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type = int , help="Port to listen on ")
    parser.add_argument("-ip", "--ip", type = str , help="IP address to listen on ")
    args = parser.parse_args()
    if(args.port):
        port = args.port
    else:
        print(f"No port provided. Using port: {port}")

    if args.ip:
        ip = args.ip
    else:
        print("No ip address provided listening for all connections")
    return (ip, port)

def accept(s):
    try: 
        connection, clientaddr = s.accept()
        return (connection, clientaddr)
    except socket.error as e:
        print(e)
        exit(0)


def recv(connection):
    try:
        data = connection.recv(1024)
        return data
    except socket.error as e:
        print(e)
        exit(0)


def send(connection, data):
    try:
        connection.sendall(str.encode(data))
    except socket.error as e:
        print(f"Unable to send data {e}")
        connection.close()

def bind(sk, addr):
    try:
        sk.bind(addr)
    except socket.error as e:
        print(e)
        exit(0)


def listen(sk):
    try:
        sk.listen(1)
    except socket.error as e:
        print(F"Socket unable to listen {e}")
        exit(0)

def runCommand(command):
    allowed_commands = ['ls']

    parts = command.strip().split()
    if not parts or parts[0] not in allowed_commands:
        return f"Error: Command '{parts[0] if parts else ''}' is not allowed."

    try:
        output = subprocess.getoutput(command)
        return output
    except Exception as e:
        return f"Error executing command: {str(e)}"

def main():
    addr = argument_parser()
    s = create_socket()
    bind(s,addr)
    listen(s)
    try:
        while(True):
            print(f"Waiting for connection on port: {addr}")
            connection, addr = accept(s)
            clientaddr, val = addr
            print(f"Connection from : {clientaddr}")

            
            data = recv(connection).decode()
            output = runCommand(data)
            send(connection, output)

                
    except KeyboardInterrupt as e:
        print("Shutting Server")
        s.close()
        exit(0)


main()