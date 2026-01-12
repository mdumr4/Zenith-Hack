// FraiTextService.h
#pragma once
#include <windows.h>
#include <msctf.h>
#include "AutoCorrect.h"

class FraiTextService : public ITfTextInputProcessor,
                        public ITfKeyEventSink {
public:
    FraiTextService();
    ~FraiTextService();

    // IUnknown methods
    STDMETHODIMP QueryInterface(REFIID riid, void **ppvObj);
    STDMETHODIMP_(ULONG) AddRef(void);
    STDMETHODIMP_(ULONG) Release(void);

    // ITfTextInputProcessor methods
    STDMETHODIMP Activate(ITfThreadMgr *ptim, TfClientId tid);
    STDMETHODIMP Deactivate();

    // ITfKeyEventSink methods
    STDMETHODIMP OnSetFocus(BOOL fForeground) { return S_OK; }
    STDMETHODIMP OnTestKeyDown(ITfContext *pic, WPARAM wParam, LPARAM lParam, BOOL *pfEaten);
    STDMETHODIMP OnKeyDown(ITfContext *pic, WPARAM wParam, LPARAM lParam, BOOL *pfEaten);
    STDMETHODIMP OnTestKeyUp(ITfContext *pic, WPARAM wParam, LPARAM lParam, BOOL *pfEaten);
    STDMETHODIMP OnKeyUp(ITfContext *pic, WPARAM wParam, LPARAM lParam, BOOL *pfEaten);
    STDMETHODIMP OnPreservedKey(ITfContext *pic, REFGUID rguid, BOOL *pfEaten) { return S_OK; }

private:
    long _cRef;
    ITfThreadMgr *_pThreadMgr;
    TfClientId _tfClientId;

    // Helpers
    BOOL _InitKeyEventSink();
    void _UninitKeyEventSink();

    AutoCorrectStack _undoStack;
};

// Global Helpers (Expected by DllMain)
void DllAddRef();
void DllRelease();
