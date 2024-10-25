from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient

# Function to handle the OSC message
def handle_wek_outputs(address, *args):
    for i, value in enumerate(args):
        if i == 0:  # Skip the first argument which is the address
            continue
        new_address = f"/wek/outputs-{i}"
        message = f"{new_address} fffff {value:.6f}"
        print(message)

# Setup the OSC dispatcher and server
def setup_server(ip="127.0.0.1", port=9001):
    disp = dispatcher.Dispatcher()
    disp.map("/wek/outputs", handle_wek_outputs)
    
    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    print(f"Serving on {server.server_address}")
    server.serve_forever()  # Start the server

if __name__ == "__main__":
    setup_server()
