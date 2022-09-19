from evolved5g.swagger_client.rest import ApiException

from evolved5g.sdk import ConnectionMonitor
import emulator_utils
import datetime
import time



def showcase_create_subscription_and_retrieve_call_backs():
    """
    This example showcases how you can create a subscription to the 5G-API in order to monitor devices that are connected or disconnected to the network.
    In order to run this example you need to follow the instructions in  readme.md in order to a) run the NEF emulator
    and b) run a local webserver that will print the notifications it retrieves from the emulator.
    A testing local webserver (Flask webserver) can be initiated by running the examples/api.py
    """

    # Create a subscription, that will notify us 1000 times, for the next 1 day starting from now
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z"
    netapp_id = "myNetapp"
    host = emulator_utils.get_host_of_the_nef_emulator()
    token = emulator_utils.get_token()
    connection_monitor = ConnectionMonitor(host, token.access_token)
    # The following external identifier was copy pasted by the NEF emulator. Go to the Map and click on a User icon. There you can retrieve the id
    external_id = "10003@domain.com"

    # In this example we are running flask at http://localhost:5000 with a POST route to (/monitoring/callback) in order to retrieve notifications.
    # If you are running on the NEF emulator, you need to provide a notification_destination with an IP that the
    # NEF emulator docker can understand
    # For latest versions of docker this should be: http://host.docker.internal:5000/monitoring/callback"
    # Alternative you can find the ip of the HOST by running 'ip addr show | grep "\binet\b.*\bdocker0\b" | awk '{print $2}' | cut -d '/' -f 1'
    # See article for details: https://stackoverflow.com/questions/48546124/what-is-linux-equivalent-of-host-docker-internal/61001152

    # Let's monitor device 10003@domain.com and retrieve a notification to http://172.17.0.1:5000/monitoring/callback
    # everytime the device is not connected to the network
    subscription_when_not_connected = connection_monitor.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination="http://172.17.0.1:5000/monitoring/callback",
        monitoring_type= ConnectionMonitor.MonitoringType.INFORM_WHEN_NOT_CONNECTED,
        maximum_detection_time_in_seconds=5,
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time
    )

    # Let's monitor device 10003@domain.com and retrieve a notification to http://172.17.0.1:5000/monitoring/callback
    # everytime the device is connected to the network
    subscription_when_connected = connection_monitor.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination="http://172.17.0.1:5000/monitoring/callback",
        monitoring_type= ConnectionMonitor.MonitoringType.INFORM_WHEN_CONNECTED,
        maximum_detection_time_in_seconds=5,
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time
    )

    # From now on we should retrieve POST notifications to http://172.17.0.1:5000/monitoring/callback





def read_and_delete_all_existing_subscriptions():
    # How to get all subscriptions
    netapp_id = "myNetapp"
    host = emulator_utils.get_host_of_the_nef_emulator()
    token = emulator_utils.get_token()
    connection_monitor = ConnectionMonitor(host, token.access_token)

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
