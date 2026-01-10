import pytest
import subprocess
import os.path
import time

from lib.serial_monitor import SerialReaderWriter

def flash_gdb(firmware_path: str, log_file: str | None) -> int:
    command = f"gdb-multiarch -f {firmware_path}"
    this_directory = os.path.dirname(__file__)

    print(f"gdb command: {command}")
    print(f"firmware: {firmware_path}")
    print(f"cwd: {this_directory}")
    print(f"logfile: {log_file}")
    
    log_file_desc = None
    if log_file != None:
        log_file_desc = open(log_file, "w")

    result = subprocess.run(
        command,
        cwd=this_directory,
        shell=True,
        stdout=log_file_desc, stderr=log_file_desc
    )
    print(f"result from gdb: {result.returncode}")
    return result.returncode


@pytest.mark.parametrize("binary_file,build_type", [
        ("/home/developer/workspace/tests/build/Debug/Examples/Board_Init/basic_board_example.elf", "Debug"),
        ("/home/developer/workspace/tests/build/Release/Examples/Board_Init/basic_board_example.elf", "Release"),
        ("/home/developer/workspace/tests/build/RelWithDebInfo/Examples/Board_Init/basic_board_example.elf", "RelWithDebInfo"),
        ("/home/developer/workspace/tests/build/MinSizeRel/Examples/Board_Init/basic_board_example.elf", "MinSizeRel")
    ]
    )
def test_echo(compile, binary_file, log_to_file, build_type):
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
    flash_gdb(binary_file, gdb_log_file)
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
    
