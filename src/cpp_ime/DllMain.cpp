// DllMain.cpp
#include <windows.h>
#include "FraiTextService.h"

HINSTANCE g_hInst = NULL;

BOOL WINAPI DllMain(HINSTANCE hInstance, DWORD dwReason, LPVOID pvReserved) {
    if (dwReason == DLL_PROCESS_ATTACH) {
        g_hInst = hInstance;
    }
    return TRUE;
}

STDAPI DllRegisterServer() {
    // TODO: Register CLSID with TSF
    return S_OK;
}

STDAPI DllUnregisterServer() {
    // TODO: Unregister
    return S_OK;
}
