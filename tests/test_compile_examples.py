import pytest



class TestCompileExamples:

    @pytest.fixture(scope="module")
    def compile_install_hal(self, toolchain_file, repo_root, build_type):
        from conftest import configure, make, make_install
        build_dir = f"{repo_root}/build/{build_type}"
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
    
    @pytest.mark.parametrize("app_dir", ["Examples/Board_Init", "Examples/simple_main"])
    def test_compile_example(self, compile_install_hal, app_dir, toolchain_file, build_type):
        from conftest import configure, make
        result = configure(
            cmake_root_dir=app_dir,
            build_dir=f"{app_dir}/build",
            toolchain_file=toolchain_file,
            build_type=build_type,
            log=True,
            install_prefix=None,
            build_logfile=None
        )
        assert result == 0, f"cmake for {app_dir} failed with: {result}"
        result = make(f"{app_dir}/build", None, True)
        assert result == 0, f"make for {app_dir} failed with: {result}"

