import pytest
import subprocess
import os
import datetime

def pytest_addoption(parser):
    parser.addoption("--clean", action="store_true", default=False)

cmake_build_types = ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"]


def repo_root() -> str:
    git_result = subprocess.run(["git", "rev-parse", "--show-toplevel"],capture_output=True)
    repo_root = git_result.stdout.strip().decode("utf-8")
    return repo_root

def clean_directory() -> int:
    build_dir = f"{repo_root()}/tests/build"
    print(f"creating build in {build_dir}")
    try: 
        result = subprocess.run([f"rm -rf {build_dir}"], shell=True)
        return result.returncode
        #subprocess.run([f"rm -rf {build_dir}"])    #this is here for checking fixture functionality
    except FileNotFoundError as ex:
        print(f"build dir was not there: {ex}")
        return -1


def create_build_dir() -> str:
    build_dir = f"{repo_root()}/tests/build"
    try: 
        subprocess.run([f"mkdir -p {build_dir}"], shell=True)
    except FileNotFoundError as ex:
        print(f"could not create build directory: {ex}")
        return ""
    
    print(f"build_dir created in {build_dir}")
    return build_dir

def cmake_run(cmake_root_dir: str, build_dir: str, build_type: str) -> int:
    result = subprocess.run(["cmake", "-S", cmake_root_dir,
       "-B", build_dir,
       "-DCMAKE_TOOLCHAIN_FILE=/home/developer/toolchain/arm-none-eabi-gcc.cmake",
       f"-DCMAKE_BUILD_TYPE={build_type}"], check=True)
    print(f"cmake result for {build_type}: {result.returncode}")
    return result.returncode

def make_run(build_type_directory: str) -> int:
    result = subprocess.run(["make", "-C", build_type_directory])
    print(f"make result for {build_type_directory}: {result.returncode}")
    return result.returncode

@pytest.fixture(scope="session")
def clean(request):
    return request.config.getoption("--clean")

@pytest.fixture(scope="session")
def compile(clean):
    print("")
    print(f"compile: {repo_root()}")
    if clean:
        clean_directory()

    build_dir = create_build_dir()

    if build_dir == "":
        print("could not create root build directory")
        pytest.exit()
    else:
        print(f"Using build directory: {build_dir}")
    
    build_durations = {}
    for build in cmake_build_types:
        build_dir_type =  f"{build_dir}/{build}"
        subprocess.run(["mkdir", "-p", build_dir_type ], check=True)
        start_time = datetime.datetime.now()
        print("##################################################")
        print(f"start compiling for {build} at {start_time}")
        cmake_result = cmake_run(cmake_root_dir=repo_root(), build_dir=build_dir_type, build_type=build)
        
        if cmake_result != 0:
            print(f"cmake failed for: {build} with returncode: {cmake_result}")
            pytest.exit()
        
        make_result = make_run(build_type_directory=build_dir_type)
        if make_result != 0:
            print(f"cmake failed for: {build} with returncode: {cmake_result}")
            pytest.exit()
        
        end_time = datetime.datetime.now()
        print(f"compilation finished for: {build} at {end_time}, duration: {end_time - start_time}")
        build_durations[build] = end_time - start_time
        print("##################################################")
    
    print("Summary:")

    for k, v in build_durations.items():
        print(f"duration for {k} : {v}")



