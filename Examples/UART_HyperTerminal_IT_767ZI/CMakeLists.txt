cmake_minimum_required(VERSION 3.16)
project(UART_HyperTerminal_IT C)

# Set source and include directories
set(SRC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/Src")
set(INC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/Inc")

# Collect all source files
set(SOURCES
    ${SRC_DIR}/main.c
    ${SRC_DIR}/stm32f7xx_it.c
    ${SRC_DIR}/stm32f7xx_hal_msp.c
    ${SRC_DIR}/system_stm32f7xx.c
    SW4STM32/syscalls.c
)

# Add executable
add_executable(${PROJECT_NAME} ${SOURCES})

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE ${INC_DIR})

target_link_libraries(${PROJECT_NAME} PRIVATE
    # Add necessary libraries here, e.g., HAL, CMSIS, etc.
    STM32F7xx_HAL_Driver
    CMSISCore
    STM32F7xx_CMSIS_Device
    hal_config
    ST_BSP
)


