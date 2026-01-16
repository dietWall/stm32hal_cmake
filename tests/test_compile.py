import pytest
import subprocess
import os.path
import time

from tcl_utils.serial_monitor import SerialReaderWriter


class Test_Uart:
    
    def log_registers(self, peripheral: str, tcl, logfile):
        registers = tcl.read_peripheral_registers(peripheral)
        for k, v in registers.items():
            logfile.write(f"Name: {k}                     value:{v}\n")


    def test_echo(self, compile, flash_binary_file, log_to_file, build_type):
        echo_message = "hello from pytest"
        print("")           # newline
        print("###################################################") 
        from conftest import log_directory, openocd_controller
        # serial logfile has always to be used for asserts
        serial_logfile = f"{log_directory(build_type)}/uart_log.txt"
        tcl = openocd_controller(host="dw-latitude-e6440",
            firmware_file=flash_binary_file, 
            map_file="/home/developer/workspace/tests/build/Debug/Examples/Board_Init/basic_board_example.map",
            )
        ser = SerialReaderWriter(logfile=serial_logfile)
        tcl.send("resume")
        initial_line = ser.receive_message()
        ser.send_message(echo_message)
        echo_line = ser.receive_message()
        if echo_line != echo_message:
            print(f"Warning: echo Line not as expected: {echo_line}")
        assert  initial_line == "Firmware initialized", f"Warning: Initial Line not as expected: {initial_line}"
        assert  echo_line == echo_message, f"Warning: echo line not as expected: {initial_line}"

    
    def test_buffer_overflow(self, compile, flash_binary_file, log_to_file, build_type):
        overflow_message = "123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
        echo_message = "hello from pytest"
        print("")           # newline

        from conftest import log_directory, openocd_controller
        
        tcl = openocd_controller(host="dw-latitude-e6440",
            firmware_file=flash_binary_file, 
            map_file="/home/developer/workspace/tests/build/Debug/Examples/Board_Init/basic_board_example.map"
            )

        reg_filename = os.path.join(log_directory(build_type=build_type), "register_dump.txt")
        register_file = open(reg_filename, "w+")

        serial_logfile = f"{log_directory(build_type)}/uart_log.txt"
        ser = SerialReaderWriter(logfile=serial_logfile)
        
        ################################
        #           Test Start         #
        ################################
        tcl.send("reset halt")
        tcl.send("resume")
        
        initial_line = ser.receive_message()
        assert  initial_line == "Firmware initialized", f"Warning: Initial Line not as expected: {initial_line}"

        ser.send_message(overflow_message)
        message = ser.receive_message()                 # this should result in a timeout

        assert message == "Error: Buffer overflow, MAX 200 characters, resetting buffer", f"Unexpected Message: {message}"
        ser.send_message(echo_message)
        echo_line = ser.receive_message()
        assert  echo_line == echo_message, f"Warning: echo line not as expected: {echo_line}"
        
