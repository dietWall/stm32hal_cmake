
# Minimal Executable for Debugging

## Overview
This Directory contains the simplest possible executable for a STM32F767, which we can run on the device.
The goal is to take care of debug configurations, network and don´t be confused with linking/compiler issues.
There is a debug configuration called docker_host|openocd:simple_main in .vscode/launch.json for this executable. If everything is setup correctly it should be possible to start a debugging session with this configuration.


## Installation
You need openocd>=0.12 to be installed on your linux docker host (available from apt in Ubuntu 24.04 on my setup).  
openocd needs to be running with:

```
openocd -f /usr/share/openocd/scripts/interface/stlink.cfg -f /usr/share/openocd/scripts/target/stm32f7x.cfg -f ~/openocd.cfg
```

The configuration files in /usr/share come with openocd installation
The file ~/openocd.cfg was created manually and contains a singe line:  
bindto 0.0.0.0

Tools in your devcontainer should be available without manual actions (in theory, I keep forgetting to modify the image)

The project is configured for the NUCLEO-F767ZI board. https://os.mbed.com/platforms/ST-Nucleo-F767ZI/  
It needs to be connected via USB to your docker/debugging host with openocd. 


## Usage
there are still few hardcoded things to configure (IP/Hostname, Ports, etc), but in general you can:

- compile the project from the repo root directory, this executable is within the cmake tree and is created automatically
- in vscode: press Run And Debug on the left side
- select docker_host|openocd:simple_main in the debug configuration
- press run
- single step through startup and initialization process, untill you get to the main function


