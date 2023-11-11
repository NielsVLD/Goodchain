import socket as sock
import threading
import pickle
import socket
import subprocess
import sys

# socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
# server_ip = '192.168.2.11'
# client_ip = '192.168.2.7'
# port = 5068
# ADDR = (server_ip, port)
# FORMAT = 'utf-8'
# HEADER = 64
# DISCONNECTED_MESSAGE = "!DISCONNECTED"

# def find_available_port(start_port=5000, max_attempts=10):
#     for _ in range(max_attempts):
#         try:
#             with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
#                 s.bind(("127.0.0.1", start_port))
#             return start_port
#         except OSError:
#             start_port += 1
#     raise Exception("Unable to find an available port.")

# def receive(conn, addr):
#     buffer = b""
#     while True:
#         data = conn.recv(65535)
#         if not data:
#             break
#         buffer += data
#     try:
#         data_dict = pickle.loads(buffer)
#         if isinstance(data_dict, dict):
#             if data_dict.get('Type') == 'pool':
#                 transactions = data_dict.get('Data')
#                 with open('data/pool.dat', 'wb') as f:
#                     f.write(transactions)
#                 print("Checking if transactions are valid...")
#                 # helper.fixTampering()
#                 # helper.check_transaction_validity()
#                 print("Transaction pool received and written to disk.")
#             elif data_dict.get('Type') == 'block':
#                 # Load the received block data as a Python object
#                 blocks = pickle.loads(data_dict.get('Data'))
#                 # Save the validated blocks to disk
#                 with open('data/block.dat', 'wb') as f:
#                     f.write(data_dict.get('Data'))
#                 print("Block file received and validated, and written to disk.")
#                 # helper.fixTampering()
#                 # helper.check_block_validity()
#             elif data_dict.get('Type') == 'database':
#                 database_data = data_dict.get('Data')
#                 with open('database_actions/goodchain.db', 'wb') as f:
#                     f.write(database_data)
#                 print("Database file received and overwritten.")
#                 # helper.fixTampering()
#             else:
#                 print("Unknown data type received.")
#         else:
#             print("Unknown data received.")
#     except pickle.UnpicklingError as e:
#         print(f"Error unpickling data: {e}")
#     conn.close()


# def send_data(data_type):
#     with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
#         s.connect((client_ip, port))
#         if data_type == 'pool':
#             with open('data/pool.dat', 'rb') as f:
#                 data = f.read()
#                 chunk_size = 65535
#                 for i in range(0, len(data), chunk_size):
#                     chunk = data[i:i+chunk_size]
#                     s.sendall(pickle.dumps({'Type': 'pool', 'Data': chunk}))
#                 print("Transaction pool sent.")
#         elif data_type == 'block':
#             with open('data/block.dat', 'rb') as f:
#                 data = f.read()
#                 chunk_size = 65535
#                 for i in range(0, len(data), chunk_size):
#                     chunk = data[i:i+chunk_size]
#                     s.sendall(pickle.dumps({'Type': 'block', 'Data': chunk}))
#                 print("Block file sent.")
#         elif data_type == 'database':
#             with open('database_actions/goodchain.db', 'rb') as f:
#                 data = f.read()
#                 s.sendall(pickle.dumps({'Type': 'database', 'Data': data}))
#                 print("Database file sent.")
#         s.close()


# def start_server():
#     port = find_available_port()
#     ADDR = (server_ip, port)

#     with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
#         s.bind(ADDR)
#         s.listen()
#         print(f'Server started and listening on {server_ip}:{port}...')

#         while True:
#             conn, addr = s.accept()
#             print(f'Connected with {addr}')
#             threading.Thread(target=receive, args=(conn,addr)).start()

# threading.Thread(target=start_server).start()



socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
server_ip = '192.168.2.11'
client_ip = '192.168.2.7'
port = 5000
ADDR = (server_ip, port)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECTED_MESSAGE = "!DISCONNECTED"

def receive(conn, addr):
    buffer = b""
    while True:
        data = conn.recv(65535)
        if not data:
            break
        buffer += data
    try:
        data_dict = pickle.loads(buffer)
        if isinstance(data_dict, dict):
            if data_dict.get('Type') == 'pool':
                transactions = data_dict.get('Data')
                with open('data/pool.dat', 'wb') as f:
                    f.write(transactions)
                print("Checking if transactions are valid...")
                helper.fixTampering()
                helper.check_transaction_validity()
                print("Transaction pool received and written to disk.")
            elif data_dict.get('Type') == 'block':
                # Load the received block data as a Python object
                blocks = pickle.loads(data_dict.get('Data'))
                # Save the validated blocks to disk
                with open('data/block.dat', 'wb') as f:
                    f.write(data_dict.get('Data'))
                print("Block file received and validated, and written to disk.")
                helper.fixTampering()
                helper.check_block_validity()
            elif data_dict.get('Type') == 'database':
                database_data = data_dict.get('Data')
                with open('database_actions/goodchain.db', 'wb') as f:
                    f.write(database_data)
                print("Database file received and overwritten.")
                helper.fixTampering()
            else:
                print("Unknown data type received.")
        else:
            print("Unknown data received.")
    except pickle.UnpicklingError as e:
        print(f"Error unpickling data: {e}")
    conn.close()


def send_data(data_type):
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.connect((client_ip, port))
        if data_type == 'pool':
            with open('data/pool.dat', 'rb') as f:
                data = f.read()
                chunk_size = 65535
                for i in range(0, len(data), chunk_size):
                    chunk = data[i:i+chunk_size]
                    s.sendall(pickle.dumps({'Type': 'pool', 'Data': chunk}))
                print("Transaction pool sent.")
        elif data_type == 'block':
            with open('data/block.dat', 'rb') as f:
                data = f.read()
                chunk_size = 65535
                for i in range(0, len(data), chunk_size):
                    chunk = data[i:i+chunk_size]
                    s.sendall(pickle.dumps({'Type': 'block', 'Data': chunk}))
                print("Block file sent.")
        elif data_type == 'database':
            with open('database_actions/goodchain.db', 'rb') as f:
                data = f.read()
                s.sendall(pickle.dumps({'Type': 'database', 'Data': data}))
                print("Database file sent.")
        s.close()


def start_server():
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.bind(ADDR)
        s.listen()
        print(f'Server started and listening on {server_ip}:{port}...')

        while True:
            conn, addr = s.accept()
            print(f'Connected with {addr}')
            threading.Thread(target=receive, args=(conn,addr)).start()


threading.Thread(target=start_server).start()

