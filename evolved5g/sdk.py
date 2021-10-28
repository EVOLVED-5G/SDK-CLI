"""SDK module"""
from evolved5g import swagger_client
from evolved5g.swagger_client import MonitoringEventAPIApi, \
    MonitoringEventSubscriptionCreate, MonitoringEventSubscription

"""
 This SKD class allows you to track devices and retrieve updates about their location.
 You can create subscriptions where each one of them can be used to track a device.
 A notification is sent to a callback url you will provide, everytime the user device changes Cell
"""


class LocationSubscriber:

    def __init__(self, host: str, bearer_access_token: str):
        """
             Initializes class LocationSubscriber

             :param str host: The url of the 5G-API
             :param str bearer_access_token: The beared access token that will be used to authenticate with the 5G-API
        """
        configuration = swagger_client.Configuration()
        configuration.host = host
        configuration.access_token = bearer_access_token
        api_client = swagger_client.ApiClient(configuration=configuration)
        self.monitoring_event_api = MonitoringEventAPIApi(api_client)

    def __create_subscription_request(self,
                                      external_id,
                                      msisdn,
                                      ipv4_addr,
                                      ipv6_addr,
                                      notification_destination,
                                      maximum_number_of_reports,
                                      monitor_expire_time) -> MonitoringEventSubscriptionCreate:
        monitoring_type = "LOCATION_REPORTING"
        return MonitoringEventSubscriptionCreate(external_id,
                                                 msisdn,
                                                 ipv4_addr,
                                                 ipv6_addr,
                                                 notification_destination,
                                                 monitoring_type,
                                                 maximum_number_of_reports,
                                                 monitor_expire_time)

    def create_subscription(self,
                            netapp_id: str,
                            external_id,
                            misisdn,
                            ipv4_addr,
                            ipv6_addr,
                            notification_destination,
                            maximum_number_of_reports,
                            monitor_expire_time):
        """
              Creates a subscription that will be used to retrieve Location information about a device.

              :param str external_id: string (The ID of the Netapp that creates a subscription)
              :param str external_id: Globally unique identifier containing a Domain Identifier and a Local Identifier. <Local Identifier>@<Domain Identifier>
              :param str misisdn: Mobile Subscriber ISDN number that consists of Country Code, National Destination Code and Subscriber Number.
              :param str ipv4_addr: String identifying an Ipv4 address
              :param ipv6_addr: String identifying an Ipv6 address.
              :param notification_destination: The url that you will notifications about the location of the user
              :param maximum_number_of_reports: Identifies the maximum number of event reports to be generated. Value 1 makes the Monitoring Request a One-time Request
              :param monitor_expire_time: Identifies the absolute time at which the related monitoring event request is considered to expire
        """
        body = self.__create_subscription_request(external_id,
                                                  misisdn,
                                                  ipv4_addr,
                                                  ipv6_addr,
                                                  notification_destination,
                                                  maximum_number_of_reports,
                                                  monitor_expire_time)

        # a monitoring event report
        response = self.monitoring_event_api.create_item_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post(
            body,
            netapp_id)
        return response

    def update_subscription(self,
                            netapp_id: str,
                            subscription_id: str,
                            external_id,
                            misisd,
                            ipv4_addr,
                            ipv6_addr,
                            notification_destination,
                            maximum_number_of_reports,
                            monitor_expire_time) -> MonitoringEventSubscription:
        """
             Creates a subscription that will be used to retrieve Location information about a device.

             :param str netapp_id: string (The ID of the Netapp that creates a subscription)
             :param str subscription_id: string (Identifier of the subscription resource)
             :param str external_id: Globally unique identifier containing a Domain Identifier and a Local Identifier. <Local Identifier>@<Domain Identifier>
             :param str misisdn: Mobile Subscriber ISDN number that consists of Country Code, National Destination Code and Subscriber Number.
             :param str ipv4_addr: String identifying an Ipv4 address
             :param ipv6_addr: String identifying an Ipv6 address.
             :param notification_destination: The url that you will notifications about the location of the user
             :param maximum_number_of_reports: Identifies the maximum number of event reports to be generated. Value 1 makes the Monitoring Request a One-time Request
             :param monitor_expire_time: Identifies the absolute time at which the related monitoring event request is considered to expire
       """
        body = self.__create_subscription_request(external_id,
                                                  misisd,
                                                  ipv4_addr,
                                                  ipv6_addr,
                                                  notification_destination,
                                                  maximum_number_of_reports,
                                                  monitor_expire_time)

        return self.monitoring_event_api.update_item_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put(
            body, netapp_id, subscription_id)

    def get_all_subscriptions(self, netapp_id: str,skip:int =0, limit: int=100):
        """
              Reads all active subscriptions

              :param skip: The number of subscriptions to skip
              :param limit: The maximum number of transcriptions to return
              :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        """

        return self.monitoring_event_api.read_active_subscriptions_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_get(
            netapp_id,
            skip=skip,
            limit=limit)

    def get_subscription(self, netapp_id: str, subscription_id: str) -> MonitoringEventSubscription:
        """
           Gets subscription by id

           :param str netapp_id: string (The ID of the Netapp that creates a subscription)
           :param str subscription_id: string (Identifier of the subscription resource)
        """
        return self.monitoring_event_api.read_item_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get(
            netapp_id,
            subscription_id)

    def delete_subscription(self, netapp_id: str, subscription_id: str):
        """
          Delete a subscription

          :param str netapp_id: string (The ID of the Netapp that creates a subscription)
          :param str subscription_id: string (Identifier of the subscription resource)
       """
        return self.monitoring_event_api.delete_item_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete(
            netapp_id,
            subscription_id)
