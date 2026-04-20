#! /usr/bin/env python3


from repo_helper.Repo_Helper import Repo_Helper
import argparse

MOUNT="/workspace"
image="ghcr.io/dietwall/arm_gcc_image:latest"
default_container_name = "stm32hal"
test_venv = ".venv"

def start_container(container_name: str = default_container_name):
    helper = Repo_Helper()
    _, repo_root = helper.repo_root()
    command = f"docker run -d -it --name {container_name} --rm --mount type=bind,source={repo_root},dst={MOUNT} {image}"
    
    print(f"starting container")
    result, output = helper.execute(command)
    print(f"result from execute: {result.returncode}")
    if result.returncode != 0:
        print(f"Starting failed with exitcode: {result.returncode}")
        for f in output:
            print(f)
    else:
        print(f"type: ")
        print(f"docker exec -it {container_name} bash")
        print(f"to work with it")
    
    helper.create_venv_in_container(container_name=container_name, venv_dir=test_venv)
    helper.exec_in_container_venv(command="pip install -r requirements.txt", container_name = container_name, venv_path=test_venv)
    helper.exec_in_container_venv("pip install repo_config/ansible/tmp_install/*.whl", container_name = container_name, venv_path=test_venv)


def exec_in_container(command, container_name: str = default_container_name):
    helper = Repo_Helper()
    print(f"running command: {command}")
    print(f"in container: {container_name}")
    result, output = helper.exec_in_container(command=command, container_name=container_name)
    if result != 0:
        print(f"Error: cmake failed with {result}")
        for l in output: print(l)
    else:
        print(f"CMake configure successful")


def exec_in_test_environment(command, container_name: str = default_container_name):
    helper = Repo_Helper()
    result, output = helper.exec_in_container_venv(command, container_name, test_venv)
    if result.returncode != 0:
        print(f"Error: {result.returncode}")
        for l in output: print(l.strip())
    

def main():
    parser = argparse.ArgumentParser(description="STM32 HAL CMake repository operations")
    parser.add_argument("--operation", "-o", 
                        help="Operation to perform",
                        choices=["start_container", "configure", "build", "test_example_compilation", "test_hal_compilation", "test_connection"],
                        action="append", nargs="+") #required=True
    parser.add_argument("--build_type", "-bt", choices=["Release", "Debug", "RelWithDebInfo", "MinSizeRel"], help="defines the build type", default="Release")
    parser.add_argument("--container", "-c", help="defines a container for the build operation", default=default_container_name)
    parser.add_argument("--stop", help="stops the container", action='store_true', default=False)
    args = parser.parse_args()

    helper = Repo_Helper()
    _, repo_root = helper.repo_root()
    
    if args.operation != None:
        if "start_container" in args.operation[0]:
            start_container(args.container)
        
        if "configure" in args.operation[0]:
            command = f"cmake -S . -B build/ -DCMAKE_TOOLCHAIN_FILE=/home/developer/toolchain/arm-none-eabi-gcc.cmake -DCMAKE_BUILD_TYPE={args.build_type}"
            exec_in_container(command)
        
        if "build" in args.operation[0]:
            command = f"make -C build/"
            exec_in_container(command)
        
        if "test_hal_compilation" in args.operation[0]:
            command = f"pytest -s -v tests/test_hal_build.py"
            exec_in_test_environment(command)
        
        if "test_example_compilation" in args.operation[0]:
            command = f"pytest -s -v tests/test_compile_examples.py"
            exec_in_test_environment(command)
        
        if "test_connection" in args.operation[0]:
            command = f"pytest -s -v tests/test_connection.py"
            exec_in_test_environment(command)
    
    if args.stop == True:
        helper.execute(f"docker stop {args.container}")



if __name__ == "__main__":
    main()
