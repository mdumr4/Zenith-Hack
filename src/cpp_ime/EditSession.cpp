#include "EditSession.h"
#include "AutoCorrect.h"
#include "Logger.h"

EditSession::EditSession(ITfContext* context, const std::wstring& text, int deleteBackCount, AutoCorrectStack* pUndoStack)
    : _cRef(1), _context(context), _text(text), _deleteBackCount(deleteBackCount), _pUndoStack(pUndoStack) {
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

    // Adjust range
    if (_deleteBackCount > 0) {
        long shifted = 0;
        HRESULT hrShift = pRange->ShiftStart(ec, -_deleteBackCount, &shifted, NULL);
        WriteLog("EditSession: Requested Shift -%d. Result HR=%X, Shifted=%ld\n", _deleteBackCount, hrShift, shifted);
    }

    // Save for Undo (Before we destroy it)
    if (_pUndoStack) {
        // Read the text we are about to replace ("teh")
        WCHAR buf[256];
        ULONG cch = 0;
        if (SUCCEEDED(pRange->GetText(ec, 0, buf, 255, &cch))) {
            buf[cch] = '\0';
            _pUndoStack->Push(pRange, buf);

            // Convert to UTF-8 for logging
            char utf8[256];
            WideCharToMultiByte(CP_UTF8, 0, buf, -1, utf8, 256, NULL, NULL);
            WriteLog("EditSession: Saved Undo Text='%s'\n", utf8);
        } else {
             WriteLog("EditSession: Failed to read text for Undo.\n");
        }
    }

    // Replace text
    pRange->SetText(ec, 0, _text.c_str(), _text.length());

    // CRITICAL FIX: Move cursor to end of inserted text
    pRange->Collapse(ec, TF_ANCHOR_END);
    TF_SELECTION sel;
    sel.range = pRange;
    sel.style.ase = TF_AE_NONE;
    sel.style.fInterimChar = FALSE;
    _context->SetSelection(ec, 1, &sel);

    pRange->Release();
    return S_OK;
}

// --------------------------------------------------------
// ReadSession Implementation
// --------------------------------------------------------

ReadSession::ReadSession(ITfContext* context, std::wstring* outText)
    : _cRef(1), _context(context), _outText(outText) {
    _context->AddRef();
}

ReadSession::~ReadSession() {
    _context->Release();
}

STDMETHODIMP ReadSession::QueryInterface(REFIID riid, void **ppvObj) {
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

STDMETHODIMP_(ULONG) ReadSession::AddRef(void) {
    return InterlockedIncrement(&_cRef);
}

STDMETHODIMP_(ULONG) ReadSession::Release(void) {
    long cr = InterlockedDecrement(&_cRef);
    if (cr == 0) delete this;
    return cr;
}

STDMETHODIMP ReadSession::DoEditSession(TfEditCookie ec) {
    TF_SELECTION tfSelection;
    ULONG cFetched;

    // Use the cookie!
    if (FAILED(_context->GetSelection(ec, TF_DEFAULT_SELECTION, 1, &tfSelection, &cFetched)))
        return E_FAIL;

    ITfRange* pRange = tfSelection.range;

    // Clone
    ITfRange* pRangeContext;
    if (SUCCEEDED(pRange->Clone(&pRangeContext))) {
        long shifted = 0;
        pRangeContext->ShiftStart(ec, -50, &shifted, NULL);

        WCHAR buf[256];
        ULONG cchCopied = 0;
        if (SUCCEEDED(pRangeContext->GetText(ec, TF_TF_MOVESTART, buf, 50, &cchCopied))) {
             buf[cchCopied] = '\0';
             *_outText = buf;
        }
        pRangeContext->Release();
    }

    pRange->Release();
    return S_OK;
}
