import pytest
import subprocess
import os
import datetime

from tcl_utils.serial_monitor import SerialReaderWriter
from repo_helper import Repo_Helper


def pytest_addoption(parser):
    parser.addoption("--clean", action="store_true", default=False, help="creates a clean cmake build for the tests")
    parser.addoption("--log", action="store_true", default=False, help="writes build logs to console")
    parser.addoption("--host", help="defines the hostname to execute the tests", default = "dw-latitude-e6440")
    parser.addoption("--build_dir", help="defines the directory to use for building the hal and test applications", default = "/home/developer/workspace/test_build")
    
@pytest.fixture(scope="session")
def build_dir_base(request):
    return request.config.getoption("--build_dir")

@pytest.fixture(scope="session", autouse=True)
def clean(request, build_dir_base):
    clean = request.config.getoption("--clean")
    print(f"clean is: {clean}")
    if clean:
        print(f"removing {build_dir_base}")
        helper = Repo_Helper.Repo_Helper()
        helper.execute(f"rm -rf {build_dir_base}")
    return clean

@pytest.fixture(scope="session")
def log(request):
    return request.config.getoption("--log")

@pytest.fixture(scope="session")
def host(request):
    return request.config.getoption("--host")

cmake_build_types = ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"]

@pytest.fixture(scope="module", params=cmake_build_types)
def build_type(request):
    return request.param

@pytest.fixture
def build_dir(build_type, build_dir_base):
    repo_helper = Repo_Helper.Repo_Helper(logfile=None)
    build_dir = f"{build_dir_base}/{build_type}"
    print(f"creating build in {build_dir}")
    repo_helper.execute(f"mkdir -p {build_dir}")
    return build_dir

@pytest.fixture
def toolchain_file():
    return "/home/developer/toolchain/arm-none-eabi-gcc.cmake"

@pytest.fixture
def build_logfile(build_dir):
    from repo_helper import Repo_Helper
    repo_helper = Repo_Helper.Repo_Helper(logfile=None)
    log_file = f"{build_dir}/build_log.txt"
    repo_helper.execute(f"touch {log_file}")
    return log_file

@pytest.fixture(scope="session")
def repo_root():
    from repo_helper import Repo_Helper
    repo_helper = Repo_Helper.Repo_Helper(logfile=None)
    _, output = repo_helper.repo_root()
    print(f"repo root is: {output}")
    return output


def configure(cmake_root_dir, build_dir, toolchain_file, build_type, log, install_prefix: str|None , build_logfile: str|None) -> int:
    cmake_command = f"cmake -S {cmake_root_dir} -B {build_dir} -DCMAKE_BUILD_TYPE={build_type} -DCMAKE_TOOLCHAIN_FILE={toolchain_file} -DCMAKE_INSTALL_PREFIX={install_prefix if install_prefix != None else build_dir + '/install/'}"
    helper = Repo_Helper.Repo_Helper(logfile=build_logfile)
    result, _ = helper.execute(cmake_command, log=log, wait=True)
    return result.returncode

def make(build_dir, build_logfile: str|None, log) -> int:
    make_command = f"make -C {build_dir}"
    helper = Repo_Helper.Repo_Helper(logfile=build_logfile)
    result, _ = helper.execute(make_command, log=log, wait=True)
    return result.returncode

def make_install(build_dir, build_logfile: str|None, log) -> int:
    make_command = f"make -C {build_dir} install"
    helper = Repo_Helper.Repo_Helper(logfile=build_logfile)
    result, _ = helper.execute(make_command, log=log, wait=True)
    return result.returncode

def clean_directory(build_dir) -> int:
    try: 
        result = subprocess.run([f"rm -rf {build_dir}"], shell=True)
        return result.returncode
    except FileNotFoundError as ex:
        print(f"build dir was not there: {ex}")
        return -1

def log_directory(build_type: str):
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
       "-DCMAKE_TOOLCHAIN_FILE=",
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
    build_dir = create_build_dir()
    if clean:
        clean_directory(build_dir)
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

@pytest.fixture()
def openocd_controller(firmware, mapfile, host):
    from tcl_utils.tcl_control import OpenOCD_TCL
    tcl = OpenOCD_TCL(host=host, 
                    verbose=False, 
                    elf_file=firmware, 
                    mapfile=mapfile, 
                    svd_file=os.path.join(repo_root(), "svd", "stm32f767.xml")
    )
    tcl.connect()
    yield tcl

    return

@pytest.fixture(scope="module") #autouse=True)
def flash_binary_file(log_to_file, build_type, firmware):
    command = f"gdb-multiarch -f {firmware}"
    this_directory = os.path.dirname(__file__)
    log_file = None
    if log_to_file == True:
        log_file = f"{log_directory(build_type)}/gdb-multiarch.txt"

    print(f"gdb command: {command}")
    print(f"firmware: {firmware}")
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

@pytest.fixture()
def serial_interface(build_type):
    serial_logfile = f"{log_directory(build_type)}/uart_log.txt"
    ser = SerialReaderWriter(logfile=serial_logfile, device=f"{repo_root()}/tty1")
    yield ser
    return

@pytest.fixture(scope="session") #autouse=True)
def setup_serial_interface(host="dw-latitude-e6440", port=3002):
    print(f"setting up serial interface for host: {host}:{port}")
    from repo_helper.Repo_Helper import Repo_Helper
    helper = Repo_Helper()
    result, output = helper.execute(command=f"socat PTY,link=/home/developer/workspace/tty1,raw,echo=0 tcp:{host}:{port}", wait=False)
    yield None
    helper.execute(f"killall socat")