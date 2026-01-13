// AutoCorrect.h
#pragma once
#include <windows.h>
#include <msctf.h>
#include <string>
#include <vector>

struct UndoAction {
    std::wstring originalText;
    ITfRange* pRange; // Range object covering the replaced text
    DWORD timestamp;
};

class AutoCorrectStack {
public:
    AutoCorrectStack();
    ~AutoCorrectStack();

    // Push an action when we perform an auto-correct
    void Push(ITfRange* pRange, const std::wstring& original);

    // Try to undo the last action if it was recent
    // Returns TRUE if an undo was performed
    BOOL TryUndo(ITfContext* pContext, TfClientId tid);

private:
    std::vector<UndoAction> _stack;
};
