import pytest
from repo_helper import Repo_Helper
import datetime

built_types = ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"]

@pytest.mark.parametrize("build_type", built_types)
def test_configure(build_type, toolchain_file, build_logfile, repo_root, build_dir, log):
    from conftest import configure
    start_time = datetime.datetime.now()
    result_code = configure(cmake_root_dir=repo_root, build_dir=build_dir, toolchain_file=toolchain_file, build_type=build_type, log=log, install_prefix=None, build_logfile=build_logfile)
    end_time = datetime.datetime.now()
    print(f"configure time for {build_type}: {end_time - start_time}")
    assert result_code == 0, f"cmake failed with: {result_code}"

@pytest.mark.parametrize("build_type", built_types)
def test_build(build_type, build_logfile, build_dir, log):
    from conftest import make
    start_time = datetime.datetime.now()
    result_code = make(build_dir, build_logfile, log)
    end_time = datetime.datetime.now()   
    print(f"build time for {build_type}: {end_time - start_time}")
    assert result_code == 0, f"make failed with: {result_code}"
    

@pytest.mark.parametrize("build_type", built_types)
def test_install(build_type, build_logfile, build_dir, log):
    from conftest import make_install
    start_time = datetime.datetime.now()
    result_code = make_install(build_dir, build_logfile, log)
    end_time = datetime.datetime.now()
    print(f"install time for {build_type}: {end_time - start_time}")
    assert result_code == 0, f"make failed with: {result_code}"
    
