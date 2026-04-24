import pytest
import subprocess
import os
import datetime
import time

from tcl_utils.serial_monitor import SerialReaderWriter
from tcl_utils.tcl_control import OpenOCD_TCL
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
def clean(request, build_dir_base, repo_root):
    clean = request.config.getoption("--clean")
    print(f"clean is: {clean}")
    if clean:
        helper = Repo_Helper.Repo_Helper()
        for dir in [build_dir_base, f"{repo_root}/build/"]:
            print(f"removing {dir}")
            helper.execute(f"rm -rf {dir}")
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

@pytest.fixture(scope="module")
def build_dir(build_type, build_dir_base):
    repo_helper = Repo_Helper.Repo_Helper(logfile=None)
    build_dir = f"{build_dir_base}/{build_type}"
    print(f"creating build in {build_dir}")
    repo_helper.execute(f"mkdir -p {build_dir}")
    return build_dir

@pytest.fixture(scope="module")
def toolchain_file():
    return "/home/developer/toolchain/arm-none-eabi-gcc.cmake"

@pytest.fixture(scope="module")
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

@pytest.fixture(scope="session")
def serial_file(repo_root):
    return f"{repo_root}/tty1"

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
        helper = Repo_Helper.Repo_Helper(logfile=None)
        result, output = helper.execute(f"rm -rf {build_dir}")
        #result = subprocess.run([f"rm -rf {build_dir}"], shell=True)
        return result.returncode
    except FileNotFoundError as ex:
        print(f"build dir was not there: {ex}")
        return -1

def log_directory(build_type: str, repo_root):
    log_dir = f"{repo_root}/tests/log/{build_type}"
    helper = Repo_Helper.Repo_Helper(logfile=None)
    _ = helper.execute(f"mkdir -p {log_dir}")
    return log_dir


@pytest.fixture(scope="module")
def openocd_controller(firmware, repo_root, host):
    print(f"Creating OpenOCD controller: {firmware[0]}, {firmware[1]}")
    tcl = OpenOCD_TCL(host=host, 
                    verbose=True, 
                    #elf_file=firmware[0], 
                    mapfile=firmware[1], 
                    svd_file=os.path.join(repo_root, "svd", "stm32f767.xml")
    )
    tcl.connect()
    yield tcl

    return


@pytest.fixture()
def serial_interface(build_type, repo_root, setup_serial_interface):
    from repo_helper.Repo_Helper import Repo_Helper
    helper = Repo_Helper()
    _, output = helper.execute('pidof socat')
    print(f"serial_interface: socat pid: {output}")
    #serial_logfile is communication log
    serial_logfile = f"{log_directory(build_type, repo_root)}/uart_log.txt"
    ser = SerialReaderWriter(logfile=serial_logfile, device=setup_serial_interface)
    ser.reset_input_buffer()
    yield ser
    return


@pytest.fixture(scope="session")
def setup_serial_interface(serial_file, host="dw-latitude-e6440", port=3002, socat_logfile="/home/developer/workspace/socat_log.txt", timeout=1):
    '''
    Fixture to set up a serial interface for testing.
        socat_logfile is socat specific logfile, not serial log
    '''
    print(f"setup_serial_interface: connecting to host: {host}:{port}")
    print(f"socat logfile: {socat_logfile}")
    print(f"serial_file: {serial_file}")
    
    from repo_helper.Repo_Helper import Repo_Helper
    helper = Repo_Helper()
    
    _, output = helper.execute('pidof socat')
    if len(output) != 0:
        #if we encounter a situation where socat is required multiple times,
        #we will find a different solution. For now we kill´em all
        print(f"found socat processes: {output}, killing them")
        helper.execute("killall socat")    
        
    command=f"socat -dd PTY,link={serial_file},raw,echo=0 tcp:{host}:{port} > {socat_logfile} 2>&1"
    print(f"command:")
    print(command)
    result, output = helper.execute(command=command, wait=False)
    #some debugging:
    _, output = helper.execute('pidof socat')
    print(f"socat pid: {output}")
    time.sleep(timeout)  # Wait a moment for socat to establish the connection
    assert os.path.exists(serial_file), f"Serial file does not exist: {serial_file} after {timeout} seconds"
    yield serial_file
    helper.execute(f"killall socat")

@pytest.fixture(scope="module")
def configure_hal(build_type, toolchain_file, repo_root, log, build_logfile):
    build_dir = f"{repo_root}/build/hal/{build_type}"
    result_code = configure(cmake_root_dir=repo_root, build_dir=build_dir, toolchain_file=toolchain_file, build_type=build_type, log=log, install_prefix=None, build_logfile=build_logfile)
    assert result_code == 0, f"cmake failed with: {result_code}"
    return build_dir

@pytest.fixture(scope="module")
def make_hal(configure_hal, log, build_logfile):
    result_code = make(configure_hal, build_logfile, log)
    assert result_code == 0, f"make failed with: {result_code}"
    return configure_hal

@pytest.fixture(scope="module")
def install_hal(make_hal, log, build_logfile):
    result_code = make_install(make_hal, build_logfile, log)
    assert result_code == 0, f"make install failed with: {result_code}"
    return make_hal


@pytest.fixture(scope="module")
def compile_install_hal(self, toolchain_file, repo_root, build_type):
    from conftest import configure, make, make_install
    build_dir = f"{repo_root}/build/hal/{build_type}"
    print(f"building and installing hal in {build_dir}")
    result_code = configure(
        cmake_root_dir=repo_root, 
        build_dir=build_dir, 
        toolchain_file=toolchain_file,
        build_type=build_type, 
        log=False, 
        install_prefix="/home/developer/toolchain/", 
        build_logfile=None)
    
    assert result_code == 0, f"cmake failed with: {result_code}"
    result_code = make(build_dir, None, None)
    assert result_code == 0, f"make failed with: {result_code}"
    result_code = make_install(build_dir, None, None)
    assert result_code == 0, f"make install failed with: {result_code}"