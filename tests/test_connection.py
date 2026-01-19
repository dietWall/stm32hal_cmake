import pytest
import subprocess
import os.path
import time


from conftest import log_directory, openocd_controller


class Test_Uart:
    
    def log_registers(self, peripheral: str, tcl, logfile):
        registers = tcl.read_peripheral_registers(peripheral)
        for k, v in registers.items():
            logfile.write(f"Name: {k}                     value:{v}\n")


    def test_echo(self, openocd_controller, serial_interface):
        echo_message = "hello from pytest"
        print("")           # newline
        openocd_controller.send("reset run")
        initial_line = serial_interface.receive_message()
        serial_interface.send_message(echo_message)
        echo_line = serial_interface.receive_message()
        assert  initial_line == "Firmware initialized", f"Warning: Initial Line not as expected: {initial_line}"
        assert  echo_line == echo_message, f"Warning: echo line not as expected: {initial_line}"
        print("###################################################")

    
    def test_buffer_overflow(self, openocd_controller, serial_interface):
        overflow_message = "123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
        echo_message = "hello from pytest"
        print("")           # newline
        openocd_controller.send("reset run")
        initial_line = serial_interface.receive_message()
        assert  initial_line == "Firmware initialized", f"Warning: Initial Line not as expected: {initial_line}"
        serial_interface.send_message(overflow_message)
        message = serial_interface.receive_message()
        assert message == "Error: Buffer overflow, MAX 200 characters, resetting buffer", f"Unexpected Message: {message}"
        serial_interface.send_message(echo_message)
        echo_line = serial_interface.receive_message()
        assert  echo_line == echo_message, f"Warning: echo line not as expected: {echo_line}"
        print("###################################################")


    def test_tx_hello_switch(self, openocd_controller, serial_interface):
        openocd_controller.send("reset halt")
        serial_interface.reset_input_buffer()
        openocd_controller.send("resume")
        
        initial_line = serial_interface.receive_message()
        assert initial_line == "Firmware initialized", f"Warning: Initial Line not as expected: {initial_line}"
        
        no_message = serial_interface.receive_message()
        assert no_message == "", f"Error: unexpected message received on startup {no_message}, tx_hello is: {openocd_controller.readvar('tx_hello')}"
    
        serial_interface.send_message("tx_hello 1")
        #check response
        response_message = serial_interface.receive_message()
        assert response_message == "toggling tx_hello", f"Error: tx_hello toggling has not responded properly {response_message}"

        #firmware echoes
        echoed_message = serial_interface.receive_message()
        assert echoed_message == "tx_hello 1", f"Error: echo has not been received {echoed_message}"
        
        #check functionality
        tx_hello_message = serial_interface.receive_message()
        assert tx_hello_message == "Hello 0 from STM32F7", f"Error: tx_hello has not responded properly {tx_hello_message}"
        