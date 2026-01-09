// FraiTextService.cpp
#include "FraiTextService.h"

// TODO: Implement IUnknown and ITfTextInputProcessor methods
// This is the core engine of the IME.

STDMETHODIMP FraiTextService::Activate(ITfThreadMgr *ptim, TfClientId tid) {
    _pThreadMgr = ptim;
    _tfClientId = tid;
    return S_OK;
}

STDMETHODIMP FraiTextService::Deactivate() {
    _pThreadMgr = NULL;
    _tfClientId = TF_CLIENTID_NULL;
    return S_OK;
}
