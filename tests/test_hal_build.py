
import os
import pytest
import os.path
import datetime
from repo_helper.Repo_Helper import Repo_Helper



def test_configure(build_type, toolchain_file, build_logfile, repo_root, build_dir, log, configure_hal):
    from conftest import configure
    start_time = datetime.datetime.now()
    result_code = configure(cmake_root_dir=repo_root, build_dir=build_dir, toolchain_file=toolchain_file, build_type=build_type, log=log, install_prefix=None, build_logfile=build_logfile)
    end_time = datetime.datetime.now()
    print(f"configure time for {build_type}: {end_time - start_time}")
    assert result_code == 0, f"cmake failed with: {result_code}"


def test_build(build_type, build_logfile, build_dir, log, configure_hal):
    from conftest import make
    start_time = datetime.datetime.now()
    result_code = make(configure_hal, build_logfile, log)
    end_time = datetime.datetime.now()   
    assert result_code == 0, f"make failed with: {result_code}"
    print(f"build time for {build_type}: {end_time - start_time}")
    

def test_install(build_type, build_logfile, build_dir, log, make_hal):
    from conftest import make_install
    start_time = datetime.datetime.now()
    result_code = make_install(make_hal, build_logfile, log)
    end_time = datetime.datetime.now()
    assert result_code == 0, f"make failed with: {result_code}"
    print(f"install time for {build_type}: {end_time - start_time}")
    


class Test_Fixtures:
    '''
    Test class to verify some conftest.py functionality
    Feel free to extend
    '''
    def test_serial_interface_fixture(self, serial_interface):
        from tcl_utils.serial_monitor import SerialReaderWriter
        assert serial_interface is not None, "serial_interface fixture is None"
        assert isinstance(serial_interface, SerialReaderWriter), "serial_interface is not of expected type"
        assert os.path.exists(serial_interface.device), f"Serial device does not exist: {serial_interface.device}"
    
    def test_setup_serial_interface_fixture(self, setup_serial_interface):
        assert setup_serial_interface is not None, "setup_serial_interface fixture is None"
        print(f"setup_serial_interface: {setup_serial_interface}")
        
        helper = Repo_Helper()
        _, output = helper.execute('pidof socat')
        print(f"setup_serial_interface: socat pid: {output}")
        
        assert output != [], f"socat pid not found: {output}"
        assert os.path.exists(setup_serial_interface), f"Serial link path does not exist: {setup_serial_interface}"
    
