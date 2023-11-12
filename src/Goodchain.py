from BlockChain import CBlock
import socket
import threading
import json
from Signature import generate_keys, sign, verify
from Transaction import Tx
from TxBlock import TxBlock
from userInterface import *
from pathlib import Path
import pathlib
import pickle
from P2P import server

if __name__ == "__main__":
    # start server
    
    # Make files
    pathlib.Path('data').mkdir(parents=True, exist_ok=True)
    pathlib.Path('data/blockchain.dat').touch()
    pathlib.Path('data/pool.dat').touch()
    pathlib.Path('data/transactionHistory.dat').touch()
    pathlib.Path('data/userDatabase.db').touch()
    pathlib.Path('data/blockchainHash.txt').touch()
    pathlib.Path('data/poolHash.txt').touch()
    pathlib.Path('data/transactionHistory.txt').touch()
    

    with open("data/blockchainHash.txt", "r") as f:
        if f.read() == '':
            Helper().create_hash('data/blockchain.dat')

    if not Helper().check_hash('data/blockchain.dat'):
            exit("Tampering with the blockchain detected!")
            
    database = Database("userDatabase.db")
    database.check_migrations()
    database.close()

    UserInterface().main_screen()

# class P2PNode:
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port
#         self.peers = set()

#     def start(self):
#         # Start a thread for UDP broadcast
#         threading.Thread(target=self.listen_for_peers, daemon=True).start()

#         pathlib.Path('data').mkdir(parents=True, exist_ok=True)
#         pathlib.Path('data/blockchain.dat').touch()
#         pathlib.Path('data/pool.dat').touch()
#         pathlib.Path('data/transactionHistory.dat').touch()
#         pathlib.Path('data/userDatabase.db').touch()
#         pathlib.Path('data/blockchainHash.txt').touch()
#         pathlib.Path('data/poolHash.txt').touch()
#         pathlib.Path('data/transactionHistory.txt').touch()
        

#         with open("data/blockchainHash.txt", "r") as f:
#             if f.read() == '':
#                 Helper().create_hash('data/blockchain.dat')

#         if not Helper().check_hash('data/blockchain.dat'):
#                 exit("Tampering with the blockchain detected!")
                
#         database = Database("userDatabase.db")
#         database.check_migrations()
#         database.close()

#         UserInterface().main_screen()

#         print(f"Node started on {self.host}:{self.port}")

#     def listen_for_peers(self):
#         # Create a UDP socket for broadcasting
#         udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#         udp_socket.bind(('0.0.0.0', 5000))  # Use a specific port for broadcasting

#         while True:
#             data, addr = udp_socket.recvfrom(1024)
#             message = json.loads(data.decode('utf-8'))

#             if message.get('type') == 'peer_discovery':
#                 peer_host = message.get('host')
#                 peer_port = message.get('port')

#                 # Add the discovered peer to the list
#                 self.peers.add((peer_host, peer_port))
#                 print(f"Discovered peer: {peer_host}:{peer_port}, Total peers: {len(self.peers)}")

#     def broadcast_peer_discovery(self):
#         # Create a UDP socket for broadcasting
#         udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#         while True:
#             # Broadcast a message for peer discovery
#             message = {'type': 'peer_discovery', 'host': self.host, 'port': self.port}
#             udp_socket.sendto(json.dumps(message).encode('utf-8'), ('<broadcast>', 5000))

#             # Adjust the interval based on your requirements
#             threading.Event().wait(5)

# if __name__ == '__main__':
#     node = P2PNode('127.0.0.1', 5001)
    
#     # Start the main application and broadcasting thread
#     threading.Thread(target=node.start, daemon=True).start()
#     threading.Thread(target=node.broadcast_peer_discovery, daemon=True).start()

#     # Keep the main thread running
#     threading.Event().wait()


# class BlockchainNode:
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port
#         self.peers = set()

#     def start(self):
#         # Start a thread for listening to peers
#         threading.Thread(target=self.listen_to_peers, daemon=True).start()

#         # Start the main application
#         # self.start_application()

#     def listen_to_peers(self):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#             server_socket.bind((self.host, self.port))
#             server_socket.listen()
#             print(f'Server started and listening on {self.host}:{self.port}...')

#             while True:
#                 try:
#                     client_socket, addr = server_socket.accept()
#                     print(f'Connected with {addr}')
#                     threading.Thread(target=self.handle_peer_connection, args=(client_socket,addr)).start()
#                 except Exception as e:
#                     print(f"Error accepting connection: {e}")

#     def handle_peer_connection(self, client_socket):
#         try:
#             data = client_socket.recv(1024)
#             if data:
#                 message = json.loads(data.decode('utf-8'))
#                 print(f"Received message from {message['host']}:{message['port']}: {message['message']}")
#         except Exception as e:
#             print(f"Error handling peer connection: {e}")
#         finally:
#             client_socket.close()

#     def start_application(self):
#         while True:
#             # Simulate sending a message
#             message = input("Enter a message to send: ")
#             self.broadcast_message(message)
        
#         # pathlib.Path('data').mkdir(parents=True, exist_ok=True)
#         # pathlib.Path('data/blockchain.dat').touch()
#         # pathlib.Path('data/pool.dat').touch()
#         # pathlib.Path('data/transactionHistory.dat').touch()
#         # pathlib.Path('data/userDatabase.db').touch()
#         # pathlib.Path('data/blockchainHash.txt').touch()
#         # pathlib.Path('data/poolHash.txt').touch()
#         # pathlib.Path('data/transactionHistory.txt').touch()
        

#         # with open("data/blockchainHash.txt", "r") as f:
#         #     if f.read() == '':
#         #         Helper().create_hash('data/blockchain.dat')

#         # if not Helper().check_hash('data/blockchain.dat'):
#         #         exit("Tampering with the blockchain detected!")
                
#         # database = Database("userDatabase.db")
#         # database.check_migrations()
#         # database.close()

#         # UserInterface().main_screen()

#     def broadcast_message(self, message):
#         for peer in self.peers:
#             try:
#                 with socket.create_connection(peer) as peer_socket:
#                     peer_socket.sendall(json.dumps({'type': 'message', 'message': message}).encode('utf-8'))
#             except Exception as e:
#                 print(f"Error connecting to peer {peer}: {e}")

# if __name__ == '__main__':
#     container_name = socket.gethostname()

#     # Access environment variables
#     node = BlockchainNode(container_name, 5000)
#     threading.Thread(target=node.start, daemon=True).start()

#     # Keep the main thread running
#     threading.Event().wait()