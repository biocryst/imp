# Autogenerated file, run build/tools/setup_cmake.py to regenerate

if (${IMP_USE_CUSTOM_CXX_FLAGS})
set(CMAKE_REQUIRED_FLAGS ${IMP_BIN_CXX_FLAGS})
endif()

INCLUDE (CheckCXXSourceCompiles)

CHECK_CXX_SOURCE_COMPILES("/**
 *  ile nothing.cpp
 *  rief nothing
 *
 *  Copyright 2007-2013 IMP Inventors. All rights reserved.
 *
 */

#define MY_MACRO _Pragma (\"warn pointless warning\")

MY_MACRO

int main()
{
  return 0;
}

"
 IMP_COMPILER_HAS_PRAGMA)

if(${IMP_COMPILER_HAS_PRAGMA} MATCHES 1)
set(IMP_COMPILER_HAS_PRAGMA 1 CACHE INTERNAL "" FORCE )
else()
set(IMP_COMPILER_HAS_PRAGMA 0 CACHE INTERNAL "" FORCE)
endif()