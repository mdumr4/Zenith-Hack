// AutoCorrect.cpp
#include "AutoCorrect.h"
#include "UndoSession.h"
#include <stdio.h>

AutoCorrectStack::AutoCorrectStack() {}

AutoCorrectStack::~AutoCorrectStack() {
    // Release all held ranges
    for (auto& action : _stack) {
        if (action.pRange) action.pRange->Release();
    }
    _stack.clear();
}

void AutoCorrectStack::Push(ITfRange* pRange, const std::wstring& original) {
    UndoAction action;
    action.originalText = original;
    action.timestamp = GetTickCount();

    // Clone the range so we persist it
    if (SUCCEEDED(pRange->Clone(&action.pRange))) {
        _stack.push_back(action);

        // Keep stack small (Last 5 actions)
        if (_stack.size() > 5) {
            _stack.front().pRange->Release();
            _stack.erase(_stack.begin());
        }
    }
}

BOOL AutoCorrectStack::TryUndo(ITfContext* pContext, TfClientId tid) {
    if (_stack.empty()) return FALSE;

    UndoAction& top = _stack.back();
    DWORD now = GetTickCount();

    // 1. Time Check: Must be within 5000ms (Increased for testing)
    if (now - top.timestamp > 5000) {
        // Too old, clear stack
        for (auto& a : _stack) a.pRange->Release();
        _stack.clear();
        return FALSE;
    }

    // 2. Perform Undo (Restore original text)
    // Create Undo Session
    UndoSession* pUndoSession = new UndoSession(pContext, top.pRange, top.originalText);
    HRESULT hr;
    pContext->RequestEditSession(tid, pUndoSession, TF_ES_SYNC | TF_ES_READWRITE, &hr);
    pUndoSession->Release();

    OutputDebugStringA("FraiIME: UNDO TRIGGERED! Reverting text.\n");

    // Cleanup
    top.pRange->Release();
    _stack.pop_back();

    return TRUE;
}
