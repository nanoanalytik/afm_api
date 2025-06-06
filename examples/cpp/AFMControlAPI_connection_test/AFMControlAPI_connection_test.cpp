// This code is a simple C++ program that connects to the AFMControl WebSocket API server using WinHTTP,
// performs authentication, then sends an APIEcho “get” command to test the connection.
// After receiving the echo response, it waits for any key press before closing the connection.
//
// Project Setup Instructions:
//
// 1. Create a new Console Application project.
// 2. Add this `main.cpp` file to the project (replace any existing `main.cpp`).
// 3. In Project Properties :
//      - C / C++ → Language → C++ Language Standard = ISO C++17 (or later).
//      - Linker → Input → Additional Dependencies : add `ws2_32.lib; winhttp.lib`.
// 4. Build and run. Enter your API Key, Server Host (IP or name), and Port when prompted.
//
// Console input example (for API server IP = 127.0.0.1 and port = 1234):
//      API Key : YOUR-SECRET-API-KEY-HERE
//      Server Host (IP or name) : 127.0.0.1
//      Server Port : 1234
//
// Expected Console output (with valid API key):
//      WebSocket connected.
//      Server replied: {"command":"response","object":"Authenticated","payload":{"message":"OK"}}
//      Sent APIEcho get command.
//      Server replied: {"command":"response","object":"APIEcho","payload":{"property":"connection test"}}
//      Press any key to close connection...
//      Disconnected.
//
// If authentication fails (invalid API key), you’ll see the error response and then “Disconnected.”
// If handshake/connection fails, you’ll see something like “Handshake failed: 12029”.

#include <windows.h>
#include <winhttp.h>
#include <iostream>
#include <string>
#include <vector>
#include <conio.h>

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

    //
    // 1) Open WinHTTP session
    //
    HINTERNET hSession = WinHttpOpen(
        L"AFMControlAPI-Tester/1.0",
        WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS,
        0
    );
    if (!hSession) {
        std::cerr << "WinHttpOpen failed: " << GetLastError() << "\n";
        return 1;
    }

    //
    // 2) Connect to server
    //
    HINTERNET hConnect = WinHttpConnect(
        hSession,
        to_wstring(host).c_str(),
        static_cast<INTERNET_PORT>(std::stoi(port)),
        0
    );
    if (!hConnect) {
        std::cerr << "WinHttpConnect failed: " << GetLastError() << "\n";
        WinHttpCloseHandle(hSession);
        return 1;
    }

    //
    // 3) Prepare an HTTP request that will be upgraded to WebSocket
    //
    HINTERNET hRequest = WinHttpOpenRequest(
        hConnect,
        WINHTTP_NO_ADDITIONAL_HEADERS,  
        L"/",                           
        nullptr,
        WINHTTP_NO_REFERER,
        WINHTTP_DEFAULT_ACCEPT_TYPES,
        0
    );
    if (!hRequest) {
        std::cerr << "WinHttpOpenRequest failed: " << GetLastError() << "\n";
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return 1;
    }

    //
    // 4) Tell WinHTTP we want to upgrade this request to WebSocket
    //
    if (!WinHttpSetOption(
        hRequest,
        WINHTTP_OPTION_UPGRADE_TO_WEB_SOCKET,
        WINHTTP_NO_OUTPUT_BUFFER,
        0))
    {
        std::cerr << "WinHttpSetOption failed: " << GetLastError() << "\n";
        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return 1;
    }

    //
    // 5) Send the HTTP handshake and wait for a response
    //
    if (!WinHttpSendRequest(
        hRequest,
        WINHTTP_NO_ADDITIONAL_HEADERS,
        0,
        WINHTTP_NO_REQUEST_DATA,
        0,
        0,
        0) ||
        !WinHttpReceiveResponse(hRequest, nullptr))
    {
        std::cerr << "Handshake failed: " << GetLastError() << "\n";
        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return 1;
    }

    //
    // 6) Complete the WebSocket upgrade
    //
    HINTERNET hWebSocket = WinHttpWebSocketCompleteUpgrade(hRequest, 0);
    // We can close the HTTP request handle now
    WinHttpCloseHandle(hRequest);
    if (!hWebSocket) {
        std::cerr << "Upgrade failed: " << GetLastError() << "\n";
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return 1;
    }

    std::cout << "WebSocket connected.\n";

    //
    // 7) Send the “authenticate” command first
    //
    std::string auth = R"({"command":"authenticate","apikey":")"
        + apiKey + R"("})";

    DWORD authSendResult = WinHttpWebSocketSend(
        hWebSocket,
        WINHTTP_WEB_SOCKET_UTF8_MESSAGE_BUFFER_TYPE,
        reinterpret_cast<PVOID>(const_cast<char*>(auth.data())),
        static_cast<DWORD>(auth.size())
    );
    if (authSendResult != ERROR_SUCCESS) {
        std::cerr << "Send (authenticate) failed: " << authSendResult << "\n";
        WinHttpWebSocketClose(hWebSocket,
            WINHTTP_WEB_SOCKET_SUCCESS_CLOSE_STATUS,
            nullptr, 0);
        WinHttpCloseHandle(hWebSocket);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return 1;
    }

    //
    // 8) Read the server’s authentication response
    //
    {
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
            std::cerr << "Receive (authenticate) failed: " << recvResult << "\n";
            WinHttpWebSocketClose(hWebSocket,
                WINHTTP_WEB_SOCKET_SUCCESS_CLOSE_STATUS,
                nullptr, 0);
            WinHttpCloseHandle(hWebSocket);
            WinHttpCloseHandle(hConnect);
            WinHttpCloseHandle(hSession);
            return 1;
        }
    }

    //
    // 9) Send the APIEcho “get” command to test the connection
    //
    std::string echoCmd = R"({"command":"get","object":"APIEcho","payload":{"property":"connection test"}})";
    DWORD echoSendResult = WinHttpWebSocketSend(
        hWebSocket,
        WINHTTP_WEB_SOCKET_UTF8_MESSAGE_BUFFER_TYPE,
        reinterpret_cast<PVOID>(const_cast<char*>(echoCmd.data())),
        static_cast<DWORD>(echoCmd.size())
    );
    if (echoSendResult != ERROR_SUCCESS) {
        std::cerr << "Send (APIEcho) failed: " << echoSendResult << "\n";
        WinHttpWebSocketClose(hWebSocket,
            WINHTTP_WEB_SOCKET_SUCCESS_CLOSE_STATUS,
            nullptr, 0);
        WinHttpCloseHandle(hWebSocket);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return 1;
    }
    std::cout << "Sent APIEcho get command.\n";

    //
    // 10) Read the server’s APIEcho response
    //
    {
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
            std::cerr << "Receive (APIEcho) failed: " << recvResult << "\n";
        }
    }

    //
    // 11) Pause and wait for any key before closing
    //
    std::cout << "Press any key to close connection...";
    _getch();  // waits for a single key press

    //
    // 12) Close and clean up
    //
    WinHttpWebSocketClose(
        hWebSocket,
        WINHTTP_WEB_SOCKET_SUCCESS_CLOSE_STATUS,
        nullptr, 0
    );
    WinHttpCloseHandle(hWebSocket);
    WinHttpCloseHandle(hConnect);
    WinHttpCloseHandle(hSession);

    std::cout << "\nDisconnected.\n";
    return 0;
}
