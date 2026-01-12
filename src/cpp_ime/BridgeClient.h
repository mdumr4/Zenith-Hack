// BridgeClient.h
#pragma once
#include <windows.h>
#include <string>

class BridgeClient {
public:
    static void SendAsync(int keyCode, const std::wstring& context);
};
