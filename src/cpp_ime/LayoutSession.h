#pragma once
#include <msctf.h>

struct CaretPosition {
    long x;
    long y;
    long h;
};

class LayoutSession : public ITfEditSession {
public:
    LayoutSession(ITfContext* context, TfClientId tid, CaretPosition* outPos);
    virtual ~LayoutSession();

    // IUnknown
    STDMETHODIMP QueryInterface(REFIID riid, void **ppvObj);
    STDMETHODIMP_(ULONG) AddRef(void);
    STDMETHODIMP_(ULONG) Release(void);

    // ITfEditSession
    STDMETHODIMP DoEditSession(TfEditCookie ec);

private:
    long _cRef;
    ITfContext* _context;
    TfClientId _tid;
    CaretPosition* _outPos;
};
