cmake_minimum_required(VERSION 3.10)
project(FraiIME)

set(CMAKE_CXX_STANDARD 17)

add_library(FraiIME SHARED
    src/cpp_ime/DllMain.cpp
    src/cpp_ime/FraiTextService.cpp
    src/cpp_ime/KeyHandler.cpp
    src/cpp_ime/AutoCorrect.cpp
    src/cpp_ime/BridgeClient.cpp
)

target_link_libraries(FraiIME PRIVATE "ws2_32" "winhttp")

# Define the exports
set_target_properties(FraiIME PROPERTIES SUFFIX ".dll")
