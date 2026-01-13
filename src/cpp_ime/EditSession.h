#pragma once
#include <msctf.h>
#include <string>

class EditSession : public ITfEditSession {
public:
    EditSession(ITfContext* context, const std::wstring& text, int deleteBackCount);
    virtual ~EditSession();

    // IUnknown
    STDMETHODIMP QueryInterface(REFIID riid, void **ppvObj);
    STDMETHODIMP_(ULONG) AddRef(void);
    STDMETHODIMP_(ULONG) Release(void);

    // ITfEditSession
    STDMETHODIMP DoEditSession(TfEditCookie ec);

private:
    long _cRef;
    ITfContext* _context;
    std::wstring _text;
    int _deleteBackCount;
};
