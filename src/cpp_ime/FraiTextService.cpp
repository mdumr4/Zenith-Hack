// FraiTextService.cpp
#include "FraiTextService.h"
#include "Globals.h"
#include <stdio.h>

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

    // TODO: Send to Python Bridge here!

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
