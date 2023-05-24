"""SDK module"""
import os
from typing import List

from evolved5g import swagger_client
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from evolved5g.swagger_client import (
    MonitoringEventAPIApi,
    MonitoringEventSubscriptionCreate,
    MonitoringEventSubscription,
    SessionWithQoSAPIApi,
    AsSessionWithQoSSubscriptionCreate,
    Snssai,
    UsageThreshold,
    AsSessionWithQoSSubscription,
    QosMonitoringInformation,
    RequestedQoSMonitoringParameters,
    ReportingFrequency,
    MonitoringEventReport,
    CellsApi,
    Cell,
)
import datetime

from OpenSSL.SSL import FILETYPE_PEM
from OpenSSL.crypto import (
    dump_certificate_request,
    dump_privatekey,
    load_publickey,
    PKey,
    TYPE_RSA,
    X509Req,
    dump_publickey,
)
import requests
import json
from uuid import uuid4
import warnings


class MonitoringSubscriber(ABC):
    def __init__(
            self,
            host: str,
            nef_bearer_access_token: str,
            folder_path_for_certificates_and_capif_api_key: str,
            capif_host: str,
            capif_https_port: int,
    ):
        configuration = swagger_client.Configuration()
        configuration.verify_ssl = False
        configuration.host = host
        service_discoverer = ServiceDiscoverer(folder_path_for_certificates_and_capif_api_key, capif_host,
                                               capif_https_port)
        api_name = "/nef/api/v1/3gpp-monitoring-event/"
        configuration.available_endpoints = {
            "MONITORING_SUBSCRIPTIONS": service_discoverer.retrieve_specific_resource_name(api_name,
                                                                                           "MONITORING_SUBSCRIPTIONS"),
            "MONITORING_SUBSCRIPTION_SINGLE": service_discoverer.retrieve_specific_resource_name(api_name,
                                                                                                 "MONITORING_SUBSCRIPTION_SINGLE"),
        }
        api_resource_description = service_discoverer.retrieve_api_description_by_name(api_name)
        configuration.access_token = nef_bearer_access_token + "," + service_discoverer.get_access_token(api_name,
                                                                                                         api_resource_description[
                                                                                                             "apiId"],
                                                                                                         api_resource_description[
                                                                                                             "aefProfiles"][
                                                                                                             0][
                                                                                                             "aefId"])
        api_client = swagger_client.ApiClient(configuration=configuration)
        self.monitoring_event_api = MonitoringEventAPIApi(api_client)
        self.cell_api = CellsApi(api_client)

    def create_subscription_request(
            self,
            monitoring_type,
            external_id,
            notification_destination,
            maximum_number_of_reports,
            monitor_expire_time,
            maximum_detection_time,
            reachability_type,
    ) -> MonitoringEventSubscriptionCreate:
        return MonitoringEventSubscriptionCreate(
            external_id,
            notification_destination,
            monitoring_type,
            maximum_number_of_reports,
            monitor_expire_time,
            maximum_detection_time,
            reachability_type,
        )

    def get_all_subscriptions(self, netapp_id: str, skip: int = 0, limit: int = 100):
        """
        Reads all active subscriptions

        :param skip: The number of subscriptions to skip
        :param limit: The maximum number of transcriptions to return
        :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        """

        return self.monitoring_event_api.read_active_subscriptions_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_get(
            netapp_id, skip=skip, limit=limit
        )

    def get_subscription(
            self, netapp_id: str, subscription_id: str
    ) -> MonitoringEventSubscription:
        """
        Gets subscription by id

        :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        :param str subscription_id: string (Identifier of the subscription resource)
        """
        return self.monitoring_event_api.read_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get(
            netapp_id, subscription_id
        )

    def delete_subscription(self, netapp_id: str, subscription_id: str):
        """
        Delete a subscription

        :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        :param str subscription_id: string (Identifier of the subscription resource)
        """
        return self.monitoring_event_api.delete_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete(
            netapp_id, subscription_id
        )


class LocationSubscriber(MonitoringSubscriber):
    def __init__(
            self,
            nef_url: str,
            nef_bearer_access_token: str,
            folder_path_for_certificates_and_capif_api_key: str,
            capif_host: str,
            capif_https_port: int,
    ):
        """
        Initializes class LocationSubscriber.
        This SKD class allows you to track devices and retrieve updates about their location.
        You can create subscriptions where each one of them can be used to track a device.
        A notification is sent to a callback url you will provide, everytime the user device changes Cell

         :param str nef_url: The url of the 5G-API
        """
        super().__init__(
            nef_url,
            nef_bearer_access_token,
            folder_path_for_certificates_and_capif_api_key,
            capif_host,
            capif_https_port,
        )

    def __get_monitoring_type(self):
        return "LOCATION_REPORTING"

    def get_location_information(
            self, netapp_id: str, external_id
    ) -> MonitoringEventReport:
        """
        Returns the location of a specific device.
        This is equivalent to creating a subscription with maximum_number_of_reports = 1
        :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        :param str external_id: Globally unique identifier containing a Domain Identifier and a Local Identifier. <Local Identifier>@<Domain Identifier>
        """

        # create a dummy expiration time. Since we are requesting for only 1 report, we will get the location information back instantly
        monitor_expire_time = (
                                      datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
                              ).isoformat() + "Z"
        body = self.create_subscription_request(
            self.__get_monitoring_type(),
            external_id,
            None,
            maximum_number_of_reports=1,
            monitor_expire_time=monitor_expire_time,
            maximum_detection_time=None,
            reachability_type=None,
        )

        # a monitoring event report
        response = self.monitoring_event_api.create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post(
            body, netapp_id
        )
        return response

    def get_coordinates_of_cell(self, cell_id: str) -> Cell:
        """
        Returns information about a specific cell

        :param str cell_id: string (The ID of the cell)
        """
        return self.cell_api.read_cell_api_v1_cells_cell_id_get(cell_id)

    def create_subscription(
            self,
            netapp_id: str,
            external_id,
            notification_destination,
            maximum_number_of_reports,
            monitor_expire_time,
    ) -> MonitoringEventSubscription:
        """
        Creates a subscription that will be used to retrieve Location information about a device.

        :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        :param str external_id: Globally unique identifier containing a Domain Identifier and a Local Identifier. <Local Identifier>@<Domain Identifier>
        :param notification_destination: The url that you will notifications about the location of the user
        :param maximum_number_of_reports: Identifies the maximum number of event reports to be generated. Value 1 makes the Monitoring Request a One-time Request
        :param monitor_expire_time: Identifies the absolute time at which the related monitoring event request is considered to expire
        """
        body = self.create_subscription_request(
            self.__get_monitoring_type(),
            external_id,
            notification_destination,
            maximum_number_of_reports,
            monitor_expire_time,
            None,
            None,
        )

        # a monitoring event report
        response = self.monitoring_event_api.create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post(
            body, netapp_id
        )
        return response

    def update_subscription(
            self,
            netapp_id: str,
            subscription_id: str,
            external_id,
            notification_destination,
            maximum_number_of_reports,
            monitor_expire_time,
    ) -> MonitoringEventSubscription:
        """
        Creates a subscription that will be used to retrieve Location information about a device.

        :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        :param str subscription_id: string (Identifier of the subscription resource)
        :param str external_id: Globally unique identifier containing a Domain Identifier and a Local Identifier. <Local Identifier>@<Domain Identifier>
        :param notification_destination: The url that you will notifications about the location of the user
        :param maximum_number_of_reports: Identifies the maximum number of event reports to be generated. Value 1 makes the Monitoring Request a One-time Request
        :param monitor_expire_time: Identifies the absolute time at which the related monitoring event request is considered to expire
        """
        body = self.create_subscription_request(
            self.__get_monitoring_type(),
            external_id,
            notification_destination,
            maximum_number_of_reports,
            monitor_expire_time,
            None,
            None,
        )

        return self.monitoring_event_api.update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put(
            body, netapp_id, subscription_id
        )


class ConnectionMonitor(MonitoringSubscriber):
    class MonitoringType(Enum):
        """
        This enum is used to describe what the kind of monitoring you will apply to your devices.
        If INFORM_WHEN_CONNECTED is selected then the 5G API will send you a notification is the device has not been connected to the 5G Network for the past X seconds
        If INFORM_WHEN_NOT_CONNECTED is selected then the 5G API will send you a notification is the device has not been connected to the 5G Network for the past X seconds
        """

        INFORM_WHEN_CONNECTED = 1
        INFORM_WHEN_NOT_CONNECTED = 2

    def __init__(
            self,
            nef_url: str,
            nef_bearer_access_token: str,
            folder_path_for_certificates_and_capif_api_key: str,
            capif_host: str,
            capif_https_port: int,
    ):
        """
        Initializes class ConnectionMonitor.
        Consider a scenario where a NetApp wants to monitor 100 devices in the 5G Network.
        The netapp wants to track, at any given time how many NetApps are connected to the 5G Network and how many netApps are disconnected.

        Using ConnectionMonitor the NetApp can retrieve notifications by the 5G Network for individual devices when
        Connection is lost (for example the user device has not been connected to the 5G network for the past 10 seconds)
        Connection is alive (for example the user device has been connected to the 5G network for the past 10 seconds)

        :param str nef_url: The url of the 5G-API
        :param folder_path_for_certificates_and_capif_api_key: The folder that contains the NetApp certificates and
         CAPIF API Key. These are created  while registering and onboarding the NetApp to the CAPIF Server
        :param capif_host: The host of the CAPIF Server (ex. "capifcore")
        :param capif_https_port: The https_port of the  CAPIF Server
        """
        super().__init__(
            nef_url,
            nef_bearer_access_token,
            folder_path_for_certificates_and_capif_api_key,
            capif_host,
            capif_https_port,
        )

    def __get_monitoring_type(self, monitoring_type: MonitoringType):
        if monitoring_type == self.MonitoringType.INFORM_WHEN_CONNECTED:
            return "UE_REACHABILITY"
        else:
            return "LOSS_OF_CONNECTIVITY"

    def create_subscription(
            self,
            netapp_id: str,
            external_id,
            notification_destination,
            monitoring_type: MonitoringType,
            wait_time_before_sending_notification_in_seconds: int,
            maximum_number_of_reports,
            monitor_expire_time,
    ) -> MonitoringEventSubscription:
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
        body = self.create_subscription_request(
            self.__get_monitoring_type(monitoring_type),
            external_id,
            notification_destination,
            maximum_number_of_reports,
            monitor_expire_time,
            wait_time_before_sending_notification_in_seconds,
            "DATA",
        )

        # a monitoring event report
        response = self.monitoring_event_api.create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post(
            body, netapp_id
        )
        return response

    def update_subscription(
            self,
            netapp_id: str,
            subscription_id: str,
            external_id,
            notification_destination,
            monitoring_type: MonitoringType,
            wait_time_before_sending_notification_in_seconds: int,
            maximum_number_of_reports,
            monitor_expire_time,
    ) -> MonitoringEventSubscription:
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
        body = self.create_subscription_request(
            monitoring_type,
            external_id,
            notification_destination,
            maximum_number_of_reports,
            monitor_expire_time,
            wait_time_before_sending_notification_in_seconds,
            "DATA",
        )

        return self.monitoring_event_api.update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put(
            body, netapp_id, subscription_id
        )


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

    def __init__(
            self,
            nef_url: str,
            nef_bearer_access_token: str,
            folder_path_for_certificates_and_capif_api_key: str,
            capif_host: str,
            capif_https_port: int,
    ):
        """
        Initializes class QosAwareness.
        This SKD class allows you to request QoS from a set of standardized values for better service experience.

        You can create subscriptions where each one of them has specific QoS parameters.
        A notification is sent to a callback url you will provide, informing you in case the QoS targets can no
        longer be full-filled.

        :param nef_url:  The url of the 5G-API (ex. NEF emulator)
        :param nef_bearer_access_token: The bearer access token that will be used to authenticate with the 5G-API
        :param folder_path_for_certificates_and_capif_api_key: The folder that contains the NetApp certificates and
         CAPIF API Key. These are created  while registering and onboarding the NetApp to the CAPIF Server
        :param capif_host: The host of the CAPIF Server (ex. "capifcore")
        :param capif_https_port: The https_port of the  CAPIF Server
        """

        configuration = swagger_client.Configuration()
        configuration.host = nef_url
        configuration.verify_ssl = False

        service_discoverer = ServiceDiscoverer(
            folder_path_for_certificates_and_capif_api_key, capif_host, capif_https_port
        )
        api_name = "/nef/api/v1/3gpp-as-session-with-qos/"
        configuration.available_endpoints = {
            "QOS_SUBSCRIPTIONS": service_discoverer.retrieve_specific_resource_name(
                api_name, "QOS_SUBSCRIPTIONS"
            ),
            "QOS_SUBSCRIPTION_SINGLE": service_discoverer.retrieve_specific_resource_name(
                api_name, "QOS_SUBSCRIPTION_SINGLE"
            ),
        }
        api_resource_description = service_discoverer.retrieve_api_description_by_name(api_name)
        configuration.access_token = nef_bearer_access_token + "," + service_discoverer.get_access_token(api_name,
                                                                                                         api_resource_description[
                                                                                                             "apiId"],
                                                                                                         api_resource_description[
                                                                                                             "aefProfiles"][
                                                                                                             0][
                                                                                                             "aefId"])
        api_client = swagger_client.ApiClient(configuration=configuration)
        self.qos_api = SessionWithQoSAPIApi(api_client)

    def create_subscription_request(
            self,
            equipment_network_identifier: str,
            network_identifier: NetworkIdentifier,
            notification_destination: str,
            qos_reference: int,
            alt_qo_s_references,
            usage_threshold: UsageThreshold,
            qos_mon_info,
    ) -> AsSessionWithQoSSubscriptionCreate:
        ip4_address_value = (
            equipment_network_identifier
            if network_identifier == QosAwareness.NetworkIdentifier.IP_V4_ADDRESS
            else None
        )
        ip6_address_value = (
            equipment_network_identifier
            if network_identifier == QosAwareness.NetworkIdentifier.IP_V6_ADDRESS
            else None
        )
        mac_address_value = (
            equipment_network_identifier
            if network_identifier == QosAwareness.NetworkIdentifier.MAC_ADDRESS
            else None
        )

        # This field indicates in which network slice the UE (vertical app) wants to establish or modify a QoS Flow.
        # There are no network slices, this field exists only for future compatibility
        # Since there is no functionality implemented you should always leave the default value sst : 1 and sd : “000001”
        snssai = Snssai()

        # Same as APN in 4G, identifies the external data network (i.e., internet). Same applies here as snssai. There is no functionality implemented
        dnn = "province1.mnc01.mcc202.gprs"
        return AsSessionWithQoSSubscriptionCreate(
            ipv4_addr=ip4_address_value,
            ipv6_addr=ip6_address_value,
            mac_addr=mac_address_value,
            notification_destination=notification_destination,
            snssai=snssai,
            dnn=dnn,
            qos_reference=qos_reference,
            alt_qo_s_references=alt_qo_s_references,
            usage_threshold=usage_threshold,
            qos_mon_info=qos_mon_info,
        )

    def create_non_guaranteed_bit_rate_subscription(
            self,
            netapp_id,
            equipment_network_identifier: str,
            network_identifier: NetworkIdentifier,
            notification_destination: str,
            non_gbr_qos_reference: NonGBRQosReference,
            usage_threshold: UsageThreshold,
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
        body = self.create_subscription_request(
            equipment_network_identifier,
            network_identifier,
            notification_destination,
            non_gbr_qos_reference.value,
            alt_qo_s_references=None,
            usage_threshold=usage_threshold,
            qos_mon_info=None,
        )

        response = self.qos_api.create_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_post(
            body, netapp_id
        )
        return response

    def update_non_guaranteed_bit_rate_subscription(
            self,
            netapp_id: str,
            subscription_id: str,
            equipment_network_identifier: str,
            network_identifier: NetworkIdentifier,
            notification_destination: str,
            non_gbr_qos_reference: NonGBRQosReference,
            usage_threshold: UsageThreshold,
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
        :param notification_destination: The url that you will notifications when QoS conditions change (for example when usage threshold is exceeded)
        :param non_gbr_qos_reference: The type of Non Guaranteed QoS that you want to achieve (TCP based or Live Streaming)
        :param usage_threshold: Allows to set thresholds on time and volume. For example establish the Qos session, up to 10 gigabytes for the upcoming 48 hours.
        5 GB for downlink, 5gb for uplink
        :return: The subscription that will contain the identifier for this QoS session.
        """
        body = self.create_subscription_request(
            equipment_network_identifier,
            network_identifier,
            notification_destination,
            non_gbr_qos_reference.value,
            alt_qo_s_references=None,
            usage_threshold=usage_threshold,
            qos_mon_info=None,
        )

        return self.qos_api.update_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_subscription_id_put(
            body, netapp_id, subscription_id
        )

    def create_guaranteed_bit_rate_subscription(
            self,
            netapp_id,
            equipment_network_identifier,
            network_identifier,
            notification_destination: str,
            gbr_qos_reference: GBRQosReference,
            usage_threshold: UsageThreshold,
            qos_monitoring_parameter: QosMonitoringParameter,
            threshold: int,
            reporting_mode: GuaranteedBitRateReportingMode,
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
        (
            alt_qo_s_references,
            qos_monitoring_info,
        ) = self.__create_gbr_request_qo_parameters(
            gbr_qos_reference, qos_monitoring_parameter, threshold, reporting_mode
        )

        body = self.create_subscription_request(
            equipment_network_identifier,
            network_identifier,
            notification_destination,
            qos_reference=gbr_qos_reference.value,
            alt_qo_s_references=alt_qo_s_references,
            usage_threshold=usage_threshold,
            qos_mon_info=qos_monitoring_info,
        )

        response = self.qos_api.create_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_post(
            body, netapp_id
        )
        return response

    def __create_gbr_request_qo_parameters(
            self,
            gbr_qos_reference,
            qos_monitoring_parameter,
            threshold,
            reporting_mode: GuaranteedBitRateReportingMode,
    ):
        # Contains the remaining Guaranted Qos references, as fallback
        alt_qo_s_references = []
        for qos_reference in QosAwareness.GBRQosReference:
            if qos_reference != gbr_qos_reference:
                alt_qo_s_references.append(qos_reference.value)
        # User has to specify
        lat_thresh_ul = (
            threshold
            if qos_monitoring_parameter == QosAwareness.QosMonitoringParameter.UPLINK
            else None
        )
        lat_thresh_dl = (
            threshold
            if qos_monitoring_parameter == QosAwareness.QosMonitoringParameter.DOWNLINK
            else None
        )
        lat_thresh_rp = (
            threshold
            if qos_monitoring_parameter == QosAwareness.QosMonitoringParameter.ROUNDTRIP
            else None
        )

        reporting_freqs = [reporting_mode.get_reporting_mode()]
        wait_time = None
        rep_period = None

        if isinstance(
                reporting_mode, QosAwareness.EventTriggeredReportingConfiguration
        ):
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
            rep_period=rep_period,
        )
        return alt_qo_s_references, qos_monitoring_info

    def update_guaranteed_bit_rate_subscription(
            self,
            netapp_id: str,
            subscription_id: str,
            equipment_network_identifier: str,
            network_identifier: NetworkIdentifier,
            notification_destination: str,
            gbr_qos_reference: GBRQosReference,
            usage_threshold: UsageThreshold,
            qos_monitoring_parameter: QosMonitoringParameter,
            threshold: int,
            reporting_mode: GuaranteedBitRateReportingMode,
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
        (
            alt_qo_s_references,
            qos_monitoring_info,
        ) = self.__create_gbr_request_qo_parameters(
            gbr_qos_reference, qos_monitoring_parameter, threshold, reporting_mode
        )

        body = self.create_subscription_request(
            equipment_network_identifier,
            network_identifier,
            notification_destination,
            qos_reference=gbr_qos_reference.value,
            alt_qo_s_references=alt_qo_s_references,
            usage_threshold=usage_threshold,
            qos_mon_info=qos_monitoring_info,
        )
        return self.qos_api.update_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_subscription_id_put(
            body, netapp_id, subscription_id
        )

    def get_all_subscriptions(
            self, netapp_id: str
    ) -> List[AsSessionWithQoSSubscription]:
        """
        Reads all active subscriptions

        :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        """

        return self.qos_api.read_active_subscriptions_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_get(
            netapp_id
        )

    def get_subscription(
            self, netapp_id: str, subscription_id: str
    ) -> AsSessionWithQoSSubscription:
        """

        :param netapp_id:
        :param subscription_id:
        :return:
        """
        return self.qos_api.read_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_subscription_id_get(
            netapp_id, subscription_id
        )

    def delete_subscription(self, netapp_id: str, subscription_id: str):
        """
        Delete a subscription

        :param str netapp_id: string (The ID of the Netapp that creates a subscription)
        :param str subscription_id: string (Identifier of the subscription resource)
        """
        return self.qos_api.delete_subscription_api_v13gpp_as_session_with_qos_v1_scs_as_id_subscriptions_subscription_id_delete(
            netapp_id, subscription_id
        )


class CAPIFInvokerConnector:
    """
    Τhis class is responsbile for onboarding an Invoker (ex. a NetApp) to CAPIF
    """

    def __init__(
            self,
            folder_to_store_certificates: str,
            capif_host: str,
            capif_http_port: str,
            capif_https_port: str,
            capif_netapp_username,
            capif_netapp_password: str,
            capif_callback_url: str,
            description: str,
            csr_common_name: str,
            csr_organizational_unit: str,
            csr_organization: str,
            crs_locality: str,
            csr_state_or_province_name,
            csr_country_name,
            csr_email_address,
    ):
        """

        :param folder_to_store_certificates: The folder where certificates will be stores. Your own certificate,
         along with the certificate root that will be retrieved by the CAPIF server
        :param capif_host: The host of the CAPIF Server. It can be an ip or a domain name (Ex. localhost)
        :param capif_http_port: The port of http port (if None is specified port 80 will be used)
        :param capif_https_port: The port of https port (if None is specified port 443 will be used)
        :param capif_netapp_username: The CAPIF username of your netapp
        :param capif_netapp_password: The CAPIF password  of your netapp
        :param capif_callback_url: A url provided by you that will be used to receive HTTP POST notifications from CAPIF.
        :param description: A short description of your netapp
        :param csr_common_name: The CommonName that will be used in the generated X.509 certificate
        :param csr_organizational_unit:The OrganizationalUnit that will be used in the generated X.509 certificate
        :param csr_organization: The Organization that will be used in the generated X.509 certificate
        :param crs_locality: The Locality that will be used in the generated X.509 certificate
        :param csr_state_or_province_name: The StateOrProvinceName that will be used in the generated X.509 certificate
        :param csr_country_name: The CountryName that will be used in the generated X.509 certificate
        :param csr_email_address: The email that will be used in the generated X.509 certificate
        """
        # add the trailing slash if it is not already there using os.path.join
        self.folder_to_store_certificates = os.path.join(
            folder_to_store_certificates.strip(), ""
        )
        # make sure the parameters are str
        capif_http_port = str(capif_http_port)
        capif_https_port = str(capif_https_port)
        if len(capif_http_port) == 0 or int(capif_http_port) == 80:
            self.capif_http_url = "http://" + capif_host.strip() + "/"
        else:
            self.capif_http_url = (
                    "http://" + capif_host.strip() + ":" + capif_http_port.strip() + "/"
            )

        if len(capif_https_port) == 0 or int(capif_https_port) == 443:
            self.capif_https_url = "https://" + capif_host.strip() + "/"
        else:
            self.capif_https_url = "https://" + capif_host.strip() + ":" + capif_https_port.strip() + "/"

        self.capif_callback_url = self.__add_trailing_slash_to_url_if_missing(
            capif_callback_url.strip()
        )
        self.capif_netapp_username = capif_netapp_username
        self.capif_netapp_password = capif_netapp_password
        self.description = description
        # adding invoker_ prefix is required by CAPIF v3
        self.csr_common_name = "invoker_" + csr_common_name
        self.csr_organizational_unit = csr_organizational_unit
        self.csr_organization = csr_organization
        self.crs_locality = crs_locality
        self.csr_state_or_province_name = csr_state_or_province_name
        self.csr_country_name = csr_country_name
        self.csr_email_address = csr_email_address

    def __add_trailing_slash_to_url_if_missing(self, url):
        if url[len(url) - 1] != "/":
            url = url + "/"
        return url

    def register_and_onboard_netapp(self) -> None:
        """
        Using this method a NetApp can get onboarded to CAPIF.
        After calling this method the following should happen:
         a) A signed certificate should exist in folder folder_to_store_certificates
         b) A json file 'capif_api_details.json' should exist with the api_invoker_id and the api discovery url

        These will be used  ServiceDiscoverer class in order to communicate with CAPIF and discover services

        """
        public_key = self.__create_private_and_public_keys()
        role = "invoker"
        registration_result = self.__register_to_capif(role)
        capif_onboarding_url = registration_result["ccf_onboarding_url"]
        capif_discover_url = registration_result["ccf_discover_url"]
        capif_access_token = self.__save_capif_ca_root_file_and_get_auth_token(role)
        api_invoker_id = (
            self.__onboard_netapp_to_capif_and_create_the_signed_certificate(
                public_key, capif_onboarding_url, capif_access_token
            )
        )
        self.__write_to_file(self.csr_common_name, api_invoker_id, capif_discover_url)

    def __create_private_and_public_keys(self) -> str:
        """
        Creates 2 keys in folder folder_to_store_certificates. A private.key and a cert_req.csr.
        :return: The contents of the public key
        """

        private_key_path = self.folder_to_store_certificates + "private.key"
        csr_file_path = self.folder_to_store_certificates + "cert_req.csr"

        # create public/private key
        key = PKey()
        key.generate_key(TYPE_RSA, 2048)

        # Generate CSR
        req = X509Req()
        req.get_subject().CN = self.csr_common_name
        req.get_subject().O = self.csr_organization
        req.get_subject().OU = self.csr_organizational_unit
        req.get_subject().L = self.crs_locality
        req.get_subject().ST = self.csr_state_or_province_name
        req.get_subject().C = self.csr_country_name
        req.get_subject().emailAddress = self.csr_email_address
        req.set_pubkey(key)
        req.sign(key, "sha256")

        with open(csr_file_path, "wb+") as f:
            f.write(dump_certificate_request(FILETYPE_PEM, req))
            public_key = dump_certificate_request(FILETYPE_PEM, req)
        with open(private_key_path, "wb+") as f:
            f.write(dump_privatekey(FILETYPE_PEM, key))

        return public_key

    def __register_to_capif(self, role):

        url = self.capif_http_url + "register"
        payload = dict()
        payload["username"] = self.capif_netapp_username
        payload["password"] = self.capif_netapp_password
        payload["role"] = role
        payload["description"] = self.description
        payload["cn"] = self.csr_common_name

        response = requests.request(
            "POST",
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
        )
        response.raise_for_status()

        response_payload = json.loads(response.text)
        return response_payload

    def __save_capif_ca_root_file_and_get_auth_token(self, role):

        url = self.capif_http_url + "getauth"

        payload = dict()
        payload["username"] = self.capif_netapp_username
        payload["password"] = self.capif_netapp_password
        payload["role"] = role

        response = requests.request(
            "POST",
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
        )
        response.raise_for_status()
        response_payload = json.loads(response.text)
        ca_root_file = open(self.folder_to_store_certificates + "ca.crt", "wb+")
        ca_root_file.write(bytes(response_payload["ca_root"], "utf-8"))
        return response_payload["access_token"]

    def __onboard_netapp_to_capif_and_create_the_signed_certificate(
            self, public_key, capif_onboarding_url, capif_access_token
    ):
        url = self.capif_https_url + capif_onboarding_url
        payload_dict = {
            "notificationDestination": self.capif_callback_url,
            "supportedFeatures": "fffffff",
            # TODO: This works fine.  But what about CapifProviderConnector class where we onboard a Provider/Exposer. On onboarding there we dont pass the username. Is this a mistake in the flow? Or a different flow is implemented there
            "apiInvokerInformation": self.csr_common_name,
            "websockNotifConfig": {
                "requestWebsocketUri": True,
                "websocketUri": "websocketUri",
            },
            "onboardingInformation": {"apiInvokerPublicKey": str(public_key, "utf-8")},
            "requestTestNotification": True,
        }
        payload = json.dumps(payload_dict)
        headers = {
            "Authorization": "Bearer {}".format(capif_access_token),
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
            verify=self.folder_to_store_certificates + "ca.crt",
        )
        response.raise_for_status()
        response_payload = json.loads(response.text)
        certification_file = open(
            self.folder_to_store_certificates + self.csr_common_name + ".crt", "wb"
        )
        certification_file.write(
            bytes(
                response_payload["onboardingInformation"]["apiInvokerCertificate"],
                "utf-8",
            )
        )
        certification_file.close()
        return response_payload["apiInvokerId"]

    def __write_to_file(self, csr_common_name, api_invoker_id, discover_services_url):
        with open(
                self.folder_to_store_certificates + "capif_api_details.json", "w"
        ) as outfile:
            json.dump(
                {
                    "csr_common_name": csr_common_name,
                    "api_invoker_id": api_invoker_id,
                    "discover_services_url": discover_services_url,
                },
                outfile,
            )


class CAPIFProviderConnector:
    """
    Τhis class is responsible for onboarding an exposer (eg. NEF emulator) to CAPIF
    """

    def __init__(
            self,
            certificates_folder: str,
            description: str,
            capif_host: str,
            capif_http_port: str,
            capif_https_port: str,
            capif_netapp_username,
            capif_netapp_password: str,
            csr_common_name: str,
            csr_organizational_unit: str,
            csr_organization: str,
            crs_locality: str,
            csr_state_or_province_name,
            csr_country_name,
            csr_email_address,
    ):
        """
        :param certificates_folder: The folder where certificates will be created and stored.
        :param description: A short description of the Provider
        :param capif_host:
        :param capif_http_port:
        :param capif_https_port:
        :param capif_netapp_username: The CAPIF username of your netapp
        :param capif_netapp_password: The CAPIF password  of your netapp
        :param csr_common_name: The CommonName that will be used in the generated X.509 certificate
        :param csr_organizational_unit:The OrganizationalUnit that will be used in the generated X.509 certificate
        :param csr_organization: The Organization that will be used in the generated X.509 certificate
        :param crs_locality: The Locality that will be used in the generated X.509 certificate
        :param csr_state_or_province_name: The StateOrProvinceName that will be used in the generated X.509 certificate
        :param csr_country_name: The CountryName that will be used in the generated X.509 certificate
        :param csr_email_address: The email that will be used in the generated X.509 certificate

        """
        # add the trailing slash if it is not already there using os.path.join
        self.certificates_folder = os.path.join(certificates_folder.strip(), "")
        self.description = description
        self.csr_common_name = capif_netapp_username
        # make sure the parameters are str
        capif_http_port = str(capif_http_port)
        self.capif_https_port = str(capif_https_port)
        if len(capif_http_port) == 0 or int(capif_http_port) == 80:
            self.capif_http_url = "http://" + capif_host.strip() + "/"
        else:
            self.capif_http_url = (
                    "http://" + capif_host.strip() + ":" + capif_http_port.strip() + "/"
            )

        if len(self.capif_https_port ) == 0 or int(self.capif_https_port ) == 443:
            self.capif_https_url = "https://" + capif_host.strip() + "/"
        else:
            self.capif_https_url = (
                    "https://" + capif_host.strip() + ":" + self.capif_https_port .strip() + "/"
            )

        self.capif_host = capif_host.strip()
        self.capif_netapp_username = capif_netapp_username
        self.capif_netapp_password = capif_netapp_password

        self.csr_common_name = csr_common_name
        self.csr_organizational_unit = csr_organizational_unit
        self.csr_organization = csr_organization
        self.crs_locality = crs_locality
        self.csr_state_or_province_name = csr_state_or_province_name
        self.csr_country_name = csr_country_name
        self.csr_email_address = csr_email_address

    def __store_certificate_authority_file(self):
        url = self.capif_http_url + "ca-root"
        response = requests.request(
            "GET", url, headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        response_payload = json.loads(response.text)
        with open(self.certificates_folder + "ca.crt", "wb+") as ca_root:
            ca_root.write(bytes(response_payload["certificate"], "utf-8"))

    def __store_certificate(self) -> None:
        """
        Retrieves and stores the cert_server.pem from CAPIF
        """
        print("Retrieve capif_cert_server.pem , process may take a few minutes")
        cmd = "openssl s_client -connect {0}:{1}  | openssl x509 -text > {2}/capif_cert_server.pem".format(
            self.capif_host,
            self.capif_https_port,
            self.certificates_folder
        )
        os.system(cmd)
        print("cert_server.pem succesfully generated!")

    def __create_private_and_public_keys(self, api_prov_func_role) -> bytes:
        """
        Creates 2 keys in folder folder_to_store_certificates. An api_prov_func_role_private.key and a api_prov_func_role_private.public.csr key"
        :return: The contents of the public key
        """
        private_key_path = (
                self.certificates_folder + api_prov_func_role + "_private_key.key"
        )
        csr_file_path = self.certificates_folder + api_prov_func_role + "_public.csr"

        # create public/private key
        key = PKey()
        key.generate_key(TYPE_RSA, 2048)

        # Generate CSR
        req = X509Req()

        # The role should always be put in the certificate .lower() by convention
        req.get_subject().CN = api_prov_func_role.lower()
        req.get_subject().O = self.csr_organization
        req.get_subject().OU = self.csr_organizational_unit
        req.get_subject().L = self.crs_locality
        req.get_subject().ST = self.csr_state_or_province_name
        req.get_subject().C = self.csr_country_name
        req.get_subject().emailAddress = self.csr_email_address
        req.set_pubkey(key)
        req.sign(key, "sha256")

        with open(csr_file_path, "wb+") as f:
            f.write(dump_certificate_request(FILETYPE_PEM, req))
            public_key = dump_certificate_request(FILETYPE_PEM, req)
        with open(private_key_path, "wb+") as f:
            f.write(dump_privatekey(FILETYPE_PEM, key))

        return public_key

    def __onboard_exposer_to_capif(self, access_token, capif_onboarding_url):
        url = self.capif_https_url + capif_onboarding_url
        payload = {
            "regSec": access_token,
            "apiProvFuncs": [
                {
                    "regInfo": {"apiProvPubKey": ""},
                    "apiProvFuncRole": "AEF",
                    "apiProvFuncInfo": "dummy_aef",
                },
                {
                    "regInfo": {"apiProvPubKey": ""},
                    "apiProvFuncRole": "APF",
                    "apiProvFuncInfo": "dummy_apf",
                },
                {
                    "regInfo": {"apiProvPubKey": ""},
                    "apiProvFuncRole": "AMF",
                    "apiProvFuncInfo": "dummy_amf",
                },
            ],
            "apiProvDomInfo": "This is provider",
            "suppFeat": "fff",
            "failReason": "string"
        }
        for api_func in payload["apiProvFuncs"]:
            public_key = self.__create_private_and_public_keys(
                api_func["apiProvFuncRole"]
            )
            api_func["regInfo"]["apiProvPubKey"] = public_key.decode("utf-8")

        headers = {
            "Authorization": "Bearer {}".format(access_token),
            "Content-Type": "application/json",
        }

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=json.dumps(payload),
            verify=self.certificates_folder + "ca.crt",
        )

        response.raise_for_status()
        response_payload = json.loads(response.text)
        return response_payload

    def __register_to_capif(self, role):

        url = self.capif_http_url + "register"
        payload = dict()
        payload["username"] = self.capif_netapp_username
        payload["password"] = self.capif_netapp_password
        payload["role"] = role
        payload["description"] = self.description
        payload["cn"] = self.csr_common_name

        response = requests.request(
            "POST",
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
        )
        response.raise_for_status()

        response_payload = json.loads(response.text)
        return response_payload

    def __perform_authorization(self) -> str:
        """
        :return: the access_token from CAPIF
        """

        url = self.capif_http_url + "getauth"

        payload = dict()
        payload["username"] = self.capif_netapp_username
        payload["password"] = self.capif_netapp_password

        response = requests.request(
            "POST",
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
        )
        response.raise_for_status()
        response_payload = json.loads(response.text)

        return response_payload["access_token"]

    def __write_to_file(self, onboarding_response, capif_registration_id, publish_url):

        for func_provile in onboarding_response["apiProvFuncs"]:
            with open(
                    self.certificates_folder
                    + "dummy_"
                    + func_provile["apiProvFuncRole"].lower()
                    + ".crt",
                    "wb",
            ) as certification_file:
                certification_file.write(
                    bytes(func_provile["regInfo"]["apiProvCert"], "utf-8")
                )

        with open(
                self.certificates_folder + "capif_provider_details.json", "w"
        ) as outfile:
            data = {
                "capif_registration_id": capif_registration_id,
                "publish_url": publish_url,
            }
            for api_prov_func in onboarding_response["apiProvFuncs"]:
                key = api_prov_func["apiProvFuncRole"] + "_api_prov_func_id"
                value = api_prov_func["apiProvFuncId"]
                data[key] = value

            json.dump(data, outfile)

    def register_and_onboard_provider(self) -> None:
        role = "provider"
        # retrieve store the .pem certificate from CAPIF
        self.__store_certificate_authority_file()
        self.__store_certificate()
        # register provider to CAPIF
        registration_result = self.__register_to_capif(role)
        capif_registration_id = registration_result["id"]
        ccf_publish_url = registration_result["ccf_publish_url"]
        capif_onboarding_url = registration_result["ccf_api_onboarding_url"]

        access_token = self.__perform_authorization()
        onboarding_response = self.__onboard_exposer_to_capif(
            access_token, capif_onboarding_url
        )
        self.__write_to_file(
            onboarding_response, capif_registration_id, ccf_publish_url
        )

    def publish_services(self, service_api_description_json_full_path) -> dict:
        """
            :param service_api_description_json_full_path: The full path fo the service_api_description.json that contains
            the endpoints that will be published
            :return: The published services dictionary that was saved in CAPIF

        """

        with open(
                self.certificates_folder + "capif_provider_details.json", "r"
        ) as openfile:
            file = json.load(openfile)
            publish_url = file["publish_url"]
            AEF_api_prov_func_id = file["AEF_api_prov_func_id"]
            APF_api_prov_func_id = file["APF_api_prov_func_id"]

        url = self.capif_https_url + publish_url.replace(
            "<apfId>", APF_api_prov_func_id
        )

        with open(service_api_description_json_full_path, "rb") as service_file:
            data = json.load(service_file)
            for profile in data["aefProfiles"]:
                profile["aefId"] = AEF_api_prov_func_id

        response = requests.request(
            "POST",
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
            cert=(
                self.certificates_folder + "dummy_apf.crt",
                self.certificates_folder + "APF_private_key.key",
            ),
            verify=self.certificates_folder + "ca.crt",
        )
        response.raise_for_status()
        capif_response = response.text

        file_name = os.path.basename(service_api_description_json_full_path)
        with open(self.certificates_folder + "CAPIF_" + file_name, "w") as outfile:
            outfile.write(capif_response)

        return json.loads(capif_response)


class ServiceDiscoverer:
    class ServiceDiscovererException(Exception):
        pass

    def __init__(
            self,
            folder_path_for_certificates_and_api_key: str,
            capif_host: str,
            capif_https_port: int,
    ):
        self.capif_host = capif_host
        self.capif_https_port = capif_https_port
        self.folder_to_store_certificates_and_api_key = os.path.join(
            folder_path_for_certificates_and_api_key.strip(), ""
        )
        self.capif_api_details = self.__load_netapp_api_details()
        self.signed_key_crt_path = (
                self.folder_to_store_certificates_and_api_key
                + self.capif_api_details["csr_common_name"] + ".crt"
        )
        self.private_key_path = self.folder_to_store_certificates_and_api_key + "private.key"
        self.ca_root_path = self.folder_to_store_certificates_and_api_key + "ca.crt"

    def get_api_invoker_id(self):
        return self.capif_api_details["api_invoker_id"]

    def __load_netapp_api_details(self):
        with open(
                self.folder_to_store_certificates_and_api_key + "capif_api_details.json",
                "r",
        ) as openfile:
            return json.load(openfile)

    def _add_trailing_slash_to_url_if_missing(self, url):
        if url[len(url) - 1] != "/":
            url = url + "/"
        return url

    def get_access_token(self, api_name, api_id, aef_id):
        """
        :param api_name: The api id name is returned by discover services
         :param api_id: The api id that is returned by discover services
        :param aef_id: The relevant aef_id that is returned by discover services
         :return: The access token (jwt)
        """
        if not self.__aef_id_already_registered(aef_id):
            self.__register_security_service(api_id, aef_id)
            self.__save_aef_id_to_already_registered_cached_list(aef_id)

        token_dic = self.__get_security_token(api_name, aef_id)
        return token_dic["access_token"]

    def __aef_id_already_registered(self, aef_id):
        return "registered_aef_ids" in self.capif_api_details and \
            aef_id in self.capif_api_details["registered_aef_ids"]

    def __save_aef_id_to_already_registered_cached_list(self, aef_id):
        if "registered_aef_ids" not in self.capif_api_details:
            self.capif_api_details["registered_aef_ids"] = []

        self.capif_api_details["registered_aef_ids"].append(aef_id)
        with open(
                self.folder_to_store_certificates_and_api_key + "capif_api_details.json", "w"
        ) as outfile:
            json.dump(self.capif_api_details, outfile)

    def __register_security_service(self, api_id, aef_id):
        """

        :param api_id: The api id that is returned by discover services
        :param aef_id: The aef_id that is returned by discover services
        :return: None
        """
        url = "https://{}/capif-security/v1/trustedInvokers/{}".format(self.capif_host,
                                                                       self.capif_api_details["api_invoker_id"])

        payload = {
            "securityInfo": [
                {
                    "prefSecurityMethods": ["OAUTH"]
                }
            ],
            "notificationDestination": "https://mynotificationdest.com",
            "requestTestNotification": True,
            "websockNotifConfig": {
                "websocketUri": "string",
                "requestWebsocketUri": True
            },
            "supportedFeatures": "fff"
        }

        for profile in payload["securityInfo"]:
            profile["aefId"] = aef_id
            profile["apiId"] = api_id

        response = requests.put(url,
                                json=payload,
                                cert=(self.signed_key_crt_path, self.private_key_path),
                                verify=self.ca_root_path
                                )
        response.raise_for_status()
        response_payload = response.json()

    def __get_security_token(self, api_name, aef_id):
        """
        :param api_name: The api id name is returned by discover services
        :param aef_id: The relevant aef_id that is returned by discover services
        :return: The access token (jwt)
        """

        url = "https://{}/capif-security/v1/securities/{}/token".format(self.capif_host,
                                                                        self.capif_api_details["api_invoker_id"])

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.capif_api_details["api_invoker_id"],
            "client_secret": "string",
            "scope": "3gpp#" + aef_id + ":" + api_name
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.post(url,
                                 headers=headers,
                                 data=payload,
                                 cert=(self.signed_key_crt_path, self.private_key_path),
                                 verify=self.ca_root_path
                                 )
        response.raise_for_status()
        response_payload = json.loads(response.text)
        return response_payload

    def discover_service_apis(self):

        url = "https://{}/{}{}".format(
            self.capif_host,
            self.capif_api_details["discover_services_url"],
            self.capif_api_details["api_invoker_id"],
        )

        response = requests.request(
            "GET",
            url,
            headers={"Content-Type": "application/json"},
            data={},
            files={},
            cert=(self.signed_key_crt_path, self.private_key_path),
            verify=self.ca_root_path
        )
        response.raise_for_status()
        response_payload = json.loads(response.text)
        return response_payload

    def retrieve_api_description_by_name(self, api_name):
        capif_apifs = self.discover_service_apis()
        endpoints = list(
            filter(lambda api: api["apiName"] == api_name, capif_apifs["serviceAPIDescriptions"])
        )
        if len(endpoints) == 0:
            raise ServiceDiscoverer.ServiceDiscovererException(
                "Could not find available endpoints for api_name: "
                + api_name
                + ".Make sure that a) your NetApp is registered and onboarded to CAPIF and b) the NEF emulator has been registered and onboarded to CAPIF"
            )
        else:
            return endpoints[0]

    def retrieve_specific_resource_name(self, api_name, resource_name):
        """
        Can be used to retrieve the URL for specific resources inside APIS.
        For example the NEF emulator exposes an api with name "nef_emulator_endpoints" that contains two resources (two endpoints)
        1. '/nef/api/v1/3gpp-monitoring-event/v1/{scsAsId}/subscriptions' with resource name:MONITORING_SUBSCRIPTIONS
        2. '/nef/api/v1/3gpp-monitoring-event/v1/{scsAsId}/subscriptions/{subscriptionId}' with resource name : MONITORING_SUBSCRIPTION_SINGLE
        """
        api_description = self.retrieve_api_description_by_name(api_name)
        version_dictionary = api_description["aefProfiles"][0]["versions"][0]
        version = version_dictionary["apiVersion"]
        resources = version_dictionary["resources"]
        uris = list(
            filter(
                lambda resource: resource["resourceName"] == resource_name,
                resources,
            )
        )

        if len(uris) == 0:
            raise ServiceDiscoverer.ServiceDiscovererException(
                "Could not find resource_name: "
                + resource_name
                + "at api_name"
                + api_name
            )
        else:
            uri = uris[0]["uri"]
            # make sure the uri starts with /
            if not uri.startswith("/"):
                uri = "/" + uri
            # make sure the API doesn't have a trailing /
            if api_name.endswith("/"):
                api_name = api_name[:-1]
            # construct the url
            return api_name + "/" + version + uri


class TSNManager:
    """
    Contains helper functions to apply Time-Sensitive Networking (TSN) standards to time-sensitive NetApps.
    Allows the configuration of certain parameters in the underlying TSN infrastructure of the testbed.
    These parameters indicate the expected QoS of the communication. Read more at https://github.com/EVOLVED-5G/TSN_AF
    """

    def __init__(
            self,
            folder_path_for_certificates_and_capif_api_key: str,
            capif_host: str,
            capif_https_port: int,
            https: bool,
            tsn_host: str,
            tsn_port: int,
    ) -> None:

        self.folder_path_for_certificates_and_capif_api_key = os.path.join(
            folder_path_for_certificates_and_capif_api_key.strip(), ""
        )
        self.api_name = "/tsn/api/"
        self.service_discoverer = ServiceDiscoverer(self.folder_path_for_certificates_and_capif_api_key, capif_host,
                                                    capif_https_port)
        api_resource_description = self.service_discoverer.retrieve_api_description_by_name(self.api_name)
        self.access_token = self.service_discoverer.get_access_token(self.api_name, api_resource_description["apiId"],
                                                                     api_resource_description["aefProfiles"][0][
                                                                         "aefId"])
        self.headers_auth = {
            "Accept": "application/json",
            'Authorization': 'Bearer ' + self.access_token
        }
        self.api_invoker_id = self.service_discoverer.get_api_invoker_id()
        self.url_prefix = "{protocol}://{host}:{port}".format(
            protocol="https" if https else "http",
            host=tsn_host,
            port=tsn_port
        )

    class TSNNetappIdentifier:
        def __init__(self, netapp_name: str):
            self.netapp_name = netapp_name
            self.__identifier = self.__generate_random_identifier()

        def __generate_random_identifier(self):
            return "{netapp_name}_{random_uuid}".format(
                netapp_name=self.netapp_name, random_uuid=uuid4().hex
            )

        @property
        def value(self):
            return self.__identifier

    class TSNProfile:
        def __init__(self, tsn_manager, profile_name):
            self.tsn_manager = tsn_manager
            self.name = profile_name
            self.configuration = self.get_configuration_for_tsn_profile()

        class TSNProfileConfiguration:
            def __init__(self, parameters_dict):
                for (
                        profile_parameter_name,
                        profile_parameter_value,
                ) in parameters_dict.items():
                    setattr(self, profile_parameter_name, profile_parameter_value)

            def get_profile_configuration_parameters(self):
                return vars(self)

        def get_configuration_for_tsn_profile(
                self,
        ) -> TSNProfileConfiguration:
            """
            Returns the configuration parameters of the selected time-sensitive networking (TSN) profile.

            :return: the default TSN profile configuration
            """

            url = self.tsn_manager.url_prefix + \
                  self.tsn_manager.service_discoverer. \
                      retrieve_specific_resource_name(self.tsn_manager.api_name, "TSN_DETAIL_PROFILE"). \
                      format(profileName=self.name)

            response = requests.get(url=url, headers=self.tsn_manager.headers_auth)
            response.raise_for_status()
            parameters_dict = json.loads(response.text)[self.name]
            return self.TSNProfileConfiguration(parameters_dict)

    def get_tsn_profiles(self) -> [TSNProfile]:
        """
        Returns the names of supported time-sensitive networking (TSN) profiles.

        :return: a list of TSN profiles. Each TSN profile is a TSNProfile class.

        """
        url = self.url_prefix + self.service_discoverer. \
            retrieve_specific_resource_name(self.api_name, "TSN_LIST_PROFILES"). \
            format(scsAsId=self.api_invoker_id)

        response = requests.get(url=url, headers=self.headers_auth)
        response.raise_for_status()
        response_dict = json.loads(response.text)
        return [
            self.TSNProfile(tsn_manager=self, profile_name=name)
            for name in response_dict["profiles"]
        ]

    def apply_tsn_profile_to_netapp(
            self,
            tsn_netapp_identifier: TSNNetappIdentifier,
            profile: TSNProfile,
    ) -> str:
        """
        Applies the time-sensitive networking (TSN) profile to the NetApp specified by <tsn_netapp_identifier>

        :param tsn_netapp_identifier: the TSN identifier class of the NetApp
        :param profile: the TSN profile whose configuration will be applied to the NetApp
        :return: token which can be used to clear the configuration from the NetApp
        """

        data = {
            "identifier": tsn_netapp_identifier.value,
            "profile": profile.name,
            "overrides": {},
        }
        url = self.url_prefix + self.service_discoverer.retrieve_specific_resource_name(self.api_name,
                                                                                        "TSN_APPLY_CONFIGURATION")

        response = requests.post(
            url=url, json=data, headers=self.headers_auth
        )
        response.raise_for_status()
        response = json.loads(response.text)
        return response["token"]

    def apply_profile_with_overriden_parameters_to_netapp(
            self,
            tsn_netapp_identifier: TSNNetappIdentifier,
            base_profile: TSNProfile,
            modified_params: dict,
    ) -> str:
        """
        Overrides the default parameters of the time-sensitive networking (TSN) profile, and applies it to the NetApp
        specified by <tsn_netapp_identifier>.


        :param tsn_netapp_identifier: the TSN identifier class of the NetApp
        :param base_profile: the profile class whose configuration will be applied to the NetApp
        :param modified_params: Dict of param-value pairs that will override the default configuration of the TSN profile
        :return token used to clear the applied TSN configuration from the NetApp
        """
        if not modified_params:
            return self.apply_tsn_profile_to_netapp(
                tsn_netapp_identifier=tsn_netapp_identifier,
                profile=base_profile,
            )

        data = {
            "identifier": tsn_netapp_identifier.value,
            "profile": base_profile.name,
            "overrides": modified_params,
        }
        url = self.url_prefix + self.service_discoverer.retrieve_specific_resource_name(self.api_name,
                                                                                        "TSN_APPLY_CONFIGURATION")

        response = requests.post(
            url=url,
            json=data,
            headers=self.headers_auth
        )
        response.raise_for_status()
        response = json.loads(response.text)
        return response["token"]

    def clear_profile_for_tsn_netapp_identifier(
            self, tsn_netapp_identifier: TSNNetappIdentifier, clearance_token: str
    ) -> None:
        """
        Disables a previously applied configuration for the selected NetApp


        :param tsn_netapp_identifier: the TSN identifier class of the NetApp
        :param clearance_token: used to clear the applied TSN configuration from the NetApp
        """

        url = self.url_prefix + self.service_discoverer.retrieve_specific_resource_name(self.api_name,
                                                                                        "TSN_CLEAR_CONFIGURATION")

        data = {
            "identifier": tsn_netapp_identifier.value,
            "token": clearance_token,
        }
        response = requests.post(
            url=url, json=data, headers=self.headers_auth
        )
        response.raise_for_status()
        assert "success" in json.loads(response.text)["message"]


class CAPIFLogCommon(ABC):
    def __init__(self,  certificates_folder,
                 capif_host,
                 capif_https_port):

        self.certificates_folder = os.path.join(certificates_folder.strip(), "")
        self.capif_https_url = ""
        if len(capif_https_port) == 0 or int(capif_https_port) == 443:
            self.capif_https_url = "https://" + capif_host.strip() + "/"
        else:
            self.capif_https_url = "https://" + capif_host.strip() + ":" + capif_https_port.strip() + "/"

        with open(
                self.certificates_folder + "capif_provider_details.json", "r"
        ) as openfile:
            self.capif_provider_details = json.load(openfile)
            self.aef_id = self.capif_provider_details["AEF_api_prov_func_id"]

    def get_capif_service_description(self, capif_service_api_description_json_full_path):
        """
        Use this method to read the api_id of  your service from the relevant file or other relevant information

        :param capif_service_api_description_json_full_path:
        This file  is generated when you register your Provider to CAPIF. It is stored inside your certificate folder.
        :return: The service description json that is stored in CAPIF
        """
        with open(
                capif_service_api_description_json_full_path, "r"
        ) as openfile:
            return json.load(openfile)

class CAPIFLogger(CAPIFLogCommon):

    def __init__(self,
                 certificates_folder,
                 capif_host,
                 capif_https_port):

        """
          :param certificates_folder: The certificated folder you used during registration of the Provider to CAPIF
          :param capif_host: The CAPIF host name
          :param capif_https_port: The CAPIF https port
        """
        super().__init__(certificates_folder,capif_host,capif_https_port)
        self.capif_logger_url = self.capif_https_url + "api-invocation-logs/v1/" + self.aef_id + "/logs"

    @dataclass
    class LogEntry:
        """
           A class representing a LogEntry that will be saved to CAPIF Invocation logs.

      Attributes:
            apiId (str): The ID of the API invoked.
            apiVersion (str): The version of the API that was invoked.
            apiName (str): The name of the API.
            resourceName (str): The name of the resource being invoked
            uri (str): Full URI  of the request.
            protocol (str): The protocol used for the request (ex. HTTP_1_1)
            invocationLatency (int): The time taken to process the request, in milliseconds.
            invocationTime (datetime): Date on which the request was invoked.
            operation (str): The HTTP operation being performed (Ex. GET,POST,PUT,DELETE)
            result (int): The HTTP status code of the results (ex. 200)
            inputParameters (dict): The input parameters for the request.
            outputParameters (dict): The output / response parameters
        """
        apiId: str
        apiVersion: str
        apiName: str
        resourceName: str
        uri: str
        protocol: str
        invocationLatency: int
        invocationTime: datetime
        operation: str
        result: int
        inputParameters: dict
        outputParameters: dict





    def save_log(self, api_invoker_id, log_entries: List[LogEntry]):

        payload = {
            "aefId": self.aef_id,
            "apiInvokerId": api_invoker_id,
            "logs": list(map(lambda logentry: logentry.__dict__, log_entries)),
            "supportedFeatures": "fffffff"
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.capif_logger_url,
                                    headers=headers,
                                    data=json.dumps(payload),
                                    cert=(
                                        self.certificates_folder + "dummy_aef.crt",
                                        self.certificates_folder + "AEF_private_key.key",
                                    ),
                                    verify=self.certificates_folder + 'ca.crt')
        response.raise_for_status()
        response_payload = json.loads(response.text)

        return response_payload




class CAPIFAuditor(CAPIFLogCommon):

    def __init__(self,
                 certificates_folder,
                 capif_host,
                 capif_https_port):
        """
        :param certificates_folder: The certificated folder you used during registration of the Provider to CAPIF
        :param capif_host: The CAPIF host name
        :param capif_https_port: The CAPIF https port
        """
        super().__init__(certificates_folder,capif_host,capif_https_port)
        self.capif_query_log_url = self.capif_https_url + "logs/v1/apiInvocationLogs"

    def query_log(self, api_invoker_id=None, time_start=None, time_end=None, api_id=None,
              api_name=None, api_version=None, result=None, resource_name=None, protocol=None,
              operation=None):

        """
        :param api_invoker_id:
        :param time_start:    # e.g. 2022-10-24T00:00:00.000Z
        :param time_end:  # e.g. 2022-10-25T00:00:00.000Z
        :param api_id:  # e.g. f7ba97e8f08a7f53365ba81be60a0c
        :param api_name:   # e.g. dummy-aef
        :param api_version:   # e.g. v1
        :param result:   # e.g. 201
        :param resource_name:   # e.g. MONITORING_SUBSCRIPTION_SINGLE
        :param protocol:  # e.g. HTTP_1_1 or HTTP_2
        :param operation:    # e.g. POST
        :return: The Log entries found in the CAPIF database
        """

        params = dict()
        params.update({'aef-id':self.aef_id})

        if api_invoker_id is not None:
            params.update({'api-invoker-id': api_invoker_id})

        if time_start is not None:
            params.update({'time-range-start': time_start})

        if time_end is not None:
            params.update({'time-range-end': time_end})

        if api_id is not None:
            params.update({'api-id': api_id})

        if api_name is not None:
            params.update({'api-name': api_name})

        if api_version is not None:
            params.update({'api-version': api_version})

        if result is not None:
            params.update({'result': result})

        if resource_name is not None:
            params.update({'resource-name': resource_name})

        if protocol is not None:
            params.update({'protocol': protocol})

        if operation is not None:
            params.update({'operation': operation})

        response = requests.request("GET", self.capif_query_log_url, params=params,
                                    cert=(
                                        self.certificates_folder + "dummy_amf.crt",
                                        self.certificates_folder + "AMF_private_key.key",
                                    ),
                                    verify=self.certificates_folder + 'ca.crt')
        response.raise_for_status()
        response_payload = json.loads(response.text)
        return response_payload
