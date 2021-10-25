from evolved5g.sdk import LocationSubscriber
import emulator_utils


def showcase_create_subscription_and_retrieve_call_backs():
    """
    This examples show cases how you can create a subscription to the 5G-API in order to monitor device location.
    In order to run this example you need to follow the instruction in  readme.md
    """
    netapp_name = "testNetApp"
    host = emulator_utils.get_host_of_the_nef_emulator()
    token = emulator_utils.get_token()
    location_helper = LocationSubscriber(host, token.access_token)
    response = location_helper.create_subscription(netapp_id= "mynet_app",
                                                   external_id= "123456789@domain.com",
                                                   misisdn= "918369110173",
                                                   ipv4_addr="10.0.0.1",
                                                   ipv6_addr="22-00-00-00-00-01",
                                                   notification_destination ="http://127.0.0.1:5000/monitoring/callback",
                                                   maximum_number_of_reports=5,
                                                   monitor_expire_time= "2021-10-21T08:52:31.169Z"
                                               )

if __name__ == "__main__":
    showcase_create_subscription_and_retrieve_call_backs()
