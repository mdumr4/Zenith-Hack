#include "UndoSession.h"

UndoSession::UndoSession(ITfContext* context, ITfRange* range, const std::wstring& text)
    : _cRef(1), _context(context), _range(range), _text(text) {
    _context->AddRef();
    _range->AddRef();
}

UndoSession::~UndoSession() {
    _context->Release();
    _range->Release();
}

STDMETHODIMP UndoSession::QueryInterface(REFIID riid, void **ppvObj) {
    if (ppvObj == NULL) return E_INVALIDARG;
    *ppvObj = NULL;
    if (IsEqualIID(riid, IID_IUnknown) || IsEqualIID(riid, IID_ITfEditSession)) {
        *ppvObj = (ITfEditSession *)this;
    } else {
        return E_NOINTERFACE;
    }
    AddRef();
    return S_OK;
}

STDMETHODIMP_(ULONG) UndoSession::AddRef(void) {
    return InterlockedIncrement(&_cRef);
}

STDMETHODIMP_(ULONG) UndoSession::Release(void) {
    long cr = InterlockedDecrement(&_cRef);
    if (cr == 0) delete this;
    return cr;
}

STDMETHODIMP UndoSession::DoEditSession(TfEditCookie ec) {
    // Restore text
    _range->SetText(ec, 0, _text.c_str(), _text.length());

    // Move cursor to end of restored text
    _range->Collapse(ec, TF_ANCHOR_END);
    TF_SELECTION sel;
    sel.range = _range;
    sel.style.ase = TF_AE_NONE;
    sel.style.fInterimChar = FALSE;
    _context->SetSelection(ec, 1, &sel);

    return S_OK;
}
