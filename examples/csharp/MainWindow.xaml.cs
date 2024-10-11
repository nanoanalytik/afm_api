using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace WebSocketClientWPF
{
	public partial class MainWindow : Window
	{
		private ClientWebSocket _webSocket;
		private CancellationTokenSource _cancellation;

		// Define the channel number (ensure it matches your server's configuration)
		private const int CHANNEL = 0;

		public MainWindow()
		{
			InitializeComponent();
		}

		private async void btnConnect_Click(object sender, RoutedEventArgs e)
		{
			string apiKey = txtApiKey.Text.Trim();
			string ip = txtIP.Text.Trim();
			string port = txtPort.Text.Trim();

			if (string.IsNullOrEmpty(apiKey))
			{
				Log("API Key is required.");
				return;
			}

			if (string.IsNullOrEmpty(ip))
			{
				Log("Server IP is required.");
				return;
			}

			if (string.IsNullOrEmpty(port) || !int.TryParse(port, out int portNumber))
			{
				Log("Valid Server Port is required.");
				return;
			}

			string uri = $"ws://{ip}:{port}";

			_webSocket = new ClientWebSocket();
			_cancellation = new CancellationTokenSource();

			try
			{
				Log($"Connecting to {uri}...");
				await _webSocket.ConnectAsync(new Uri(uri), _cancellation.Token);
				Log("Connected to the WebSocket server.");

				// Send authentication command
				var authRequest = new
				{
					command = "authenticate",
					apikey = apiKey
				};
				string authMessage = JsonConvert.SerializeObject(authRequest);
				await SendMessage(authMessage);
				Log("Authentication command sent.");

				// Wait for authentication response
				string authResponse = await ReceiveMessageAsync();
				if (IsErrorResponse(authResponse))
				{
					Log($"Authentication failed: {ExtractErrorMessage(authResponse)}");
					await DisconnectWebSocket();
					return;
				}
				else
				{
					Log("Authentication successful.");
				}

				// Subscribe to Measurement Data
				var subscribeMeasurement = new
				{
					command = "set",
					@object = "MeasurementDataSubscription",
					payload = new
					{
						property = "type",
						type = "line",
						format = "float",
						channel = CHANNEL, // Ensure CHANNEL is defined appropriately
						subscription = true
					}
				};
				string subscribeMeasurementMessage = JsonConvert.SerializeObject(subscribeMeasurement);
				await SendMessage(subscribeMeasurementMessage);
				Log("Subscribed to Measurement Data.");

				// Subscribe to System Log
				var subscribeLog = new
				{
					command = "set",
					@object = "DataSubscription",
					payload = new
					{
						property = "type",
						type = "log",
						format = "txt",
						subscription = true
					}
				};
				string subscribeLogMessage = JsonConvert.SerializeObject(subscribeLog);
				await SendMessage(subscribeLogMessage);
				Log("Subscribed to System Log.");

				// Start listening to incoming messages
				_ = ReceiveMessages(_cancellation.Token);

				// Update button states
				btnConnect.IsEnabled = false;
				btnDisconnect.IsEnabled = true;
			}
			catch (Exception ex)
			{
				Log($"Error connecting: {ex.Message}");
			}
		}

		private async void btnDisconnect_Click(object sender, RoutedEventArgs e)
		{
			await DisconnectWebSocket();
		}

		private async Task DisconnectWebSocket()
		{
			if (_webSocket != null)
			{
				try
				{
					if (_webSocket.State == WebSocketState.Open ||
						_webSocket.State == WebSocketState.CloseReceived ||
						_webSocket.State == WebSocketState.CloseSent)
					{
						// Disable Disconnect button to prevent multiple clicks
						btnDisconnect.IsEnabled = false;

						_cancellation.Cancel();
						await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Client disconnecting", CancellationToken.None);
						Log("Disconnected from the WebSocket server.");
					}
					else if (_webSocket.State == WebSocketState.Aborted)
					{
						// Log a non-cryptic message for aborted state
						Log("WebSocket connection aborted.");
					}
					else
					{
						// Log a general message for other invalid states
						Log($"Cannot disconnect. WebSocket is in an invalid state: {_webSocket.State}.");
					}
				}
				catch (WebSocketException ex) when (ex.Message.Contains("Aborted"))
				{
					// Suppress the cryptic error message for 'Aborted' state
					Log("WebSocket connection aborted.");
				}
				catch (Exception ex)
				{
					Log($"Error disconnecting: {ex.Message}");
				}
				finally
				{
					if (_webSocket != null)
					{
						_webSocket.Dispose();
						_webSocket = null;
					}

					btnConnect.IsEnabled = true;
					btnDisconnect.IsEnabled = false;
				}
			}
			else
			{
				Log("WebSocket is not connected.");
			}
		}

		private async Task SendMessage(string message)
		{
			if (_webSocket != null && _webSocket.State == WebSocketState.Open)
			{
				byte[] bytes = Encoding.UTF8.GetBytes(message);
				await _webSocket.SendAsync(new ArraySegment<byte>(bytes), WebSocketMessageType.Text, true, _cancellation.Token);
			}
			else
			{
				Log("Cannot send message. WebSocket is not connected.");
			}
		}

		private async Task<string> ReceiveMessageAsync()
		{
			var buffer = new byte[4096];
			var result = await _webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), _cancellation.Token);
			if (result.MessageType == WebSocketMessageType.Close)
			{
				Log("WebSocket server initiated close. Disconnecting...");
				await DisconnectWebSocket();
				return null;
			}
			else
			{
				return Encoding.UTF8.GetString(buffer, 0, result.Count);
			}
		}

		private async Task ReceiveMessages(CancellationToken token)
		{
			var buffer = new byte[4096];

			try
			{
				while (_webSocket != null && _webSocket.State == WebSocketState.Open && !token.IsCancellationRequested)
				{
					var result = await _webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), token);

					if (result.MessageType == WebSocketMessageType.Close)
					{
						Log("WebSocket server initiated close. Disconnecting...");
						await DisconnectWebSocket();
						break;
					}
					else
					{
						var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
						ProcessIncomingMessage(message);
					}
				}
			}
			catch (OperationCanceledException)
			{
				// Expected when the token is canceled
				Log("Receive operation canceled.");
			}
			catch (Exception ex)
			{
				Log($"Error receiving messages: {ex.Message}");
			}
		}

		private void ProcessIncomingMessage(string message)
		{
			try
			{
				var json = JObject.Parse(message);
				string command = json["command"]?.ToString();
				string obj = json["object"]?.ToString();
				var payload = json["payload"];

				if (command == "response")
				{
					switch (obj)
					{
						case "MeasurementDataSubscription":
							Log("Received Measurement Data Subscription response.");
							// Handle measurement data as needed
							break;

						case "DataSubscription":
							Log("Received Data Subscription response.");
							// Handle data subscription confirmation
							break;

						case "LogEvent":
							string logMessage = payload["message"]?.ToString();
							if (!string.IsNullOrEmpty(logMessage))
							{
								Log($"[Log] {logMessage}");
							}
							else
							{
								Log("[Log] Received a log event without a message.");
							}
							break;

						default:
							// Handle unknown objects by checking for a message in the payload
							string unknownMessage = payload?["message"]?.ToString();
							if (!string.IsNullOrEmpty(unknownMessage))
							{
								Log($"Received unknown response object: {obj}. Message: {unknownMessage}");
							}
							else
							{
								Log($"Received unknown response object: {obj}. No additional message provided.");
								// Optionally log the entire message for debugging
								Log($"Full Response: {message}");
							}
							break;
					}
				}
				else if (command == "error")
				{
					string errorDetails = payload["details"]?.ToString() ?? json["message"]?.ToString() ?? "Unknown error";
					Log($"[Error] {errorDetails}");
				}
				else
				{
					Log($"Received unknown command: {command}");
					// Optionally log the entire message for debugging
					Log($"Full Response: {message}");
				}
			}
			catch (JsonException ex)
			{
				Log($"Failed to parse JSON message: {ex.Message}");
				Log($"Full Message: {message}");
			}
			catch (Exception ex)
			{
				Log($"Error processing message: {ex.Message}");
			}
		}

		private bool IsErrorResponse(string message)
		{
			try
			{
				var json = JObject.Parse(message);
				return json["command"]?.ToString() == "error";
			}
			catch
			{
				return false;
			}
		}

		private string ExtractErrorMessage(string message)
		{
			try
			{
				var json = JObject.Parse(message);
				return json["payload"]?["details"]?.ToString() ?? json["message"]?.ToString() ?? "Unknown error";
			}
			catch
			{
				return "Unknown error";
			}
		}

		private void Log(string message)
		{
			Dispatcher.Invoke(() =>
			{
				txtLog.AppendText($"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] {message}{Environment.NewLine}");
				txtLog.ScrollToEnd();
			});
		}

		protected override async void OnClosing(System.ComponentModel.CancelEventArgs e)
		{
			await DisconnectWebSocket();
			base.OnClosing(e);
		}
	}
}
