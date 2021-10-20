"""Tests for `evolved5g` SKD."""
from evolved5g.sdk import LocationHelper
from tests import emulator_utils

def test_location_helper_registering_subscription():
    # We assume that you have initiated the NEF_EMULATOR https://github.com/EVOLVED-5G/NEF_emulator
    # first at url http://localhost:8888
    host = emulator_utils.get_host_of_the_nef_emulator()
    access_token = emulator_utils.get_token()
    netapp_name = "testNetApp"
    location_helper = LocationHelper(host, access_token)

    response =location_helper.create_subscription(netapp_name)
    assert False

