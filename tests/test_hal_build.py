#this file tests not the hal itself, but rather the infrastructure
# build system, packaging and installation process

import pytest
from repo_helper import Repo_Helper
import datetime

built_types = ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"]

@pytest.mark.parametrize("build_type", built_types)
def test_configure(build_type, toolchain_file, build_logfile, repo_root, build_dir, log):
    repo_helper = Repo_Helper.Repo_Helper(logfile=build_logfile)
    cmake_command = f"cmake -S {repo_root} -B {build_dir} -DCMAKE_BUILD_TYPE={build_type} -DCMAKE_TOOLCHAIN_FILE={toolchain_file} -DCMAKE_INSTALL_PREFIX={build_dir}/install/"
    result, _ = repo_helper.execute(cmake_command, log=log, wait=True)
    assert result.returncode == 0, f"cmake failed with: {result.returncode}"


@pytest.mark.parametrize("build_type", built_types)
def test_build(build_type, build_logfile, build_dir, log):
    make_command = f"make -C {build_dir}"
    repo_helper = Repo_Helper.Repo_Helper(logfile=build_logfile)
    start_time = datetime.datetime.now()
    result, _ = repo_helper.execute(make_command, log=log, wait=True)
    end_time = datetime.datetime.now()
    print(f"build time for {build_type}: {end_time - start_time}")
    assert result.returncode == 0, f"make failed with: {result.returncode}"
    


@pytest.mark.parametrize("build_type", built_types)
def test_install(build_type, build_logfile, build_dir, log):
    make_command = f"make -C {build_dir} install"
    repo_helper = Repo_Helper.Repo_Helper(logfile=build_logfile)
    start_time = datetime.datetime.now()
    result, _ = repo_helper.execute(make_command, log=log, wait=True)
    end_time = datetime.datetime.now()
    print(f"install time for {build_type}: {end_time - start_time}")
    assert result.returncode == 0, f"make failed with: {result.returncode}"
    
