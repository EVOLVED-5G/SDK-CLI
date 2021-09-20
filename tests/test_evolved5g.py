#!/usr/bin/env python

"""Tests for `evolved5g` package."""

import pytest
import os
from click.testing import CliRunner

from evolved5g import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


# def test_command_line_interface():
#     """Test the CLI."""
#     runner = CliRunner()
#     result = runner.invoke(cli.main)
#     assert result.exit_code == 0
#     assert 'evolved5g.cli.main' in result.output
#     help_result = runner.invoke(cli.main, ['--help'])
#     assert help_result.exit_code == 0
#     assert '--help  Show this message and exit.' in help_result.output

def test_cli():
    """ Test the CLI  """
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert "interface for EVOLVED-5G" in result.output
    assert "generate" in result.output
    help_result = runner.invoke(cli.cli, ['--help'])
    assert help_result.exit_code == 0
    # assert '--help  Show this message and exit.' in help_result.output


def test_cli_generate():
    """ Test the CLI generate command """
    runner = CliRunner()
    assert not os.path.isdir('NetApp')
    result = runner.invoke(cli.cli, ['generate', "--help"])
    assert result.exit_code == 0
    assert "EVOLVED-5G compliant" in result.output
    # shutil.rmtree('NetApp')  -- IF cleanup is needed


def test_cli_default_generate():
    """ Test the CLI default valued generate command """
    runner = CliRunner()
    with runner.isolated_filesystem():
        assert not os.path.isdir('NetApp')
        result = runner.invoke(cli.cli, ['generate', "--template", "gh:skolome/netapp-ckcutter-template"])
        assert result.exit_code == 0
        assert os.path.isdir('NetApp')
        assert os.path.isdir(os.path.join('NetApp', 'netapp'))
        assert os.path.isfile(os.path.join('NetApp', 'netapp', 'main.py'))
        # shutil.rmtree('NetApp')  -- IF cleanup is needed


# def test_cli_custom_generate():
#     """ Test the CLI generate command with custom values through prompt """
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         result = runner.invoke(cli.cli, ['generate',  "--template", "gh:skolome/netapp-ckcutter-template"], input="Tested")
#         assert result.exit_code == 0
#         assert os.path.isdir('Tested')
#         assert os.path.isdir(os.path.join('Tested', 'tested'))
#     # shutil.rmtree('NetApp')  -- IF cleanup is needed


def test_cli_custom_generate_through_options():
    """ Test the CLI generate command with custom values """
    runner = CliRunner()
    with runner.isolated_filesystem():
        assert not os.path.isdir('Test2')
        result = runner.invoke(cli.cli, ['generate', "--template", "gh:skolome/netapp-ckcutter-template", '-r', "Test2"])
        assert result.exit_code == 0
        assert os.path.isdir('Test2')
        assert os.path.isdir(os.path.join('Test2', 'test2'))
    # shutil.rmtree('NetApp')  -- IF cleanup is needed


def test_cli_generate_no_prompt():
    """ Test the CLI generate command no prompt asked """
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli.cli, ['generate', '--no-input', "--template", "gh:skolome/netapp-ckcutter-template"], input="Tested")
        assert result.exit_code == 0
        assert os.path.isdir('NetApp')
        assert not os.path.isdir('Tested')
        assert os.path.isdir(os.path.join('NetApp', 'netapp'))
        assert not os.path.isdir(os.path.join('Tested', 'tested'))


def test_cli_generate_no_prompt_custom():
    """ Test the CLI generate command no prompt asked but custom value gived """
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli.cli, [
                               'generate', "--template", "gh:skolome/netapp-ckcutter-template", '--no-input', '-r', "Test2", "-p", "not_test"], input="Tested")
        assert result.exit_code == 0
        assert os.path.isdir('Test2')
        assert not os.path.isdir('Tested')
        assert os.path.isdir(os.path.join('Test2', 'not_test'))
        assert not os.path.isdir(os.path.join('Tested', 'tested'))


def test_cli_generate_custom_package():
    """ Test the CLI generate command with custom package name """
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli.cli, ['generate', "--template", "gh:skolome/netapp-ckcutter-template", "-p", "not_test"])
        assert result.exit_code == 0
        assert os.path.isdir(os.path.join('NetApp', 'not_test'))


# def test_cli_generate_custom_package_prompt_repo():
#     """ Test the CLI generate command no prompt asked but custom value gived """
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         result = runner.invoke(
#             cli.cli, ['generate',"--location", "gh:skolome/netapp-ckcutter-template", "-p", "not_test"], input="Test2")
#         assert result.exit_code == 0
#         assert os.path.isdir('Test2')
#         # assert not os.path.isdir('NetApp')
#         assert os.path.isdir(os.path.join('Test2', 'not_test'))
