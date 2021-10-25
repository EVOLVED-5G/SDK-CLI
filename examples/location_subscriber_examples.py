from evolved5g.sdk import LocationSubscriber
import emulator_utils
import datetime
import uuid



def showcase_create_subscription_and_retrieve_call_backs():
    """
    This example showcases how you can create a subscription to the 5G-API in order to monitor device location.
    In order to run this example you need to follow the instructions in  readme.md in order to run the NEF emulator
    and a local webserver that will print the location notifications it retrieves from the emulator
    """

    ## Create a subscription, that will notify us 30 times, for the next 15 minutes starting from now
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=15)).isoformat() + "Z"
    netapp_id = "myNetapp"
    host = emulator_utils.get_host_of_the_nef_emulator()
    token = emulator_utils.get_token()
    location_subscriber = LocationSubscriber(host, token.access_token)
    # Let's create a subscription id
    subscription = location_subscriber.create_subscription(
                                                   netapp_id= netapp_id,
                                                   external_id= "123456789@domain.com",
                                                   misisdn= "918369110173",
                                                   ipv4_addr="10.0.0.1",
                                                   ipv6_addr="::1",
                                                   notification_destination ="http://127.0.0.1:5000/monitoring/callback",
                                                   maximum_number_of_reports=30,
                                                   monitor_expire_time=expire_time
                                               )

    print(subscription)

    # Get all subscriptions
    all_subscriptions = location_subscriber.get_all_subscriptions(netapp_id)
    print(all_subscriptions)

    # Request information about a subscription
    subscription_info = location_subscriber.get_subscription(netapp_id, subscription.link)
    print(subscription_info)

if __name__ == "__main__":
    showcase_create_subscription_and_retrieve_call_backs()

