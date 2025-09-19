cmake_minimum_required(VERSION 3.14)
project(hal_config_header_only LANGUAGES CXX)

# Specify the include directory
set(HAL_CONFIG_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/include")

# Create the header-only library
add_library(hal_config INTERFACE)
target_include_directories(hal_config INTERFACE ${HAL_CONFIG_INCLUDE_DIR})

# Optionally, install the header files and the target
install(DIRECTORY ${HAL_CONFIG_INCLUDE_DIR}/ DESTINATION include)
install(TARGETS hal_config EXPORT hal_configTargets)