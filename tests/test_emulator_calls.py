"""
Tests that demonstrate how to interact with the Emulator.
We assume that you have initiated the NEF_EMULATOR https://github.com/EVOLVED-5G/NEF_emulator
first at url http://localhost:8888
"""
from evolved5g import swagger_client
from evolved5g.swagger_client import LoginApi, User
from evolved5g.swagger_client.models import Token


def test_login_to_the_emulator():
    token = __getToken()
    assert isinstance(token, Token)


def test_token_validation():
    token = __getToken()
    configuration = swagger_client.Configuration()
    configuration.host = __getUrlOfNefEmulator()
    configuration.access_token = token.access_token
    api_client = swagger_client.ApiClient(configuration=configuration)
    api = LoginApi(api_client)  # noqa: E501

    response = api.test_token_api_v1_login_test_token_post_with_http_info()
    assert isinstance(response, User)


def __getToken() -> Token :
    username = "admin@my-email.com";
    password = "pass"
    configuration = swagger_client.Configuration()
    #The host of the 5G API (emulator)
    configuration.host = __getUrlOfNefEmulator()
    api_client = swagger_client.ApiClient(configuration=configuration)
    api_client.select_header_content_type(["application/x-www-form-urlencoded"])
    api = LoginApi(api_client)
    token = api.login_access_token_api_v1_login_access_token_post("", username, password,"" , "", "")
    return token

def __getUrlOfNefEmulator():
    return "http://localhost:8888";

