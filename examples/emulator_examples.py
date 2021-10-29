
from evolved5g.swagger_client import LoginApi, User
import emulator_utils

def showcase_login_to_the_emulator_and_test_token():
    """
    Demonstrate how to interact with the Emulator, to a token and the current logged in User
    """

    token = emulator_utils.get_token()
    print("-----")
    print("Got token")
    print(token)
    api_client = emulator_utils.get_api_client(token)
    api = LoginApi(api_client)
    print("-----")
    print("Getting login info")
    response = api.test_token_api_v1_login_test_token_post_with_http_info()
    assert isinstance(response[0], User)
    print(response[0])


if __name__ == "__main__":
    showcase_login_to_the_emulator_and_test_token()
