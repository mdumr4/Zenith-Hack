#pragma once
#include <windows.h>
#include <stdio.h>

inline void WriteLog(const char* format, ...) {
    FILE* f = nullptr;
    fopen_s(&f, "C:\\Users\\Public\\frai_debug.txt", "a");
    if (f) {
        va_list args;
        va_start(args, format);
        vfprintf(f, format, args);
        va_end(args);
        fclose(f);
    }
}
