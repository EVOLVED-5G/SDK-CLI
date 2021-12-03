"""SDK module"""
from typing import List

from evolved5g import swagger_client
from enum import Enum
from evolved5g.swagger_client import MonitoringEventAPIApi, \
    MonitoringEventSubscriptionCreate, MonitoringEventSubscription, SessionWithQoSAPIApi, \
    AsSessionWithQoSSubscriptionCreate, Snssai, UsageThreshold, AsSessionWithQoSSubscription, QosMonitoringInformation, \
    RequestedQoSMonitoringParameters, ReportingFrequency


class LocationSubscriber:

    def __init__(self, host: str, bearer_access_token: str):
        """
            Initializes class LocationSubscriber.
            This SKD class allows you to track devices and retrieve updates about their location.
            You can create subscriptions where each one of them can be used to track a device.
            A notification is sent to a callback url you will provide, everytime the user device changes Cell

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
                                      notification_destination,
                                      maximum_number_of_reports,
                                      monitor_expire_time) -> MonitoringEventSubscriptionCreate:
        monitoring_type = "LOCATION_REPORTING"
        return MonitoringEventSubscriptionCreate(external_id,
                                                 notification_destination,
                                                 monitoring_type,
                                                 maximum_number_of_reports,
                                                 monitor_expire_time)

    def create_subscription(self,
                            netapp_id: str,
                            external_id,
                            notification_destination,
                            maximum_number_of_reports,
                            monitor_expire_time):
        """
              Creates a subscription that will be used to retrieve Location information about a device.

              :param str netapp_id: string (The ID of the Netapp that creates a subscription)
              :param str external_id: Globally unique identifier containing a Domain Identifier and a Local Identifier. <Local Identifier>@<Domain Identifier>
              :param notification_destination: The url that you will notifications about the location of the user
              :param maximum_number_of_reports: Identifies the maximum number of event reports to be generated. Value 1 makes the Monitoring Request a One-time Request
              :param monitor_expire_time: Identifies the absolute time at which the related monitoring event request is considered to expire
        """
        body = self.__create_subscription_request(external_id,
                                                  notification_destination,
                                                  maximum_number_of_reports,
                                                  monitor_expire_time)

        # a monitoring event report
        response = self.monitoring_event_api.create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post(
            body,
            netapp_id)
        return response

    def update_subscription(self,
                            netapp_id: str,
                            subscription_id: str,
                            external_id,
                            notification_destination,
                            maximum_number_of_reports,
                            monitor_expire_time) -> MonitoringEventSubscription:
        """
             Creates a subscription that will be used to retrieve Location information about a device.

             :param str netapp_id: string (The ID of the Netapp that creates a subscription)
             :param str subscription_id: string (Identifier of the subscription resource)
             :param str external_id: Globally unique identifier containing a Domain Identifier and a Local Identifier. <Local Identifier>@<Domain Identifier>
             :param notification_destination: The url that you will notifications about the location of the user
             :param maximum_number_of_reports: Identifies the maximum number of event reports to be generated. Value 1 makes the Monitoring Request a One-time Request
             :param monitor_expire_time: Identifies the absolute time at which the related monitoring event request is considered to expire
       """
        body = self.__create_subscription_request(external_id,
                                                  notification_destination,
                                                  maximum_number_of_reports,
                                                  monitor_expire_time)

        return self.monitoring_event_api.update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put(
            body, netapp_id, subscription_id)

    def get_all_subscriptions(self, netapp_id: str, skip: int = 0, limit: int = 100):
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
        return self.monitoring_event_api.read_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get(
            netapp_id,
            subscription_id)

    def delete_subscription(self, netapp_id: str, subscription_id: str):
        """
          Delete a subscription

          :param str netapp_id: string (The ID of the Netapp that creates a subscription)
          :param str subscription_id: string (Identifier of the subscription resource)
       """
        return self.monitoring_event_api.delete_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete(
            netapp_id,
            subscription_id)


class QosAwareness:
    class IdentifierType(Enum):
        IP_V4_ADDRESS = 1,
        IP_V6_ADDRESS = 2
        MAC_ADDRESS = 3

    class NonGBRQosReference(Enum):
        """
            Non guaranteed bit rate Qos Reference values.
            NEF Emulator has an endpoint that explains these GET /api/v1/qosInfo/qosCharacteristics
        """
        TCP_BASED = 9,
        LIVE_STREAMING = 8

    class GBRQosReference(Enum):
        """
           Guaranteed bit rate Qos Reference values
           NEF Emulator has an endpoint that explains these GET /api/v1/qosInfo/qosCharacteristics
        """
        CONVERSATIONAL_VOICE = 1,
        CONVERSATIONAL_VIDEO = 2,
        DISCRETE_AUTOMATION = 82

    class QosMonitoringParameter(Enum):
        """
        It's easier for the developer to use Enums in the code rather the swagger type RequestedQoSMonitoringParameters
        which inherits from object.
        The mapping is done here, and QosAwareness uses QosMonitoringParameter in method declarations
        """
        UPLINK = RequestedQoSMonitoringParameters.UPLINK,
        DOWNLINK = RequestedQoSMonitoringParameters.DOWNLINK,
        ROUNDTRIP = RequestedQoSMonitoringParameters.ROUND_TRIP



    def __init__(self, host: str, bearer_access_token: str):
        """
            Initializes class QosAwareness.
            This SKD class allows you to requests QoS from a set of standardized values for better service experience.

            You can create subscriptions where each one of them has specific QoS parameters.
            A notification is sent to a callback url you will provide, informing you in case tge QoS targets can no
             longer be fullfilledd

             :param str host: The url of the 5G-API
             :param str bearer_access_token: The beared access token that will be used to authenticate with the 5G-API
        """
        configuration = swagger_client.Configuration()
        configuration.host = host
        configuration.access_token = bearer_access_token
        api_client = swagger_client.ApiClient(configuration=configuration)
        self.qos_api = SessionWithQoSAPIApi(api_client)

    def __create_subscription_request(self,
                                      equipment_identifier: str,
                                      identifier_type: IdentifierType,
                                      notification_destination: str,
                                      qos_reference: int,
                                      alt_qo_s_references,
                                      usage_threshold: UsageThreshold,
                                      qos_mon_info
                                      ) -> AsSessionWithQoSSubscriptionCreate:
        ip4_address_value = equipment_identifier if identifier_type == QosAwareness.IdentifierType.IP_V4_ADDRESS else None
        ip6_address_value = equipment_identifier if identifier_type == QosAwareness.IdentifierType.IP_V6_ADDRESS else None
        mac_address_value = equipment_identifier if identifier_type == QosAwareness.IdentifierType.MAC_ADDRESS else None

        # This field indicates in which network slice the UE (vertical app) wants to establish or modify a QoS Flow.
        # There are no network slices, this field exists only for future compatibility
        # Since there is no functionality implemented you should always leave the default value sst : 1 and sd : “000001”
        snssai = Snssai()

        # Same as APN in 4G, identifies the external data network (i.e., internet). Same applies here as snssai. There is no functionality implemented
        dnn = "province1.mnc01.mcc202.gprs"
        return AsSessionWithQoSSubscriptionCreate(ipv4_addr=ip4_address_value,
                                                  ipv6_addr=ip6_address_value,
                                                  mac_addr=mac_address_value,
                                                  notification_destination=notification_destination,
                                                  snssai=snssai,
                                                  dnn=dnn,
                                                  qos_reference=qos_reference,
                                                  alt_qo_s_references=alt_qo_s_references,
                                                  usage_threshold=usage_threshold,
                                                  qos_mon_info=qos_mon_info
                                                  )

    def create_non_guaranteed_bit_rate_subscription(self,
                                                    netapp_id,
                                                    equipment_identifier: str,
                                                    identifier_type: IdentifierType,
                                                    notification_destination: str,
                                                    non_gbr_qos_reference: NonGBRQosReference,
                                                    usage_threshold: UsageThreshold
                                                    ) -> AsSessionWithQoSSubscription:
        body = self.__create_subscription_request(equipment_identifier,
                                                  identifier_type,
                                                  notification_destination,
                                                  non_gbr_qos_reference.value,
                                                  alt_qo_s_references=None,
                                                  usage_threshold=usage_threshold,
                                                  qos_mon_info=None
                                                  )

        response = self.qos_api.create_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_post(
            body,
            netapp_id)
        return response

    def update_non_guaranteed_bit_rate_subscription(self,
                                                    netapp_id: str,
                                                    subscription_id: str,
                                                    equipment_identifier: str,
                                                    identifier_type: IdentifierType,
                                                    notification_destination: str,
                                                    non_gbr_qos_reference: NonGBRQosReference,
                                                    usage_threshold: UsageThreshold) -> AsSessionWithQoSSubscription:

        body = self.__create_subscription_request(equipment_identifier,
                                                  identifier_type,
                                                  notification_destination,
                                                  non_gbr_qos_reference.value,
                                                  alt_qo_s_references=None,
                                                  usage_threshold=usage_threshold,
                                                  qos_mon_info=None
                                                  )

        return self.qos_api.update_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_subscription_id_put(
            body, netapp_id, subscription_id)

    def create_guaranteed_bit_rate_subscription(self,
                                                netapp_id,
                                                equipment_identifier: str,
                                                identifier_type: IdentifierType,
                                                notification_destination: str,
                                                gbr_qos_reference: GBRQosReference,
                                                usage_threshold: UsageThreshold,
                                                qos_monitoring_parameter:QosMonitoringParameter,
                                                threshold: int,
                                                wait_time_between_reports: int
                                                ) -> AsSessionWithQoSSubscription:

        alt_qo_s_references, qos_monitoring_info = self.__create_gbr_request_qo_parameters(gbr_qos_reference,
                                                                                           qos_monitoring_parameter,
                                                                                           threshold,
                                                                                    wait_time_between_reports)

        body = self.__create_subscription_request(equipment_identifier,
                                                  identifier_type,
                                                  notification_destination,
                                                  qos_reference=gbr_qos_reference.value,
                                                  alt_qo_s_references=alt_qo_s_references,
                                                  usage_threshold=usage_threshold,
                                                  qos_mon_info=qos_monitoring_info
                                                  )

        response = self.qos_api.create_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_post(
            body,
            netapp_id)
        return response


    def __create_gbr_request_qo_parameters(self, gbr_qos_reference, qos_monitoring_parameter, threshold, wait_time_between_reports):
        # Contains the remaining Guaranted Qos references, as fallback
        alt_qo_s_references = []
        for qos_reference in QosAwareness.GBRQosReference:
            if qos_reference != gbr_qos_reference:
                alt_qo_s_references.append(qos_reference.value)
        # User has to specify
        lat_thresh_ul = threshold if qos_monitoring_parameter == QosAwareness.QosMonitoringParameter.UPLINK else None
        lat_thresh_dl = threshold if qos_monitoring_parameter == QosAwareness.QosMonitoringParameter.DOWNLINK else None
        lat_thresh_rp = threshold if qos_monitoring_parameter == QosAwareness.QosMonitoringParameter.ROUNDTRIP else None
        # WaitTime since we are doing EVENT_TRIGGERED ONLY
        qos_monitoring_info = QosMonitoringInformation(
            req_qos_mon_params=[qos_monitoring_parameter.value],
            rep_freqs=[ReportingFrequency.EVENT_TRIGGERED],
            lat_thresh_dl=lat_thresh_dl,
            lat_thresh_ul=lat_thresh_ul,
            lat_thresh_rp=lat_thresh_rp,
            wait_time=wait_time_between_reports,  # Has to specified in EVENT_TRIGGERED_ONLY
            rep_period=None  # Has to specified in PERIODIC ONLY, currently not supported
        )
        return alt_qo_s_references, qos_monitoring_info

    def update_guaranteed_bit_rate_subscription(self,
                                                netapp_id: str,
                                                subscription_id: str,
                                                equipment_identifier: str,
                                                identifier_type: IdentifierType,
                                                notification_destination: str,
                                                gbr_qos_reference: GBRQosReference,
                                                usage_threshold: UsageThreshold,
                                                qos_monitoring_parameter:QosMonitoringParameter,
                                                threshold: int,
                                                wait_time_between_reports: int) -> AsSessionWithQoSSubscription:

        alt_qo_s_references, qos_monitoring_info = self.__create_gbr_request_qo_parameters(gbr_qos_reference,
                                                                                           qos_monitoring_parameter,
                                                                                           threshold,
                                                                                           wait_time_between_reports)

        body = self.__create_subscription_request(equipment_identifier,
                                                  identifier_type,
                                                  notification_destination,
                                                  qos_reference=gbr_qos_reference.value,
                                                  alt_qo_s_references=alt_qo_s_references,
                                                  usage_threshold=usage_threshold,
                                                  qos_mon_info=qos_monitoring_info
                                                  )
        return self.qos_api.update_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_subscription_id_put(
            body, netapp_id, subscription_id)
        pass

    def get_all_subscriptions(self, netapp_id: str, skip: int = 0, limit: int = 100) -> List[
        AsSessionWithQoSSubscription]:
        """
              Reads all active subscriptions

              :param skip: The number of subscriptions to skip
              :param limit: The maximum number of transcriptions to return
              :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        """

        return self.qos_api.read_active_subscriptions_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_get(
            netapp_id,
            skip=skip,
            limit=limit)

    def get_subscription(self, netapp_id: str, subscription_id: str) -> AsSessionWithQoSSubscription:

        return self.qos_api.read_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_subscription_id_get(
            netapp_id,
            subscription_id)

    def delete_subscription(self, netapp_id: str, subscription_id: str):
        """
          Delete a subscription

          :param str netapp_id: string (The ID of the Netapp that creates a subscription)
          :param str subscription_id: string (Identifier of the subscription resource)
       """
        return self.qos_api.delete_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_subscription_id_delete(
            netapp_id,
            subscription_id)
