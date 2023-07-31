set(test_script TestNamespaceModScript)

if ("${CMAKE_VERSION}" VERSION_LESS "3.12.0")
  find_package(PythonInterp REQUIRED)
else()
  find_package(Python COMPONENTS Interpreter REQUIRED)
endif()

if (Python_Interpreter_FOUND) 
    message("${Python_EXECUTABLE} found")
else()
    message(FATAL "No Python interpreter found")
endif()

add_test(NAME ${test_script} 
COMMAND ${Python_EXECUTABLE} -m unittest -v
WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
set_property(TEST ${test_script} PROPERTY LABELS regular)