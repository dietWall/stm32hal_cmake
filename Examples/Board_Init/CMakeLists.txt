cmake_minimum_required(VERSION 3.25)
project(basic_board_example LANGUAGES C CXX ASM)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

# Collect all source files
set(SOURCES
    Src/eth.c
    Src/gpio.c
    Src/main.c
    Src/stm32f7xx_hal_msp.c
    Src/stm32f7xx_it.c
    Src/syscalls.c              #newlib-stuff
    Src/sysmem.c
    Src/system_stm32f7xx.c
    Src/usart.c
    Src/usb_otg.c
)

add_executable(${PROJECT_NAME} ${SOURCES})

target_include_directories(${PROJECT_NAME}
    PUBLIC Inc/
)

target_link_libraries(${PROJECT_NAME} PRIVATE
    STM32F7xx_CMSIS_Device          #startup files
    STM32F7xx_HAL_Driver            #HAL drivers
)

target_link_options(${PROJECT_NAME}
    PUBLIC "-T/home/developer/workspace/Examples/simple_main/STM32F767ZITX_FLASH.ld"
    PUBLIC "-Wl,-Map=${PROJECT_NAME}.map"       #export map after linking, still required for debugging
)

target_compile_options(${PROJECT_NAME}
#todo: figure out minimum compile options
PUBLIC "-ffunction-sections"
    PUBLIC "-fdata-sections"
    PUBLIC "-Wall"
    PUBLIC "-fstack-usage"
    PUBLIC "-MMD"
    PUBLIC "-MP"
    PUBLIC "--specs=nano.specs"
    PUBLIC "-mfpu=fpv5-d16"
    PUBLIC "-mcpu=cortex-m7"
)

