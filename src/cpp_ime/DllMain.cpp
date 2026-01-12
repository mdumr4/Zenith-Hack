// DllMain.cpp
#include <windows.h>
#include <olectl.h>
#include <msctf.h>
#include "Globals.h"
#include "FraiTextService.h"

HINSTANCE g_hInst = NULL;
LONG g_cDllRef = 0;

void DllAddRef() {
    InterlockedIncrement(&g_cDllRef);
}

void DllRelease() {
    InterlockedDecrement(&g_cDllRef);
}

BOOL WINAPI DllMain(HINSTANCE hInstance, DWORD dwReason, LPVOID pvReserved) {
    if (dwReason == DLL_PROCESS_ATTACH) {
        g_hInst = hInstance;
        DisableThreadLibraryCalls(hInstance);
    }
    return TRUE;
}

class CClassFactory : public IClassFactory {
public:
    // IUnknown
    STDMETHODIMP QueryInterface(REFIID riid, void **ppvObj) {
        if (IsEqualIID(riid, IID_IUnknown) || IsEqualIID(riid, IID_IClassFactory)) {
            *ppvObj = this;
            AddRef();
            return S_OK;
        }
        *ppvObj = NULL;
        return E_NOINTERFACE;
    }
    STDMETHODIMP_(ULONG) AddRef() { return 2; } // Static object
    STDMETHODIMP_(ULONG) Release() { return 1; }

    // IClassFactory
    STDMETHODIMP CreateInstance(IUnknown *pUnkOuter, REFIID riid, void **ppvObj) {
        if (pUnkOuter != NULL) return CLASS_E_NOAGGREGATION;
        FraiTextService *pTextService = new FraiTextService();
        if (pTextService == NULL) return E_OUTOFMEMORY;
        HRESULT hr = pTextService->QueryInterface(riid, ppvObj);
        pTextService->Release();
        return hr;
    }
    STDMETHODIMP LockServer(BOOL fLock) {
        if (fLock) DllAddRef();
        else DllRelease();
        return S_OK;
    }
};

static CClassFactory g_ClassFactory;

STDAPI DllGetClassObject(REFCLSID rclsid, REFIID riid, void **ppv) {
    if (IsEqualCLSID(rclsid, CLSID_FraiIME)) {
        return g_ClassFactory.QueryInterface(riid, ppv);
    }
    return CLASS_E_CLASSNOTAVAILABLE;
}

STDAPI DllCanUnloadNow() {
    return (g_cDllRef == 0) ? S_OK : S_FALSE;
}

// ----------------------------------------------------------------------
// Registration Helper Logic (The Hard Part)
// ----------------------------------------------------------------------

const TCHAR c_szInfoKeyPrefix[] = TEXT("CLSID\\");
const TCHAR c_szInProcSvr32[] = TEXT("InProcServer32");
const TCHAR c_szModelName[] = TEXT("ThreadingModel");
const TCHAR c_szApartment[] = TEXT("Apartment");
const TCHAR c_szDescription[] = TEXT("Frai AI Keyboard");

BOOL RegisterServer(CLSID clsid, const TCHAR *szDesc) {
    // Basic Registry Setup for COM
    TCHAR szKey[MAX_PATH];
    TCHAR szCLSID[MAX_PATH];
    TCHAR szModule[MAX_PATH];

    if (GetModuleFileName(g_hInst, szModule, ARRAYSIZE(szModule)) == 0) return FALSE;
    StringFromGUID2(clsid, szCLSID, ARRAYSIZE(szCLSID));

    wsprintf(szKey, TEXT("%s%s"), c_szInfoKeyPrefix, szCLSID);

    HKEY hKey;
    // Create CLSID\{GUID}
    if (RegCreateKeyEx(HKEY_CLASSES_ROOT, szKey, 0, NULL, REG_OPTION_NON_VOLATILE, KEY_WRITE, NULL, &hKey, NULL) != ERROR_SUCCESS) return FALSE;
    RegSetValueEx(hKey, NULL, 0, REG_SZ, (const BYTE *)szDesc, (lstrlen(szDesc) + 1) * sizeof(TCHAR));
    RegCloseKey(hKey);

    // Create CLSID\{GUID}\InProcServer32
    wsprintf(szKey, TEXT("%s%s\\%s"), c_szInfoKeyPrefix, szCLSID, c_szInProcSvr32);
    if (RegCreateKeyEx(HKEY_CLASSES_ROOT, szKey, 0, NULL, REG_OPTION_NON_VOLATILE, KEY_WRITE, NULL, &hKey, NULL) != ERROR_SUCCESS) return FALSE;
    RegSetValueEx(hKey, NULL, 0, REG_SZ, (const BYTE *)szModule, (lstrlen(szModule) + 1) * sizeof(TCHAR));
    RegSetValueEx(hKey, c_szModelName, 0, REG_SZ, (const BYTE *)c_szApartment, (lstrlen(c_szApartment) + 1) * sizeof(TCHAR));
    RegCloseKey(hKey);

    return TRUE;
}

STDAPI DllRegisterServer() {
    if (!RegisterServer(CLSID_FraiIME, c_szDescription)) return E_FAIL;

    // TSF Registration
    ITfInputProcessorProfiles *pProfiles;
    HRESULT hr = CoCreateInstance(CLSID_TF_InputProcessorProfiles, NULL, CLSCTX_INPROC_SERVER, IID_ITfInputProcessorProfiles, (void**)&pProfiles);
    if (SUCCEEDED(hr)) {
        hr = pProfiles->Register(CLSID_FraiIME);
        if (SUCCEEDED(hr)) {
            // Add English Language Profile
            hr = pProfiles->AddLanguageProfile(CLSID_FraiIME, 0x0409, GUID_FraiProfile, c_szDescription, (ULONG)wcslen(c_szDescription), NULL, 0, 0);
        }
        pProfiles->Release();
    }
    return hr;
}

STDAPI DllUnregisterServer() {
    // Unregister from TSF
    ITfInputProcessorProfiles *pProfiles;
    HRESULT hr = CoCreateInstance(CLSID_TF_InputProcessorProfiles, NULL, CLSCTX_INPROC_SERVER, IID_ITfInputProcessorProfiles, (void**)&pProfiles);
    if (SUCCEEDED(hr)) {
        pProfiles->Unregister(CLSID_FraiIME);
        pProfiles->Release();
    }

    // Regular COM Unreg (Skipped implementation for brevity, typically deletes Registry keys)
    return S_OK;
}
