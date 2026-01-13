// BridgeClient.h
#pragma once
#include <windows.h>
#include <string>

struct BridgeAction {
    std::string type;
    std::string text;
    int rangeStart = 0;
    int rangeEnd = 0;
};

class BridgeClient {
public:
    static void SendAsync(int keyCode, const std::wstring& context);
    static BridgeAction SendSync(int keyCode, const std::wstring& context);
};
