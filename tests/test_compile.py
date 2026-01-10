import pytest
import subprocess
import os.path
import time

from lib.serial_monitor import SerialReaderWriter

def flash_gdb(firmware_path):
    command = f"gdb-multiarch -f {firmware_path}"
    this_directory = os.path.dirname(__file__)
    print(f"flashing {firmware_path} with cwd as: {this_directory} using gdb-multiarch")
    result = subprocess.run(
        command,
        cwd=this_directory,
        shell=True
    )
    print(f"result from gdb: {result.returncode}")


@pytest.mark.parametrize("binary_file", 
    [
        "/home/developer/workspace/tests/build/Debug/Examples/Board_Init/basic_board_example.elf",
        "/home/developer/workspace/tests/build/Release/Examples/Board_Init/basic_board_example.elf",
        "/home/developer/workspace/tests/build/RelWithDebInfo/Examples/Board_Init/basic_board_example.elf",
        "/home/developer/workspace/tests/build/MinSizeRel/Examples/Board_Init/basic_board_example.elf",
    ])
def test_echo(compile, binary_file):
    ser = SerialReaderWriter()
    ser.createRxThread()
    flash_gdb(binary_file)
    
    time.sleep(1)
    ser.serial.write("hello from pytest\n".encode("utf-8"))
    time.sleep(5)
    ser.stopRxThread()

    with open("logfile.txt", "r") as f:
        for l in f.readlines(-1):
            print(l)
            if l.strip() == "hello from pytest":
                print("echo successful")
    
