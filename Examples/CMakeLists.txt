cmake_minimum_required(VERSION 3.16)

project(example_project LANGUAGES CXX C)

#this directory contains mutliple applications, to verify different functionalities#
#with simple_main you can verify that the toolchain and debugging works as expected

#board_init extends this by including board initialization. with this you can verify
#that the board is working as expected and see how to use the drivers
#also the goal is here to provide as many different peripherals as possible 
#and test them out without the need of threads/tasks and more


add_subdirectory(simple_main)
add_subdirectory(board_init)