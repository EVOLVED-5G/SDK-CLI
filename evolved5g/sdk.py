"""SDK module"""

""" This helper class allows you to subscribe to the Location monitoring API """


class LocationHelper:

    def __init__(self, host, access_token):
        self.host = host
        """The host of the API (EX. http://localhost:8888"""
        self.accessToken = access_token
        """The beared key of the API """

    def create_subscription(self, netapp_id: str):
        # todo:  POST to /api/v1/3gpp-monitoring-event/v1/{scsAsId}/subscriptions
        raise NotImplementedError

    def get_all_subscriptions(self, netapp_id: str):
        # todo: GET to /api/v1/3gpp-monitoring-event/v1/{scsAsId}/subscriptions
        raise NotImplementedError

    def get_subscription(self, netapp_id: str, subscription_id: str):
        # todo: GET /api/v1/3gpp-monitoring-event/v1/{scsAsId}/subscriptions/{subscriptionId}
        raise NotImplementedError

    def update_subscription(self, netapp_id: str, subscription_id: str):
        raise NotImplementedError

    def delete_subscription(self, netapp_id: str, subscription_id: str):
        raise NotImplementedError
