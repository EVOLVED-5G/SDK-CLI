from evolved5g.swagger_client.rest import ApiException

from evolved5g.sdk import QosAwareness
import emulator_utils
from evolved5g.swagger_client import UsageThreshold

def showcase_create_quaranteed_bit_rate_subscription_for_conversational_voice():
    """
        This example showcases how you can create a subscription to the 5G-API in order to establish
        a Guaranteed Bit Rate (NON-GBR) QoS.

        In order to run this example, to follow the instructions in  readme.md (https://evolved5g-cli.readthedocs.io/en/latest/libraries.html) in order to
        a) run the CAPIF server (this should run always first, because NEF in step b) has to communicate with NEF)
        b) run the NEF emulator
        c) connect your NetAPP to the CAPIF server (you have to do this only once)
        d) run a local webserver that will print the notifications it retrieves from the emulator. A testing local webserver (Flask webserver) can be initiated by running the examples/api.py
    """
    netapp_id = "myNetapp"

    qos_awereness = QosAwareness(nef_url=emulator_utils.get_url_of_the_nef_emulator(),
                                 folder_path_for_certificates_and_capif_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                 capif_host=emulator_utils.get_capif_host(),
                                 capif_https_port=emulator_utils.get_capif_https_port())
    # The following external identifier was copy pasted by the NEF emulator.
    # Go to the Map and hover over a User icon.There you can retrieve the id address.
    # Notice that the NEF emulator is able to establish a guaranteed bit rate only if one and only one user is connected to a shell
    # This is done in purpose in the NEF emulator, to allow testing the lost of guaranteed connectivity to your code
    # in the NEF if a user "10.0.0.3" is connected to Cell only by her self (she is the only connection within range)
    # the NEF guarantees the connection. If another user walks by, within the same Cell range then the connection is no
    # more guaranteed and a callback notification will be retrieved.
    equipment_network_identifier = "10.0.0.3"
    network_identifier = QosAwareness.NetworkIdentifier.IP_V4_ADDRESS
    conversational_voice = QosAwareness.GBRQosReference.CONVERSATIONAL_VOICE
    # In this scenario we monitor UPLINK
    uplink = QosAwareness.QosMonitoringParameter.UPLINK
    # Minimum delay of data package during uplink, in milliseconds
    uplink_threshold = 20
    gigabyte = 1024 * 1024 * 1024
    # Up to 10 gigabytes 5 GB downlink, 5gb uplink
    usage_threshold = UsageThreshold(duration= None, # not supported
                                     total_volume=10 * gigabyte,  # 10 Gigabytes of total volume
                                     downlink_volume=5 * gigabyte,  # 5 Gigabytes for downlink
                                     uplink_volume=5 * gigabyte  # 5 Gigabytes for uplink
                                     )

    # In this example we are running flask at http://localhost:5000 with a POST route to (/monitoring/callback) in order to retrieve notifications.
    # If you are running on the NEF emulator, you need to provide a notification_destination with an IP that the
    # NEF emulator docker can understand
    # For latest versions of docker this should be: http://host.docker.internal:5000/monitoring/callback"
    # Alternative you can find the ip of the HOST by running 'ip addr show | grep "\binet\b.*\bdocker0\b" | awk '{print $2}' | cut -d '/' -f 1'
    # See article for details: https://stackoverflow.com/questions/48546124/what-is-linux-equivalent-of-host-docker-internal/61001152
    notification_destination="http://172.17.0.1:5000/monitoring/callback"


    subscription = qos_awereness.create_guaranteed_bit_rate_subscription(
        netapp_id=netapp_id,
        equipment_network_identifier=equipment_network_identifier,
        network_identifier=network_identifier,
        notification_destination=notification_destination,
        gbr_qos_reference=conversational_voice,
        usage_threshold=usage_threshold,
        qos_monitoring_parameter=uplink,
        threshold=uplink_threshold,
        # BREAKING CHANGE. At version v0.8.0 this parameter is removed!
        # wait_time_between_reports=10
        # You need to declare it as the following
        reporting_mode= QosAwareness.EventTriggeredReportingConfiguration(wait_time_in_seconds=10)
        # You can now choose also the PeriodicReportConfiguration for reporting mode
        #reporting_mode= QosAwareness.PeriodicReportConfiguration(repetition_period_in_seconds=10)

    )
    # From now on we should retrieve POST notifications to http://172.17.0.1:5000/monitoring/callback
    # every time:
    # a) two users connect to the same cell at the same time  (which is how NEF simulates loss of GBT), or
    # b) when Usage threshold is exceeded(notice this is not supported by the NEF, so you will never retrieve this notification while testing with the NEF)

    print("--- PRINTING THE SUBSCRIPTION WE JUST CREATED ----")
    print(subscription)

    # Request information about a subscription
    id = subscription.link.split("/")[-1]
    subscription_info = qos_awereness.get_subscription(netapp_id, id)
    print("--- RETRIEVING INFORMATION ABOUT SUBSCRIPTION " + id + "----")
    print(subscription_info)

def showcase_create_non_quaranteed_bit_rate_subscription_for_live_streaming():
    """
    This example showcases how you can create a subscription to the 5G-API in order to establish
    a Non-Guaranteed Bit Rate (NON-GBR) QoS.


    In order to run this example you need to follow the instructions in  readme.md in order to a) run the NEF emulator
    and b) run a local webserver that will print the location notifications it retrieves from the emulator.
    A testing local webserver (Flask webserver) can be initiated by running the examples/api.py
    """

    # Create a subscription, that will notify us 1000 times, for the next 1 day starting from now
    netapp_id = "myNetapp"
    qos_awereness = QosAwareness(nef_url=emulator_utils.get_url_of_the_nef_emulator(),
                                 folder_path_for_certificates_and_capif_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                 capif_host=emulator_utils.get_capif_host(),
                                 capif_https_port=emulator_utils.get_capif_https_port())
    # The following external identifier was copy pasted by the NEF emulator. Go to the Map and hover over a User icon.
    # There you can retrieve the id address
    equipment_network_identifier = "10.0.0.3"
    network_identifier = QosAwareness.NetworkIdentifier.IP_V4_ADDRESS
    qos_reference = QosAwareness.NonGBRQosReference.LIVE_STREAMING

    gigabyte = 1024 * 1024 * 1024
    # Up to 10 gigabytes. 5 GB downlink, 5gb uplink
    usage_threshold = UsageThreshold(duration=None,  # not supported
                                     total_volume=10 * gigabyte,  # 10 Gigabytes of total volume
                                     downlink_volume=5 * gigabyte,  # 5 Gigabytes for downlink
                                     uplink_volume=5 * gigabyte  # 5 Gigabytes for uplink
                                     )

    # In this example we are running flask at http://localhost:5000 with a POST route to (/monitoring/callback) in order to retrieve notifications.
    # If you are running on the NEF emulator, you need to provide a notification_destination with an IP that the
    # NEF emulator docker can understand
    # For latest versions of docker this should be: http://host.docker.internal:5000/monitoring/callback"
    # Alternative you can find the ip of the HOST by running 'ip addr show | grep "\binet\b.*\bdocker0\b" | awk '{print $2}' | cut -d '/' -f 1'
    # See article for details: https://stackoverflow.com/questions/48546124/what-is-linux-equivalent-of-host-docker-internal/61001152
    notification_destination="http://172.17.0.1:5000/monitoring/callback"

    subscription = qos_awereness.create_non_guaranteed_bit_rate_subscription(
        netapp_id=netapp_id,
        equipment_network_identifier=equipment_network_identifier,
        network_identifier=network_identifier,
        notification_destination=notification_destination,
        non_gbr_qos_reference=qos_reference,
        usage_threshold=usage_threshold
    )
    # From now on we should retrieve POST notifications to http://172.17.0.1:5000/monitoring/callback

    print("--- PRINTING THE SUBSCRIPTION WE JUST CREATED ----")
    print(subscription)

    # Request information about a subscription
    id = subscription.link.split("/")[-1]
    subscription_info = qos_awereness.get_subscription(netapp_id, id)
    print("--- RETRIEVING INFORMATION ABOUT SUBSCRIPTION " + id + "----")
    print(subscription_info)

def read_and_delete_all_existing_subscriptions():
    # How to get all subscriptions
    netapp_id = "myNetapp"
    qos_awareness = QosAwareness(nef_url=emulator_utils.get_url_of_the_nef_emulator(),
                                 folder_path_for_certificates_and_capif_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                 capif_host=emulator_utils.get_capif_host(),
                                 capif_https_port=emulator_utils.get_capif_https_port())

    try:
        all_subscriptions = qos_awareness.get_all_subscriptions(netapp_id)
        print(all_subscriptions)

        for subscription in all_subscriptions:
            id = subscription.link.split("/")[-1]
            print("Deleting subscription with id: " + id)
            qos_awareness.delete_subscription(netapp_id, id)
    except ApiException as ex:
        if ex.status == 404:
            print("No active transcriptions found")
        else: #something else happened, re-throw the exception
            raise




if __name__ == "__main__":
    read_and_delete_all_existing_subscriptions()
    showcase_create_quaranteed_bit_rate_subscription_for_conversational_voice()
    read_and_delete_all_existing_subscriptions()
    showcase_create_non_quaranteed_bit_rate_subscription_for_live_streaming()
