from click.testing import CliRunner

from fastapi_to_openapi.main import cli

import os
import difflib

def check_file_diff(target_file_1, target_file_2):
    target_file_path_1 = os.path.join(os.getcwd(),"tests",target_file_1)
    target_file_path_2 = os.path.join(os.getcwd(),"tests",target_file_2)

    if not os.path.exists(target_file_path_1) or not os.path.exists(target_file_path_2):
        raise FileNotFoundError

    f_p = open(target_file_path_1).read()
    f_d = open(target_file_path_2).read()

    diff = difflib.unified_diff(f_p.split(), f_d.split())
    diff_str = '\n'.join(diff)

    assert not diff_str, f"{target_file_1}, {target_file_2} FAILED!!"

def test_f_to_o_cli_yaml():
    runner = CliRunner()
    result = runner.invoke(cli, ["-i","tests/fastapi","-o","tests/openapi_test.yaml"])

    assert result.exit_code == 0
    check_file_diff("openapi_test.yaml", "openapi.yaml")

def test_f_to_o_cli_json():
    runner = CliRunner()
    result = runner.invoke(cli, ["-i","tests/fastapi","-o","tests/openapi_test.json","-t","json"])

    assert result.exit_code == 0
    check_file_diff("openapi_test.json", "openapi.json")

