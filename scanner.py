
#Basically threading.
from concurrent.futures import ThreadPoolExecutor
#Gathering the def function from the utils file so the main code doesnt get too messy
from utils import get_service
#Library for working with sockets. Using it for making TCP connection
import socket
#Library for working with time. Using it to calc how much it takes for the app to run.
import time
import re


WORKERS = 100



def generate_port_chunks(port_range):
    #Get the min and max ports from the port range
    port_ranges = port_range.split('-')
    port_chunks = []
    #Divide the port ranges into chunks
    chunk_size = int((int(port_ranges[1])- int(port_ranges[0])) / WORKERS)
    #Create a nested list of port chunks to be handled by each worker
    for i in range(WORKERS):
        start = int(port_ranges[0]) + (chunk_size * i)
        end = start + chunk_size
        port_chunks.append([start, end])
    return port_chunks

def scan_ip_address(ip_address,port_chunk):
    print(f"[~] Scanning {ip_address} from {port_chunk[0]} to {port_chunk[1]}.")
    #Loop through min and max port chunks
    for port in range(int(port_chunk[0]), int(port_chunk[1])):
        #Attempt a TCP IPv4 connection to the provided port and ip address
        try:
            scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scan_socket.settimeout(2)
            scan_socket.connect((ip_address, port))
            service = get_service(port)
            print(f"[!][OPEN] Port {port} {service}")
            #If the port is closed and exception will be thrown, capture it here
        except:
            None

def main():

    ip_add_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    while True:
        ip_add_entered = input("\nPlease enter the ip address that you want to scan: ")
        if ip_add_pattern.search(ip_add_entered):
            print(f"{ip_add_entered} is a valid ip address")
        break

    port_range = '0-65535'

    #Divide port range into chunks
    port_chunks = generate_port_chunks(port_range)

    #Start the timer
    start_timer = time.time()
    #Submit task to be excecuted by the thread using a map
    with ThreadPoolExecutor(max_workers=WORKERS) as excecutor:
        excecutor.map(scan_ip_address, [ip_add_entered] * len(port_chunks), port_chunks)
    #Finish the timer
    end_time = time.time()

    print(f"Scanned {port_range[1]} ports in {end_time - start_timer} seconds. ")

if __name__ == '__main__':
    main()
