#! /usr/bin/env python3


from repo_helper.Repo_Helper import Repo_Helper
import argparse

MOUNT="/workspace"
base_image="ghcr.io/dietwall/arm_gcc_image:latest"
image="stm32hal_cmake_dev"
default_container_name = "stm32hal"
test_venv = ".venv"

def create_container_env(container_name: str = default_container_name):
    helper = Repo_Helper()
    _, repo_root = helper.repo_root()
    command = f"source {MOUNT}/repo_config/.env_container && \
        {MOUNT}/repo_config/download_release.sh -r dietwall/openocd-tcl-controller -o {MOUNT}/repo_config/tmp_download"
    
    result, output = helper.exec_in_container(command=command, container_name=container_name)
    if result != 0:
        print(f"Error: {result}")
        for l in output: print(l.strip())
    else:
        print(f"Downloaded release successfully")

def start_container(container_name: str = default_container_name):
    helper = Repo_Helper()
    _, repo_root = helper.repo_root()
    print(f"starting container: {container_name}")
    command = f"docker run -d -it --name {container_name} --rm --mount type=bind,source={repo_root},dst={MOUNT} {image}"
    print(f"starting container")
    result, output = helper.execute(command)
    print(f"result from execute: {result.returncode}")
    if result.returncode == 125:
        print(f"Returncode: {result.returncode}, is it running?")
        for f in output:
            print(f)
    elif result.returncode != 0:
        print(f"Starting failed with exitcode: {result.returncode}")
        for f in output:
            print(f)
    else:
        print(f"type: ")
        print(f"docker exec -it {container_name} bash")
        print(f"to work with it")
    
    print(f"setting up container environment")
    create_container_env(container_name)
    helper.create_venv_in_container(container_name=container_name, venv_dir=test_venv)
    print(f"Installing requirements from {MOUNT}/requirements.txt")
    helper.exec_in_container_venv(command=f"pip install -r {MOUNT}/requirements.txt", container_name = container_name, venv_path=test_venv)
    print(f"Installing downloaded dependencies")
    helper.exec_in_container_venv(command=f"pip install {MOUNT}/repo_config/tmp_download/*.whl", container_name = container_name, venv_path=test_venv)

def build_image(image_name: str = image):
    print(f"re-building image: {image_name}")
    helper = Repo_Helper()
    command = f"docker build -t {image_name} -f .devcontainer/Dockerfile ."
    print(f"building image")
    result, output = helper.execute(command)
    if result.returncode != 0:
        print(f"Building failed with exitcode: {result.returncode}")
        for f in output:
            print(f.strip())
    else:
        print(f"Image built successfully")


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
                        choices=["clean", "start_container", "configure", "build", "test_example_compilation", "test_hal_compilation", "test_connection"],
                        action="append", nargs="+") #required=True
    parser.add_argument("--build_type", "-bt", choices=["Release", "Debug", "RelWithDebInfo", "MinSizeRel"], help="defines the build type", default="Release")
    parser.add_argument("--container", "-c", help="defines a container for the build operation", default=default_container_name)
    parser.add_argument("--stop", help="stops the container", action='store_true', default=False)
    args = parser.parse_args()

    helper = Repo_Helper()
    _, repo_root = helper.repo_root()
    
    if args.operation != None:
        if "clean" in args.operation[0]:
            print(f"cleaning up environment, stopping any containers")
            helper.execute(f"docker stop {args.container}")
            #make sure it is removed, even if -rm is given
            helper.execute(f"docker rm {args.container}")
            for dir in ["build", test_venv, ".venv"]:
                print(f"removing {repo_root}/{dir}")
                helper.execute(f"rm -rf {repo_root}/{dir}")

        if "start_container" in args.operation[0]:
            build_image()
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
