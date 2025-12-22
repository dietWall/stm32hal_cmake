
#include "systick_config.h"
#include "stm32f7xx_hal_def.h"
#include "stm32f7xx_hal.h"


int systick_setup(systick_configuration* config)
{
    if(config == NULL)
    {
        return -1;
    }

    //HAL_SYSTICK_CLKSourceConfig is declared void.. no return value, 
    //wrap it in a if
    if(config->clocksource == SYSTICK_CLKSOURCE_HCLK || config->clocksource == SYSTICK_CLKSOURCE_HCLK_DIV8)
    {
        HAL_SYSTICK_CLKSourceConfig(config->clocksource); 
    }
    else
    {
        return -1;
    }
    
    HAL_StatusTypeDef result = HAL_InitTick(0);
    
    HAL_NVIC_EnableIRQ(SysTick_IRQn);
    
    if(result == HAL_OK)
    {
        return 0;
    }
    else
    {
        return 1;
    }
}