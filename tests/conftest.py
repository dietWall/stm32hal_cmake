import pytest
import subprocess
import os
import datetime

def pytest_addoption(parser):
    parser.addoption("--clean", action="store_true", default=False, help="creates a clean cmake build for the tests")
    parser.addoption("--log_to_file", action="store_true", default=False, help="writes build and gdb logs to files to: <repo_root>/tests/log/<build_type>/")

@pytest.fixture(scope="session")
def clean(request):
    return request.config.getoption("--clean")

@pytest.fixture(scope="session")
def log_to_file(request):
    return request.config.getoption("--log_to_file")


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
    

def log_directory(build_type: str) -> str:
    log_dir = f"{repo_root()}/tests/log/{build_type}"
    #make sure it exists
    subprocess.run([f"mkdir -p {log_dir}"], shell=True)
    return log_dir


def create_build_dir() -> str:
    build_dir = f"{repo_root()}/tests/build"
    try: 
        subprocess.run([f"mkdir -p {build_dir}"], shell=True)
    except FileNotFoundError as ex:
        print(f"could not create build directory: {ex}")
        return ""
    print(f"build_dir created in {build_dir}")
    return build_dir

def cmake_run(cmake_root_dir: str, build_dir: str, build_type: str, cmake_log_file: str|None) -> int:
    logfile = None
    
    if cmake_log_file != None:
        logfile = open(cmake_log_file, "w")
    
    result = subprocess.run(["cmake", "-S", cmake_root_dir,
       "-B", build_dir,
       "-DCMAKE_TOOLCHAIN_FILE=/home/developer/toolchain/arm-none-eabi-gcc.cmake",
       f"-DCMAKE_BUILD_TYPE={build_type}"], check=True,
       stdout=logfile, stderr=logfile
       )
    print(f"cmake result for {build_type}: {result.returncode}")
    return result.returncode


def make_run(build_type_directory: str, make_log_file: str|None) -> int:
    logfile = None
    
    if make_log_file != None:
        logfile = open(make_log_file, "w")

    result = subprocess.run(["make", "-C", build_type_directory], stdout=logfile, stderr=logfile)
    print(f"make result for {build_type_directory}: {result.returncode}")
    return result.returncode


@pytest.fixture(scope="session")
def compile(clean, log_to_file):
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
        
        cmake_log_file = None
        make_log_file = None
        
        if log_to_file == True:
            cmake_log_file = f"{log_directory(build_type=build)}/cmake_output.txt"
            make_log_file = f"{log_directory(build_type=build)}/make_output.txt"

        subprocess.run(["mkdir", "-p", build_dir_type ], check=True)
        start_time = datetime.datetime.now()
        print("##################################################")
        print(f"start compiling for {build} at {start_time}")
        cmake_result = cmake_run(cmake_root_dir=repo_root(), build_dir=build_dir_type, build_type=build, cmake_log_file=cmake_log_file)
        
        if cmake_result != 0:
            print(f"cmake failed for: {build} with returncode: {cmake_result}")
            pytest.exit()
        
        make_result = make_run(build_type_directory=build_dir_type, make_log_file=make_log_file)
        if make_result != 0:
            print(f"make failed for: {build} with returncode: {cmake_result}")
            pytest.exit()
        
        end_time = datetime.datetime.now()
        print(f"compilation finished for: {build} at {end_time}, duration: {end_time - start_time}")
        build_durations[build] = end_time - start_time
        print("##################################################")
    
    print("Build Time Summary:")

    for k, v in build_durations.items():
        print(f"duration for {k} : {v}")

    print("##################################################")



