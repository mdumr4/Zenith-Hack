// FraiTextService.h
#pragma once
#include <msctf.h>

class FraiTextService : public ITfTextInputProcessor {
public:
    // IUnknown methods
    STDMETHODIMP QueryInterface(REFIID riid, void **ppvObj);
    STDMETHODIMP_(ULONG) AddRef(void);
    STDMETHODIMP_(ULONG) Release(void);

    // ITfTextInputProcessor methods
    STDMETHODIMP Activate(ITfThreadMgr *ptim, TfClientId tid);
    STDMETHODIMP Deactivate();

private:
    long _cRef;
    ITfThreadMgr *_pThreadMgr;
    TfClientId _tfClientId;
};
