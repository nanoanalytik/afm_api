"""
Real-Time Data Plotter Using WebSocket API

Compatible with API v1.1 and above

This script demonstrates how clients can connect to an API server via WebSocket, authenticate, and subscribe to data streams such as measurement data and system log messages. The primary purpose of this example is to illustrate the API mechanism for real-time data communication between a client and server.

The script performs the following actions:
- Connects to a WebSocket server.
- Authenticates using an API key.
- Subscribes to line measurement data on a specified channel.
- Subscribes to system log messages.
- Sends commands to start and stop measurements.
- Processes incoming data and displays it.
  - Measurement data is plotted in real-time using Tkinter.
  - Log messages and other outputs are displayed in a console text area.

Note:
- The programming language used is Python with Tkinter for GUI and asyncio for asynchronous operations.
- The data processing and plotting are included to demonstrate that the API mechanism works and how data can be handled upon reception.
- The actual data processing logic and GUI implementation are beyond the scope of this example.

Usage:
- Replace `"your_actual_api_key"` with your actual API key.
- Run the script using Python 3.7 or higher.

"""

import sys
import asyncio
import json
import tkinter as tk
from datetime import datetime
import websockets

# API Key for authentication
# API_KEY = "d1f89a72-3f0b-4d57-b3a9-0f7c63a2e914"  # Replace with your actual API key

# Specify the channel you want to subscribe to
CHANNEL = 0  # Change this to the desired channel number


class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, s):
        self.text_widget.insert(tk.END, s)
        self.text_widget.see(tk.END)  # Scroll to the end

    def flush(self):
        pass  # This method is needed for file-like objects


class ClientWindow:
    def __init__(self, root, loop):
        self.root = root
        self.loop = loop
        self.root.title('Real-time Data Plots')

        # Connection status
        self.websocket = None
        self.connected = False
        self.api_key = None
        self.websocket_uri = None

        # Create a frame for the configuration
        config_frame = tk.Frame(root)
        config_frame.pack(side=tk.TOP, anchor=tk.W)

        # New Row: API Key Entry
        self.api_key_label = tk.Label(config_frame, text="API Key:")
        self.api_key_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.api_key_entry = tk.Entry(config_frame, width=50)
        self.api_key_entry.insert(0, "your-afm-api-key")  # Default API Key
        self.api_key_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky='w')

        # First row: Server IP, IP entry, Connect button, Start Measurement button
        self.ip_label = tk.Label(config_frame, text="Server IP:")
        self.ip_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.ip_entry = tk.Entry(config_frame)
        self.ip_entry.insert(0, "127.0.0.1")  # Default IP
        self.ip_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.connect_button = tk.Button(config_frame, text="Connect", command=self.start_connection, width=15)
        self.connect_button.grid(row=1, column=2, padx=5, pady=5, sticky='w')

        self.start_measurement_button = tk.Button(config_frame, text="Start Measurement",
                                                  command=self.start_measurement, width=15, state='disabled')
        self.start_measurement_button.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # Second row: Server Port, Port entry, Disconnect button, Stop Measurement button
        self.port_label = tk.Label(config_frame, text="Server Port:")
        self.port_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.port_entry = tk.Entry(config_frame)
        self.port_entry.insert(0, "1234")  # Default Port
        self.port_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.disconnect_button = tk.Button(config_frame, text="Disconnect", command=self.disconnect, width=15)
        self.disconnect_button.grid(row=2, column=2, padx=5, pady=5, sticky='w')

        # Add the Stop Measurement button
        self.stop_measurement_button = tk.Button(config_frame, text="Stop Measurement",
                                                 command=self.stop_measurement, width=15, state='disabled')
        self.stop_measurement_button.grid(row=2, column=3, padx=5, pady=5, sticky='w')

        # Initialize canvas dimensions and margins
        self.canvas_width = 600
        self.canvas_height = 400
        self.margin_left = 100  # Adjusted margin to prevent overlap
        self.margin_bottom = 50  # Adjusted margin to prevent overlap with X-axis label
        self.margin_right = 20
        self.margin_top = 20

        # Create the canvas for plotting
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bind the configure event to update canvas size
        self.canvas.bind('<Configure>', self.on_canvas_resize)

        # Data queue
        self.line_data_queue = []

        # Variables to store data for scaling
        self.x_values = []
        self.y_values = []
        self.last_plot_data = None  # Store the last plot data

        # Create a frame for the console output
        console_frame = tk.Frame(self.root)
        console_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Create a scrollbar for the console output
        console_scrollbar = tk.Scrollbar(console_frame)
        console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a text widget for console output
        self.console_text = tk.Text(console_frame, height=10, yscrollcommand=console_scrollbar.set)
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure the scrollbar
        console_scrollbar.config(command=self.console_text.yview)

        # Redirect stdout to the console_text widget
        sys.stdout = StdoutRedirector(self.console_text)

        # Start the update loop for tkinter
        self.root.after(100, self.update_plots)

    def on_canvas_resize(self, event):
        # Update canvas dimensions
        self.canvas_width = event.width
        self.canvas_height = event.height
        # Redraw the plot with new dimensions
        self.redraw_plot()

    def scale_x(self, x):
        x_min, x_max = min(self.x_values), max(self.x_values)
        plot_width = self.canvas_width - self.margin_left - self.margin_right
        if x_max == x_min:
            # Avoid division by zero
            return self.margin_left + plot_width / 2
        else:
            return self.margin_left + (x - x_min) / (x_max - x_min) * plot_width

    def scale_y(self, y):
        y_min, y_max = min(self.y_values), max(self.y_values)
        plot_height = self.canvas_height - self.margin_top - self.margin_bottom
        if y_max == y_min:
            # Avoid division by zero
            return self.margin_top + plot_height / 2
        else:
            # Invert y-axis for canvas coordinates
            return self.margin_top + (y_max - y) / (y_max - y_min) * plot_height

    def start_connection(self):
        if not self.connected:
            # Get IP and port from entry fields
            server_ip = self.ip_entry.get()
            server_port = self.port_entry.get()
            self.websocket_uri = f"ws://{server_ip}:{server_port}"
            self.api_key = self.api_key_entry.get()

            # Start the WebSocket connection in the background
            asyncio.ensure_future(self.connect_and_subscribe(), loop=self.loop)

    async def connect_and_subscribe(self):
        try:
            self.websocket = await websockets.connect(self.websocket_uri)
            print("Connected to the WebSocket server.")
            self.connected = True
            self.start_measurement_button.config(state='normal')  # Enable the Start Measurement button
            self.stop_measurement_button.config(state='normal')   # Enable the Stop Measurement button

            api_key = self.api_key

            # Authenticate with the API key
            auth_request = {
                "command": "authenticate",
                "apikey": api_key
            }
            await self.websocket.send(json.dumps(auth_request))
            response = await self.websocket.recv()
            response_data = json.loads(response)
            if response_data.get("command") == "error":
                print("Authentication failed:", response_data)
                return
            else:
                print("Authentication successful.")

            # Subscribe to line data
            subscribe_line_request = {
                "command": "set",
                "object": "MeasurementDataSubscription",
                "payload": {
                    "property": "type",
                    "type": "line",
                    "format": "float",
                    "channel": CHANNEL,
                    "subscription": True
                }
            }
            await self.websocket.send(json.dumps(subscribe_line_request))
            response = await self.websocket.recv()
            response_data = json.loads(response)
            if response_data.get("command") == "error":
                print("Line data subscription failed:", response_data)
                return
            else:
                print(f"Subscribed to line data on channel {CHANNEL}.")

            # Subscribe to log data
            subscribe_log_request = {
                "command": "set",
                "object": "DataSubscription",
                "payload": {
                    "property": "type",
                    "type": "log",
                    "format": "txt",
                    "subscription": True
                }
            }
            await self.websocket.send(json.dumps(subscribe_log_request))
            response = await self.websocket.recv()
            response_data = json.loads(response)
            if response_data.get("command") == "error":
                print("Log data subscription failed:", response_data)
                return
            else:
                print("Subscribed to log data")

            # Listen for incoming measurement and log data
            async for message in self.websocket:
                await self.process_message(message)
        except Exception as e:
            print("Error in connect_and_subscribe:", e)
            self.connected = False
            self.start_measurement_button.config(state='disabled')  # Disable the Start Measurement button
            self.stop_measurement_button.config(state='disabled')   # Disable the Stop Measurement button

    async def process_message(self, message):
        try:
            data = json.loads(message)
            command = data.get("command")
            obj = data.get("object")
            payload = data.get("payload", {})

            if command == "response":
                if obj == "MeasurementDataSubscription":
                    # Handle measurement data
                    data_type = payload.get("type", "")
                    channel = payload.get("channel")
                    if channel != CHANNEL:
                        return  # Ignore data from other channels
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if data_type == "line":
                        value = payload.get("value", {})
                        x_values = value.get("x", [])
                        y_forward = value.get("y_forward", [])
                        y_backward = value.get("y_backward", [])

                        # Validate data
                        if not x_values or not y_forward or not y_backward:
                            print("Invalid data received: x_values or y_values are empty.")
                            return

                        if len(x_values) != len(y_forward) or len(x_values) != len(y_backward):
                            print("Invalid data received: lengths of x_values and y_values do not match.")
                            return

                        # Store the last plot data
                        self.last_plot_data = {
                            'x_values': x_values,
                            'y_forward': y_forward,
                            'y_backward': y_backward,
                            'signal_name': payload.get("signal", "Measurement Data"),
                            'channel': channel,
                            'timestamp': timestamp
                        }

                        # Add the data to the line data queue
                        self.line_data_queue.append(self.last_plot_data)

                        # Print timestamp and data receipt message
                        print(f"[{timestamp}] Received line data on channel {channel}.")

                    else:
                        print(f"Received unknown data type '{data_type}' on channel {channel}.")

                elif obj == "LogEvent":
                    # Handle log messages
                    message_text = payload.get("message", "")
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] Log: {message_text}")

                else:
                    # Handle other responses, e.g., subscription confirmations
                    pass

            elif command == "error":
                # Handle error messages
                error_text = payload.get("details", data.get("message", "Unknown error"))
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{timestamp}] Error response: {error_text}")

            else:
                print(f"Received unknown command '{command}'.")
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
        except Exception as e:
            print("Error processing message:", e)

    def start_measurement(self):
        if self.connected and self.websocket:
            asyncio.ensure_future(self.send_start_measurement_command(), loop=self.loop)
        else:
            print("Not connected to the server. Please connect first.")

    async def send_start_measurement_command(self):
        try:
            start_measurement_command = {
                "command": "set",
                "object": "ActionMeasurementStart",
                "payload": {
                    "property": "triggered",
                    "value": True
                }
            }
            await self.websocket.send(json.dumps(start_measurement_command))
            print("Sent start measurement command.")
        except Exception as e:
            print("Error sending start measurement command:", e)

    def stop_measurement(self):
        if self.connected and self.websocket:
            asyncio.ensure_future(self.send_stop_measurement_command(), loop=self.loop)
        else:
            print("Not connected to the server. Please connect first.")

    async def send_stop_measurement_command(self):
        try:
            stop_measurement_command = {
                "command": "set",
                "object": "ActionMeasurementStop",
                "payload": {
                    "property": "triggered",
                    "value": True
                }
            }
            await self.websocket.send(json.dumps(stop_measurement_command))
            print("Sent stop measurement command.")
        except Exception as e:
            print("Error sending stop measurement command:", e)

    def update_plots(self):
        try:
            if self.line_data_queue:
                data = self.line_data_queue.pop(0)
                self.draw_plot(data)
        except Exception as e:
            print("Error in update_plots:", e)
        finally:
            self.root.after(100, self.update_plots)

    def redraw_plot(self):
        if self.last_plot_data:
            self.draw_plot(self.last_plot_data)

    def draw_plot(self, data):
        try:
            x_values = data['x_values']
            y_forward = data['y_forward']
            y_backward = data['y_backward']

            # Validate data
            if not x_values or not y_forward or not y_backward:
                print("Invalid data: Empty x_values or y_values.")
                return

            if len(x_values) != len(y_forward) or len(x_values) != len(y_backward):
                print("Invalid data: x_values and y_values lengths do not match.")
                return

            # Store data for scaling
            self.x_values = x_values
            self.y_values = y_forward + y_backward  # Combine for scaling

            # Clear the canvas
            self.canvas.delete("all")

            # Draw axes
            self.draw_axes()

            # Draw forward scan line
            scaled_points_forward = []
            for x, y in zip(x_values, y_forward):
                scaled_x = self.scale_x(x)
                scaled_y = self.scale_y(y)
                scaled_points_forward.extend([scaled_x, scaled_y])

            self.canvas.create_line(scaled_points_forward, fill='red', tags='forward_line', width=2)

            # Draw backward scan line
            scaled_points_backward = []
            for x, y in zip(x_values, y_backward):
                scaled_x = self.scale_x(x)
                scaled_y = self.scale_y(y)
                scaled_points_backward.extend([scaled_x, scaled_y])

            self.canvas.create_line(scaled_points_backward, fill='blue', tags='backward_line', width=2)

        except Exception as e:
            print("Error in draw_plot:", e)

    def draw_axes(self):
        # Draw x and y axes
        try:
            x0 = self.margin_left
            y0 = self.canvas_height - self.margin_bottom
            x1 = self.canvas_width - self.margin_right
            y1 = self.margin_top

            # X-axis
            self.canvas.create_line(x0, y0, x1, y0, fill='black')
            # Y-axis
            self.canvas.create_line(x0, y0, x0, y1, fill='black')

            # Check if we have valid data
            if not self.x_values or not self.y_values:
                print("No data to draw axes.")
                return

            x_min, x_max = min(self.x_values), max(self.x_values)
            y_min, y_max = min(self.y_values), max(self.y_values)

            # Handle cases where x_max == x_min or y_max == y_min
            if x_max == x_min:
                x_ticks_count = 1
                x_ticks = [x_min]
                x_positions = [(x0 + x1) / 2]
            else:
                x_ticks_count = 10
                x_ticks = [x_min + i * (x_max - x_min) / x_ticks_count for i in range(x_ticks_count + 1)]
                x_positions = [x0 + i * (x1 - x0) / x_ticks_count for i in range(x_ticks_count + 1)]

            if y_max == y_min:
                y_ticks_count = 1
                y_ticks = [y_min]
                y_positions = [(y0 + y1) / 2]
            else:
                y_ticks_count = 10
                y_ticks = [y_min + i * (y_max - y_min) / y_ticks_count for i in range(y_ticks_count + 1)]
                y_positions = [y0 - i * (y0 - y1) / y_ticks_count for i in range(y_ticks_count + 1)]

            # Draw tick marks and labels for x-axis
            for x, x_value in zip(x_positions, x_ticks):
                self.canvas.create_line(x, y0, x, y0 + 5, fill='black')
                self.canvas.create_text(x, y0 + 15, text=f"{x_value:.2f}", font=('Arial', 8), anchor='n')

            # Draw tick marks and labels for y-axis
            for y, y_value in zip(y_positions, y_ticks):
                self.canvas.create_line(x0 - 5, y, x0, y, fill='black')
                self.canvas.create_text(x0 - 20, y, text=f"{y_value:.2f}", font=('Arial', 8), anchor='e')

            # Labels for axes
            self.canvas.create_text((x0 + x1) / 2, y0 + 35, text="X Axis", font=('Arial', 10))
            self.canvas.create_text(x0 - 70, (y0 + y1) / 2, text="Y Axis", font=('Arial', 10), angle=90)

        except Exception as e:
            print("Error in draw_axes:", e)

    def disconnect(self):
        if self.connected and self.websocket:
            asyncio.ensure_future(self.close_connection(), loop=self.loop)
        else:
            print("Not connected to any server.")

    async def close_connection(self):
        try:
            await self.websocket.close()
            print("Disconnected from the WebSocket server.")
        except Exception as e:
            print("Error during disconnect:", e)
        finally:
            self.connected = False
            self.start_measurement_button.config(state='disabled')  # Disable the Start Measurement button
            self.stop_measurement_button.config(state='disabled')   # Disable the Stop Measurement button


def main():
    root = tk.Tk()
    loop = asyncio.get_event_loop()

    window = ClientWindow(root, loop)

    # Periodically run the asyncio event loop
    def run_loop():
        try:
            loop.run_until_complete(asyncio.sleep(0.1))
        except Exception as e:
            print("Error in event loop:", e)
        finally:
            root.after(50, run_loop)

    root.after(50, run_loop)
    root.mainloop()


if __name__ == '__main__':
    main()
