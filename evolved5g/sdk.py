"""SDK module"""
from typing import List

from evolved5g import swagger_client
from abc import ABC, abstractmethod
from enum import Enum
from evolved5g.swagger_client import MonitoringEventAPIApi, \
    MonitoringEventSubscriptionCreate, MonitoringEventSubscription, SessionWithQoSAPIApi, \
    AsSessionWithQoSSubscriptionCreate, Snssai, UsageThreshold, AsSessionWithQoSSubscription, QosMonitoringInformation, \
    RequestedQoSMonitoringParameters, ReportingFrequency, MonitoringEventReport, CellsApi, Cell
import datetime


class MonitoringSubscriber(ABC):
    def __init__(self, host: str, bearer_access_token: str):
        configuration = swagger_client.Configuration()
        configuration.host = host
        configuration.access_token = bearer_access_token
        api_client = swagger_client.ApiClient(configuration=configuration)
        self.monitoring_event_api = MonitoringEventAPIApi(api_client)
        self.cell_api = CellsApi(api_client)

    def create_subscription_request(self,
                                      monitoring_type,
                                      external_id,
                                      notification_destination,
                                      maximum_number_of_reports,
                                      monitor_expire_time,
                                      maximum_detection_time,
                                      reachability_type) -> MonitoringEventSubscriptionCreate:
        return MonitoringEventSubscriptionCreate(external_id,
                                                 notification_destination,
                                                 monitoring_type,
                                                 maximum_number_of_reports,
                                                 monitor_expire_time,
                                                 maximum_detection_time,
                                                 reachability_type)

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


class LocationSubscriber(MonitoringSubscriber):

    def __init__(self, host: str, bearer_access_token: str):
        """
            Initializes class LocationSubscriber.
            This SKD class allows you to track devices and retrieve updates about their location.
            You can create subscriptions where each one of them can be used to track a device.
            A notification is sent to a callback url you will provide, everytime the user device changes Cell

             :param str host: The url of the 5G-API
             :param str bearer_access_token: The bearer access token that will be used to authenticate with the 5G-API
        """
        super().__init__(host,bearer_access_token)

    def __get_monitoring_type(self):
        return "LOCATION_REPORTING"

    def get_location_information(self, netapp_id: str,
                                 external_id) -> MonitoringEventReport:
        """
             Returns the location of a specific device.
             This is equivalent to creating a subscription with maximum_number_of_reports = 1
             :param str netapp_id: string (The ID of the Netapp that creates a subscription)
             :param str external_id: Globally unique identifier containing a Domain Identifier and a Local Identifier. <Local Identifier>@<Domain Identifier>
       """

        # create a dummy expiration time. Since we are requesting for only 1 report, we will get the location information back instantly
        monitor_expire_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).isoformat() + "Z"
        body = self.create_subscription_request(external_id,
                                                  self.__get_monitoring_type(),
                                                  None,
                                                  maximum_number_of_reports=1,
                                                  monitor_expire_time=monitor_expire_time,
                                                  maximum_detection_time = None,
                                                  reachability_type = None)

        # a monitoring event report
        response = self.monitoring_event_api.create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post(
            body,
            netapp_id)
        return response

    def get_coordinates_of_cell(self, cell_id: str) -> Cell:
        """
             Returns information about a specific cell

             :param str cell_id: string (The ID of the cell)
       """
        return self.cell_api.read_cell_api_v1_cells_cell_id_get(cell_id)

    def create_subscription(self,
                            netapp_id: str,
                            external_id,
                            notification_destination,
                            maximum_number_of_reports,
                            monitor_expire_time) -> MonitoringEventSubscription:
        """
              Creates a subscription that will be used to retrieve Location information about a device.

              :param str netapp_id: string (The ID of the Netapp that creates a subscription)
              :param str external_id: Globally unique identifier containing a Domain Identifier and a Local Identifier. <Local Identifier>@<Domain Identifier>
              :param notification_destination: The url that you will notifications about the location of the user
              :param maximum_number_of_reports: Identifies the maximum number of event reports to be generated. Value 1 makes the Monitoring Request a One-time Request
              :param monitor_expire_time: Identifies the absolute time at which the related monitoring event request is considered to expire
        """
        body = self.create_subscription_request(self.__get_monitoring_type(),
                                                  external_id,
                                                  notification_destination,
                                                  maximum_number_of_reports,
                                                  monitor_expire_time,
                                                  None,
                                                  None)

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
        body = self.create_subscription_request(self.__get_monitoring_type(),
                                                  external_id,
                                                  notification_destination,
                                                  maximum_number_of_reports,
                                                  monitor_expire_time,
                                                  None,
                                                  None)

        return self.monitoring_event_api.update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put(
            body, netapp_id, subscription_id)


class ConnectionMonitor(MonitoringSubscriber):

    class MonitoringType(Enum):
        """
            This enum is used to describe what the kind of monitoring you will apply to your devices.
            If INFORM_WHEN_CONNECTED is selected then the 5G API will send you a notification is the device has not been connected to the 5G Network for the past X seconds
            If INFORM_WHEN_NOT_CONNECTED is selected then the 5G API will send you a notification is the device has not been connected to the 5G Network for the past X seconds
        """
        INFORM_WHEN_CONNECTED = 1
        INFORM_WHEN_NOT_CONNECTED = 2

    def __init__(self, host: str, bearer_access_token: str):
        """
            Initializes class ConnectionMonitor.
            Consider a scenario where a NetApp wants to monitor 100 devices in the 5G Network.
            The netapp wants to track, at any given time how many NetApps are connected to the 5G Network and how many netApps are disconnected.

            Using ConnectionMonitor the NetApp can retrieve notifications by the 5G Network for individual devices when
            Connection is lost (for example the user device has not been connected to the 5G network for the past 10 seconds)
            Connection is alive (for example the user device has been connected to the 5G network for the past 10 seconds)

            :param str host: The url of the 5G-API
            :param str bearer_access_token: The bearer access token that will be used to authenticate with the 5G-API
        """
        super().__init__(host,bearer_access_token)

    def __get_monitoring_type(self, monitoring_type: MonitoringType):
        if monitoring_type == self.MonitoringType.INFORM_WHEN_CONNECTED:
            return "UE_REACHABILITY"
        else:
            return "LOSS_OF_CONNECTIVITY"

    def create_subscription(self,
                            netapp_id: str,
                            external_id,
                            notification_destination,
                            monitoring_type: MonitoringType,
                            wait_time_before_sending_notification_in_seconds: int,
                            maximum_number_of_reports,
                            monitor_expire_time) -> MonitoringEventSubscription:
        """
              Creates a subscription that will be used to track the Network Connectivity about a device.

              :param str netapp_id: string (The ID of the Netapp that creates a subscription)
              :param str external_id: Globally unique identifier containing a Domain Identifier and a Local Identifier. <Local Identifier>@<Domain Identifier>
              :param notification_destination: The url that you will retrieve notifications when a device is connected or not connected for the past X seconds
              :param monitoring_type: If you choose MonitoringType.INFORM_WHEN_CONNECTED you will receive a notification every time the device is connected to the network
               If you choose MonitoringType.INFORM_WHEN_NOT_CONNECTED you will receive a notification every time the device is not connected to the network
              :param wait_time_before_sending_notification_in_seconds: How long the network should wait before it sends you a notification.
               This is usefull because in our netapp we may not care about small lasting disturbances/disconnections. For example consider the following scenario:
                  a) We set monitoring_type to INFORM_WHEN_NOT_CONNECTED to get notification when the netapp looses connection
                  b) We set wait_time_before_sending_notification_in_seconds =5 and
                  c) the netapp loses connection at 12:00:00 and
                  d) the netapp regains connection at 12:00:02
                 because only 2 seconds have passed with no connection, we will not retrieve a notification from the network. At least 5 seconds must pass in order to get a notification
              :param maximum_number_of_reports: Identifies the maximum number of event reports to be generated. Value 1 makes the Monitoring Request a One-time Request
              :param monitor_expire_time: Identifies the absolute time at which the related monitoring event request is considered to expire
        """
        body = self.create_subscription_request(self.__get_monitoring_type(monitoring_type),
                                                  external_id,
                                                  notification_destination,
                                                  maximum_number_of_reports,
                                                  monitor_expire_time,
                                                  wait_time_before_sending_notification_in_seconds,
                                                  "DATA")

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
                            monitoring_type: MonitoringType,
                            wait_time_before_sending_notification_in_seconds: int,
                            maximum_number_of_reports,
                            monitor_expire_time) -> MonitoringEventSubscription:
        """
             Creates a subscription that will be used to retrieve Location information about a device.

             :param str netapp_id: string (The ID of the Netapp that creates a subscription)
             :param str subscription_id: string (Identifier of the subscription resource)
             :param str external_id: Globally unique identifier containing a Domain Identifier and a Local Identifier. <Local Identifier>@<Domain Identifier>
              :param notification_destination: The url that you will retrieve notifications when a device is connected or not connected for the past X seconds
              :param monitoring_type: If you choose MonitoringType.INFORM_WHEN_CONNECTED you will receive a notification every time the device is connected to the network
               If you choose MonitoringType.INFORM_WHEN_NOT_CONNECTED you will receive a notification every time the device is not connected to the network
              :param wait_time_before_sending_notification_in_seconds: How long the network should wait before it sends you a notification.
               This is usefull because in our netapp we may not care about small lasting disturbances/disconnections. For example consider the following scenario:
                  a) We set monitoring_type to INFORM_WHEN_NOT_CONNECTED to get notification when the netapp looses connection
                  b) We set wait_time_before_sending_notification_in_seconds =5 and
                  c) the netapp loses connection at 12:00:00 and
                  d) the netapp regains connection at 12:00:02
                 because only 2 seconds have passed with no connection, we will not retrieve a notification from the network. At least 5 seconds must pass in order to get a notification
              :param maximum_number_of_reports: Identifies the maximum number of event reports to be generated. Value 1 makes the Monitoring Request a One-time Request
              :param monitor_expire_time: Identifies the absolute time at which the related monitoring event request is considered to expire
       """
        body = self.create_subscription_request(monitoring_type,
                                                  external_id,
                                                  notification_destination,
                                                  maximum_number_of_reports,
                                                  monitor_expire_time,
                                                  wait_time_before_sending_notification_in_seconds,
                                                  "DATA")

        return self.monitoring_event_api.update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put(
            body, netapp_id, subscription_id)


class QosAwareness:
    class NetworkIdentifier(Enum):
        """
            This enum is used to describe what kind of user equipment identifier you are going to pass
            to the subscription creation endpoints
        """
        IP_V4_ADDRESS = 1
        IP_V6_ADDRESS = 2
        MAC_ADDRESS = 3

    class NonGBRQosReference(Enum):
        """
            Non guaranteed bit rate Qos Reference values.
            NEF Emulator has an endpoint that explains these GET /api/v1/qosInfo/qosCharacteristics
        """
        TCP_BASED = 9
        LIVE_STREAMING = 7

    class GBRQosReference(Enum):
        """
           Guaranteed bit rate Qos Reference values
           NEF Emulator has an endpoint that explains these GET /api/v1/qosInfo/qosCharacteristics
        """
        CONVERSATIONAL_VOICE = 1
        CONVERSATIONAL_VIDEO = 2
        DISCRETE_AUTOMATION = 82

    class QosMonitoringParameter(Enum):
        """
            The type of QoS connection that you can monitor.
        """
        UPLINK = "UPLINK"
        DOWNLINK = "DOWNLINK"
        ROUNDTRIP = "ROUND_TRIP"

    class GuaranteedBitRateReportingMode(ABC):
        @abstractmethod
        def get_reporting_mode(self):
            pass

        @abstractmethod
        def get_reporting_configuration(self):
            pass

    class EventTriggeredReportingConfiguration(GuaranteedBitRateReportingMode):
        """
         Use this class to configure how you will receive reports (notification) from the 5G Network when
         Quaranteed Bit Rate can be achieved (nor not achieved).
         Consider a scenario were you want to monitor your UPLINK connection and make sure the delay
         of data packages is always less than 20 milliseconds.

         Use Event Triggered reporting if you want to retrieve an event every time the network changes:
         For example:the QoS threshold (minimum delay of 20ms) cannot be achieved.
         a) when the 20ms delay on UPLINK was established, but suddenly it can not be guaranteed, you will receive a notification.
         a) when the 20ms delay on UPLINK was not established, but suddenly it can be guaranteed, you will receive a notification.

        """

        wait_time_in_seconds: int

        def __init__(self, wait_time_in_seconds: int):
            """
            :param wait_time: Specifies the minimum amount of time we want to wait between two different notifications.
            For example in a very unstable network you may not want to receive notifications every second.
            Setting wait_time = 5 seconds, will mean that in case that the network is still unstable, you won't retrieve
            more than one notification in a duration of 5 seconds.
            """
            self.wait_time_in_seconds = wait_time_in_seconds

        def get_reporting_mode(self):
            return ReportingFrequency.EVENT_TRIGGERED

        def get_reporting_configuration(self):
            return self.wait_time_in_seconds

    class PeriodicReportConfiguration(GuaranteedBitRateReportingMode):
        """
        Use this class to configure how you will receive reports (notification) from the 5G Network when
        Quaranted Bit Rate can be achieved (nor not achieved).
        Consider a scenario were you want to monitor your UPLINK connection and make sure the delay
        of data packages is always less than 20 milliseconds.

        Use Periodic reporting if you want to retrieve an event about the status of the network every X seconds.
        For example every X seconds get a report (notification) if the minimum delay of 20ms for your UPLINK connection
        is guaranteed, or not!

       """
        repetition_period_in_seconds: int

        def __init__(self, repetition_period_in_seconds: int):
            self.repetition_period_in_seconds = repetition_period_in_seconds

        def get_reporting_mode(self):
            return ReportingFrequency.PERIODIC

        def get_reporting_configuration(self):
            return self.repetition_period_in_seconds

    def __init__(self, host: str, bearer_access_token: str):
        """
            Initializes class QosAwareness.
            This SKD class allows you to requests QoS from a set of standardized values for better service experience.

            You can create subscriptions where each one of them has specific QoS parameters.
            A notification is sent to a callback url you will provide, informing you in case the QoS targets can no
            longer be full-filled.

            :param str host: The url of the 5G-API
            :param str bearer_access_token: The bearer access token that will be used to authenticate with the 5G-API
        """
        configuration = swagger_client.Configuration()
        configuration.host = host
        configuration.access_token = bearer_access_token
        api_client = swagger_client.ApiClient(configuration=configuration)
        self.qos_api = SessionWithQoSAPIApi(api_client)

    def create_subscription_request(self,
                                      equipment_network_identifier: str,
                                      network_identifier: NetworkIdentifier,
                                      notification_destination: str,
                                      qos_reference: int,
                                      alt_qo_s_references,
                                      usage_threshold: UsageThreshold,
                                      qos_mon_info
                                      ) -> AsSessionWithQoSSubscriptionCreate:
        ip4_address_value = equipment_network_identifier if network_identifier == QosAwareness.NetworkIdentifier.IP_V4_ADDRESS else None
        ip6_address_value = equipment_network_identifier if network_identifier == QosAwareness.NetworkIdentifier.IP_V6_ADDRESS else None
        mac_address_value = equipment_network_identifier if network_identifier == QosAwareness.NetworkIdentifier.MAC_ADDRESS else None

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
                                                    equipment_network_identifier: str,
                                                    network_identifier: NetworkIdentifier,
                                                    notification_destination: str,
                                                    non_gbr_qos_reference: NonGBRQosReference,
                                                    usage_threshold: UsageThreshold
                                                    ) -> AsSessionWithQoSSubscription:
        """
        Initializes a Non Guaranteed Bit Rate (NGBR) Quality of Service (QoS) subscription.
        This is useful for TCP based or Live Streaming scenarios.

        :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        :param equipment_network_identifier: The IP 4 address or IP 6 address or Mac address of the user device / equiment.
        If you choose to pass a IP 4 address then the network_identified parameter should be set to NetworkIdentifier.IP_V4_ADDRESS
        If you choose to pass a IP 6 address then the network_identified parameter should be set to NetworkIdentifier.IP_V6_ADDRESS
        If you choose to pass a MAC address then the network_identified parameter should be set to NetworkIdentifier.MAC_ADDRESS
        :param network_identifier: An enum that specifies what type of equipment_network_identifier you are passing as a parameters (IP4,IP6 or MAC address)
        :param notification_destination: The url that you will notifications when QoS conditions change (for example when usage threshold is exceeded)
        :param non_gbr_qos_reference: The type of Non Guaranteed QoS that you want to achieve (TCP based or Live Streaming)
        :param usage_threshold: Allows to set thresholds on time and volume. For example establish the Qos session, up to 10 gigabytes for the upcoming 48 hours.
        5 GB for downlink, 5gb for uplink
        :return: :return: The subscription that will contain the identifier for this QoS session.
        """
        body = self.create_subscription_request(equipment_network_identifier,
                                                  network_identifier,
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
                                                    equipment_network_identifier: str,
                                                    network_identifier: NetworkIdentifier,
                                                    notification_destination: str,
                                                    non_gbr_qos_reference: NonGBRQosReference,
                                                    usage_threshold: UsageThreshold) -> AsSessionWithQoSSubscription:
        """
        Updates a given subscription.

        :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        :param str subscription_id: string (Identifier of the subscription resource)
        :param equipment_network_identifier: The IP 4 address or IP 6 address or Mac address of the user device / equiment.
        If you choose to pass a IP 4 address then the network_identified parameter should be set to NetworkIdentifier.IP_V4_ADDRESS
        If you choose to pass a IP 6 address then the network_identified parameter should be set to NetworkIdentifier.IP_V6_ADDRESS
        If you choose to pass a MAC address then the network_identified parameter should be set to NetworkIdentifier.MAC_ADDRESS
        :param network_identifier: An enum that specifies what type of equipment_network_identifier you are passing as a parameters (IP4,IP6 or MAC address)
        :param notification_destination: The url that you will notifications when QoS conditions change (for example when usage threshold is exceeded)
        :param non_gbr_qos_reference: The type of Non Guaranteed QoS that you want to achieve (TCP based or Live Streaming)
        :param usage_threshold: Allows to set thresholds on time and volume. For example establish the Qos session, up to 10 gigabytes for the upcoming 48 hours.
        5 GB for downlink, 5gb for uplink
        :return: The subscription that will contain the identifier for this QoS session.
        """
        body = self.create_subscription_request(equipment_network_identifier,
                                                  network_identifier,
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
                                                equipment_network_identifier,
                                                network_identifier,
                                                notification_destination: str,
                                                gbr_qos_reference: GBRQosReference,
                                                usage_threshold: UsageThreshold,
                                                qos_monitoring_parameter: QosMonitoringParameter,
                                                threshold: int,
                                                reporting_mode: GuaranteedBitRateReportingMode
                                                ) -> AsSessionWithQoSSubscription:

        """
            Initializes a Guaranteed Bit Rate (NGBR) Quality of Service (QoS) subscription.
            This is useful for Conversational Voice / Video or Discrete automation scenarios.

            :param str netapp_id: string (The ID of the Netapp that creates a subscription)
            :param equipment_network_identifier: The IP 4 address or IP 6 address or Mac address of the user device / equiment.
                If you choose to pass a IP 4 address then the network_identified parameter should be set to NetworkIdentifier.IP_V4_ADDRESS
                If you choose to pass a IP 6 address then the network_identified parameter should be set to NetworkIdentifier.IP_V6_ADDRESS
                If you choose to pass a MAC address then the network_identified parameter should be set to NetworkIdentifier.MAC_ADDRESS
            :param network_identifier: An enum that specifies what type of equipment_network_identifier you are passing as a parameters (IP4,IP6 or MAC address)
            :param notification_destination: The url that you will receive notifications when QoS conditions change (for example when threshold cannot be achieved)
            :param gbr_qos_reference:  The type of Guaranteed QoS that you want to achieve (CONVERSATIONAL_VOICE or CONVERSATIONAL_VIDEO or DISCRETE_AUTOMATION)
            :param usage_threshold: Allows to set thresholds on time and volume. For example establish the Qos session, up to 10 gigabytes for the upcoming 48 hours.
            5 GB for downlink, 5gb for uplink
            :param qos_monitoring_parameter: The type of connection that will be monitored: UPLINK or DOWNLINK or ROUNDTRIP
            :param threshold: The minimum delay of data package in milliseconds, during UPLINK or DOWNLINK or ROUNDTRIP
            :param reporting_mode: Can be an instance of EventTriggeredReportingConfiguration or PeriodicReportConfiguration. These dictate how you will receive
            notifications (reports) from the network.
            :return: The subscription that will contain the identifier for this QoS session.
        """
        alt_qo_s_references, qos_monitoring_info = self.__create_gbr_request_qo_parameters(gbr_qos_reference,
                                                                                           qos_monitoring_parameter,
                                                                                           threshold,
                                                                                           reporting_mode)

        body = self.create_subscription_request(equipment_network_identifier,
                                                  network_identifier,
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

    def __create_gbr_request_qo_parameters(self, gbr_qos_reference, qos_monitoring_parameter, threshold,
                                           reporting_mode: GuaranteedBitRateReportingMode):
        # Contains the remaining Guaranted Qos references, as fallback
        alt_qo_s_references = []
        for qos_reference in QosAwareness.GBRQosReference:
            if qos_reference != gbr_qos_reference:
                alt_qo_s_references.append(qos_reference.value)
        # User has to specify
        lat_thresh_ul = threshold if qos_monitoring_parameter == QosAwareness.QosMonitoringParameter.UPLINK else None
        lat_thresh_dl = threshold if qos_monitoring_parameter == QosAwareness.QosMonitoringParameter.DOWNLINK else None
        lat_thresh_rp = threshold if qos_monitoring_parameter == QosAwareness.QosMonitoringParameter.ROUNDTRIP else None

        reporting_freqs =[reporting_mode.get_reporting_mode()]
        wait_time = None
        rep_period = None

        if isinstance(reporting_mode, QosAwareness.EventTriggeredReportingConfiguration):
            wait_time = reporting_mode.get_reporting_configuration()
        else:
            rep_period = reporting_mode.get_reporting_configuration()

        qos_monitoring_info = QosMonitoringInformation(
            req_qos_mon_params=[qos_monitoring_parameter.value],
            rep_freqs=reporting_freqs,
            lat_thresh_dl=lat_thresh_dl,
            lat_thresh_ul=lat_thresh_ul,
            lat_thresh_rp=lat_thresh_rp,
            wait_time=wait_time,
            rep_period=rep_period
        )
        return alt_qo_s_references, qos_monitoring_info

    def update_guaranteed_bit_rate_subscription(self,
                                                netapp_id: str,
                                                subscription_id: str,
                                                equipment_network_identifier: str,
                                                network_identifier: NetworkIdentifier,
                                                notification_destination: str,
                                                gbr_qos_reference: GBRQosReference,
                                                usage_threshold: UsageThreshold,
                                                qos_monitoring_parameter: QosMonitoringParameter,
                                                threshold: int,
                                                reporting_mode: GuaranteedBitRateReportingMode
                                                ) -> AsSessionWithQoSSubscription:
        """
            Updates a given subscription.


            :param str netapp_id: string (The ID of the Netapp that creates a subscription)
            :param str subscription_id: string (Identifier of the subscription resource)
            :param equipment_network_identifier: The IP 4 address or IP 6 address or Mac address of the user device / equiment.
                If you choose to pass a IP 4 address then the network_identified parameter should be set to NetworkIdentifier.IP_V4_ADDRESS
                If you choose to pass a IP 6 address then the network_identified parameter should be set to NetworkIdentifier.IP_V6_ADDRESS
                If you choose to pass a MAC address then the network_identified parameter should be set to NetworkIdentifier.MAC_ADDRESS
            :param network_identifier: An enum that specifies what type of equipment_network_identifier you are passing as a parameters (IP4,IP6 or MAC address)
            :param notification_destination: The url that you will receive notifications when QoS conditions change (for example when threshold cannot be achieved)
            :param gbr_qos_reference:  The type of Guaranteed QoS that you want to achieve (CONVERSATIONAL_VOICE or CONVERSATIONAL_VIDEO or DISCRETE_AUTOMATION)
            :param usage_threshold: Allows to set thresholds on time and volume. For example establish the Qos session, up to 10 gigabytes for the upcoming 48 hours.
            5 GB for downlink, 5gb for uplink
            :param qos_monitoring_parameter: The type of connection that will be monitored: UPLINK or DOWNLINK or ROUNDTRIP
            :param threshold: The minimum delay of data package in milliseconds, during UPLINK or DOWNLINK or ROUNDTRIP
            :param reporting_mode: Can be an instance of EventTriggeredReportingConfiguration or PeriodicReportConfiguration. These dictate how you will receive
            notifications (reports) from the network.
            :return: The subscription that will contain the identifier for this QoS session.
        """
        alt_qo_s_references, qos_monitoring_info = self.__create_gbr_request_qo_parameters(gbr_qos_reference,
                                                                                           qos_monitoring_parameter,
                                                                                           threshold,
                                                                                           reporting_mode)

        body = self.create_subscription_request(equipment_network_identifier,
                                                  network_identifier,
                                                  notification_destination,
                                                  qos_reference=gbr_qos_reference.value,
                                                  alt_qo_s_references=alt_qo_s_references,
                                                  usage_threshold=usage_threshold,
                                                  qos_mon_info=qos_monitoring_info
                                                  )
        return self.qos_api.update_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_subscription_id_put(
            body, netapp_id, subscription_id)

    def get_all_subscriptions(self, netapp_id: str) -> List[
        AsSessionWithQoSSubscription]:
        """
              Reads all active subscriptions

              :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        """

        return self.qos_api.read_active_subscriptions_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_get(
            netapp_id)

    def get_subscription(self, netapp_id: str, subscription_id: str) -> AsSessionWithQoSSubscription:
        """

        :param netapp_id:
        :param subscription_id:
        :return:
        """
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

