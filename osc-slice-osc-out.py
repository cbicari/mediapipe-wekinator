from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient

# Function to handle the OSC message and send to port 9002
def handle_wek_outputs(address, *args):
    client = SimpleUDPClient("127.0.0.1", 9002)  # Client to send messages to port 9002
    for i, value in enumerate(args):
        if i == 0:  # Skip the first argument which is the address
            continue
        new_address = f"/wek/outputs-{i}"
        client.send_message(new_address, [value])  # Send formatted OSC message

# Setup the OSC dispatcher and server
def setup_server(ip="127.0.0.1", port=9001):
    disp = dispatcher.Dispatcher()
    disp.map("/wek/outputs", handle_wek_outputs)
    
    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    print(f"Serving on {server.server_address}")
    server.serve_forever()  # Start the server

if __name__ == "__main__":
    setup_server()
