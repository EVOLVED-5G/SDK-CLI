"""Tests for `evolved5g` SKD."""
import pytest

from evolved5g.sdk import LocationHelper
from tests import emulator_utils


@pytest.mark.skip(reason="Assumes that you have EMULATOR running")
def test_location_helper_registering_subscription():
    # We assume that you have initiated the NEF_EMULATOR https://github.com/EVOLVED-5G/NEF_emulator
    # at url http://localhost:8888
    netapp_name = "testNetApp"
    host = emulator_utils.get_host_of_the_nef_emulator()
    token =  emulator_utils.get_token()
    location_helper = LocationHelper(host, token.access_token)
    response = location_helper.create_subscription(netapp_id= "mynet_app",
                                        external_id= "123456789@domain.com",
                                        misisdn= "918369110173",
                                        ipv4_addr="127.0.0.1",
                                        ipv6_addr="0:0:0:0:0:0:0:1",
                                        notification_destination =  "http://localhost:80/api/v1/utils/monitoring/callback",
                                        maximum_number_of_reports=5,
                                        monitor_expire_time= "2021-10-21T08:52:31.169Z"
                                        )
    assert response is not None
