#pragma once
#include <msctf.h>
#include <string>

class AutoCorrectStack;

class EditSession : public ITfEditSession {
public:
    EditSession(ITfContext* context, const std::wstring& text, int deleteBackCount, AutoCorrectStack* pUndoStack = nullptr);
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
    AutoCorrectStack* _pUndoStack;
};

class ReadSession : public ITfEditSession {
public:
    ReadSession(ITfContext* context, std::wstring* outText);
    virtual ~ReadSession();

    // IUnknown
    STDMETHODIMP QueryInterface(REFIID riid, void **ppvObj);
    STDMETHODIMP_(ULONG) AddRef(void);
    STDMETHODIMP_(ULONG) Release(void);

    // ITfEditSession
    STDMETHODIMP DoEditSession(TfEditCookie ec);

private:
    long _cRef;
    ITfContext* _context;
    std::wstring* _outText;
};
