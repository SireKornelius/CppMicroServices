if(US_BUILD_TESTING AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/unittest/CMakeLists.txt")
  add_subdirectory(unittest)
endif()