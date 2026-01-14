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
    // Send Input Event (Async - Fire and Forget)
    static void SendAsync(int keyCode, const std::wstring& context, int x, int y, int h);

    // Send Input Event (Sync - Wait for Response)
    static BridgeAction SendSync(int keyCode, const std::wstring& context, int x, int y, int h);
};
