"""SDK module"""
from evolved5g.swagger_client import MonitoringEventAPIApi, AsSessionWithQoSSubscription, \
    MonitoringEventSubscriptionCreate, MonitoringEventSubscription
from evolved5g.swagger_client.api_client import ApiClient

""" This helper class allows you to subscribe to the Location monitoring API """


class LocationHelper:

    def __init__(self, apiClient: ApiClient):
        self.monitoring_event_api = MonitoringEventAPIApi(apiClient)

    def __create_subscription_request(self,
                                      external_id,
                                      msisdn,
                                      ipv4_addr,
                                      ipv6_addr,
                                      notification_destination,
                                      maximum_number_of_reports,
                                      monitor_expire_time) -> MonitoringEventSubscriptionCreate:

        monitoring_type = "LOCATION_REPORTING"
        return MonitoringEventSubscriptionCreate(external_id,msisdn,ipv4_addr,ipv6_addr,notification_destination,
                                                 monitoring_type,
                                                 maximum_number_of_reports,
                                                 monitor_expire_time)

    def create_subscription(self, netapp_id: str,
                            external_id,
                            misisd,
                            ipv4_addr, #todo: to discuss, could the SKD get it automatically? or should the developer pass it
                            ipv6_addr,
                            notification_destination,
                            maximum_number_of_reports,
                            monitor_expire_time) -> MonitoringEventSubscription:

        body = self.__create_subscription_request(external_id, misisd, ipv4_addr, ipv6_addr, notification_destination,
                                                  maximum_number_of_reports, monitor_expire_time)
        #todo: Do we always return a MonitoringEventSubscription ? Why at swagger it has a 200 response too that returns
        # a monitoring event report
        return self.monitoring_event_api.create_item_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post(body,
                                                                                                          netapp_id)

    def update_subscription(self, netapp_id: str, subscription_id: str, external_id,
                            misisd, ipv4_addr, ipv6_addr, notification_destination,
                            maximum_number_of_reports, monitor_expire_time) -> MonitoringEventSubscription:

        body = self.__create_subscription_request(external_id, misisd, ipv4_addr, ipv6_addr, notification_destination,
                                                  maximum_number_of_reports, monitor_expire_time)
        return self.monitoring_event_api.update_item_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put(
            body, netapp_id, subscription_id)

    def get_all_subscriptions(self, netapp_id: str):
        #todo: check the return type here
        return self.monitoring_event_api.read_active_subscriptions_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_get(
            netapp_id)

    def get_subscription(self, netapp_id: str, subscription_id: str) -> MonitoringEventSubscription:
        return self.monitoring_event_api.read_item_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get(
            netapp_id,
            subscription_id)



    def delete_subscription(self, netapp_id: str, subscription_id: str):
        return self.monitoring_event_api.delete_item_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete(
            netapp_id,
            subscription_id)
