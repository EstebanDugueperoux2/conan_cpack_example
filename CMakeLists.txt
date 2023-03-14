cmake_minimum_required(VERSION 3.15)
project(conan_cpack_example CXX)

set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -Wall -Wextra -fcompare-debug-second")

# Turn on automatic invocation of the MOC, UIC & RCC
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Core)

set(target conan_cpack_example)

add_executable(${target} src/main.cpp)

target_link_libraries(${target} Qt6::Core)


install(TARGETS ${target} RUNTIME_DEPENDENCIES DESTINATION "."
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        )

# install(RUNTIME_DEPENDENCY_SET ${target}
# RUNTIME_DEPENDENCY_SET dependencies
# LIBRARY
#         DESTINATION "lib"
        
# )

# install(IMPORTED_RUNTIME_ARTIFACTS "Qt6::Core")

set(CPACK_GENERATOR "RPM;DEB")
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Me")
include(CPack)
