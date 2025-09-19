cmake_minimum_required(VERSION 3.16)
project(STM32F7_HAL LANGUAGES CXX C)

add_subdirectory(hal_config)

add_library(STM32F7xx_HAL_Driver
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_adc.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_adc_ex.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_cortex.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_dma.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_dma_ex.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_exti.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_flash.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_flash_ex.c
    #stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_flash_ramfunc.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_gpio.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_i2c.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_i2c_ex.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_pwr.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_pwr_ex.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_rcc.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_rcc_ex.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_tim.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_tim_ex.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_uart.c
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_uart_ex.c
    # Add or remove files as needed
)
target_link_libraries(STM32F7xx_HAL_Driver PUBLIC STM32F7xx_CMSIS_Device hal_config)
target_include_directories(STM32F7xx_HAL_Driver PRIVATE
    stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Inc
)


# Create an interface library target for header-only usage
add_library(CMSISCore INTERFACE)
# Specify the include directories for consumers of this library
target_include_directories(CMSISCore INTERFACE
    stm32f7_hal/Drivers/CMSIS/Core/Include
)

add_library(STM32F7xx_CMSIS_Device STATIC
    stm32f7_hal/Drivers/CMSIS/Device/ST/STM32F7xx/Source/Templates/gcc/startup_stm32f769xx.s
    stm32f7_hal/Drivers/CMSIS/Device/ST/STM32F7xx/Source/Templates/system_stm32f7xx.c
)

target_compile_definitions(STM32F7xx_CMSIS_Device PUBLIC STM32F769xx)
target_include_directories(STM32F7xx_CMSIS_Device PUBLIC
    stm32f7_hal/Drivers/CMSIS/Device/ST/STM32F7xx/Include
)

target_link_libraries(STM32F7xx_CMSIS_Device PUBLIC CMSISCore)
set_target_properties(STM32F7xx_CMSIS_Device PROPERTIES
    OUTPUT_NAME "stm32f7xx_cmsis_device"
)