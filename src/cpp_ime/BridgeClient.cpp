// BridgeClient.cpp
#include "BridgeClient.h"
#include <winhttp.h>
#include <thread>
#include <sstream>
#include <iostream>

#pragma comment(lib, "winhttp.lib")

void DoSend(int keyCode, std::wstring context) {
    HINTERNET hSession = NULL, hConnect = NULL, hRequest = NULL;

    // 1. Open Session
    hSession = WinHttpOpen(L"FraiIME/1.0", WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
    if (!hSession) return;

    // 2. Connect to Localhost:18492
    hConnect = WinHttpConnect(hSession, L"127.0.0.1", 18492, 0);
    if (!hConnect) { WinHttpCloseHandle(hSession); return; }

    // 3. Create Request
    hRequest = WinHttpOpenRequest(hConnect, L"POST", L"/input", NULL, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, 0);
    if (!hRequest) { WinHttpCloseHandle(hConnect); WinHttpCloseHandle(hSession); return; }

    // 4. Build JSON Payload
    // Simple JSON construction string for now to avoid external dependencies
    std::wstring headers = L"Content-Type: application/json\r\n";

    // Convert wide context to escaped JSON string (Simplified for MVP)
    // NOTE: In production, use a real JSON library.
    // Build JSON Payload (Strict Schema per Instruction.md)
    std::string jsonBody =
        "{ \"trigger_key\": " + std::to_string(keyCode) +
        ", \"text\": \"\"" +
        ", \"app_name\": \"notepad.exe\"" +
        ", \"caret\": { \"x\":0, \"y\":0, \"h\":0 } }";

    // 5. Send
    WinHttpSendRequest(hRequest, headers.c_str(), headers.length(), (LPVOID)jsonBody.c_str(), jsonBody.length(), jsonBody.length(), 0);
    WinHttpReceiveResponse(hRequest, NULL);

    // Cleanup
    WinHttpCloseHandle(hRequest);
    WinHttpCloseHandle(hConnect);
    WinHttpCloseHandle(hSession);
}

void BridgeClient::SendAsync(int keyCode, const std::wstring& context) {
    // Fire and forget thread to avoid blocking the input stream
    std::thread t(DoSend, keyCode, context);
    t.detach();
}
