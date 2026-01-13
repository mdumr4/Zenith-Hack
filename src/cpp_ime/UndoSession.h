#pragma once
#include <msctf.h>
#include <string>

class UndoSession : public ITfEditSession {
public:
    UndoSession(ITfContext* context, ITfRange* range, const std::wstring& text);
    virtual ~UndoSession();

    // IUnknown
    STDMETHODIMP QueryInterface(REFIID riid, void **ppvObj);
    STDMETHODIMP_(ULONG) AddRef(void);
    STDMETHODIMP_(ULONG) Release(void);

    // ITfEditSession
    STDMETHODIMP DoEditSession(TfEditCookie ec);

private:
    long _cRef;
    ITfContext* _context;
    ITfRange* _range;
    std::wstring _text;
};
