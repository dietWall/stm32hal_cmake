# stm32hal_cmake
This repo adds cmake files to the STM32F7XX_HAL Library in order to be able to create a static library with CMake and make. Additionally, it provides a devcontainer definition and an example Application based on the HAL Library.  
The goal is to provide a simple build process integration of a STM32 Application in a CI/CD pipeline and enable Hardware in the Loop Testing for my hobby projects.

The compilation process asumes the repository is opened within the image from https://github.com/dietWall/arm_none_eabi_dockerimage. Please follow the instructions provided in this repo first. Once the docker image is existing on your PC, you can progress with the setup described here.

# Usage
To compile the library you need to install:
- Windows with WSL and docker integration
- A Linux PC with docker
- git
- VsCode with devcontainer extension, Additional extensions will be installed in the setup process

- checkout the repository
```bash
git clone https://github.com/dietWall/stm32hal_cmake && cd stm32hal_cmake
```
- update the submodules
```bash
git submodule init && git submodule update --recursive
```
- open the directory with VsCode:
```bash
code .
```
VsCode should ask you if you want to reopen the directory in a container. If not, press F1 and type Reopen in Container.
Once inside the container, VsCode should configure the project already.


# ST Libraries:
HAL consists of 3 main libraries  
- STMF7xx_CMSIS_Device: describes the CMSIS features for the device  
- ST_BSP: contains the board support package for different STM32 developer boards  
- STM32F7xx_HAL_Driver: contains the actual hardware abstraction layer and drivers  

There are more middleware/drivers included as submodules, but I didn´t need them yet. So they are not included in the CMake file. If you need some of them, please contact me, we can talk about that.    
Due to usage of the libs as git submodules, the main CMakeLists.txt contains all the libs declarations in one file. (I wished I found a way to make use of the cmake include hierarchy without actually changing submodules.). However, the example application and HAL config have their own CMake files.

# Example Project:
The Example directory contains a simple CMake-based example application from ST. You can explore the project structure and CMake Files there as a starting point to write another applications.

The HAL Library needs a compile-time configuration file. This file for the example project can be found in repo_root/hal_config/
This file is built into an Header-Only static library. The application and HAL-Libs are the linked together within the build process.

