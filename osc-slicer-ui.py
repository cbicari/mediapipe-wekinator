import tkinter as tk
from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient
import threading

class OSCFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OSC Message Filter")
        
        # Setup OSC client to send messages to port 9002
        self.client = SimpleUDPClient("127.0.0.1", 9002)
        
        # Labels and checkboxes to toggle messages
        self.check_vars = []
        for i in range(1, 6):  # We have 5 messages to toggle
            var = tk.IntVar(value=1)  # Set default to 1 (checked)
            self.check_vars.append(var)
            checkbox = tk.Checkbutton(root, text=f"Send OSC message {i}", variable=var)
            checkbox.pack(anchor=tk.W)
        
        # Button to toggle all messages on/off
        self.toggle_all_button = tk.Button(root, text="Toggle All Off", command=self.toggle_all)
        self.toggle_all_button.pack()
        self.all_on = True

    # Function to toggle all messages on or off
    def toggle_all(self):
        self.all_on = not self.all_on
        new_value = 1 if self.all_on else 0
        for var in self.check_vars:
            var.set(new_value)
        self.toggle_all_button.config(text="Toggle All Off" if self.all_on else "Toggle All On")

    # Send only enabled OSC messages
    def handle_wek_outputs(self, address, *args):
        for i, value in enumerate(args):
            if i == 0:  # Skip the first argument (address)
                continue
            if self.check_vars[i - 1].get() == 1:  # Only send if checkbox is checked
                new_address = f"/wek/outputs-{i}"
                self.client.send_message(new_address, [value])

# OSC server setup function
def setup_server(app, ip="127.0.0.1", port=9001):
    disp = dispatcher.Dispatcher()
    disp.map("/wek/outputs", app.handle_wek_outputs)

    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    print(f"Serving on {server.server_address}")
    server.serve_forever()

# Run the GUI and OSC server in parallel
if __name__ == "__main__":
    root = tk.Tk()
    app = OSCFilterApp(root)

    # Run the OSC server in a separate thread to keep the GUI responsive
    osc_thread = threading.Thread(target=setup_server, args=(app,))
    osc_thread.daemon = True
    osc_thread.start()

    root.mainloop()
