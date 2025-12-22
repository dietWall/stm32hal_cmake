#ifndef SYSTIC_CONFIG_H
#define SYSTIC_CONFIG_H

#include <stdint.h>

#include "stm32f7xx_hal_cortex.h"

typedef enum
{
    //order is defined by underlying integer values
    hclk_div8_clock = SYSTICK_CLKSOURCE_HCLK_DIV8,
    hclk_clock = SYSTICK_CLKSOURCE_HCLK
}systic_sources;

typedef struct 
{
    systic_sources clocksource;         //SYSTICK_CLKSOURCE_HCLK || SYSTICK_CLKSOURCE_HCLK_DIV8
    uint32_t ticks;                     //counter for systick, max: 16777215
}systick_configuration;

/**
 * Simple initialization for systick handler
 * declare systick_configuration, call this function and it will be done
 * returns:
 * -1: parameter error, either config null or clock sources invalid
 * 0: success
 * 1: ticks is out of range
 */
int systick_setup(systick_configuration* config);

#endif //SYSTIC_CONFIG_H