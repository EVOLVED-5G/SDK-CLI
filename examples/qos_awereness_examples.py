from evolved5g.sdk import QosAwareness
import emulator_utils
import datetime

from evolved5g.swagger_client import UsageThreshold


def showcase_create_non_quaranteed_bit_rate_subscription_for_live_streaming():
    """
    This example showcases how you can create a subscription to the 5G-API in order to establish
    a) Non-Guaranteed Bit Rate (NON-GBR) QoS or
    a) Guaranteed Bit Rate (NON-GBR) QoS

    In order to run this example you need to follow the instructions in  readme.md in order to a) run the NEF emulator
    and b) run a local webserver that will print the location notifications it retrieves from the emulator.
    A testing local webserver (Flask webserver) can be initiated by running the examples/api.py
    """

    # Create a subscription, that will notify us 1000 times, for the next 1 day starting from now
    netapp_id = "myNetapp"
    host = emulator_utils.get_host_of_the_nef_emulator()
    token = emulator_utils.get_token()
    qos_awereness = QosAwareness(host, token.access_token)
    # The following external identifier was copy pasted by the NEF emulator. Go to the Map and hover over a User icon.
    # There you can retrieve the id address
    equipment_network_identifier = "10.0.0.3"
    network_identifier = QosAwareness.NetworkIdentifier.IP_V4_ADDRESS
    qos_reference = QosAwareness.NonGBRQosReference.LIVE_STREAMING

    gigabyte = 1024 * 1024 * 1024
    # Up to 10 gigabytes for the upcoming 48 hours. 5 GB downlink, 5gb uplink
    usage_threshold = UsageThreshold(duration=48 * 3600,
                                     total_volume=10 * gigabyte,  # 10 Gigabytes of total volume
                                     downlink_volume=5 * gigabyte,  # 5 Gigabytes for downlink
                                     uplink_volume=5 * gigabyte  # 5 Gigabytes for uplink
                                     )

    subscription = qos_awereness.create_non_guaranteed_bit_rate_subscription(
        netapp_id=netapp_id,
        equipment_network_identifier=equipment_network_identifier,
        network_identifier=network_identifier,
        notification_destination="http://172.17.0.1:5000/monitoring/callback",
        non_gbr_qos_reference=qos_reference,
        usage_threshold=usage_threshold
    )
    # From now on we should retrieve POST notifications to http://172.17.0.1:5000/monitoring/callback

    print(subscription)

    # How to get all subscriptions
    all_subscriptions = qos_awereness.get_all_subscriptions(netapp_id, 0, 100)
    print(all_subscriptions)

    # Request information about a subscription
    id = subscription.link.split("/")[-1]
    subscription_info = qos_awereness.get_subscription(netapp_id, id)
    print(subscription_info)


if __name__ == "__main__":
    showcase_create_non_quaranteed_bit_rate_subscription_for_live_streaming()
