import pytest
import subprocess
import os.path


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

def test_output(compile):
    print("")
    print("test")

def test_output2(compile):
    print("")
    print("test2")


def test3(compile):
    file = "/home/developer/workspace/tests/build/Debug/Examples/Board_Init/basic_board_example.elf"
    flash_gdb(file)