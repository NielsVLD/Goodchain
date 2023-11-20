import socket as sock
import threading
import pickle
import socket

message = ""

def broadcast_data(data):

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


    broadcast_address = ("255.255.255.255", 5000)

  
    udp_socket.sendto(data, broadcast_address)


    udp_socket.close()

    print("Sending data...")


def send_pool_data():
        path_pool = 'data/pool.dat'
        with open(path_pool, 'rb') as f:
            data = f.read()
            broadcast_data(pickle.dumps({'Type': 'pool', 'Data': data}))
            print("Pool broadcasted.")

def send_blockchain_data():
        path_chain = 'data/blockchain.dat'
        with open(path_chain, 'rb') as f:
            data = f.read()
            broadcast_data(pickle.dumps({'Type': 'chain', 'Data': data}))
            print("Blockchain broadcasted.")

def send_user_database():
        path_database = 'data/userDatabase.db'
        with open(path_database, 'rb') as f:
            data = f.read()
            broadcast_data(pickle.dumps({'Type': 'database', 'Data': data}))
            print("Database broadcasted.")

def send_transaction_history():
        path_history = 'data/transactionHistory.dat'
        with open(path_history, 'rb') as f:
            data = f.read()
            broadcast_data(pickle.dumps({'Type': 'history', 'Data': data}))
            print("Transaction History broadcasted.")

def send_blockchain_tamper_data():
        path_chain = 'data/blockchainHash.txt'
        with open(path_chain, 'rb') as f:
            data = f.read()
            broadcast_data(pickle.dumps({'Type': 'chainTamper', 'Data': data}))
            print("Blockchain broadcasted.")


def receive_broadcast():
    global message
    print(f"Listening for broadcasts...")

    # Set up UDP socket for receiving broadcasts
    udp_receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_receive_socket.bind(("0.0.0.0", 5000))
    udp_receive_socket.settimeout(5)  
    udp_receive_socket.setblocking(0)  

    while True:
        try:
            data,addr = udp_receive_socket.recvfrom(65536) 
            more_data = b""

            if addr[0] == socket.gethostbyname(socket.gethostname()):
                continue
            else:
                while data:
                    try:
                        received_data = pickle.loads(data)
                        break
                    except pickle.UnpicklingError:
                        data, _ = udp_receive_socket.recvfrom(65536)  
                        more_data += data
            

                if isinstance(received_data, dict) and received_data.get('Type') == 'pool':
                    pool_data = received_data.get('Data')

                    message = "\nReceived broadcast with pool data.\n"
                    # print(f"\nReceived broadcast with pool data.\n")
                    with open('data/pool.dat', 'wb+') as f:
                        f.write(pool_data)
                
                elif isinstance(received_data, dict) and received_data.get('Type') == 'chain':
                    chain_data = received_data.get('Data')
                    
                    message = "\nReceived broadcast with chain data.\n"
                    # print(f"\nReceived broadcast with chain data.")
                    with open('data/blockchain.dat', 'wb+') as f:
                        f.write(chain_data)
                
                elif isinstance(received_data, dict) and received_data.get('Type') == 'database':
                    database_data = received_data.get('Data')

                    message = "\nReceived broadcast with database data.\n"
                    # print(f"\nReceived broadcast with database data.")
                    with open('data/userDatabase.db', 'wb+') as f:
                        f.write(database_data)

                elif isinstance(received_data, dict) and received_data.get('Type') == 'history':
                    history_data = received_data.get('Data')

                    message = "\nReceived broadcast with history data.\n"
                    # print(f"\nReceived broadcast with history data.")
                    with open('data/transactionHistory.dat', 'wb+') as f:
                        f.write(history_data)
                
                elif isinstance(received_data, dict) and received_data.get('Type') == 'chainTamper':
                    chain_data = received_data.get('Data')
                    
                    message = "\nReceived broadcast with chain data.\n"
                    # print(f"\nReceived broadcast with chain data.")
                    with open('data/blockchainHash.txt', 'wb+') as f:
                        f.write(chain_data)

                else:
                    print(f"Ignoring broadcast with unknown or non-pool data: {received_data}")

        except BlockingIOError:
            continue


receive_thread = threading.Thread(target=receive_broadcast)


receive_thread.start()