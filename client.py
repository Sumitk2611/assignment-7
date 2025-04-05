import socket
import sys
import argparse
import os

def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s
    except socket.error as e:
        print(f"Could not create socket due to {e}")
        exit(0)


def send(connection, data):
    try:
        connection.sendall(str.encode(data))
    except socket.error as e:
        print(f"Unable to send data {e}")
        connection.close()

def recv(connection):
    try:
        data = connection.recv(1024)
        return data
    except socket.error as e:
        print(e)
        exit(0)

def connect(sk,ip_addr, port):
    try:
        sk.connect((ip_addr,port))
    except socket.error as e:
        print(f"Unable to connect. Error: {e}")
        exit(0)


def argument_parser():
    port = 5000
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cmd",required=True,help="Command to run on the server")
    parser.add_argument("-p", "--port", type = int , help="Port number the server is running on")
    parser.add_argument("-ip_addr", "--ip_address", required=True, help="IP address of the server")
    args = parser.parse_args()
    if(args.cmd):
        cmd=args.cmd
    else:
        print("No Command provided")
        exit(0)
    
    if(args.port):
        port = args.port
    else:
        print(f"No port provided. Using port: {port}")

    if(args.ip_address):
        ip_addr = args.ip_address
    else:
        print("No IP address provied")
        exit(0)

    return (port,cmd,ip_addr)

def main():
    s = create_socket()
    port,cmd, ip_addr = argument_parser()
    print(f"Connnecting to {ip_addr} on port {port}")
    connect(s,ip_addr,port)
    try:
        send(s, cmd)
        data = recv(s).decode()
        print(data)

    finally:
        print("closing socket")
        s.close()

main()