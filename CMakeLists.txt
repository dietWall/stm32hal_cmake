cmake_minimum_required(VERSION 3.16)
project(STM32F7_HAL LANGUAGES CXX C ASM)

#temporarily taken out, taking care of launch.json and debugging configuration
# add_subdirectory(hal_config)

# add_library(STM32F7xx_HAL_Driver
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_adc.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_adc_ex.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_cortex.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_dma.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_dma_ex.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_exti.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_flash.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_flash_ex.c
#     #stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_flash_ramfunc.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_gpio.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_i2c.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_i2c_ex.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_pwr.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_pwr_ex.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_rcc.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_rcc_ex.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_spi.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_tim.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_tim_ex.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_uart.c
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_uart_ex.c
#     # Add or remove files as needed
# )
# target_link_libraries(STM32F7xx_HAL_Driver PUBLIC STM32F7xx_CMSIS_Device hal_config)
# target_include_directories(STM32F7xx_HAL_Driver PUBLIC
#     stm32f7_hal/Drivers/STM32F7xx_HAL_Driver/Inc
# )


add_library(CMSISCore INTERFACE)
target_include_directories(CMSISCore INTERFACE
    stm32f7_hal/Drivers/CMSIS/Core/Include
)

add_library(STM32F7xx_CMSIS_Device STATIC
    stm32f7_hal/Drivers/CMSIS/Device/ST/STM32F7xx/Source/Templates/gcc/startup_stm32f767xx.s
    stm32f7_hal/Drivers/CMSIS/Device/ST/STM32F7xx/Source/Templates/system_stm32f7xx.c
)

target_compile_definitions(STM32F7xx_CMSIS_Device PUBLIC STM32F767xx)
target_include_directories(STM32F7xx_CMSIS_Device PUBLIC
     stm32f7_hal/Drivers/CMSIS/Device/ST/STM32F7xx/Include
)

target_link_libraries(STM32F7xx_CMSIS_Device PUBLIC CMSISCore)
set_target_properties(STM32F7xx_CMSIS_Device PROPERTIES
    OUTPUT_NAME "stm32f7xx_cmsis_device"
)


target_compile_options(STM32F7xx_CMSIS_Device
# some of this settings are required for correct compilation of initialization code
# I can´t tell yet, which of them are required and which are not
# I guess -mcpu.. and -mfpu should be the same as in executable, 
# otherwise mcu goes into HardFault because of illegal instruction
# todo: reduce this instructions to a minimum, better: inherit this settings from executable cmake file
# or maybe even better: provide this settings with MCU selection process
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


target_link_options(STM32F7xx_CMSIS_Device
# some of this settings are required for correct selection of the newlib(-nano)
# if they are not passed, the cpu enters Hardfault before calling main function (because ld links wrong libraries)

# I can´t tell yet, which of them are required and which are not
# I guess -mcpu.. and -mfpu should be the same as in executable, 
# otherwise mcu goes into HardFault because of illegal instruction

#todo: same as in compile_definitions: provide a mcu specific cmake file? / Inherit from executable

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

#temporarily taken out, as long as taking care of debugging configuration
# add_library(ST_BSP 
#     stm32f7_hal/Drivers/BSP/STM32F7xx_Nucleo_144/stm32f7xx_nucleo_144.c
# )
# target_include_directories(ST_BSP PUBLIC
#     stm32f7_hal/Drivers/BSP/STM32F7xx_Nucleo_144
# )
# target_link_libraries(ST_BSP 
#     PUBLIC STM32F7xx_HAL_Driver
# )

add_subdirectory(Examples)