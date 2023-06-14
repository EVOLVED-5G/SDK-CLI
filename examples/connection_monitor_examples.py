from evolved5g.swagger_client.rest import ApiException

from evolved5g.sdk import ConnectionMonitor
import emulator_utils
import datetime
import time



def showcase_create_subscription_and_retrieve_call_backs():
    """
    This example showcases how you can create a subscription to the 5G-API in order to monitor devices that are connected or disconnected to the network.
    In order to run this example, to follow the instructions in  readme.md (https://evolved5g-cli.readthedocs.io/en/latest/libraries.html) in order to
     a) run the CAPIF server (this should run always first, because NEF in step b) has to communicate with NEF)
     b) run the NEF emulator
     c) connect your NetAPP to the CAPIF server (you have to do this only once)
     d) run a local webserver that will print the notifications it retrieves from the emulator. A testing local webserver (Flask webserver) can be initiated by running the examples/api.py
    """

    # Create a subscription, that will notify us 1000 times, for the next 1 day starting from now
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z"
    netapp_id = "myNetapp"
    connection_monitor = ConnectionMonitor(nef_url=emulator_utils.get_url_of_the_nef_emulator(),
                                           folder_path_for_certificates_and_capif_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                           capif_host=emulator_utils.get_capif_host(),
                                           capif_https_port=emulator_utils.get_capif_https_port())
    # The following external identifier was copy pasted by the NEF emulator. Go to the Map and click on a User icon. There you can retrieve the id
    external_id = "10003@domain.com"

    # In this example we are running flask at http://localhost:5000 with a POST route to (/monitoring/callback) in order to retrieve notifications.
    # If you are running on the NEF emulator, you need to provide a notification_destination with an IP that the
    # NEF emulator docker can understand
    # For latest versions of docker this should be: http://host.docker.internal:5000/monitoring/callback"
    # Alternative you can find the ip of the HOST by running 'ip addr show | grep "\binet\b.*\bdocker0\b" | awk '{print $2}' | cut -d '/' -f 1'
    # See article for details: https://stackoverflow.com/questions/48546124/what-is-linux-equivalent-of-host-docker-internal/61001152

    # Let's monitor device 10003@domain.com and retrieve a notification to http://172.17.0.1:5000/monitoring/callback
    # everytime the device is not connected (has lost access) to the network.
    # If connection has been lost, we want the network to inform us after 5 seconds.
    # For this reason we set wait_time_before_sending_notification_in_seconds =5
    # This is useful because in our netapp we may not care about "small lasting" disturbances/disconnections.
    # For example consider the following scenario:
    # We
    #  a) set wait_time_before_sending_notification_in_seconds =5 in the code below and
    #  b) the netapp loses connection at 12:00:00 and
    #  c) the netapp regains connection at 12:00:02
    # because only 2 seconds have passed with no connection, we will not retrieve a notification from the network.
    subscription_when_not_connected = connection_monitor.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination="http://172.17.0.1:5000/monitoring/callback",
        monitoring_type= ConnectionMonitor.MonitoringType.INFORM_WHEN_NOT_CONNECTED,
        wait_time_before_sending_notification_in_seconds=5,
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time
    )

    # Let's monitor device 10003@domain.com and retrieve a notification to http://172.17.0.1:5000/monitoring/callback
    # everytime the device is connected to (has gained access to) the network
    # If connection is alive and active, we want the network to inform us after 5 seconds.
    # For this reason we set wait_time_before_sending_notification_in_seconds =5
    # This is useful because in our netapp we may not care about small lasting disturbances/changes in the connectivity
    # For example consider the following scenario:
    # We
    #  a) set wait_time_before_sending_notification_in_seconds =5 and
    #  b) a net that was previously disconnected, connects to the network at 12:00:00 and
    #  c) the netapp disconnects again at 12:00:02
    # because only 2 seconds have passed with connection, we will not retrieve a notification from the network.
    subscription_when_connected = connection_monitor.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination="http://172.17.0.1:5000/monitoring/callback",
        monitoring_type= ConnectionMonitor.MonitoringType.INFORM_WHEN_CONNECTED,
        wait_time_before_sending_notification_in_seconds=5,
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time
    )

    # From now on we should retrieve POST notifications to http://172.17.0.1:5000/monitoring/callback





def read_and_delete_all_existing_subscriptions():
    # How to get all subscriptions
    netapp_id = "myNetapp"
    connection_monitor = ConnectionMonitor(nef_url=emulator_utils.get_url_of_the_nef_emulator(),
                                           folder_path_for_certificates_and_capif_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                           capif_host=emulator_utils.get_capif_host(),
                                           capif_https_port=emulator_utils.get_capif_https_port())

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
        else: #something else happened, re-throw the exception
            raise



if __name__ == "__main__":
    read_and_delete_all_existing_subscriptions()
    showcase_create_subscription_and_retrieve_call_backs()
