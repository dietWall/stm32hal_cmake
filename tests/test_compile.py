import pytest
import subprocess
import os.path
import time

from lib.serial_monitor import SerialReaderWriter


class Test_Uart:
    def test_echo(self, compile,flash_binary_file,log_to_file, build_type):
        print("")           # newline
        print("###################################################") 
        gdb_log_file = None

        if log_to_file == True:
            from conftest import log_directory
            gdb_log_file = f"{log_directory(build_type)}/gdb-multiarch.txt"
        # serial logfile has always to be used for asserts
        serial_logfile = f"{log_directory(build_type)}/uart_log.txt"

        ser = SerialReaderWriter(logfile=serial_logfile)
        ser.createRxThread()
        time.sleep(1)   #let firmware initialize
        ser.serial.write("hello from pytest\n".encode("utf-8"))
        time.sleep(1)   # let device response
        ser.stopRxThread()

        with open(serial_logfile, "r") as f:
            uart_output = f.readlines()
            for l in uart_output:
                print(f"analyzing: {l.strip()}")
                if l.strip() == "hello from pytest":
                    print("echo successful")
        print("###################################################") 
    
    def test_2(self, build_type):
        print(build_type)

    def test_3(self, build_type):
        print(build_type)
