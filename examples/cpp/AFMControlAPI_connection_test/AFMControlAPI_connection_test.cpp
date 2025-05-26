// This code is a simple C++ program that connects to the AFMControl WebSocket API server using WinHTTP.
//
// Project Setup Instructions for Visual Studio 2022:
// 
// 1. Create a new Console Application project.
// 2. Add this `main.cpp` file to the project(replace any existing `main.cpp`).
// 3. In Project Properties :
//      - C / C++ → Language → C++ Language Standard = ISO C++17 (or later).
//      - Linker → Input → Additional Dependencies : add `ws2_32.lib; winhttp.lib`.
// 4. Build and run.Enter your API Key, Server Host(IP or name), and Port when prompted.
// 
// Console input example (for API server IP = 127.0.0.1 and port = 1234):
//      API Key : YOUR - SECRET - API - KEY - HERE
//      Server Host(IP or name) : 127.0.0.1
//      Server Port : 1234
// 
// Console output for successfull connection with a valid API-Key:
//      WebSocket connected 
//      Server replied : {"command":"response", "object" : "Authenticated", "payload" : {"message":"OK"}}
//      Disconnected.
//
// Console output for successfull connection but with an invalid API-Key:
//      WebSocket connected.
//      Server replied: {"command":"error","payload":{"details":"Invalid API key","title":"Unauthorized"}}
//      Disconnected.
//
// Console output for failed connection (e.g., API server not started, wrong host IP or port):
//      Handshake failed: 12029
//


#include <windows.h>
#include <winhttp.h>
#include <iostream>
#include <string>
#include <vector>

#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "winhttp.lib")

static std::wstring to_wstring(const std::string& s) {
    return std::wstring(s.begin(), s.end());
}

int main() {
    std::string apiKey, host, port;
    std::cout << "API Key: ";
    std::getline(std::cin, apiKey);
    std::cout << "Server Host (IP or name): ";
    std::getline(std::cin, host);
    std::cout << "Server Port: ";
    std::getline(std::cin, port);

    HINTERNET hSession = WinHttpOpen(
        L"AFMControlAPI-Tester/1.0",
        WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS,
        0
    );
    if (!hSession) { std::cerr << "WinHttpOpen failed: " << GetLastError() << "\n"; return 1; }

    HINTERNET hConnect = WinHttpConnect(
        hSession,
        to_wstring(host).c_str(),
        static_cast<INTERNET_PORT>(std::stoi(port)),
        0
    );
    if (!hConnect) { std::cerr << "WinHttpConnect failed: " << GetLastError() << "\n"; return 1; }

    HINTERNET hRequest = WinHttpOpenRequest(
        hConnect,
        WINHTTP_NO_ADDITIONAL_HEADERS,
        L"/",
        nullptr,
        WINHTTP_NO_REFERER,
        WINHTTP_DEFAULT_ACCEPT_TYPES,
        0
    );
    if (!hRequest) { std::cerr << "WinHttpOpenRequest failed: " << GetLastError() << "\n"; return 1; }

    if (!WinHttpSetOption(
        hRequest,
        WINHTTP_OPTION_UPGRADE_TO_WEB_SOCKET,
        WINHTTP_NO_OUTPUT_BUFFER,
        0))
    {
        std::cerr << "WinHttpSetOption failed: " << GetLastError() << "\n"; return 1;
    }

    if (!WinHttpSendRequest(hRequest,
        WINHTTP_NO_ADDITIONAL_HEADERS, 0,
        WINHTTP_NO_REQUEST_DATA, 0, 0, 0) ||
        !WinHttpReceiveResponse(hRequest, nullptr))
    {
        std::cerr << "Handshake failed: " << GetLastError() << "\n"; return 1;
    }

    HINTERNET hWebSocket = WinHttpWebSocketCompleteUpgrade(hRequest, 0);
    WinHttpCloseHandle(hRequest);
    if (!hWebSocket) { std::cerr << "Upgrade failed: " << GetLastError() << "\n"; return 1; }

    std::cout << "WebSocket connected.\n";

    std::string auth = R"({"command":"authenticate","apikey":")"
        + apiKey + R"("})";

    DWORD sendResult = WinHttpWebSocketSend(
        hWebSocket,
        WINHTTP_WEB_SOCKET_UTF8_MESSAGE_BUFFER_TYPE,
        reinterpret_cast<PVOID>(const_cast<char*>(auth.data())),
        static_cast<DWORD>(auth.size())
    );
    if (sendResult != ERROR_SUCCESS) {
        std::cerr << "Send failed: " << sendResult << "\n";
        WinHttpWebSocketClose(hWebSocket,
            WINHTTP_WEB_SOCKET_SUCCESS_CLOSE_STATUS,
            nullptr, 0);
        return 1;
    }

    std::vector<BYTE> buffer(4096);
    DWORD readBytes = 0;
    WINHTTP_WEB_SOCKET_BUFFER_TYPE bufferType;
    DWORD recvResult = WinHttpWebSocketReceive(
        hWebSocket,
        buffer.data(),
        static_cast<DWORD>(buffer.size()),
        &readBytes,
        &bufferType
    );
    if (recvResult == ERROR_SUCCESS &&
        bufferType == WINHTTP_WEB_SOCKET_UTF8_MESSAGE_BUFFER_TYPE)
    {
        std::string reply(reinterpret_cast<char*>(buffer.data()), readBytes);
        std::cout << "Server replied: " << reply << "\n";
    }
    else {
        std::cerr << "Receive failed: " << recvResult << "\n";
    }

    WinHttpWebSocketClose(
        hWebSocket,
        WINHTTP_WEB_SOCKET_SUCCESS_CLOSE_STATUS,
        nullptr, 0
    );
    WinHttpCloseHandle(hWebSocket);
    WinHttpCloseHandle(hConnect);
    WinHttpCloseHandle(hSession);

    std::cout << "Disconnected.\n";
    return 0;
}
