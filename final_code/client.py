import socket
import final_code.price_evaluation as price_evaluation
from final_code.price_evaluation import our_products
from final_code.price_evaluation import transaction_evaluation

def client():
    host = '127.0.0.1'  
    port = 12345  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = s.recv(1024)
        data = eval(data.decode())  
        data=transaction_evaluation(our_products)  

        print(data)

if __name__ == "__main__":
    client()