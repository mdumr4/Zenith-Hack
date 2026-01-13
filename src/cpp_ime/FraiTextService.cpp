// FraiTextService.cpp
#include "FraiTextService.h"
#include "Globals.h"
#include "BridgeClient.h"
#include "EditSession.h"
#include <stdio.h>
#include <string>
#include <vector>

// Lifecycle
FraiTextService::FraiTextService() : _cRef(1), _pThreadMgr(NULL), _tfClientId(TF_CLIENTID_NULL) {
    DllAddRef();
}

FraiTextService::~FraiTextService() {
    DllRelease();
}

// IUnknown Implementation
STDMETHODIMP FraiTextService::QueryInterface(REFIID riid, void **ppvObj) {
    if (ppvObj == NULL) return E_INVALIDARG;
    *ppvObj = NULL;

    if (IsEqualIID(riid, IID_IUnknown) || IsEqualIID(riid, IID_ITfTextInputProcessor)) {
        *ppvObj = (ITfTextInputProcessor *)this;
    }
    else if (IsEqualIID(riid, IID_ITfKeyEventSink)) {
        *ppvObj = (ITfKeyEventSink *)this;
    }
    else {
        return E_NOINTERFACE;
    }

    AddRef();
    return S_OK;
}

STDMETHODIMP_(ULONG) FraiTextService::AddRef(void) {
    return InterlockedIncrement(&_cRef);
}

STDMETHODIMP_(ULONG) FraiTextService::Release(void) {
    long cr = InterlockedDecrement(&_cRef);
    if (cr == 0) {
        delete this;
    }
    return cr;
}

// ITfTextInputProcessor
STDMETHODIMP FraiTextService::Activate(ITfThreadMgr *ptim, TfClientId tid) {
    _pThreadMgr = ptim;
    _pThreadMgr->AddRef();
    _tfClientId = tid;

    if (!_InitKeyEventSink()) {
        return E_FAIL;
    }

    return S_OK;
}

STDMETHODIMP FraiTextService::Deactivate() {
    _UninitKeyEventSink();

    if (_pThreadMgr) {
        _pThreadMgr->Release();
        _pThreadMgr = NULL;
    }
    _tfClientId = TF_CLIENTID_NULL;
    return S_OK;
}

// ----------------------------------------------------------------------
// ITfKeyEventSink Implementation
// ----------------------------------------------------------------------

BOOL FraiTextService::_InitKeyEventSink() {
    ITfKeystrokeMgr *pKeystrokeMgr;
    if (SUCCEEDED(_pThreadMgr->QueryInterface(IID_ITfKeystrokeMgr, (void **)&pKeystrokeMgr))) {
        pKeystrokeMgr->AdviseKeyEventSink(_tfClientId, (ITfKeyEventSink *)this, TRUE);
        pKeystrokeMgr->Release();
        return TRUE;
    }
    return FALSE;
}

void FraiTextService::_UninitKeyEventSink() {
    ITfKeystrokeMgr *pKeystrokeMgr;
    if (_pThreadMgr && SUCCEEDED(_pThreadMgr->QueryInterface(IID_ITfKeystrokeMgr, (void **)&pKeystrokeMgr))) {
        pKeystrokeMgr->UnadviseKeyEventSink(_tfClientId);
        pKeystrokeMgr->Release();
    }
}

STDMETHODIMP FraiTextService::OnTestKeyDown(ITfContext *pic, WPARAM wParam, LPARAM lParam, BOOL *pfEaten) {
    // We strictly "peek" here.
    // If we want to swallow a key (like Voice Mode Trigger), we set *pfEaten = TRUE.
    *pfEaten = FALSE;
    return S_OK;
}

STDMETHODIMP FraiTextService::OnKeyDown(ITfContext *pic, WPARAM wParam, LPARAM lParam, BOOL *pfEaten) {
    // DEBUG LOGGING
    char msg[100];
    sprintf_s(msg, "FraiIME::OnKeyDown: %llu\n", wParam);
    OutputDebugStringA(msg);

    // Logic: If Backspace, check Undo Stack
    if (wParam == VK_BACK) {
        if (_undoStack.TryUndo(pic)) {
            *pfEaten = TRUE; // We handled it (reverted text), so eat the backspace
            return S_OK;
        }
    }

    // Synchronous Bridge for "Action Keys" (Space, Enter, Tab)
    if (wParam == VK_SPACE || wParam == VK_RETURN || wParam == VK_TAB) {
        BridgeAction action = BridgeClient::SendSync((int)wParam, L"");

        char log[256];
        sprintf_s(log, "Bridge Response: Action=%s, Text=%s, Range=[%d, %d]\n",
            action.type.c_str(), action.text.c_str(), action.rangeStart, action.rangeEnd);
        OutputDebugStringA(log);

        if (action.type == "replace") {
             // Convert text to wstring
             int size_needed = MultiByteToWideChar(CP_UTF8, 0, &action.text[0], (int)action.text.size(), NULL, 0);
             std::wstring wText(size_needed, 0);
             MultiByteToWideChar(CP_UTF8, 0, &action.text[0], (int)action.text.size(), &wText[0], size_needed);

             // Calculate delete count (absolute value of negative start range)
             int deleteBack = abs(action.rangeStart);

             // Execute Edit Session
             EditSession* pEditSession = new EditSession(pic, wText, deleteBack);
             HRESULT hrSession;
             pic->RequestEditSession(_tfClientId, pEditSession, TF_ES_SYNC | TF_ES_READWRITE, &hrSession);
             pEditSession->Release();
        }
    }
    else {
        // Async for typing (Ghost Text generation)
        BridgeClient::SendAsync((int)wParam, L"");
    }

    *pfEaten = FALSE; // Pass through to App
    return S_OK;
}

STDMETHODIMP FraiTextService::OnTestKeyUp(ITfContext *pic, WPARAM wParam, LPARAM lParam, BOOL *pfEaten) {
    *pfEaten = FALSE;
    return S_OK;
}

STDMETHODIMP FraiTextService::OnKeyUp(ITfContext *pic, WPARAM wParam, LPARAM lParam, BOOL *pfEaten) {
    *pfEaten = FALSE;
    return S_OK;
}
