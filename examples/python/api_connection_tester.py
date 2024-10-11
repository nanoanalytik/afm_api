"""
Title: API Connection Tester to AFM Control by nano analytik GmbH

Compatible with API v1.0 and above

Description:
This script implements a GUI application using Tkinter that allows users to test WebSocket connections 
between a client and AFM Control API Server.

Users can input the server IP, port, and API key to connect to a WebSocket server. The application
attempts to connect and authenticate with the provided API key, displaying the connection and authentication
status. It supports connecting and disconnecting from the server.

Dependencies:
- Python 3.6 or higher
- asyncio
- websockets
- tkinter
- json

Usage:
1. Ensure that the 'websockets' library is installed:
   Install via pip if necessary: pip install websockets
2. Run the script: python api_connection_tester.py
3. In the GUI window:
- Enter the API Key, Server IP, and Server Port.
- Click 'Connect' to establish a connection and authenticate.
- Click 'Disconnect' to close the connection.

Author:
- nano analytik GmbH

License:
- MIT License

"""



import asyncio
import json
import tkinter as tk
import websockets


class ClientWindow:
    def __init__(self, root, loop):
        self.root = root
        self.loop = loop
        self.root.title('WebSocket Connection Tester')

        # Allow window resizing
        self.root.geometry('450x200')  # Starting size
        self.root.minsize(450, 200)  # Minimum size
        self.root.resizable(False, False)

        # Connection and authentication status
        self.websocket = None
        self.connected = False
        self.authenticated = False
        self.api_key = None
        self.websocket_uri = None

        # Configure grid layout for the root window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create a main frame
        main_frame = tk.Frame(root)
        main_frame.grid(sticky='nsew', padx=10, pady=10)

        # Configure grid layout for the main frame
        main_frame.columnconfigure(1, weight=1)  # Make entry fields expand

        # API Key Entry
        self.api_key_label = tk.Label(main_frame, text="API Key:")
        self.api_key_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.api_key_entry = tk.Entry(main_frame)
        self.api_key_entry.insert(0, "AFM-Control-API-Key")  # Default API Key
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        # Server IP Entry
        self.ip_label = tk.Label(main_frame, text="Server IP:")
        self.ip_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.ip_entry = tk.Entry(main_frame)
        self.ip_entry.insert(0, "127.0.0.1")  # Default IP
        self.ip_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')

        # Server Port Entry
        self.port_label = tk.Label(main_frame, text="Server Port:")
        self.port_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.port_entry = tk.Entry(main_frame)
        self.port_entry.insert(0, "1234")  # Default Port
        self.port_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')

        # Connect and Disconnect Buttons aligned to the left
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky='w')

        self.connect_button = tk.Button(button_frame, text="Connect", command=self.start_connection, width=15)
        self.connect_button.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.disconnect_button = tk.Button(button_frame, text="Disconnect", command=self.disconnect, width=15,
                                           state='disabled')
        self.disconnect_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Status Label to inform the user about connection and authentication status
        status_frame = tk.Frame(main_frame)
        status_frame.grid(row=4, column=0, columnspan=2, pady=5, sticky='w')

        self.status_label = tk.Label(status_frame, text="Status: Disconnected", fg="red")
        self.status_label.pack(side=tk.LEFT)

        # Start the update loop for tkinter
        self.root.after(100, self.update_event_loop)

    def start_connection(self):
        if not self.connected or not self.authenticated:
            # Get IP, port, and API key from entry fields
            server_ip = self.ip_entry.get().strip()
            server_port = self.port_entry.get().strip()
            self.api_key = self.api_key_entry.get().strip()

            if not self.api_key:
                self.update_status("Please enter a valid API key.", "red")
                return

            if not server_ip or not server_port:
                self.update_status("Please enter valid Server IP and Port.", "red")
                return

            self.websocket_uri = f"ws://{server_ip}:{server_port}"
            self.update_status(f"Connecting to {self.websocket_uri}...", "orange")
            asyncio.ensure_future(self.connect_and_authenticate(), loop=self.loop)

    async def connect_and_authenticate(self):
        try:
            self.websocket = await websockets.connect(self.websocket_uri)
            self.connected = True
            self.authenticated = False  # Initially not authenticated
            self.update_status("Connected. Authenticating...", "orange")

            # Update button states: Connect disabled until authentication
            self.connect_button.config(state='disabled')
            # Disconnect button remains disabled until authenticated

            # Authenticate with the API key
            auth_request = {
                "command": "authenticate",
                "apikey": self.api_key
            }
            await self.websocket.send(json.dumps(auth_request))

            response = await self.websocket.recv()
            response_data = json.loads(response)

            if response_data.get("command") == "error":
                error_message = response_data.get("payload", {}).get("details", "Unknown error.")
                self.authenticated = False
                self.update_status(f"Connected. Authentication Failed: {error_message}", "red")
                # Optionally, keep the connection open for re-authentication
                self.connect_button.config(state='normal')  # Allow re-attempt
            else:
                self.authenticated = True
                self.update_status("Authenticated successfully.", "green")
                # Enable Disconnect button now that authenticated
                self.disconnect_button.config(state='normal')

        except Exception as e:
            self.update_status(f"Connection Error: {e}", "red")
            self.connected = False
            self.authenticated = False
            self.connect_button.config(state='normal')
            self.disconnect_button.config(state='disabled')

    def disconnect(self):
        if self.connected and self.authenticated and self.websocket:
            asyncio.ensure_future(self.close_connection(), loop=self.loop)
        else:
            self.update_status("Cannot disconnect: Not connected or not authenticated.", "red")

    async def close_connection(self):
        try:
            await self.websocket.close()
            self.update_status("Disconnected from the server.", "red")
        except Exception as e:
            self.update_status(f"Disconnect Error: {e}", "red")
        finally:
            self.connected = False
            self.authenticated = False
            self.connect_button.config(state='normal')
            self.disconnect_button.config(state='disabled')

    def update_status(self, message, color):
        self.status_label.config(text=f"Status: {message}", fg=color)

    def update_event_loop(self):
        try:
            self.loop.run_until_complete(asyncio.sleep(0.1))
        except Exception as e:
            self.update_status(f"Event Loop Error: {e}", "red")
        finally:
            self.root.after(50, self.update_event_loop)


def main():
    root = tk.Tk()
    loop = asyncio.get_event_loop()

    window = ClientWindow(root, loop)

    root.mainloop()


if __name__ == '__main__':
    main()
