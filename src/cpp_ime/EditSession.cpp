#include "EditSession.h"

EditSession::EditSession(ITfContext* context, const std::wstring& text, int deleteBackCount)
    : _cRef(1), _context(context), _text(text), _deleteBackCount(deleteBackCount) {
    _context->AddRef();
}

EditSession::~EditSession() {
    _context->Release();
}

STDMETHODIMP EditSession::QueryInterface(REFIID riid, void **ppvObj) {
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

STDMETHODIMP_(ULONG) EditSession::AddRef(void) {
    return InterlockedIncrement(&_cRef);
}

STDMETHODIMP_(ULONG) EditSession::Release(void) {
    long cr = InterlockedDecrement(&_cRef);
    if (cr == 0) delete this;
    return cr;
}

STDMETHODIMP EditSession::DoEditSession(TfEditCookie ec) {
    ITfRange* pRange = NULL;
    TF_SELECTION tfSelection;
    ULONG cFetched;

    // Get current selection (insertion point)
    if (FAILED(_context->GetSelection(ec, TF_DEFAULT_SELECTION, 1, &tfSelection, &cFetched)))
        return E_FAIL;

    pRange = tfSelection.range;

    // Adjust range to cover the word to be replaced
    // e.g., if deleteBackCount is 3 ("teh"), we move start back 3 chars.
    if (_deleteBackCount > 0) {
        long shifted = 0;
        pRange->ShiftStart(ec, -_deleteBackCount, &shifted, NULL);
    }

    // Replace text
    pRange->SetText(ec, 0, _text.c_str(), _text.length());

    pRange->Release();
    return S_OK;
}
