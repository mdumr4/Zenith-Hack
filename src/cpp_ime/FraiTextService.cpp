// FraiTextService.cpp
#include "FraiTextService.h"
#include "Globals.h"
#include "BridgeClient.h"
#include "EditSession.h"
#include "LayoutSession.h"
#include "Logger.h"
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
    // Check for Ctrl+Space (Global Hotkey)
    // Using Ctrl+Space instead of Alt+Space (which is reserved for System Menu)
    if (wParam == VK_SPACE && (GetKeyState(VK_CONTROL) & 0x8000)) {
        *pfEaten = TRUE;
        return S_OK;
    }

    *pfEaten = FALSE;
    return S_OK;
}

// Helper to get preceding text (context)
std::wstring _GetTextContext(ITfContext *pic, TfClientId tid) {
    std::wstring context = L"";
    if (!pic) return context;

    ReadSession* pReadSession = new ReadSession(pic, &context);
    HRESULT hr;
    // Request read-only sync session
    pic->RequestEditSession(tid, pReadSession, TF_ES_SYNC | TF_ES_READ, &hr);
    pReadSession->Release();

    return context;
}



// Helper to get caret position
CaretPosition _GetCaretPosition(ITfContext *pic, TfClientId tid) {
    CaretPosition pos = {0, 0, 0};
    if (!pic) return pos;

    LayoutSession* pLayoutSession = new LayoutSession(pic, tid, &pos);
    HRESULT hr;
    // Request read-only sync session
    pic->RequestEditSession(tid, pLayoutSession, TF_ES_SYNC | TF_ES_READ, &hr);
    pLayoutSession->Release();

    return pos;
}

STDMETHODIMP FraiTextService::OnKeyDown(ITfContext *pic, WPARAM wParam, LPARAM lParam, BOOL *pfEaten) {
    // DEBUG LOGGING
    WriteLog("FraiIME::OnKeyDown: %llu\n", wParam);

    // Global Hotkey: Ctrl + Space -> Trigger Chat Plan Mode
    // 999 is our magic keycode for "Show Chat"
    if (wParam == VK_SPACE && (GetKeyState(VK_CONTROL) & 0x8000)) {
        WriteLog("Hotkey: Ctrl+Space Detected. Sending Magic Key 999.\n");
        BridgeClient::SendAsync(999, L"", 0, 0, 0);
        *pfEaten = TRUE;
        return S_OK;
    }

    // Logic: If Backspace, check Undo Stack
    if (wParam == VK_BACK) {
        if (_undoStack.TryUndo(pic, _tfClientId)) {
            *pfEaten = TRUE; // We handled it (reverted text), so eat the backspace
            return S_OK;
        }
    }

    // Get Context
    std::wstring context = _GetTextContext(pic, _tfClientId);

    // Get Caret Position
    CaretPosition caret = _GetCaretPosition(pic, _tfClientId);
    WriteLog("Caret: x=%ld, y=%ld, h=%ld\n", caret.x, caret.y, caret.h);

    // Synchronous Bridge for "Action Keys" (Space, Enter, Tab)
    if (wParam == VK_SPACE || wParam == VK_RETURN || wParam == VK_TAB) {
        BridgeAction action = BridgeClient::SendSync((int)wParam, context, caret.x, caret.y, caret.h);

        WriteLog("Bridge Response: Action=%s, Text=%s, Range=[%d, %d]\n",
            action.type.c_str(), action.text.c_str(), action.rangeStart, action.rangeEnd);

        if (action.type == "replace" || action.type == "accept") {
             // Convert text to wstring
             int size_needed = MultiByteToWideChar(CP_UTF8, 0, &action.text[0], (int)action.text.size(), NULL, 0);
             std::wstring wText(size_needed, 0);
             MultiByteToWideChar(CP_UTF8, 0, &action.text[0], (int)action.text.size(), &wText[0], size_needed);

             // Calculate delete count (absolute value of negative start range)
             int deleteBack = abs(action.rangeStart);

             // Execute Edit Session
             // Pass undo stack to EditSession so it can record the change safely
             EditSession* pEditSession = new EditSession(pic, wText, deleteBack, &_undoStack);
             HRESULT hrSession;
             pic->RequestEditSession(_tfClientId, pEditSession, TF_ES_SYNC | TF_ES_READWRITE, &hrSession);
             pEditSession->Release();

             // If we accepted ghost text (TAB), we must consume the key so it doesn't insert a real Tab
             if (action.type == "accept") {
                 *pfEaten = TRUE;
                 return S_OK;
             }
        }
    }
    else {
        // Async for typing (Ghost Text generation)
        BridgeClient::SendAsync((int)wParam, context, caret.x, caret.y, caret.h);
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
