#include "LayoutSession.h"

LayoutSession::LayoutSession(ITfContext* context, TfClientId tid, CaretPosition* outPos)
    : _cRef(1), _context(context), _tid(tid), _outPos(outPos) {
    _context->AddRef();
}

LayoutSession::~LayoutSession() {
    _context->Release();
}

STDMETHODIMP LayoutSession::QueryInterface(REFIID riid, void **ppvObj) {
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

STDMETHODIMP_(ULONG) LayoutSession::AddRef(void) {
    return InterlockedIncrement(&_cRef);
}

STDMETHODIMP_(ULONG) LayoutSession::Release(void) {
    long cr = InterlockedDecrement(&_cRef);
    if (cr == 0) delete this;
    return cr;
}

STDMETHODIMP LayoutSession::DoEditSession(TfEditCookie ec) {
    TF_SELECTION tfSelection;
    ULONG cFetched;

    // Get Selection
    if (FAILED(_context->GetSelection(ec, TF_DEFAULT_SELECTION, 1, &tfSelection, &cFetched)))
        return E_FAIL;

    ITfContextView* pView = NULL;
    if (SUCCEEDED(_context->GetActiveView(&pView))) {
        RECT rc;
        BOOL fClipped;
        // Get Text Extent of the selection Range
        // If selection is empty (caret), this returns the caret position.
        if (SUCCEEDED(pView->GetTextExt(ec, tfSelection.range, &rc, &fClipped))) {
             _outPos->x = rc.right; // End of selection/caret
             _outPos->y = rc.top;   // Top of line
             _outPos->h = rc.bottom - rc.top; // Height
        }
        pView->Release();
    }

    tfSelection.range->Release();
    return S_OK;
}
