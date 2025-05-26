# AFMControl WebSocket Client (C++ / WinHTTP)

This is a simple C++ console application that connects to the AFMControl WebSocket API server using WinHTTP.

## Project Setup (Visual Studio 2022)

### 1. Create the Project
- Open Visual Studio 2022.
- Create a new **Console Application** project.
- Replace the default `main.cpp` with the provided file.

### 2. Project Configuration
Open the **Project Properties** and apply the following settings:

#### C/C++ Settings:
- `Language → C++ Language Standard` → **ISO C++17** (or later).

#### Linker Settings:
- `Linker → Input → Additional Dependencies` → add:
  ```
  ws2_32.lib; winhttp.lib
  ```

### 3. Build & Run
Build the project and run the executable.

You will be prompted to enter:
- API Key
- Server Host (IP or domain)
- Server Port

### Example Console Input
```
API Key: YOUR-SECRET-API-KEY-HERE  
Server Host (IP or name): 127.0.0.1  
Server Port: 1234
```

---

## Example Output

### ✅ Valid API Key:
```
WebSocket connected  
Server replied: {"command":"response", "object":"Authenticated", "payload":{"message":"OK"}}  
Disconnected.
```

### ❌ Invalid API Key:
```
WebSocket connected.  
Server replied: {"command":"error","payload":{"details":"Invalid API key","title":"Unauthorized"}}  
Disconnected.
```

### ⚠️ Connection Failure (e.g. server not running or wrong IP/port):
```
Handshake failed: 12029
```

---

## Requirements
- Windows with Visual Studio 2022
- Internet access to reach the AFMControl API server
- A valid API Key

---

## License
MIT (or specify your project's license)
