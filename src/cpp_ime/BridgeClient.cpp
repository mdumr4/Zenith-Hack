// BridgeClient.cpp
#include "BridgeClient.h"
#include <winhttp.h>
#include <thread>
#include <sstream>
#include <iostream>

#pragma comment(lib, "winhttp.lib")

// Helper to read full response
std::string ReadResponse(HINTERNET hRequest) {
    std::string response;
    DWORD dwSize = 0;
    DWORD dwDownloaded = 0;
    LPSTR pszOutBuffer;

    do {
        dwSize = 0;
        if (!WinHttpQueryDataAvailable(hRequest, &dwSize)) break;
        if (!dwSize) break;

        pszOutBuffer = new char[dwSize + 1];
        if (!pszOutBuffer) break;

        ZeroMemory(pszOutBuffer, dwSize + 1);

        if (WinHttpReadData(hRequest, (LPVOID)pszOutBuffer, dwSize, &dwDownloaded)) {
            response.append(pszOutBuffer, dwDownloaded);
        }

        delete[] pszOutBuffer;
    } while (dwSize > 0);

    return response;
}

std::string DoSendSync(int keyCode, std::wstring context) {
    HINTERNET hSession = NULL, hConnect = NULL, hRequest = NULL;
    std::string result = "";

    // 1. Open Session
    hSession = WinHttpOpen(L"FraiIME/1.0", WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
    if (!hSession) return "";

    // 2. Connect to Localhost:18492
    hConnect = WinHttpConnect(hSession, L"127.0.0.1", 18492, 0);
    if (!hConnect) { WinHttpCloseHandle(hSession); return ""; }

    // 3. Create Request
    hRequest = WinHttpOpenRequest(hConnect, L"POST", L"/input", NULL, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, 0);
    if (!hRequest) { WinHttpCloseHandle(hConnect); WinHttpCloseHandle(hSession); return ""; }

    // 4. Build JSON Payload
    std::wstring headers = L"Content-Type: application/json\r\n";
    std::string jsonBody =
        "{ \"trigger_key\": " + std::to_string(keyCode) +
        ", \"text\": \"\"" +
        ", \"app_name\": \"notepad.exe\"" +
        ", \"caret\": { \"x\":0, \"y\":0, \"h\":0 } }";

    // 5. Send
    if (WinHttpSendRequest(hRequest, headers.c_str(), headers.length(), (LPVOID)jsonBody.c_str(), jsonBody.length(), jsonBody.length(), 0) &&
        WinHttpReceiveResponse(hRequest, NULL)) {

        // 6. Read Response
        result = ReadResponse(hRequest);
    }

    // Cleanup
    WinHttpCloseHandle(hRequest);
    WinHttpCloseHandle(hConnect);
    WinHttpCloseHandle(hSession);

    return result;
}

// Manual JSON Parser (Simplified)
BridgeAction ParseResponse(const std::string& json) {
    BridgeAction action;
    action.type = "none";

    // 1. Extract "action": "VALUE"
    size_t actionKey = json.find("\"action\"");
    if (actionKey != std::string::npos) {
        size_t valStart = json.find("\"", actionKey + 8);
        if (valStart != std::string::npos) {
             valStart++; // Skip quote
             size_t valEnd = json.find("\"", valStart);
             if (valEnd != std::string::npos) {
                 action.type = json.substr(valStart, valEnd - valStart);
             }
        }
    }

    // 2. Extract "text": "VALUE" (for replacement)
    if (action.type == "replace") {
        size_t textKey = json.find("\"text\"");
        if (textKey != std::string::npos) {
            size_t valStart = json.find("\"", textKey + 6);
            if (valStart != std::string::npos) {
                valStart++;
                size_t valEnd = json.find("\"", valStart);
                if (valEnd != std::string::npos) {
                    action.text = json.substr(valStart, valEnd - valStart);
                }
            }
        }

        // Extract "range": [start, end]
        size_t rangeKey = json.find("\"range\"");
        if (rangeKey != std::string::npos) {
             size_t openBracket = json.find("[", rangeKey);
             size_t comma = json.find(",", openBracket);
             size_t closeBracket = json.find("]", comma);

             if (openBracket != std::string::npos && comma != std::string::npos && closeBracket != std::string::npos) {
                 std::string startStr = json.substr(openBracket + 1, comma - (openBracket + 1));
                 std::string endStr = json.substr(comma + 1, closeBracket - (comma + 1));
                 try {
                    action.rangeStart = std::stoi(startStr);
                    action.rangeEnd = std::stoi(endStr);
                 } catch(...) {}
             }
        }
    }

    // 3. Extract "suggestion": "VALUE" (for ghost text)
    if (action.type == "suggest") {
         size_t suggKey = json.find("\"suggestion\"");
         if (suggKey != std::string::npos) {
            size_t valStart = json.find("\"", suggKey + 12);
            if (valStart != std::string::npos) {
                valStart++;
                size_t valEnd = json.find("\"", valStart);
                if (valEnd != std::string::npos) {
                    action.text = json.substr(valStart, valEnd - valStart);
                }
            }
         }
    }

    return action;
}

void BridgeClient::SendAsync(int keyCode, const std::wstring& context) {
    // Fire and forget thread
    std::thread t([=](){
        DoSendSync(keyCode, context);
    });
    t.detach();
}

BridgeAction BridgeClient::SendSync(int keyCode, const std::wstring& context) {
    std::string jsonResponse = DoSendSync(keyCode, context);
    return ParseResponse(jsonResponse);
}
