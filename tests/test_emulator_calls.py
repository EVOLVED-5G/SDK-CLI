"""
Tests that demonstrate how to interact with the Emulator.
We assume that you have initiated the NEF_EMULATOR https://github.com/EVOLVED-5G/NEF_emulator
first at url http://localhost:8888
"""
import pytest

from evolved5g.swagger_client import LoginApi, User
from evolved5g.swagger_client.models import Token
from tests import emulator_utils


@pytest.mark.skip(reason="This can only be run on localhost")
def test_login_to_the_emulator():
    token = emulator_utils.get_token()
    assert isinstance(token, Token)


@pytest.mark.skip(reason="This can only be run on localhost")
def test_token_validation():
    token = emulator_utils.get_token()
    api_client = emulator_utils.get_api_client(token)
    api = LoginApi(api_client)  # noqa: E501

    response = api.test_token_api_v1_login_test_token_post_with_http_info()
    assert isinstance(response[0], User)
