import socket as sock
import threading
import pickle
import socket
import subprocess
import sys
import os
from Helper import Helper

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



# socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
# server_ip = sock.gethostname()
# client_ip = '172.17.0.2'
# port = 5000
# ADDR = (server_ip, port)
# FORMAT = 'utf-8'
# HEADER = 64
# DISCONNECTED_MESSAGE = "!DISCONNECTED"

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
#     with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
#         s.bind(ADDR)
#         s.listen()
#         print(f'Server started and listening on {server_ip}:{port}...')

#         while True:
#             conn, addr = s.accept()
#             print(f'Connected with {addr}')
#             threading.Thread(target=receive, args=(conn,addr)).start()


# threading.Thread(target=start_server).start()



# server_ip = '0.0.0.0'  # Listen on all available interfaces
# port = 5000
# ADDR = (server_ip, port)
# FORMAT = 'utf-8'
# HEADER = 64
# DISCONNECTED_MESSAGE = "!DISCONNECTED"

# # Shared data between threads (you might want to use locks for better thread safety)
# transaction_pool = Helper().get_pool()
# block_data = b""
# database_data = b""

# peer_addresses = (os.environ.get("PEER_HOST", "127.0.0.1"), int(os.environ.get("PEER_PORT", 5000)))


# def receive(conn, addr):
#     global transaction_pool, block_data, database_data
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
#                 # Lock around shared resource
#                 with threading.Lock():
#                     transaction_pool = transactions
#                 print(f"Transaction pool received from {addr}.")
#             elif data_dict.get('Type') == 'block':
#                 # Load the received block data as a Python object
#                 blocks = pickle.loads(data_dict.get('Data'))
#                 # Lock around shared resource
#                 with threading.Lock():
#                     block_data = data_dict.get('Data')
#                 print(f"Block data received from {addr}.")
#             elif data_dict.get('Type') == 'database':
#                 # Lock around shared resource
#                 with threading.Lock():
#                     database_data = data_dict.get('Data')
#                 print(f"Database data received from {addr}.")
#             else:
#                 print(f"Unknown data type received from {addr}.")
#         else:
#             print(f"Unknown data received from {addr}.")
#     except pickle.UnpicklingError as e:
#         print(f"Error unpickling data from {addr}: {e}")
#     conn.close()

# def send_data(data_type, peer_address):
#     global transaction_pool, block_data, database_data
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         try:
#             s.connect(peer_address)
#             if data_type == 'pool':
#                 with open('data/pool.dat', 'rb') as f:
#                     data = f.read()
#             elif data_type == 'block':
#                 data = block_data
#             elif data_type == 'database':
#                 data = database_data
#             else:
#                 print("Unknown data type.")
#                 return

#             # Lock around shared resource
#             with threading.Lock():
#                 chunk_size = 65535
#                 for i in range(0, len(data), chunk_size):
#                     chunk = data[i:i+chunk_size]
#                     s.sendall(pickle.dumps({'Type': data_type, 'Data': chunk}))
#                 print(f"{data_type.capitalize()} sent to {peer_address}.")
#         except Exception as e:
#             print(f"Error sending {data_type} to {peer_address}: {e}")

# def start_server():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind(ADDR)
#         s.listen()
#         print(f'Server started and listening on {server_ip}:{port}...')

#         while True:
#             conn, addr = s.accept()
#             print(f'Connected with {addr}')
#             threading.Thread(target=receive, args=(conn, addr)).start()

# # Example usage:

# # Assuming you have multiple peers with known addresses

# # Start the server in a separate thread
# threading.Thread(target=start_server).start()

# # In this example, each node sends its transaction pool, block data, and database data to other peers.
# # You might want to customize this logic based on your specific requirements.

# while True:
#     user_input = input("Enter 'pool', 'block', 'database' to send data (q to quit): ")
#     if user_input.lower() == 'q':
#         break
#     elif user_input.lower() in ['pool', 'block', 'database']:
#         for peer_address in [peer_addresses]:
#             threading.Thread(target=send_data, args=(user_input.lower(), peer_address)).start()
#     else:
#         print("Invalid input.")
# Set up UDP socket for broadcasting





# udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# # Set up UDP socket for receiving broadcasts
# udp_receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp_receive_socket.bind(("0.0.0.0", 5000))

# # Function to broadcast data
# def broadcast_data(data):
#     udp_socket.sendto(pickle.dumps(data), ("255.255.255.255", 5000))

# # Function to receive broadcast messages
# def receive_broadcast():
#     while True:
#         try:
#             data, _ = udp_receive_socket.recvfrom(1024)
#             while True:
#                 try:
#                     # Attempt to load the pickle data
#                     received_data = pickle.loads(data)
#                     break  # Break the inner loop if successful
#                 except pickle.UnpicklingError:
#                     # If unpickling fails, receive additional data
#                     more_data, _ = udp_receive_socket.recvfrom(1024)
#                     data += more_data

#             if received_data.get('Type') == 'pool':
#                 pool_data = received_data.get('Data')
#                 print(f"Received broadcast with pool data: {pool_data}")
#                 with open('data/pool.dat', 'wb') as f:
#                     f.write(pool_data)
#             else:
#                 print(f"Ignoring broadcast with unknown or non-pool data: {received_data}")

#         except socket.timeout:
#             # Handle timeout (no data received within the specified timeout)
#             print("No data received within the timeout period.")
    

# # Function to read data from the 'pool.dat' file and broadcast it
# def send_pool_data():
#     with open('data/pool.dat', 'rb') as f:
#         data = f.read()
#         chunk_size = 65535
#         for i in range(0, len(data), chunk_size):
#             chunk = data[i:i+chunk_size]
#             broadcast_data({'Type': 'pool', 'Data': chunk})
#         print("Transaction pool sent.")

# def start_server():
#     # Start the receive thread
#     receive_thread = threading.Thread(target=receive_broadcast)
#     receive_thread.start()



# Function to broadcast data
def broadcast_data(data):
    # Set up UDP socket for broadcasting
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Define broadcast address and port
    broadcast_address = ("255.255.255.255", 5000)

    # Send a broadcast message
    udp_socket.sendto(data, broadcast_address)

    # Close the socket
    udp_socket.close()

    print("Sending data...")


def send_pool_data():
        path_pool = 'data/pool.dat'
        with open(path_pool, 'rb') as f:
            data = f.read()
            chunk_size = 65535
            for i in range(0, len(data), chunk_size):
                data_chunk = data[i:i+chunk_size]
                broadcast_data(pickle.dumps({'Type': 'pool', 'Data': data_chunk}))
            print("Pool broadcasted.")


# Function to receive broadcast messages
def receive_broadcast():
    print(f"Listening for broadcasts...")

    # Set up UDP socket for receiving broadcasts
    udp_receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_receive_socket.bind(("0.0.0.0", 5000))
    udp_receive_socket.settimeout(5)  # Set a timeout of 5 seconds
    udp_receive_socket.setblocking(0)  # Set non-blocking mode

    while True:
        try:
            data, _ = udp_receive_socket.recvfrom(65536)  # Specify a larger buffer size, e.g., 65536 bytes
            more_data = b""

            while data:
                try:
                    # Attempt to load the pickle data
                    decoded_data = data.decode('utf-8')
                    received_data = pickle.loads(decoded_data)
                    break  # Break the inner loop if successful
                except pickle.UnpicklingError:
                    # If unpickling fails, receive additional data
                    data, _ = udp_receive_socket.recvfrom(65536)  # Specify the same buffer size
                    more_data += data
            # while True:
            #     try:
            #         # Attempt to load the pickle data
            #         received_data = pickle.loads(data)
            #         break  # Break the inner loop if successful
            #     except pickle.UnpicklingError:
            #         # If unpickling fails, receive additional data
            #         more_data, _ = udp_receive_socket.recvfrom(1024)
            #         data += more_data

            if isinstance(received_data, dict) and received_data.get('Type') == 'pool':
                pool_data = received_data.get('Data')
            
                print(f"Received broadcast with pool data.")
                with open('data/pool.dat', 'wb') as f:
                    pickle.dump(pool_data.decode(), f)
                    print("Transactions added to pool.")
            else:
                print(f"Ignoring broadcast with unknown or non-pool data: {received_data}")

        except BlockingIOError:
            # Handle the case where no data is available yet
            continue

# Create threads for broadcasting and receiving
receive_thread = threading.Thread(target=receive_broadcast)

# Start the threads
receive_thread.start()



# # Function to broadcast data
# def broadcast_data():
#     # Set up UDP socket for broadcasting
#     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#     # Define broadcast address and port
#     broadcast_address = ("255.255.255.255", 5000)

#     # Send a broadcast message
#     message = "Hello, Blockchain Nodes!"
#     udp_socket.sendto(message.encode(), broadcast_address)

#     # Close the socket
#     udp_socket.close()

# # Function to receive broadcast messages
# def receive_broadcast():
#     # Set up UDP socket for receiving broadcasts
#     udp_receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_receive_socket.bind(("0.0.0.0", 5000))

#     # Receive broadcast messages
#     while True:
#         data, _ = udp_receive_socket.recvfrom(1024)
#         print(f"Received broadcast: {data.decode()}")

#     # Close the socket (this will not be reached in this example)
#     udp_receive_socket.close()

# # Create threads for broadcasting and receiving
# broadcast_thread = threading.Thread(target=broadcast_data)
# receive_thread = threading.Thread(target=receive_broadcast)

# # Start the threads
# broadcast_thread.start()
# receive_thread.start()

# # Wait for threads to finish (this won't happen in this example)
# broadcast_thread.join()
# receive_thread.join()