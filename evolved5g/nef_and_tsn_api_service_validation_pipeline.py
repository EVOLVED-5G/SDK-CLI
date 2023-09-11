import json
import json.decoder
from evolved5g.sdk import TSNManager, LocationSubscriber, ConnectionMonitor, QosAwareness, ServiceDiscoverer
from evolved5g.swagger_client.rest import ApiException
from evolved5g import swagger_client
from evolved5g.swagger_client import LoginApi, User, UsageThreshold
from evolved5g.swagger_client.models import Token
import datetime


def validate_all_endpoints_returned_by_service_discoverer(config_file_full_path: str) -> bool:
    """
    This method finds all the released APIs in CAPIF (via ServiceDiscovery) and performs tests to make sure that they work as expected
    :param config_file_full_path:
    :return: True if the endpoints work as expected. Else an exception is raised
    """
    with open(config_file_full_path, "r") as openfile:
        config = json.load(openfile)

    service_discoverer = ServiceDiscoverer(folder_path_for_certificates_and_api_key=config["folder_to_store_certificates"],
                                           capif_host=config["capif_host"],
                                           capif_https_port=config["capif_https_port"]
                                           )
    service_apis = service_discoverer.discover_service_apis()

    # We iterate to all of the available published services.
    # Notice that if a new api is published and we dont have tests for it, an exception is raised
    for api_description in service_apis["serviceAPIDescriptions"]:
        print("Starting testing endpoints for ApiName: " + api_description["apiName"] )
        aef_profile = api_description["aefProfiles"][0]
        if api_description["apiName"] == "/nef/api/v1/3gpp-monitoring-event/":
            nef_url = __get_nef_url(aef_profile)
            __test_location_subscriber(config,nef_url)
            __test_connection_monitor(config,nef_url)
        elif api_description["apiName"] == "/nef/api/v1/3gpp-as-session-with-qos/":
            nef_url = __get_nef_url(aef_profile)
            __test_qos_awereness(config,nef_url)
        elif api_description["apiName"] == "/tsn/api/":
            host_info = aef_profile['interfaceDescriptions'][0]
            tsn_port = host_info["port"]

            if aef_profile['domainName']!=None:
               tsn_host = aef_profile['domainName']
            else:
                tsn_host = host_info["ipv4Addr"]

            __test_tsn_manager(config, tsn_host, tsn_port)
        else:
            raise NotImplementedError("Could not find Validation tests for ApiName" + api_description["apiName"])

    print("All endpoints work as expected")
    return True

def __get_nef_url(aef_profile) -> str:
    if aef_profile['domainName']!=None:
        return "https://{domain_name}".format(domain_name=aef_profile['domainName'])
    else:
        host_info = aef_profile['interfaceDescriptions'][0]
        return "https://{host}:{port}".format(host=host_info["ipv4Addr"], port=host_info["port"])

def __test_location_subscriber(config,url_of_the_nef_emulator) -> None:
    """
    Tests the NEF api name /nef/api/v1/3gpp-monitoring-event/ with dummy data
    :param config:
    """

    # Create a subscription, that will notify us 1000 times, for the next 1 day starting from now
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z"
    netapp_id = "myNetapp"
    location_subscriber = LocationSubscriber(nef_url=url_of_the_nef_emulator,
                                             folder_path_for_certificates_and_capif_api_key=config["folder_to_store_certificates"],
                                             capif_host=config["capif_host"],
                                             capif_https_port=config["capif_https_port"])
    # The following external identifier was copy pasted by the NEF emulator. Go to the Map and click on a User icon. There you can retrieve the id
    external_id = "10003@domain.com"

    subscription = location_subscriber.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination="http://172.17.0.1:5000/monitoring/callback",
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time
    )
    # if we reached this point without an exception, then NEF subscriptions work

    try:
        all_subscriptions = location_subscriber.get_all_subscriptions(netapp_id, 0, 100)

        print(all_subscriptions)

        for subscription in all_subscriptions:
            id = subscription.link.split("/")[-1]
            print("Deleting subscription with id: " + id)
            location_subscriber.delete_subscription(netapp_id, id)
    except ApiException as ex:
        if ex.status == 404:
            print("No active transcriptions found")
        else:
            # something else happened, test failed! Re-throw the exception
            raise


def __test_connection_monitor(config,url_of_the_nef_emulator):
    """
     Tests the NEF api name /nef/api/v1/3gpp-monitoring-event/ with dummy data
     :param config:
   """

    # Create a subscription, that will notify us 1000 times, for the next 1 day starting from now
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z"
    netapp_id = "myNetapp"
    connection_monitor = ConnectionMonitor(nef_url=url_of_the_nef_emulator,
                                           folder_path_for_certificates_and_capif_api_key=config["folder_to_store_certificates"],
                                           capif_host=config["capif_host"],
                                           capif_https_port=config["capif_https_port"])
    # The following external identifier was copy pasted by the NEF emulator. Go to the Map and click on a User icon. There you can retrieve the id
    external_id = "10003@domain.com"

    subscription_when_not_connected = connection_monitor.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination="http://172.17.0.1:5000/monitoring/callback",
        monitoring_type=ConnectionMonitor.MonitoringType.INFORM_WHEN_NOT_CONNECTED,
        wait_time_before_sending_notification_in_seconds=5,
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time
    )
    # if we reached this point without an exception, then NEF subscriptions work

    try:
        all_subscriptions = connection_monitor.get_all_subscriptions(netapp_id, 0, 100)
        print(all_subscriptions)

        for subscription in all_subscriptions:
            id = subscription.link.split("/")[-1]
            print("Deleting subscription with id: " + id)
            connection_monitor.delete_subscription(netapp_id, id)
    except ApiException as ex:
        if ex.status == 404:
            print("No active transcriptions found")
        else:  # something else happened, re-throw the exception
            raise


def __test_qos_awereness(config,url_of_the_nef_emulator):
    """
     Tests the NEF api name  /nef/api/v1/3gpp-as-session-with-qos/  with dummy data
     :param config:
   """
    netapp_id = "myNetapp"

    qos_awereness = QosAwareness(nef_url=url_of_the_nef_emulator,
                                 folder_path_for_certificates_and_capif_api_key=config["folder_to_store_certificates"],
                                 capif_host=config["capif_host"],
                                 capif_https_port=config["capif_https_port"])
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
    notification_destination = "http://172.17.0.1:5000/monitoring/callback"

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
        reporting_mode=QosAwareness.EventTriggeredReportingConfiguration(wait_time_in_seconds=10)
        # You can now choose also the PeriodicReportConfiguration for reporting mode
        # reporting_mode= QosAwareness.PeriodicReportConfiguration(repetition_period_in_seconds=10)

    )
    # If we reached this point with no exception raised, it works

    # Let's delete the subscriptions
    try:
        all_subscriptions = qos_awereness.get_all_subscriptions(netapp_id)
        print(all_subscriptions)

        for subscription in all_subscriptions:
            id = subscription.link.split("/")[-1]
            print("Deleting subscription with id: " + id)
            qos_awereness.delete_subscription(netapp_id, id)
    except ApiException as ex:
        if ex.status == 404:
            print("No active transcriptions found")
        else:  # something else happened, re-throw the exception
            raise


def __test_tsn_manager(config,tsn_host,tsn_port):
    """
      Tests the TSN api name  with dummy data
     :param config:
   """

    netapp_name = "MyNetapp1"  # The name of our NetApp
    tsn = TSNManager(  # Initialization of the TNSManager
        folder_path_for_certificates_and_capif_api_key=config["folder_to_store_certificates"],
        capif_host=config["capif_host"],
        capif_https_port=config["capif_https_port"],
        https=False,
        tsn_host=tsn_host,
        tsn_port=tsn_port
    )

    # Retrieve information on all the available TSN profiles
    profiles = tsn.get_tsn_profiles()
    for profile in profiles:
        profile_configuration = profile.get_configuration_for_tsn_profile()

    # Let's select the last profile to apply,
    profile_to_apply = profiles[-1]
    profile_configuration = profile_to_apply.get_configuration_for_tsn_profile()
    # Let's create an TSN identifier for this Net App.
    # This tsn_netapp_identifier can be used in two scenarios
    # a) When you want to apply a profile configuration for your net app
    # b) When you want to clear a profile configuration for your net app
    tsn_netapp_identifier = tsn.TSNNetappIdentifier(netapp_name=netapp_name)

    #   Demonstrates how to clear a previously applied TSN profile configuration from a NetApp
    clearance_token = tsn.apply_tsn_profile_to_netapp(
        profile=profile_to_apply, tsn_netapp_identifier=tsn_netapp_identifier
    )

    tsn.clear_profile_for_tsn_netapp_identifier(tsn_netapp_identifier, clearance_token)

    # If we reached this point with no exceptions, then we tested all the endpoints of TSN




if __name__ == "__main__":
    config_file_path= "/home/alex/Projects/maggioli/evolved-5g/SDK-CLI/examples/netapp_capif_config/netapp_capif_connector_config_file.json"
    validate_all_endpoints_returned_by_service_discoverer(config_file_path)

