cmake_minimum_required(VERSION 3.16)
project(board_init LANGUAGES C CXX ASM)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

# Collect all source files
set(SOURCES
    main.c
    syscalls.c              #newlib-stuff
    stm32f7xx_it.c          #interrupt handlers
    stm32f7xx_hal_msp.c
    sysmem.c
)

add_executable(${PROJECT_NAME} ${SOURCES})

target_link_libraries(${PROJECT_NAME} PRIVATE
    STM32F7xx_CMSIS_Device      #startup files
)

target_link_options(${PROJECT_NAME}
    PUBLIC "-T/home/developer/workspace/Examples/simple_main/STM32F767ZITX_FLASH.ld"
    PUBLIC "-T/home/developer/workspace/Examples/simple_main/STM32F767ZITX_RAM.ld"
    PUBLIC "-Wl,-Map=${PROJECT_NAME}.map"       #export map after linking, useful for debugging
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

target_link_libraries(${PROJECT_NAME} PRIVATE
    # Add necessary libraries here, e.g., HAL, CMSIS, etc.
    STM32F7xx_HAL_Driver
    CMSISCore
    STM32F7xx_CMSIS_Device
    hal_config
    ST_BSP
)
