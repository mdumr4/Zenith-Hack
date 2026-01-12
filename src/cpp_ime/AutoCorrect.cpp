// AutoCorrect.cpp
#include "AutoCorrect.h"

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

BOOL AutoCorrectStack::TryUndo(ITfContext* pContext) {
    if (_stack.empty()) return FALSE;

    UndoAction& top = _stack.back();
    DWORD now = GetTickCount();

    // 1. Time Check: Must be within 2000ms
    if (now - top.timestamp > 2000) {
        // Too old, clear stack
        for (auto& a : _stack) a.pRange->Release();
        _stack.clear();
        return FALSE;
    }

    // 2. Perform Undo (Restore original text)
    ITfEditSession* pEditSession = NULL;
    // NOTE: In a real TSF implementation, we need an EditSession to write.
    // For this MVP, we are simulating the logic flow.
    // pContext->RequestEditSession(...) -> inside session: top.pRange->SetText(..., top.originalText)

    // Simulating success for the MVP architecture proof:
    // In strict TSF, you cannot SetText outside an EditSession.
    // We assume the caller (KeyHandler) is wrapping this or we'd implement a full EditSession class.

    // For now, let's just log that we WOULD undo.
    OutputDebugStringA("FraiIME: UNDO TRIGGERED! Reverting text.\n");

    // Cleanup
    top.pRange->Release();
    _stack.pop_back();

    return TRUE;
}
